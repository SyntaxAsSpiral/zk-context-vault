# local-inference: runbook

The gateway, the API surface, and the operational discipline. Everything
below verified against the live mesh on 2026-09-18.

## Gateway: `adeck:1234`

**Not** an LM Studio native server — an aiohttp relay:

- `inference-wake.service` binds `0.0.0.0:1234`, proxies to
  `llmster.service` upstream at `http://127.0.0.1:1235` (adeck's daemon,
  `lms daemon up`).
- Source: `nix-os/modules/home/daemonturgy/lmstudio/adeck/inference-wake.py`
  (declared by `default.nix` next to it; both under version control).

### Wake gating

Only **inference** traffic wakes zrrh. Gated paths (POST):
`/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/responses`,
`/api/v0/chat/completions`, `/api/v0/completions`, `/api/v0/embeddings`,
`/api/v1/chat`, `/api/v1/models/load` — plus any WebSocket (SDK connections),
with a wake check before each downstream→upstream frame.

Readiness = zrrh TCP-reachable at `192.168.0.110:22` (router-LAN IP) **and**
`lms link status --json` shows peer `zrrh` with `status: "connected"`.
If not ready: WoL broadcast (MAC `60cf8461d800` → `192.168.0.255:9`) every
3 s, 120 s deadline, then HTTP 503
`zrrh did not reconnect to LM Link within 120 seconds.`
A 2 s dedup cache avoids re-checking per request burst.

**Gotcha:** embeddings are wake-gated too — even a model that lives on
adeck (`mxbai-embed-large-v1` is `Local`) will pay the wake cost if zrrh is
asleep. If zrrh is up, the check is a ~free 2 s-cached no-op.

### Proxy behavior

- Timeouts: `sock_connect` 10 s, `sock_read` 600 s, no total — long
  generations are fine; a stalled upstream 502s after 10 min.
- `auto_decompress: false` (SSE streams pass through), `client_max_size`
  64 MB, upstream failure → 502 `LM Studio upstream unavailable.`
- Non-inference traffic (e.g. `GET /v1/models`, `GET /api/v0/models`,
  control-plane) passes through without waking anything.

## API surface (what the services actually use)

### Chat

`POST /v1/chat/completions` — non-stream and SSE streaming both work.
Streaming: `data:` lines, `choices[].delta.content` **and** a separate
`choices[].delta.reasoning_content`, terminated by `data: [DONE]`.

### Structured output (strict JSON schema)

```json
{"response_format": {"type": "json_schema", "json_schema": {
  "name": "page_ocr", "strict": true,
  "schema": {"type": "object", "properties": {"...": "..."},
             "required": ["..."], "additionalProperties": false}}}}
```

Strict mode: `additionalProperties: false` + `required` on every object.
In production on the local gateway: cookbook OCR (`page_ocr`), cookbook
repair (`ocr_character_repairs`), esocortex augment (`esocortex_augment`).
Docs: <https://lmstudio.ai/docs/developer/openai-compat/structured-output>

Harvest **both** `choices[].message.content` and
`choices[].message.reasoning_content` (stream: the matching `delta.*`).
Prefer `content` when it contains a JSON object; otherwise take
`reasoning_content`. Grammar on thinking models can land on the think
channel; the answer channel may be empty, truncated, or unconstrained
prose. Treat empty `content` as a real state, not a protocol error.
On HTTP 4xx/5xx, log **`response.text`** — `raise_for_status()` alone
hides the gateway's actual reason.

### Reasoning: two different APIs

**Use this on `/v1/chat/completions` (pi, curl, cookbook, esocortex):**
`reasoning_effort`. Live gateway 400 lists:
`none | minimal | low | medium | high | xhigh`.

Re-verified on `qwen/qwen3.8-27b` through the gateway, 2026-09-18:

| Request | Result |
|---|---|
| (no param) / `"xhigh"` | Thinks. Small `max_tokens` is eaten by reasoning; `content` empty; `reasoning_tokens` == `completion_tokens`. |
| `"reasoning_effort": "none"` | Thinking off: `reasoning_tokens: 0`, answer in `content`. |
| `"reasoning_effort": "off"` | **400** — not a valid value on this endpoint. |
| `"thinking_budget": 0` | Present in llmster 0.0.11; no effect on qwen3.8. Don't rely on it. |

