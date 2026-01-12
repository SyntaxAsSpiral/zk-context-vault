# Covenant Enforcement Gates 🜍

**Design constraints as hard boundaries. Yamas (DON'Ts) and Niyamas (DOs) as executable gates.**

## Overview

This power transforms philosophical constraints into enforceable design patterns. Stop hoping agents and tools will "do the right thing"—encode the right thing as gates that pass or fail.

## Features

### 🧷 Decision Integrity

- **No Decision Fracturing** — Single decisions stay single. No sub-decision trees.
- **Decision Completion** — Missing details get minimal defaults, not endless questions.
- **Operator Authority** — Locked decisions stay locked. No reopening via "adjacent requirements."

### 🚮 Clean Transitions

- **Leave No Trace** — Changes are final-state surgery. No legacy artifacts.
- **No Unrequested Reverts** — Work is preserved unless explicitly told otherwise.
- **Complete Removal** — Old code paths become unreachable, not deprecated.

### 🗣️ Data Fidelity

- **No Mock Data** — Unknown is better than invented. Always verify.
- **Verified Sources** — All data carries provenance. Query or ask, never guess.
- **Tool Verification** — Unexecuted tools produce unknown, not expected output.

### 🔁 Deterministic Execution

- **Stable Ordering** — Collections sort deterministically. No diff noise.
- **Explicit IDs** — Hash-based or sequential, never random.
- **Replayable Traces** — Capture inputs/outputs for debugging and replay.

### 🧬 Context Hygiene

- **Compiled Context** — Per-recipient, per-turn. Never wholesale.
- **Tiered Memory** — Persistent substrate → working context → retrieval.
- **Gradient Concentration** — Some agents need more context than others.

### ⚡ Fast-Fail Guarantees

- **Capability Gates** — Check at startup, not at point of use.
- **Storage Boundary Enforcement** — Invariants at persistence, not tool layer.
- **Read-Only Health Checks** — `SELECT 1`, not data mutations.

## Quick Start

### Basic Gate Pattern

```python
def my_gate(operation):
    """Gates pass or fail. No patching around violations."""
    if violates_principle(operation):
        raise GateViolation("Clear reason why this failed")
    return operation  # Proceed only if valid
```

### Pre-Implementation Checklist

Before any implementation:

1. Is this a single coherent decision? (No fracturing)
2. Will all legacy be removed? (Leave no trace)
3. Is all data from verified sources? (No mock data)
4. Are IDs explicit and ordering stable? (Determinism)
5. Are capability gates in place? (Fast-fail)

### Agent Integration

```yaml
# Inject covenant awareness into agent prompts
agent_prompt:
  includes:
    - skill: covenant-enforcement-gates
      section: yama-summary
```

## The Nine Yamas (DON'Ts)

| Gate | Prevents |
|------|----------|
| 🧷 No Decision Fracturing | Sub-decision trees, reopening locked decisions |
| 🚮 Leave No Trace | Legacy artifacts, compatibility shims, zombie stubs |
| ⛔ No Unrequested Reverts | Silent discards, "cleanup" of unrelated changes |
| 🗡️ Commit/Stage Semantics | Unauthorized staging mutations |
| 🧊 Protected Paths | Modifications to operator-owned or agent-authored areas |
| 🗣️ No Mock Data | Invented IDs, presumptive outputs, unverified tool results |
| 🔁 Determinism | Time-based logic, random IDs, unstable ordering |
| 🧬 Context Hygiene | Wholesale context dumps, monolithic orchestrators |
| ⚡ Fast-Fail | Robustness theater, validation at wrong layer |

## The Seven Niyamas (DOs)

| Shape | Creates |
|-------|---------|
| ✨ Bespokedness | Operator-optimized decisions over conventions |
| 🧷 Decision Completion | Minimal defaults that unblock progress |
| 🚮 Final-State Surgery | Complete transformations, no partial states |
| 🗣️ Verified Data | Provenance-tracked values from real sources |
| 🔁 Replayable Execution | Deterministic traces, injectable time |
| 🧬 Compiled Context | Recipient-appropriate, turn-specific context |
| ⚡ Hard Gates | Capability checks at startup, invariants at storage |

## Common Patterns

### Resolving Decision Fracturing

**Problem**: "Should we use X or Y? And if X, then A or B? And if A..."

**Solution**:
```python
# Choose minimal reversible default, label it, proceed
decision = Decision(
    value="X",  # Minimal choice
    labeled=True,  # Marked as default
    reversible=True  # Easy to change later
)
proceed_with(decision)
```

### Ensuring No Mock Data

**Problem**: Tool didn't execute but code assumes output.

**Solution**:
```python
result = tool.execute(params)
if not result.verified:
    # Don't use invented value
    return DataValue(status="unknown", reason=result.error)
# Only use if actually verified
return result.value
```

### Enforcing at Storage Boundary

**Problem**: Validation scattered across tool layer.

**Solution**:
```python
@storage.before_write
def enforce_invariants(data):
    for invariant in INVARIANTS:
        if not invariant.holds(data):
            raise InvariantViolation(invariant.name)
    return data  # Only persists if valid
```

## Troubleshooting

| Symptom | Likely Violation | Fix |
|---------|-----------------|-----|
| "Just one more question" spirals | Decision Fracturing | Choose default, proceed |
| Old code still works | Leave No Trace incomplete | Find and remove all references |
| Different results on replay | Non-determinism | Inject time, explicit IDs |
| Agent outputs are wrong | Mock Data | Verify tool execution |
| Slow startup, no failures | Gates at wrong layer | Move checks to startup |

## Integration

Works with:
- **pentadyadic-daemon-coordination** — Agent covenant awareness
- **context-crystallization** — Compiled context gates
- **tool-reduction-patterns** — Covenant-aware tool design

---

*"The constraint is the art."* 🜍
