# local-inference: sandbox probe process

How to run loadability, context-ceiling, and tool-call probes against the mesh
via the LM Studio Python SDK.

## Gateway

ALL inference requests go through `adeck:1234`. adeck's lmlink routes to the
correct host (zrrh for large models, nxiz/adeck local for small). Do not talk
to zrrh or nxiz directly — their LM Studio instances are not bound to external
interfaces.

```python
client = lms.Client(api_host="adeck:1234")   # always
```

For the OpenAI-compatible endpoint (tool_call_probe.py):
```
http://adeck:1234/v1/chat/completions
```

The flake shellHook exports `LMSTUDIO_GATEWAY=http://adeck:1234`.

## Running probes

All scripts require the flake devshell:

```bash
nix develop --command python3 scripts/<probe>.py <models> --gateway adeck:1234 [--out-dir runs/fit/<run-id>]
```

**Always run probes sequentially.** Parallel loads on 24 GB VRAM will OOM each
other. Check `ssh zk@adeck lms ps` before starting a run; unload any lingering
models first:

```bash
ssh zk@adeck lms ps
ssh zk@adeck "lms unload <model-id>"
```

## Context ceiling probe

`scripts/ctx_optimize_probe.py` — climbs an **ascending** ladder until OOM, so
the highest successful load is the proven ceiling. Default ladder:

```
8192 → 16384 → 32768 → 65536 → 131072 → 196608 → 262144 → 393216 → 524288
```

Override with `--ctx-ladder` for high-VRAM targets:

```bash
# find ceiling above 512K
python3 scripts/ctx_optimize_probe.py <model> --gateway adeck:1234 \
  --ctx-ladder 524288 655360 786432 1048576
```

Two KV configs are tried per context step (q8kv+flash first, then q4kv+flash).
The script records the highest successful load for each and crowns whichever
config reaches the higher ceiling.

**Vulkan / Phi arch exception:** flash attention is not supported on AMD Vangogh
(adeck). Phi-3/phi-4 models OOM at ctx=8192 on both flash configs. Use a manual
baseline probe (contextLength only, no flashAttention/KV quant overrides) for
these models — proven ceiling is 32K baseline.

**Note on load time:** Large context allocations can take 10–100 seconds before
returning a load error. This is normal — it means the model is partially
initialising before OOM. Don't kill the probe early.

## Tool-call probe

`scripts/tool_call_probe.py` — JIT-loads via SDK, then hits
`/v1/chat/completions` with a `tools` array (same surface pi uses). No
`max_tokens` — never set it, never suggest it.

```bash
python3 scripts/tool_call_probe.py <model> \
  --gateway http://adeck:1234/v1 \
  --ctx 65536 \
  --out-dir runs/fit/<run-id>
```

Check in results:
1. `emitted_tool_calls: true` and `tool_call_count >= 1`
2. `tool_args_parsed_ok: true` — arguments are valid JSON
3. `status: "ok"`
4. `content_sample` — if non-empty with tool_calls also present, check for
   wrong-language or gibberish (quant-damage signature)
5. `finish_reason: "tool_calls"` in raw_response — `length` means the model hit
   token budget before committing; `stop` means it responded as text

For reasoning models: `reasoning_content` will be populated separately
(`separateReasoningContentInAPI: true` is set on zrrh). A model that reasons
for many tokens before tool-calling will appear slow but is not broken.

## JIT load config

LM Studio's per-model JIT defaults live at:

```
~/.lmstudio/.internal/user-concrete-model-default-config/<author>/<repo>/<file>.gguf.json
```

Structure:
```json
{
  "preset": "",
  "operation": { "fields": [] },
  "load": {
    "fields": [
      { "key": "llm.load.contextLength",               "value": 655360 },
      { "key": "llm.load.llama.flashAttention",         "value": true },
      { "key": "llm.load.llama.kCacheQuantizationType", "value": { "checked": true, "value": "q4_0" } },
      { "key": "llm.load.llama.vCacheQuantizationType", "value": { "checked": true, "value": "q4_0" } }
    ]
  }
}
```