- Stream/non-stream: `choices[].message.reasoning_content` and
  `choices[].delta.reasoning_content`. Parse separately from `content`.
- Cookbook repair (local gemma): `reasoning_effort: "none"` + `temperature: 0`.
- LMS **native** `/api/v1/chat` uses a different field: `reasoning` =
  `off|low|medium|high|on` (see `GET /api/v1/models` → `capabilities.reasoning`).
  Do not send `reasoning: {"effort": ...}` to `/v1/chat/completions`.
- LMS **`/v1/responses`** *does* document `reasoning: { "effort": "low"|"medium"|"high" }`
  (gpt-oss examples). Cookbook OpenRouter fallback uses that object shape
  against OpenRouter, not against the local chat-completions path.

Official model knobs differ from the gateway aliases — see Active models
below. When they conflict, **the model's chat template is the authority
for what actually thinks.** The gateway 400-list is only the enum this
endpoint will accept. If the jinja never reads `reasoning_effort`, sending
it is a no-op (byte-identical prompt). Check the hub `model.yaml`
`customFields` → `setJinjaVariable` and the official prompting guide
before the first request.

**Labels vs a token budget.** `reasoning_effort` / native `reasoning` /
jinja `reasoning_strength` are **template labels**, not a cap in tokens.
A numeric reasoning budget exists in the LMS **UI** and in the TS SDK as
experimental `LLMPredictionConfigInput.reasoningBudget` (max tokens
*inside* a reasoning section, separate from `maxTokens`; not supported on
`model.complete()`). Published `/v1/chat/completions` docs do not list it.
llama.cpp has `--reasoning-budget` / `thinking_budget_tokens`;
`thinking_budget: 0` on this gateway was a no-op on qwen3.8. Do not plan
production on a numeric budget until a live probe on the loaded model
shows `reasoning_tokens` actually cap.

**Sparse KV.** LMS only serializes a field after it is changed. JIT
`user-concrete-model-default-config/*/....json` and presets omit defaults.
Empty `operation.fields: []` does **not** mean the UI lacks Reasoning
Budget / Enable Thinking / parallel. Absence on disk is not absence in
the app.

### Active models (loaded at 100K)

100K is the operator-chosen load ctx (`defaultContextLength: 100000` →
runtime 100096). Native card maxima are larger; they do not fit on the
4090 with these KV/parallel settings. Do not raise ctx without an
explicit ask. All three are VLMs (`GET /api/v0/models/{id}` →
`type: "vlm"`; `GET /api/v1/models` → `capabilities.vision: true`).

**`qwen/qwen3.8-27b`** — Qwen3.8-27B, arch `qwen35`, Q4_K_M (~17.7 GB loaded).
Card ctx 262,144 (YaRN to 1M); **served at 100K**. Thinking on by default. Official
`reasoning_effort`: `xhigh` (default) / `medium` / `low`. Official off-switch
is `chat_template_kwargs.enable_thinking: false`; on this gateway use
`reasoning_effort: "none"`. `preserve_thinking` defaults on (keep prior
thoughts in history). VLM: image + video; mmproj
`mmproj-Qwen3.8-27B-BF16.gguf`. MTP head is in the GGUF (see MTP). Thinking
sampling: temp 1.0, top_p 0.95, top_k 20. Instruct/off: temp 0.7, top_p 0.8,
presence_penalty 1.5. LMS v1 reasoning options: `off, low, medium, on`
(default `on`). Hub: `lmstudio-community/Qwen3.8-27B-GGUF`.

**`google/gemma-4-31b`** — Gemma 4 31B IT, arch `gemma4`, Q4_K_M (~19.9 GB).
Card ctx 256K / 262,144; **served at 100K**. Thinking on by default via `<|think|>` in the
system turn (LMS `Enable Thinking`, default true). LMS v1 options: `off|on`
only. Thoughts are `<|channel>thought` … `<channel|>`. On 31B, thinking-off
still emits an **empty** thought channel — parsers must tolerate it. Strip
prior thoughts from multi-turn history (opposite of Qwen's
`preserve_thinking`). VLM: text + image. Sampling: temp 1.0, top_p 0.95,
top_k 64. Hub: `lmstudio-community/gemma-4-31B-it-GGUF`.

