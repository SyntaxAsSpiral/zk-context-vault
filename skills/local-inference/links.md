# local-inference: links & source locations

## LM Studio

- <https://lmstudio.ai/docs/developer/> — developer docs root
- <https://lmstudio.ai/docs/developer/openai-compat/structured-output> — strict `json_schema` on `/v1/chat/completions`
- <https://lmstudio.ai/docs/developer/openai-compat/chat-completions> — OpenAI-compat chat (documented payload is a subset; gateway also accepts `reasoning_effort`)
- <https://lmstudio.ai/docs/developer/openai-compat/responses> — `/v1/responses` (`reasoning: { "effort": ... }`, gpt-oss examples)
- <https://lmstudio.ai/docs/developer/rest/load> — `POST /api/v1/models/load`
- <https://lmstudio.ai/docs/developer/rest/endpoints> — REST v0 (`GET /api/v0/models`, `type: "vlm"`)
- <https://lmstudio.ai/docs/developer/core/ttl-and-auto-evict> — JIT TTL default 60 min, auto-evict
- <https://lmstudio.ai/docs/app/basics/lmstudio-vs-llmster-vs-lms> — app vs llmster vs `lms`
- <https://lmstudio.ai/docs/developer/core/headless> — install llmster: `curl -fsSL https://lmstudio.ai/install.sh | bash`
- `lms` CLI — `lms link status` / `lms ls` / `lms ps` / `lms unload`;
  `lms --version` → commit-based (adeck `0b2a176`, zrrh `71bd99c` as of 2026-09)

## llama.cpp

- <https://github.com/ggerganov/llama.cpp> — runtime under LM Studio
  (MTP/speculative decoding, KV quant, `print_timing` draft-acceptance lines)

## Flake / config sources (nix-os repo)

- `modules/home/daemonturgy/lmstudio/adeck/default.nix` — llmster + inference-wake services
- `modules/home/daemonturgy/lmstudio/adeck/inference-wake.py` — the wake proxy
- `modules/home/daemonturgy/lmstudio/adeck/settings.json` / `http-server-config.json` — JIT defaults (ctx 100k, TTL, unload-on-load)
- `modules/home/daemonturgy/lmstudio/adeck/user-concrete-model-default-config/` — per-GGUF load configs
- `modules/home/daemonturgy/lmstudio/config-presets/` — shared presets

## Per-host state

- zrrh: `~/.lmstudio/.internal/user-concrete-model-default-config/` (per-model JIT), `~/.lmstudio/config-presets/` (e.g. `gemma4`; leftover filename `zrrh hermes test`), `~/.lmstudio/server-logs/YYYY-MM/*.log` (MTP acceptance, load logs)
- pi (nxiz): `~/.pi/agent/models.json` (provider `local`), `~/.pi/agent/AGENTS.md`

## Consumer services (adeck, `/mnt/echo/`)

- `/mnt/echo/family-cookbook/ocr/sidecar.py` — batch OCR (tiles, strict schema, vision preflight, retry rule)
- `/mnt/echo/family-cookbook/ocr/repair.py` — local repair (gemma, `reasoning_effort: "none"`)
- `/mnt/echo/family-cookbook/ocr/result.schema.json` — result shape
- `/mnt/echo/family-cookbook/babette/server.py` — app backend (`settings.base_url` → adeck:1234)
- `~/.config/systemd/user/cookbook-ocr.service` — the unit
- `/mnt/echo/esocortex/src/llm.py` — GPU lock, `ensure_loaded`, complete/embed
- `/mnt/echo/esocortex/src/augment.py` — strict-schema LLM augment

## Model sources (hub IDs + cards)

- Qwen3.8-27B: [HF card](https://huggingface.co/Qwen/Qwen3.8-27B) · [LMS](https://lmstudio.ai/models/qwen/qwen3.8-27b) · GGUF `lmstudio-community/Qwen3.8-27B-GGUF` (`Qwen3.8-27B-Q4_K_M.gguf` + `mmproj-Qwen3.8-27B-BF16.gguf`)
- Gemma 4 31B: [thinking docs](https://ai.google.dev/gemma/docs/capabilities/thinking) · [LMS](https://lmstudio.ai/models/google/gemma-4-31b) · GGUF `lmstudio-community/gemma-4-31B-it-GGUF`
- Muse Glimmer 30B: [Meta card](https://ai.developer.meta.com/docs/muse-glimmer.md) · [prompting](https://ai.developer.meta.com/docs/muse-glimmer/prompting) · [LMS](https://lmstudio.ai/models/meta/muse-glimmer) · GGUF `lmstudio-community/Muse-Glimmer-30B-GGUF`
- `Jackrong/Qwopus3.6-27B-v2-MTP-GGUF` — explicit MTP config model
- embeddings: `Qwen3-Embedding-8B`, `nomic-embed-text-v1.5`, `mxbai-embed-large-v1`