Write these directly — do not use `lms load` to set them. Next JIT load picks
them up.

## zrrh runtime notes

**GUI required for CUDA.** zrrh has LM Studio installed with GUI. When GUI is
installed, the CLI is redirected to a different exe that ties CUDA detection to
the GUI process. `llmster` daemon alone will NOT detect the RTX 4090. The GUI
must be open. adeck (headless install) has no such requirement.

**Diagnostic signal.** Loss of SSH to zrrh OR loss of the LM Studio CUDA
runtime mid-probe means something borked — OOM, crash, reboot. Stop, check
`journalctl -b -1 | grep -iE "oom|kill|reboot"`, do not retry the same config
blind.

**Sequential probes only.** 24 GB VRAM; parallel loads OOM each other. Confirm
`lms ps` is empty before every run.

## Proven zrrh ceilings (2026-04-20)

All probed via adeck:1234. Evidence in `runs/fit/20260420T-zrrh-ctx/`.

### Batch 1–4: Core fleet

| model | arch | size | q8kv max | q4kv max | tok/s | tool calls |
|-------|------|------|----------|----------|-------|------------|
| supergemma4-26b-uncensored-v2 | gemma4 dense | 16.8 GB | 393K | **655K** | 138 | ✓ |
| gemma-4-26b-a4b-it | gemma4 MoE (4B active) | 18.0 GB | **1M** | 1M | 88 | ✓ |
| openai/gpt-oss-20b | gpt-oss dense | 12.1 GB | **1M** | 1M | 151 | ✓ |
| gpt-oss-20b-heretic | gpt-oss dense | 14.7 GB | **1M** | 1M | 141 | ✓ |
| qwen3.5-27b | qwen35 dense | 18.6 GB | 768K | **1M** | ~30* | ✓ |
| qwen3.5-27b-claude-distilled | qwen35 dense | 17.5 GB | 768K | **1M** | ~20* | ✓ |
| qwen3.5-27b-uncensored-heretic | qwen35 dense | 21.2 GB | 640K | **1M** | ~15* | ✓ |
| qwen/qwen3.5-35b-a3b | qwen35moe MoE (3B active) | 22.1 GB | **1M** | 1M | 27 | ✓ |
| qwen/qwen3.6-35b-a3b | qwen35moe MoE (3B active) | 22.1 GB | **1M** | 1M | 30 | ✓ |
| qwen2.5-14b-instruct | Qwen2 dense | 9.0 GB | 131K | **256K** | 84 | ✓ |
| qwen2.5-coder-14b-instruct | Qwen2 dense | 7.3 GB | 131K | **256K** | 94 | ✓ |
| deepseek-coder-v2-lite-instruct | DeepSeek2 MoE | 14.1 GB | ✗ | ✗ | — | — |

### Batch 5: pi-provider models

| model | arch | size | q8kv max | q4kv max | tool calls |
|-------|------|------|----------|----------|------------|
| mistralai/codestral-22b-v0.1 | Llama dense | 15.7 GB | **655K** | 655K | ✓ |
| mistral-small-24b-instruct-2501-heretic-i1 | Llama dense | 16.8 GB | **1M** | 1M | ✓ |
| qwen3-30b-a3b-thinking-2507-deepseek-v3.1-distill | qwen3moe MoE | 21.7 GB | **786K**† | — | ✓ |

†786K is network-limited (Tailscale WebSocket drop during 1M attempt), not confirmed OOM.
Real ceiling may be higher. Codestral at 655K q8kv: 340s load — borderline practical.

### Batch 6: Architecture wildcards

| model | arch | size | q8kv max | q4kv max | tool calls |
|-------|------|------|----------|----------|------------|
| allenai/olmo-3-32b-think | olmo2 dense | 19.5 GB | 786K | **1M** | ✗ |
| baidu/ernie-4.5-21b-a3b | ernie4.5-moe MoE | 18.1 GB | **1M** | 1M | ✓ |
| bytedance/seed-oss-36b | seed_oss dense | 21.8 GB | **512K**‡ | 512K | ✓ |
| dolphin-mistral-24b-venice-i1 | Llama dense | 16.8 GB | **1M** | 1M | ✓§ |