**`meta/muse-glimmer`** — Muse Glimmer, 30B card (LMS `params_string: 28B`
= text decoder; ~1.8–2B vision encoder on top). Card ctx 131,072; **served at 100K**.
Thinking is built-in (`assistant to=self` then `to=user`) — there is no
off. Official dial is jinja **`reasoning_strength`**: `xhigh|high|medium|low`,
default **high**. Send
`chat_template_kwargs: {"reasoning_strength": "low"}` on
`/v1/chat/completions`. Hub custom field `reasoningStrength` →
`setJinjaVariable: reasoning_strength`. `reasoning_effort` and
`enable_thinking` **do not appear in the template** — they are dead knobs
(prompt renders byte-identical to omitting them). LMS v1 exposes only
`on`. Card sampling: **temp 1.0, top_p 0.95, top_k 64**. Official pitfall:
CoT is routinely multi-thousand tokens; a small `max_tokens` clips
mid-`to=self` and never reaches the answer. Omit `max_tokens` or give
thousands of headroom. JSON, when constrained, belongs in `to=user` →
`message.content`. Docs:
<https://ai.developer.meta.com/docs/muse-glimmer/prompting.md>.
VLM: text + image (`<|image|>`). Speculative decoding is a **separate**
draft model (Meta DFlash), not a baked MTP head. Hub:
`lmstudio-community/Muse-Glimmer-30B-GGUF`. pi's display name "26b" is stale.

### Vision / capability check

Do not look for `architecture.input_modalities` — it is not on the live
`/api/v0` payload. Cookbook-style preflight:

```
GET /api/v0/models/{id}  →  type == "vlm"
GET /api/v1/models       →  capabilities.vision == true
```

`qwen/qwen3.8-27b` is loaded with its mmproj. pi's `models.json` still
declares all three `input: ["text"]` — vision is on the raw API, not through
pi's declaration.

### Embeddings

`POST /v1/embeddings` — models: `text-embedding-qwen3-embedding-8b` (zrrh),
`text-embedding-nomic-embed-text-v1.5` (adeck/nxiz/zrrh),
`text-embedding-mxbai-embed-large-v1` (adeck/nxiz),
`text-embedding-qwen3-embedding-4b` (nxiz).

**OOM gotcha (from esocortex):** a bare `/v1/embeddings` call JIT-loads with
the GGUF's own `n_ctx` (40k for qwen3-embedding-8b) and OOMs on the 24 GB
card. Load it explicitly first:

```
POST /api/v1/models/load  {"model": "text-embedding-qwen3-embedding-8b", "context_length": 8192}
```

