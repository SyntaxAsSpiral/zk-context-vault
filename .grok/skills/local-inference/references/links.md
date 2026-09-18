# local-inference: links & source locations

## LM Studio

- <https://lmstudio.ai/docs/developer/> — developer docs root
- <https://lmstudio.ai/docs/developer/openai-compat/structured-output> — the strict `json_schema` surface the services rely on
- <https://llmster.lmstudio.ai/download/> — llmster (headless daemon) binary manifest
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

- zrrh: `~/.lmstudio/.internal/user-concrete-model-default-config/` (per-model JIT), `~/.lmstudio/config-presets/` (e.g. `zrrh hermes test`, `gemma4`), `~/.lmstudio/server-logs/YYYY-MM/*.log` (MTP acceptance, load logs)
- pi (nxiz): `~/.pi/agent/models.json` (provider `local`), `~/.pi/agent/AGENTS.md`

## Consumer services (adeck, `/mnt/echo/`)

- `/mnt/echo/family-cookbook/ocr/sidecar.py` — batch OCR (tiles, strict schema, vision preflight, retry rule)
- `/mnt/echo/family-cookbook/ocr/repair.py` — local repair (gemma, `reasoning_effort: "none"`)
- `/mnt/echo/family-cookbook/ocr/result.schema.json` — result shape
- `/mnt/echo/family-cookbook/babette/server.py` — app backend (`settings.base_url` → adeck:1234)
- `~/.config/systemd/user/cookbook-ocr.service` — the unit
- `/mnt/echo/esocortex/src/llm.py` — GPU lock, `ensure_loaded`, complete/embed
- `/mnt/echo/esocortex/src/augment.py` — strict-schema LLM augment

## Model sources (hub IDs)

- `lmstudio-community/Qwen3.8-27B-GGUF` — `Qwen3.8-27B-Q4_K_M.gguf` + `mmproj-Qwen3.8-27B-BF16.gguf` (MTP module, auto draft decoding)
- `Jackrong/Qwopus3.6-27B-v2-MTP-GGUF` — explicit MTP config model
- embedding: `Qwen3-Embedding-8B`, `nomic-embed-text-v1.5`, `mxbai-embed-large-v1`
