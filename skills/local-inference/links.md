# local-inference: useful links

## LM Studio

- <https://lmstudio.ai/docs/developer/> — developer docs root (GUI help points here)
- <https://lmstudio.ai/docs/python/llm-prediction/parameters> — Python SDK prediction/load params (stub page; defers to TS types)
- <https://github.com/lmstudio-ai/lmstudio-python> — SDK source
- <https://llmster.lmstudio.ai/download/> — llmster binary manifest

## llama.cpp

- <https://github.com/ggerganov/llama.cpp> — upstream (LM Studio is llama.cpp + ergonomics)

## Agents / harnesses

### pi (badlogic/pi-mono)
- <https://github.com/badlogic/pi-mono> — monorepo root (pinned v0.67.68 in mirkolenz snapshot)
- <https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent> — the `pi` coding-agent package (minimal terminal harness: read/write/edit/bash)
- Config lives at `~/.pi/agent/settings.json` (global) + `.pi/settings.json` (project)
- Project instructions auto-load from `AGENTS.md` / `CLAUDE.md` in cwd and parents
- Custom providers via `~/.pi/agent/models.json` — OpenAI- or Anthropic-compatible endpoints → this is the LM Studio hook

### hermes (Nous Research)
- <https://github.com/NousResearch> — Nous Research org (Hermes Agent released Feb 2026)
- <https://github.com/alchaincyf/hermes-agent-orange-book> — HuaShu's community guide (CC BY-NC-SA, Chinese-language "橙皮书"/Orange Book series), covers Hermes' self-improving loop, three-layer memory, auto-skill creation
- <https://github.com/ksimback/hermes-ecosystem> — "Hermes Atlas": community-curated index of 84 Hermes-compatible tools/skills/integrations across 12 categories; single-page app + RAG chatbot over the corpus. Unofficial. Cloud-oriented (OpenRouter + Gemma 4), no local-endpoint docs — treat as discovery index, not a local-inference reference.

#### Cloud fallbacks (not local, kept for completeness)
- **Google AI Studio → Vercel AI Gateway → Hermes**: Google AI Studio grants 1,500 free daily requests to Gemma 4 31B. Route via BYOK (Google) in Vercel AI Gateway, then select "Vercel AI Gateway" + Google model in Hermes. Useful when the mesh is down or for A/B comparison against local runs; not private.

## Reference: mirkolenz nixos snapshot patterns

- `tmp/nixos/pkgs/derivations/llmster-bin/package.nix` — Bun-binary patching via `LD_LIBRARY_PATH` + `addDriverRunpath` (skip rpath)
- `tmp/nixos/pkgs/derivations/pi-agent-bin/` — GitHub binary fetch pattern
- `tmp/nixos/home/options/pi-agent.nix` — home-manager module shape (enable + settings JSON → `~/.pi/agent/settings.json`)
