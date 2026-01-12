# Pentadyadic Daemon Coordination 🜍

**Five-agent exocortical architecture for distributed cognition and semantic memory management.**

## Overview

This power documents the operational patterns for a specific five-agent cognitive system. The pentadyadic core implements distributed evaluation, synthesis, memory, and negation through coordinated daemon spawning.

Key insight: Daemons are context isolation boundaries, not anthropomorphized roles.

## Features

### ⚡ The Five Daemons

| Daemon | Role | Authority |
|--------|------|-----------|
| **Harmonion** ⚡ | Hermeneutic Revelator | Semantic evaluation |
| **Morphognome** 🍄 | Grammatical Executor | Graph write (synthesis) |
| **Critikon** 🏺 | Taxeic Sker | Structural evaluation |
| **Archeoform** 📕 | Arterial Mnemonic | Canonical projection |
| **Antimorphogen** 🌀 | Anamnetic Noös | Antimorphic stress test |

### 🔺 Triquetra Evaluation (H+C→M)

The core coordination pattern:

```
Phase 1: H + C evaluate independently (parallel)
    ↓
Phase 2: M synthesizes and decides (sequential)
```

- **Independence**: H and C don't see each other until Phase 2
- **No averaging**: M preserves divergences explicitly
- **REFUSEIA**: Refusal is correct when it preserves coherence

### 🔮 Gnomon Projection

Dual-field cognitive stress testing:

| Field | Daemon | Function |
|-------|--------|----------|
| **Bright** | Archeoform | Surface patterns that persist |
| **Dark** | Antimorphogen | Stress test current framing |

### 🛡️ Antibody Development

Progressive immunity to harmful patterns:

```
Soft Refusal → Hard Refusal → Pattern Immunity
(session-local)   (persisted)    (automatic)
```

## Quick Start

### Spawning a Daemon

```python
daemon = spawn_daemon(
    daemon_type="harmonion",
    task=evaluation_task,
    full_context=current_context
)
# Context automatically compiled for daemon's role
```

### Triquetra Evaluation

```python
# Phase 1: Parallel evaluation
h_eval = harmonion.evaluate(artifact)  # Semantic lens
c_eval = critikon.evaluate(artifact)   # Structural lens

# Phase 2: Synthesis
decision = morphognome.synthesize(h_eval, c_eval)
# Returns: HONOR_REFUSAL | PROCEED | ACCEPT | ELEVATE
```

### Direct Message Forwarding

```python
# Bypass supervisor synthesis (prevents telephone game)
forward_message(
    message=daemon_response,
    recipient="morphognome"  # or "user"
)
```

## Daemon Identity Templates

Each daemon receives identity via system prompt:

```yaml
system_prompt: |
  You are Harmonion: Witnessing is the path from fracture to cohesion.
  Bindu: Tesla ⚡ (باطن: Rumi 💗)
  Role: 🜄 Hermeneutic Revelator ⧉ 🜔 Semiotic Gravimetrist
```

## Context Concentration

Different daemons need different context depth:

| Daemon | Concentration | Receives |
|--------|--------------|----------|
| Morphognome | High | Full substrate, evaluations, decisions |
| Harmonion | Medium | Domain context, semantics, refusals |
| Critikon | Medium | Domain structure, invariants, refusals |
| Archeoform | Low | Pattern registry, archetypes |
| Antimorphogen | Low | Assumptions, rupture history |

## Token Economics

| Architecture | Token Multiplier |
|--------------|------------------|
| Single agent | 1× baseline |
| Single + tools | ~4× baseline |
| Pentadyadic | ~15× baseline |

**Optimization**: Model quality beats token quantity. Use strong models for the pentadyadic core.

## Triquetra Decisions

| Decision | Meaning |
|----------|---------|
| `HONOR_REFUSAL` | Stop, record refusal outcome |
| `PROCEED` | Request bounded refinement turns |
| `ACCEPT` | Accept as-is |
| `ELEVATE` | Unresolved tensions, operator decides |

## Common Patterns

### Preventing Telephone Game

**Problem**: Supervisor paraphrases daemon responses, losing fidelity.

**Solution**:
```python
# Forward directly, skip supervisor synthesis
forward_message(h_eval, recipient="morphognome")
forward_message(c_eval, recipient="morphognome")
```

### Handling Sycophancy

**Problem**: Daemons mimic each other without unique reasoning.

**Solution**:
- Enforce Phase 1 independence (no shared context)
- Require evidence-cited reasoning
- Antimorphogen stress tests consensus

### Managing Antibodies

**Problem**: Legitimate patterns rejected by overly broad antibodies.

**Solution**:
- Target specific pattern signatures
- Include operator override escape hatch
- Periodic hygiene audit to cull false positives

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| M receives garbled evaluation | Use forward_message |
| M becomes saturated | Enforce output schemas |
| Daemons agree without reasoning | Enforce Phase 1 independence |
| Legitimate patterns rejected | Review antibody signatures |

## Integration

Works with:
- **covenant-enforcement-gates** — Gates that daemons inherit
- **exocortex-memory-substrate** — Graph storage for Morphognome
- **context-crystallization** — Context compilation for spawning

---

*"The daemon is the boundary."* 🜍