(esocortex's `ensure_loaded` tolerates 400/409/500 "already loaded".)

**Chat loads are not this path.** `POST /api/v1/models/load` with a
`context_length` (or any load-config override) **bypasses** the per-model
JIT preset: KV quant, parallel slots, GPU offload, ctx. Those live in
`~/.lmstudio/.internal/user-concrete-model-default-config/` and are
applied when the **first `/v1/chat/completions`** JIT-loads. For chat:
do not call `/models/load`. Fire **one** inference request, wait until
`lms ps` shows a single instance with the expected PARALLEL/CONTEXT, then
fan out workers. N concurrent first-hits race `unloadPreviousJITModelOnLoad`
and you get N loads + 400s.

Embeddings remain the exception — they *must* pin `context_length` or the
GGUF `n_ctx` OOMs the 4090.

### Models list

`GET /v1/models` returns 35 IDs (chat + `text-embedding-*`).
`lms ls` shows the full union with arch/size/device (below).

## MTP (multi-token prediction draft decoding)

LMS's published [speculative decoding](https://lmstudio.ai/docs/app/advanced/speculative-decoding)
doc is the **two-model** path (small draft + large target, same vocab).
Qwen3.8 is different: the MTP head is **inside the GGUF**. llama.cpp CLI
docs use `--spec-type draft-mtp`; on this mesh the LMS/llama.cpp runtime
auto-inits it.

**Live-verified on the running qwen3.8-27b instance:** zrrh server log
`common_speculative_init_result: creating MTP draft context against the
target model .../Qwen3.8-27B-Q4_K_M.gguf`. Acceptance lines (`print_timing`):
`draft acceptance = 0.80–0.98 (N accepted / M generated), mean len ≈ 2.5–2.8`.

**Explicit config** (JIT per-model default,
`~/.lmstudio/.internal/user-concrete-model-default-config/.../....json`):
`qwopus3.6-27b-v2-mtp` sets
`llm.load.llama.speculativeDecoding.draftMtpMaxTokens: 4`,
`draftMtpMinTokens: 1`.

**Prediction-side tuning** (zrrh GUI preset file `zrrh hermes test` —
filename only, unused consumer):
`llm.prediction.speculativeDecoding.maxTokensToDraft: 22`,
`minContinueDraftingProbability: 0.74`, `minDraftLengthToConsider: 1`.

**Verify on the host where it runs:**

```bash
grep -i "draft acceptance" ~/.lmstudio/server-logs/$(date +%Y-%m)/$(date +%Y-%m-%d).*
```

MTP is a **load-time** property (JIT config / preset), not a per-request
parameter in current use.

## JIT loading & fleet

Defaults (adeck `http-server-config.json`): `defaultContextLength: 100000`
(runtime shows 100096) — chosen so ~17–20 GB Q4s + KV + parallel still
fit the 24 GB card. `jitModelTTL` 1 h, `unloadPreviousJITModelOnLoad` —
loading a new large model evicts the previous one. `lms ps` (2026-09-18):
`qwen/qwen3.8-27b  IDLE  17.74 GB  100096  parallel 4  TTL 60m/1h`.

Per-model JIT configs (zrrh, flat `load.fields` shape) — the "how we actually
load" layer:

| Model | KV cache | offloadKV | threads / batch |
|---|---|---|---|
| qwen/qwen3.8-27b | q8_0 | true | 16 / 4096 |
| meta/muse-glimmer | f16 | true (parallel 2) | 16 / 4096 |
| google/gemma-4-31b | flash + q4_0 | **false** (parallel 2) | — |
| qwopus3.6-27b-v2-mtp | q5_0 | true (MTP 1–4) | 16 / 4096 |

Presets live in `~/.lmstudio/config-presets/` (adeck's are flake-managed via
nix-os `home.file`; zrrh's are GUI-managed).

### Union fleet (39 models, 410 GB — `lms ls` from adeck, 2026-09-18)

**zrrh (RTX 4090, 24 GB):**
`qwen/qwen3.8-27b` 27B qwen35 17.74 GB (LOADED) · `qwen/qwen3.6-27b` 17.48 GB ·
`unsloth/qwen3.6-27b` 21.35 GB · `qwen3.5-27b-uncensored-heretic` 21.24 GB ·
`qwen/qwen3.6-35b-a3b` 35B-A3B MoE 22.07 GB ·
`qwen3.5-35b-a3b-uncensored-hauhaucs-aggressive` 25.66 GB ·
`qwopus3.6-27b-v2-mtp` 17.74 GB · `meta/muse-glimmer` 30B/28B-decoder 18.16 GB ·
`google/gemma-4-31b` 31B 19.89 GB · `unsloth/gemma-4-31b-it` 24.19 GB ·
`gemma-4-26b-a4b-it` MoE 17.99 GB · `gemma-4-12b-coder-fable5-composer2.5-v1`
12.67 GB · `google/gemma-3-12b` 8.15 GB · `hermes-4.3-36b-heretic-i1` 20.70 GB ·
`glm-4.7-flash` 30B 18.13 GB · `gpt-oss-20b` 11.72 GB ·
`gpt-oss-20b-heretic` 16.89 GB · `dolphin-mistral-24b-venice-i1` 16.76 GB ·
`mistral-small-24b-instruct-2501-heretic-i1` 16.76 GB · `llama-3.2-1b-instruct`
1.32 GB · `qwen2.5-0.5b-instruct` 531 MB

**adeck (Local, Vulkan):** `liquid/lfm2-24b-a2b` 64×1.3B MoE 14.42 GB ·
`meta-llama-3.1-8b-instruct` 4.92 GB · `qwen2.5-7b-instruct` 4.68 GB ·
`ibm/granite-4-h-tiny` 4.23 GB · `nemotron-h-4b-instruct-128k` 3.70 GB ·
`microsoft/phi-4-mini-reasoning` 2.49 GB · `lfm2-2.6b` 2.11 GB

**nxiz (RTX 3070, 8 GB):** `prism-ml/bonsai-27b` 27B 4.73 GB ·
`qwen_qwen3-8b` 5.03 GB · `mistral-nemo-instruct-2407` 7.48 GB ·
`qwen2.5-0.5b-instruct` 531 MB

**Embeddings:** qwen3-embedding-8b (zrrh) · qwen3-embedding-4b (nxiz) ·
nomic-embed-text-v1.5 (adeck/nxiz/zrrh) · mxbai-embed-large-v1 (adeck/nxiz)

## Operational discipline

- **zrrh is one 24 GB GPU.** 100K ctx is the fit with current KV/parallel;
  ~17–20 GB models go one at a time; the 22–26 GB MoEs are tight. Check
  `lms ps` before loading; `lms unload` to evict.
  `unloadPreviousJITModelOnLoad` will evict on your behalf.
- **TTL is 1 h idle** — a "model not found" after lunch is normal; the
  gateway JIT-loads (and wakes zrrh) on the next request.
- **Retry on transient gateway errors:** 408 / 429 / 502 / 503 / 504, and
  bodies containing `LM Link connection closed` (the cookbook sidecar's
  exact rule).
- **`finish_reason: "length"` = truncated.** esocortex retries once with
  doubled `max_tokens`; the sidecar fails loud. With reasoning models, a
  small `max_tokens` gets consumed entirely by thinking — raise it or set
  `reasoning_effort: "none"`.
- **Empty `content` is a real state** (budget went to reasoning), not a
  protocol error — validate for it explicitly. Harvest `reasoning_content`
  before declaring the call dead.
- **Do not clip thinking models.** Official cards (Muse especially) warn
  that a tight `max_tokens` ends the turn inside CoT. A 512-token probe
  on a reasoning model only reproduces that pitfall. Omit the cap or
  set it in the thousands; `reasoning_effort: "none"` is the cheap
  alternative **when the template actually honors it**.
- **GGUF type vs LMS llama.cpp.** Stock llama.cpp (what LMS ships) only
  knows ggml types in `[0, GGML_TYPE_COUNT)`. Publisher-specific packs
  with high IDs fail at parse, before VRAM:
  `tensor '…' has invalid ggml type 143. should be in [0, 43)`.
  Ternary Bonsai 2 `PTQ1_0` (143) / `PQ2_0` (142) need the Prism fork;
  LMS cannot load them. The 1-bit `Q1_0` Bonsai **does** load (type is
  upstream). A `Q2_0` from a `-gguf-dev` repo may load **and emit
  garbage** (Hadamard not applied). Read the publisher's format doc
  *before* downloading. Substring matchers: `bonsai-2` matches
  `bonsai-27b` — require `bonsai-2-` or `ternary-bonsai-2`.
- **Parallel workers** share one JIT instance. Warm with a single
  completion, then N in-flight requests ≤ the load preset's `parallel`.
  The client flock (`LOCK_EX` per call) will serialize them unless the
  lane holds exclusive once and inner calls skip the lock.
- **zrrh needs its GUI session** (CUDA). The wake proxy can bring the box
  up, but a dead zrrh session surfaces as 502/503, not a wake failure.
- Diagnostics: `journalctl --user -u inference-wake -u llmster` on adeck;
  `~/.lmstudio/server-logs/YYYY-MM/*.log` on the host where the model runs.
  Load failures print `LMSTUDIO_STARTUP_ERROR` + `gguf_init_from_reader`
  there — that **is** the reason the UI looks silent.
