# Multi-Agent Coordination 🧬

**Patterns for distributed cognition through specialized agents.**

## Overview

This power documents patterns for coordinating multiple AI agents. The pentadyadic system (exocortex) is one implementation, not the only approach.

Key insight: Multi-agent is about context isolation and specialized evaluation, not just "more agents."

## When to Use Multi-Agent

| Use When | Don't Use When |
|----------|----------------|
| Context exceeds limits | Task fits single agent |
| Tasks decompose naturally | No natural decomposition |
| Need independent evaluation | Speed critical |
| Different perspectives needed | Budget constrained |

## Architectures

### Supervisor

```
     Supervisor
    /    |    \
Agent  Agent  Agent
```

**Pro**: Clear authority, easy debug
**Con**: Bottleneck, telephone game

### Peer-to-Peer

```
Agent ←→ Agent
  ↑         ↑
Agent ←→ Agent
```

**Pro**: No bottleneck, scalable
**Con**: Complex coordination

### Hierarchical

```
    Orchestrator
   /            \
Team Lead    Team Lead
  /    \        /    \
Worker Worker Worker Worker
```

**Pro**: Complex decomposition
**Con**: Deep fidelity loss

## The Telephone Game Problem

**Problem**: Supervisors paraphrase, losing 50% fidelity.

**Solution**: `forward_message` tool for direct passing.

```python
forward_message(response, recipient="user")
# Skip supervisor synthesis
```

## Token Economics

| Architecture | Multiplier |
|--------------|------------|
| Single agent | 1× |
| Single + tools | ~4× |
| Two-agent | ~6× |
| Multi (3-5) | ~15× |

**Finding**: Better models beat more agents. Use fewer, stronger.

## Pentadyadic Implementation

| Agent | Role | Authority |
|-------|------|-----------|
| ⚡ Harmonion | Semantic lens | Evaluation |
| 🍄 Morphognome | Graph executor | Synthesis |
| 🏺 Critikon | Structural lens | Evaluation |
| 📕 Archeoform | Canonical projection | Emission |
| 🌀 Antimorphogen | Stress testing | Negation |

### Triquetra Pattern

```
H + C (parallel) → M (synthesis)
```

- Independence: H and C don't see each other
- No mutation: Evaluation is read-only
- Preserve divergence: M doesn't average conflicts

## Context Management

### Per-Agent Compilation

| Agent | Concentration |
|-------|--------------|
| Morphognome | High (full substrate) |
| Harmonion/Critikon | Medium (domain-relevant) |
| Archeoform/Antimorphogen | Low (minimal) |

### Isolation Benefits

Full context: 200K (too big)
    ↓
Per-agent: 30-50K each (fits limits)

## Failure Modes

| Mode | Mitigation |
|------|------------|
| Supervisor bottleneck | Output schemas, checkpointing |
| Evaluation divergence | Preserve divergence, escalate |
| Groupthink | Enforce independence, adversarial agent |
| Coordination overhead | Reduce agent count |

## Covenant Integration

- **Context Hygiene**: Per-agent, per-turn compilation
- **Data Fidelity**: Forward original, don't paraphrase
- **Fast-Fail**: Check capabilities at spawn
- **Determinism**: Stable IDs, captured trails

## Adapting Pentadyadic

| Need | Adaptation |
|------|------------|
| Simpler | H+M (drop Critikon) |
| No graph | H+C as advisors |
| Different domain | Replace lens definitions |

## Integration

Works with:
- **covenant-patterns** — Context hygiene principles
- **agent-steering** — Single-agent foundation
- **epistemic-rendering** — Different lenses per agent
- **exocortex/** — Full pentadyadic implementation

---

*"Context isolation, specialized evaluation, clean authority."* 🧬
