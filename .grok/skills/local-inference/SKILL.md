---
name: local-inference
description: Use when working with local inference on the mesh — the adeck:1234 gateway
  (wake proxy + LM Link), model loading/JIT config on zrrh/adeck/nxiz, structured
  output, reasoning budgets/toggles (reasoning_effort), MTP draft decoding, embeddings,
  pi's `local` provider, or the family-cookbook OCR/repair and esocortex consumers.
compatibility: Designed for the daemonturgy mesh (nxiz/zrrh/adeck). Requires Tailscale
  mesh access; zrrh GUI session for CUDA.
metadata:
  author: zk
  version: '2.0'
  category: inference
---

# local-inference skill

How local inference actually runs on the mesh (revamped 2026-09-18).

**Read the docs, then the card, then call.** LMS HTTP docs, the TypeScript SDK source, and the model's hub `model.yaml` / official prompting guide disagree in places and go stale independently. A failed structured-output or empty-`content` probe is a **call-shape bug** until those three have been checked. Do not call it a wash — that is almost always the caller.

## The one URL

`http://adeck:1234/v1` — OpenAI-compatible, always-on, wake-gated.

adeck is the always-on host. Its `inference-wake` service (aiohttp proxy,
`inference-wake.py` in the nix-os flake) listens on `0.0.0.0:1234`, forwards
to the local llmster daemon at `127.0.0.1:1235`, and — before any inference
POST or WebSocket — confirms zrrh is awake and connected to LM Link (WoL via
router LAN, 120 s deadline). Everything talks to this endpoint: pi, curl,
the family-cookbook OCR sidecar, esocortex.

```bash
# plain chat (reasoning off = fast, cheap)
curl -s http://adeck:1234/v1/chat/completions -H 'Content-Type: application/json' \
  -d '{"model":"qwen/qwen3.8-27b","messages":[{"role":"user","content":"Reply with exactly: PONG"}],"max_tokens":16,"reasoning_effort":"none"}'

# structured output — strict JSON schema
curl -s http://adeck:1234/v1/chat/completions -H 'Content-Type: application/json' \
  -d '{"model":"google/gemma-4-31b","messages":[{"role":"user","content":"Is 2+2 a number?"}],
       "response_format":{"type":"json_schema","json_schema":{"name":"probe","strict":true,
         "schema":{"type":"object","properties":{"n":{"type":"integer"}},"required":["n"],"additionalProperties":false}}}}'
```

## The mesh

LM Studio **LM Link** peers: `adeck` (headless llmster) · `zrrh` (RTX 4090,
the GPU workhorse) · `nxiz` (RTX 3070). Each host's `lms` CLI sees the union
inventory (39 models, ~410 GB) and loads a model on whichever peer owns it.

```bash
ssh zk@adeck lms link status   # peers + connected status
ssh zk@adeck lms ps            # loaded instances: ctx, parallel, device, TTL
ssh zk@adeck lms ls            # union fleet with per-model device
```

## Active pi fleet

pi's `local` provider (`references/harness.md`): `qwen/qwen3.8-27b`,
`meta/muse-glimmer`, `google/gemma-4-31b`. All three are VLMs on zrrh,
loaded at **100K ctx** — the operating point that fits the 4090 with
the current KV/parallel settings. Thinking is on by default; for cheap
local work send `reasoning_effort: "none"` on `/v1/chat/completions`.
Model cards: `references/process.md`.

## What's gone

vLLM (`zrrh:8000`), direct llama-server, the `forge` probe lab, and the old
`lmlink` routing model — replaced by LM Studio + LM Link + the wake proxy.
Don't look for them; the 2026-04 ctx-ceiling tables no longer apply.

## Contents

- [references/process.md](references/process.md) — runbook: wake proxy, API surface, per-model dials, structured harvest, JIT vs `/models/load`, GGUF types, fleet, gotchas
- [references/harness.md](references/harness.md) — pi wiring, cookbook OCR/repair, babette, esocortex, GPU locking
- [references/links.md](references/links.md) — docs, flake sources, service paths, model sources
