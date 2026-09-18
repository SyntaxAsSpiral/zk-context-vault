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

### Reasoning: budget & toggle

Verified against `qwen/qwen3.8-27b` through the gateway, 2026-09-18:

| Request | Result |
|---|---|
| (no param) | Thinks by default. With `max_tokens: 15` all 15 completion tokens were reasoning (`usage.completion_tokens_details.reasoning_tokens: 15`), content empty. |
| `"reasoning_effort": "none"` | **Toggle verified off**: `reasoning_tokens: 0`, answer in 3 tokens. |
| `"thinking_budget": 0` | Present in the llmster 0.0.11 runtime, but had no effect on qwen3.8 (identical to default). Don't rely on it. |

- `reasoning_content` comes back as its own message field (non-stream) and
  SSE delta (stream) — parse it separately, don't splice into `content`.
- The cookbook repair workflow (local gemma) runs `reasoning_effort: "none"`
  + `temperature: 0` — the pattern for deterministic local work.
- The OpenRouter-style `reasoning: {"effort": "low"}` object is for the
  **openrouter** path (cookbook sidecar fallback), not the LMS gateway.
- gemma-4 thinking is also prompt-triggered: the `gemma4` preset injects a
  `<|think|>` system-prompt marker.

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

### Vision / capability check

`qwen/qwen3.8-27b` loads with its `mmproj` — it **is** a VLM on the gateway
(even though pi's `models.json` declares it text-only).
The cookbook sidecar's preflight pattern:

```
GET /api/v0/models  →  model.type == "vlm"  or
    "image" in model.architecture.input_modalities
```

### Models list

`GET /v1/models` returns 35 IDs (chat + `text-embedding-*`).
`lms ls` shows the full union with arch/size/device (below).

## MTP (multi-token prediction draft decoding)

**Live-verified on the running qwen3.8-27b instance:** the runtime
auto-initializes an MTP draft context for GGUFs that ship an MTP module —
zrrh server log: `common_speculative_init_result: creating MTP draft
context against the target model .../Qwen3.8-27B-Q4_K_M.gguf`. Acceptance
lines (llama.cpp `print_timing`): `draft acceptance = 0.80–0.98 (N accepted /
M generated), mean len ≈ 2.5–2.8` — that's the speed boost.

**Explicit config** (JIT per-model default,
`~/.lmstudio/.internal/user-concrete-model-default-config/.../....json`):
`qwopus3.6-27b-v2-mtp` sets
`llm.load.llama.speculativeDecoding.draftMtpMaxTokens: 4`,
`draftMtpMinTokens: 1`.

**Prediction-side tuning** (preset `zrrh hermes test`):
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
(runtime shows 100096), `jitModelTTL` 1 h, `unloadPreviousJITModelOnLoad` —
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
`qwopus3.6-27b-v2-mtp` 17.74 GB · `meta/muse-glimmer` 28B 18.16 GB ·
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

- **zrrh is one 24 GB GPU.** ~17–20 GB models + 100K ctx fit one at a time;
  the 22–26 GB MoEs are tight. Check `lms ps` before loading; `lms unload`
  to evict. `unloadPreviousJITModelOnLoad` will evict on your behalf.
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
  protocol error — validate for it explicitly.
- **zrrh needs its GUI session** (CUDA). The wake proxy can bring the box
  up, but a dead zrrh session surfaces as 502/503, not a wake failure.
- Diagnostics: `journalctl --user -u inference-wake -u llmster` on adeck;
  `~/.lmstudio/server-logs/YYYY-MM/*.log` on the host where the model runs.
