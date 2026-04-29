---
name: local-inference
description: Use when running inference probes on the mesh, routing tasks to pi or hermes harnesses, or configuring model loading across LM Studio (adeck:1234), vLLM (zrrh:8000), or llama-server (zrrh direct). Covers gateway config, ctx ceiling procedure, tool-call probing, KV quant config, dense vs MoE tradeoffs, and harness architecture.
compatibility: Designed for the daemonturgy mesh (nxiz/zrrh/adeck). Requires nix develop flake shell and Tailscale mesh access.
---

# local-inference skill

Reference docs for the daemonturgy mesh inference lab.

## Contents

- [references/process.md](references/process.md) — probe procedure, gateway config, proven ceilings, gotchas
- [references/harness.md](references/harness.md) — pi vs hermes architecture, vLLM, llama-server, provider wiring
- [references/links.md](references/links.md) — LM Studio SDK, llama.cpp, pi, hermes documentation links

## Quick reference

**LM Studio gateway:** `adeck:1234` — all SDK and OpenAI endpoint calls for LMS-served models.

**vLLM (NVFP4/modelopt models):** `http://zrrh:8000` — not routed through adeck. Direct only.

**llama-server (direct/benchmarking):** `zrrh` via `scripts/launch_llamacpp_zrrh.sh`

**Run a ctx ceiling probe:**
```bash
nix develop --command python3 scripts/ctx_optimize_probe.py <model> \
  --gateway adeck:1234 --out-dir runs/fit/<run-id>
```

**Run a tool call probe:**
```bash
nix develop --command python3 scripts/tool_call_probe.py <model> \
  --gateway http://adeck:1234/v1 --ctx 65536 --out-dir runs/fit/<run-id>
```

**Check what's loaded / unload before new probe:**
```bash
ssh zk@adeck lms ps
ssh zk@adeck "lms unload <model-id>"
```

See [references/process.md](references/process.md) for full procedure, proven ceilings table, and gotchas.
