# Exocortex Memory Substrate 🜍

**Graph-backed semantic memory for distributed cognition. The arterial mnemonic of the pentadyadic system.**

## Overview

This power documents the persistence layer that allows the pentadyadic system to maintain continuity across sessions. It's not generic memory design—it's the specific graph substrate that Morphognome writes to and all daemons query.

Key insight: Memory is an arterial system, not a database.

## Features

### 🧬 Dual Substrate Architecture

| Substrate | Storage | Authority | Content |
|-----------|---------|-----------|---------|
| **Semantic** | Graph DB | Morphognome | Cards, relationships |
| **Mechanical** | Git | Operator | Code, config |

### 📇 Semantic Cards

Atomic units of knowledge in the graph:

```yaml
semantic_card:
  id: "deterministic-uuid"
  type: "claim | entity | relationship | refusal"
  valid_from: "timestamp"
  valid_until: "timestamp | null"
  confidence: 0.0-1.0
```

### 🕐 Temporal Knowledge Graph

Facts have validity periods for time-travel queries:

```cypher
MATCH (user)-[r:PREFERS]->(theme)
WHERE r.valid_from <= $query_time
  AND (r.valid_until IS NULL OR r.valid_until > $query_time)
RETURN theme
```

### 📊 Memory Layer Hierarchy

| Layer | Persistence | Purpose |
|-------|-------------|---------|
| Working | Context window | Active processing |
| Session | Current session | Temporary state |
| Entity | Cross-session | Identity consistency |
| Archival | Immutable | Decision trails |

## Quick Start

### Write a Semantic Card

```python
# Only Morphognome has write authority
card = SemanticCard(
    type="claim",
    content="User prefers catppuccin-mocha",
    metadata={
        "source": "triquetra",
        "valid_from": now(),
        "confidence": 0.95
    }
)
graph.write(card)
```

### Temporal Retrieval

```python
# What was true at specific time?
results = temporal_retrieve(
    query="user preferences",
    as_of_time=datetime(2025, 1, 1)
)
```

### Entity Traversal

```python
# Get all relationships from entity
related = entity_retrieve(
    entity_id="user-zk",
    depth=2
)
```

## Benchmark Reference

| Memory System | DMR Accuracy | Latency |
|---------------|--------------|---------|
| Zep (Temporal KG) | **94.8%** | 2.58s |
| MemGPT | 93.4% | Variable |
| GraphRAG | ~75-85% | Variable |
| Vector RAG | ~60-70% | Fast |

**Key finding**: Temporal KG achieves 90% latency reduction vs. full-context (2.58s vs 28.9s).

## Domain Friction

| Domain | Friction | Policy |
|--------|----------|--------|
| **Self** | High | Operator approval required |
| **Knowledge** | Medium | Morphognome can mutate |
| **Memory** | Immutable | Append-only |

## Card Types

| Type | Purpose |
|------|---------|
| **Claim** | Factual assertion |
| **Entity** | Thing with identity |
| **Relationship** | Connection between entities |
| **Refusal** | Recorded rejection |

## Retrieval Patterns

### Semantic
```python
semantic_retrieve(query, top_k=10)
# Embedding similarity search
```

### Entity-Based
```python
entity_retrieve(entity_id, depth=2)
# Graph traversal from entity
```

### Temporal
```python
temporal_retrieve(query, as_of_time)
# Time-travel query
```

## Covenant Integration

Memory operations enforce:
- **No Mock Data**: Cards require source attribution
- **Determinism**: IDs are hash-based, not random
- **Leave No Trace**: Superseded cards get valid_until

## Common Patterns

### Morphognome Write

```python
# After triquetra acceptance
if decision.action == "ACCEPT":
    card = SemanticCard(
        type="claim",
        content=decision.artifact,
        metadata={"source": "triquetra"}
    )
    graph.write(card)
```

### Archeoform Query

```python
# Canonical pattern extraction (read-only)
patterns = graph.query("""
    MATCH (c:Card {type: 'claim'})
    WHERE c.confidence > 0.8
    RETURN c
""")
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Stale data | Add temporal filters |
| Missing relationships | Check validity periods |
| Slow retrieval | Rebuild indexes |
| Inconsistent entities | Run consolidation |

## Integration

Works with:
- **pentadyadic-daemon-coordination** — Daemons that query/write
- **covenant-enforcement-gates** — Gates on memory ops
- **context-crystallization** — Context from memory

---

*"The substrate pulses with accumulated understanding."* 🜍