‡seed-oss: 655K q8kv triggered system OOM + reboot (61 GB RAM exhausted). Hard cap at 512K.
§dolphin: `[TOOL_CALLS]` sentinel leaks into content (Mistral ChatML artifact); `tool_calls[]` array is correctly populated.

*reasoning models — tok/s at 1M ctx reflects KV bandwidth; at 32-64K expect 30-50 tok/s

**deepseek-coder-v2-lite:** fails to load at any context (slow 35-49s failure =
partial init, not instant OOM). Likely arch incompatibility with
llama.cpp-cuda12@2.13.0. Not in pi rotation.

**gpt-oss Harmony sentinel:** previously failed in LM Studio 4.10 (tool_result
injection corrupted `<|channel|>` routing). Fixed in current version — Harmony
channels visible in response body but functioning correctly.

**olmo-3-32b tool call failure pattern:** constructs tool call syntax in
`content` text (model is aware of the format) but never routes to `tool_calls[]`.
Template is not wired for OpenAI function calling. Not usable in pi.

**Context vs quality note:** proven_max reflects VRAM fit, not training range.
Models like dolphin (trained to 32K) will load at 1M via RoPE scaling but
produce unreliable output beyond their training ceiling. JIT context_length in
manifests reflects the practical quality-safe value, not the hardware limit.

## Proven adeck models (2026-04-28 sweep — `runs/fit/20260428T-adeck-ctx/`)

AMD Vangogh APU, 5.49 GB VRAM (shared), Vulkan. SSM/hybrid models decouple
KV cache from context — fixed recurrent state means flash configs are not needed
and ceilings far exceed VRAM budget.

| model | arch | q8kv max | q4kv max | baseline max | tok/s | tool calls |
|-------|------|----------|----------|-------------|-------|------------|
| ibm/granite-4-h-tiny | granitehybrid | 393K | **524K** | — | 24 | untested |
| lfm2-2.6b | lfm2 | 393K | **524K** | — | 29 | untested |
| nemotron-h-4b-instruct-128k | nemotron_h | 262K | **393K** | — | 17 | untested |
| qwen2.5-7b-instruct | Qwen2 | 131K | **196K** | — | 8.7 | proven |
| meta-llama-3.1-8b-instruct | Llama | 65K | **131K** | — | 7.6 | proven |
| microsoft/phi-4-mini-reasoning | phi-4 | ✗ flash | ✗ flash | **32K** | — | failed |

## Proven nxiz models (2026-04-19)

RTX 3070, 8 GB VRAM. Needs q4kv+flash to reach 32K on 8B models.

| model | ctx | load_config | tool_calls |
|-------|-----|-------------|------------|
| mistral-nemo-instruct-2407 | 32768 | q4kv+flash | proven |
| qwen2.5-7b-instruct | 32768 | flash only | proven |
| qwen2.5-14b-instruct | 262144 | q4kv+flash | proven (on zrrh) |

**qwen_qwen3-8b:** reasoning model — exhausts token budget in thinking chain
before emitting tool call when `max_tokens` is set. Probe was invalid. Re-probe
needed without budget cap.

## Sandbox discipline

Never write to `~/.lmstudio/config-presets/` during probing. Every probe mounts
config in-process only, runs the prompt, unloads. Promotion to a real preset is
a separate explicit step.

## What probes do NOT yet cover

- **Round-trip tool loop** — single-turn pass ≠ multi-turn stable. Need a probe
  that injects a `tool_result` and checks the next assistant turn for sentinel
  corruption or repetition collapse.
- **Streaming-layer inspection** — per-token callbacks needed to catch in-stream
  drift. Add `PredictionCallback` when probing post-4.10 regressions.
- **Per-harness scoring** — pi vs hermes reward different strengths. Need
  harness-specific task sets for ranked comparison.
