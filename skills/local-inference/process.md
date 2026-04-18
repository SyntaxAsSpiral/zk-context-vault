# local-inference: sandbox probe process

How to run a loadability + coherence probe against LM Studio with the
Python SDK, without touching any live preset.

## Why SDK + why sandbox

- **SDK**: LM Studio's Python SDK lets you JIT-load a model for the life of one request, pass per-load config, and unload. This is the "throwaway eval" surface — the complement to the GUI's persistent-preset surface.
- **Sandbox discipline**: we never write to `~/.lmstudio/config-presets/` during probing. Every probe mounts config in-process only, runs the prompt, unloads, exits. Promotion of a good config to a real preset is a separate, explicit step the operator performs.

## Per-host requirement

LM Studio exposes the SDK against a *local* instance. To sandbox-probe models that are *local to host X*, the SDK must be running on host X (or the gateway on X must accept remote SDK connections — which LM Studio 4.10 does not reliably do for `load_new_instance`). Practically: drop the flake devshell on each host you want to probe. `nxiz` is covered via this repo's `flake.nix`; `zrrh` and `adeck` need the same shell made reachable (either mount the repo over tailscale or `nix shell nixpkgs#python3Packages.lmstudio`).

## The loop

```python
import lmstudio as lms
client = lms.Client(api_host="localhost:1234")   # explicit — default doesn't self-resolve
llm = client.llm.load_new_instance(
    "ibm/granite-4-h-tiny",
    config={"contextLength": 32768},
    ttl=600,
)
result = llm.respond("tell me about yourself")
print(result.content)
print(result.stats.tokens_per_second, result.stats.stop_reason)
llm.unload()
```

Wrapper: `scripts/sandbox_probe.py` at the repo root runs this across an arg list of models, writes per-model JSON to a run dir, and uses a context ladder (32K → 16K → 8K → 4K) to find the ceiling.

## Context ladder — what the response codes mean

LM Studio's overflow error is opaque:

```
Model load error:
  Reported cause: (Exit code: null).
```

There's no distinction in the error between "KV won't fit in VRAM", "weights + KV exceed total memory", or "this arch rejects that rope config". Treat all load failures as "try the next rung down" and let the ladder tell you the ceiling.

## What probes need to capture

1. **loaded_context_length** — first rung that succeeded.
2. **model_info.max_context_length** — what the model *claims* to support natively.
3. **stats.tokens_per_second** + **time_to_first_token_sec** — fitness for chat vs long-gen vs RAG.
4. **stats.stop_reason** — `eosFound` (clean) vs `maxPredictedTokensReached` (truncated) vs other (bad). Anything other than `eosFound` on a short factual prompt is a red flag — possible template drift (see the gpt-oss Harmony signature in `project_observed_failures.md`).
5. **response_sample (first ~1500 chars)** — minimal sanity check that output is coherent English and carries the right self-identity.

## Gotchas

- **`lms.Client()` with no args fails silently.** Always pass `api_host="localhost:1234"`. The "self-resolve" path assumes an environment flag that the SDK doesn't populate under `nix develop`.
- **`ttl=` is the auto-unload timer in seconds.** Set low (300–600) on probes so a crashed run doesn't pin VRAM.
- **Don't assume `max_context_length` from metadata is loadable.** Granite-4 reports 1M; phi-4-mini-instruct reports 131K; actual loadable ceiling on an 8 GB card is much lower.
- **Dense 14B weights leave almost no room for KV on 8 GB.** qwen2.5-coder-14b landed at 8K context on nxiz — any real agent use needs the 14B on zrrh (24 GB), or a smaller coder.
- **Self-identity drift is a template signal, not a bug.** Granite-4 introducing itself as "HermesAI" means the chat template is pulling a sysprompt chunk from somewhere — worth tracing if that model will be used in a harness that depends on identity stability.

## Tool-call probe process

Separate from the loadability ladder. Uses LM Studio's OpenAI-compatible `/v1/chat/completions` endpoint with a `tools` array — the same surface pi uses via its `openai-completions` provider type.

```python
import httpx, lmstudio as lms
client = lms.Client(api_host="localhost:1234")
llm = client.llm.load_new_instance(model_key, config={"contextLength": 8192}, ttl=300)
r = httpx.post("http://localhost:1234/v1/chat/completions", json={
    "model": model_key,
    "messages": [{"role": "user", "content": "What's the current date? Use the tool."}],
    "tools": [{"type": "function", "function": {...}}],
    "tool_choice": "auto",
}, timeout=120)
tool_calls = r.json()["choices"][0]["message"]["tool_calls"]
```

Wrapper: `scripts/tool_call_probe.py`.

**What to check in the response:**
1. `tool_calls[0].function.name` matches a real tool.
2. `tool_calls[0].function.arguments` is a JSON-parseable string.
3. `message.content` (if non-empty) is coherent English — wrong-language content alongside valid tool_calls is a **quant-damage signature** (seen on Qwen2.5-14B at Q3_K_S emitting Thai). The call works but the chat surface is broken.
4. `finish_reason` is `tool_calls` (not `stop` or `length` — the latter two mean the call got cut or the model never committed).

## Quant gotcha

`lms get -y <URL>` auto-picks a quant based on VRAM. On 8 GB that means it'll pick Q3_K_S for 14B models — below the viability floor for coherent chat. **Always** append `@q4_k_m` (or higher) or pass `--select` for interactive choice. Measured: Hermes-3-8B at Q4_K_S gave clean English + clean tool calls at 78 tok/s; Qwen2.5-14B at Q3_K_S gave Thai content + (still) parseable tool calls at 16 tok/s.

## What this does NOT cover

- Tool-call round-trip probing. `respond()` with a plain string sends no tools; to reproduce the gpt-oss Harmony-sentinel leakage you need `llm.act()` with tool definitions matching the harness' contract. Separate probe, separate script.
- Streaming-layer inspection. Per-token callbacks are needed to catch in-stream sentinel drift; add a `PredictionCallback` when we go after the post-4.10 gpt-oss regression.
- Remote-gateway probing. `load_new_instance` via the mesh (e.g. `adeck:1234` routing to a `zrrh`-hosted model) is possible for inference but the load path has been unreliable. For now: SDK runs on the host that owns the weights.
