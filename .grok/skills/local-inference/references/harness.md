# local-inference: harness architecture

Which agent harness to use for which task, and why.

## Two harnesses, two roles

**pi** (`badlogic/pi-mono`) — structured coding agent. Lightweight, stateless per session,
minimal system surface. Uses a `tools` array over the OpenAI-compatible endpoint.
Config: `~/.pi/agent/models.json` (providers + models) + `~/.pi/agent/settings.json`.

**hermes** (Nous Research) — full agentic system. Persistent shell, browser, file ops, cron,
memory, skills, delegation. Runs on adeck as the always-on orchestrator.
Config: `~/.hermes/config.yaml`.

## Division of labor

```
hermes (adeck, orchestrator)
  └── delegates short tool tasks → pi (nxiz/zrrh models via NXIZ/ZRRH provider)
```

Nxiz models (RTX 3070, 8 GB) are good for short focused tool-call tasks.
Zrrh models (RTX 4090, 24 GB) handle long-context or high-precision tasks.
Hermes is the long-running coordinator: session memory, scheduling, real tool
execution, subagent delegation.

## pi invocation (non-interactive)

```bash
pi --provider NXIZ --model mistral-nemo-instruct-2407 --no-session -p "<task>"
pi --provider ZRRH --model qwen2.5-14b-instruct --no-session -p "<task>"
```

`--no-session` prevents session state accumulation for one-off calls.
`--provider` must match the key in `models.json` (case-sensitive: `NXIZ`, `ZRRH`).

## hermes invocation (non-interactive)

```bash
hermes chat -m <lms_id> -q "<task>" -Q --max-turns <n>
```

`-Q` suppresses banner/spinner/previews — clean output for programmatic use.
`-m` overrides the default model while keeping the configured `base_url`
(`http://localhost:1234/v1` on adeck = the LM Studio inference gateway).

## hermes provider config

hermes on adeck uses `provider: custom` with `base_url: http://localhost:1234/v1`.
The `--provider` CLI flag's hardcoded enum (openrouter, anthropic, etc.) does NOT
include custom — it only applies to cloud providers. The custom config is set via
`hermes config edit` or `hermes config set model <id>`.

## Probe surface differences

| | pi | hermes |
|---|---|---|
| tools | synthetic stubs (`get_weather`, etc.) | real tools (bash, file, browser) |
| probe signal | `tool_calls` array in JSON response | task actually completes (bash output matches) |
| state | stateless | persistent shell session |
| good probe task | "call get_weather for London" | "run `echo tool-call-test` and report output" |

Don't use synthetic tool probes against hermes — it will try to execute them and fail.
Use real shell/file tasks that produce verifiable output.

## ZRRH models in pi

Proven ZRRH models (14B+, 4090) are wired into pi's ZRRH provider via adeck's
inference gateway. adeck:1234 routes to zrrh via lmlink. Same pi invocation,
different `--provider ZRRH`.

## vLLM on zrrh (NVFP4 / modelopt-only models)

For models with no GGUF release (NVFP4/modelopt format only):

```
Endpoint: http://zrrh:8000
Currently serving: AEON Qwen3.6-27B NVFP4
Launch: scripts/launch_vllm_zrrh.sh
```

Runs in emulation on RTX 4090 (sm_89; NVFP4 native requires sm_100+ Blackwell) —
dequants FP4→BF16 per layer, ~0.8 tok/s. Venv at `~/.venv/vllm/` on zrrh.

**Not routed through adeck:1234.** Hit `http://zrrh:8000` directly for vLLM.

## llama-server on zrrh (direct / benchmarking)

For testing without LMS or vLLM overhead:

```bash
# binary: `llama` on zrrh
# launch: scripts/launch_llamacpp_zrrh.sh
```

Installed 2026-04-28. Use for direct benchmarking or when LMS GUI is unavailable
(CUDA detection on zrrh is tied to the LMS GUI process — without it, RTX 4090
is invisible to `llmster`).

## Model registry

`scripts/gen_model_registry.py` (repo root) is the single source of truth for all
models across the mesh. Run it to regenerate `models/*.yaml` after any inventory change.
It embeds INVENTORY, EVAL, PI_WIRING, and JIT_CTX dicts — update those dicts, rerun.
