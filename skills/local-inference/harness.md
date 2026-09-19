# local-inference: wiring & consumers

Who talks to the gateway, how, and with what patterns.

## pi

`~/.pi/agent/models.json` — provider `local`:

```json
{
  "baseUrl": "http://adeck:1234/v1",
  "api": "openai-completions",
  "apiKey": "lms",
  "models": [
    {"id": "qwen/qwen3.8-27b",  "name": "Qwen 3.8 27B Q4", "reasoning": true, "input": ["text"], "contextWindow": 100000},
    {"id": "meta/muse-glimmer", "name": "Muse Glimmer 26b","reasoning": true, "input": ["text"], "contextWindow": 100000},
    {"id": "google/gemma-4-31b","name": "Gemma 4 31B Q4",  "reasoning": true, "input": ["text"], "contextWindow": 100000}
  ]
}
```

- Default provider/model is `openrouter` / `stealth/ox-alpha` (1M ctx,
  `thinkingFormat: openrouter`). Local is opt-in per session:
  `pi --provider local --model qwen/qwen3.8-27b`
  (same for `meta/muse-glimmer`, `google/gemma-4-31b`).
- Costs are zero; `reasoning: true` so pi shows thinking controls.
- All three gateway models are VLMs. pi still declares `input: ["text"]`
  and names Muse "26b" (stale — it is a 30B card). Vision is raw-API only.
  `contextWindow: 100000` matches the 100K load setting, not the card max.
- Local thinking off: send `reasoning_effort: "none"` (not `"off"`).

## Consumer services (the real "how it's used")

### family-cookbook — `/mnt/echo/family-cookbook` (adeck)

- **`ocr/sidecar.py`** — batch OCR: 4 page workers, sqlite queue,
  tile-based pipeline (per-tile transcribe → whole-page assembly).
  - Default `--base-url http://adeck:1234/v1` (unit currently overrides to
    openrouter + `google/gemini-3-flash-preview` for throughput).
  - **Structured output:** strict `json_schema` (`page_ocr`), validated
    client-side with `Draft202012Validator`.
  - **Vision preflight:** `GET /api/v0/models`, requires `type: "vlm"`
    (live payload; an `input_modalities` fallback in the sidecar is not
    present on current `/api/v0`).
  - **Retry rule:** transient = HTTP 408/429/502/503/504 or body
    containing `LM Link connection closed`; 600 s request timeout;
    `finish_reason: "length"` → hard fail (no partial drafts).
  - OpenRouter fallback adds `reasoning: {"effort": "low"}`,
    `provider: {"sort": "throughput"}`, `OPENROUTER_API_KEY`,
    `HTTP-Referer` / `X-Title: Holliday Table OCR`.
- **`ocr/repair.py`** — the **local repair workflow**: text-only repair of
  corrupted OCR characters.
  - Default model `google/gemma-4-31b` (local, zrrh),
    `temperature: 0`, `stream: true`, **`reasoning_effort: "none"`**.
  - Strict schema `ocr_character_repairs`; every proposed `before` span must
    match the original draft; never auto-imports (proposes, operator applies).
  - Streams SSE, tracks `delta.reasoning_content` separately, requires
    `finish_reason: "stop"`.
- **`babette/server.py`** — the Holliday Table app backend:
  `settings.base_url` defaults to `http://adeck:1234/v1`
  (`OPENAI_BASE_URL` override), model via `COOKBOOK_MODEL`.
- Service: `cookbook-ocr.service` (systemd user unit on adeck,
  `Restart=on-failure`, `KillMode=mixed`, `TimeoutStopSec=120`).

### esocortex — `/mnt/echo/esocortex` (adeck)

Knowledge-cortex pipeline (chunking → LLM augment → embeddings → RAG).

- `src/llm.py`: `ESOCORTEX_LLM_BASE` default `http://adeck:1234/v1`.
  - `complete()` — `response_format` support, retries `length` once with
    doubled `max_tokens` (4096 → 8192) unless `max_tokens` is omitted.
    Harvests JSON from `content` or `reasoning_content`. Include HTTP
    error bodies. `exclusive=False` for in-flight workers after the
    lane already holds `LOCK_EX`.
  - `ensure_loaded(model, context_length)` — **embeddings only**
    (`POST /api/v1/models/load` to pin n_ctx). Do **not** use this for
    chat: it clobbers JIT VRAM/parallel/KV presets. Chat JIT is one
    `/v1/chat/completions`, then fan-out ≤ load `parallel`.
  - `embed()` — `/v1/embeddings`, sorted by `index`.
- `src/augment.py` — strict schema `esocortex_augment` (translation /
  system / mode / keys), defensive JSON parsing (`_loads_json` repair path).
- **GPU locking pattern** (`_gpu_lock`, `/tmp/esocortex-zrrh-gpu.lock`):
  chat takes `LOCK_EX` (exclusive), embed calls take `LOCK_SH` (multiple
  concurrent against one GGUF). Copy this pattern for anything sharing the
  zrrh GPU.

## Rules of thumb

1. One gateway URL for everything: `http://adeck:1234/v1`.
2. Structured output = strict `json_schema` + client-side validation.
3. Deterministic local work = `reasoning_effort: "none"` + `temperature: 0`
   **when the template honors that field**. Muse uses
   `chat_template_kwargs.reasoning_strength` and card sampling (1.0 / 0.95 / 64).
4. Embeddings = explicit `models/load` with `context_length` first.
   Chat = first completion JIT (presets), never `/models/load`.
5. Sharing the zrrh GPU = file lock, chat exclusive / embed shared.
   Concurrent chat workers: one lock around the lane, inner calls unlocked.
6. Treat 408/429/502/503/504 + `LM Link connection closed` as retryable.
7. A schema-ignoring or empty-content result is a call-shape bug until
   the hub card and LMS docs say otherwise. Not a wash.
