# Exocortex Memory Substrate

*Graph-backed semantic memory for distributed cognition. The arterial mnemonic of the pentadyadic system.*

## Overview

Exocortex Memory Substrate documents the persistence layer that allows the pentadyadic system to maintain continuity across sessions and reason over accumulated knowledge. This is not generic memory system design—it's the specific graph substrate that Morphognome writes to, Archeoform projects from, and all daemons query.

This skill provides:

- **Dual substrate architecture** (semantic graph + mechanical git)
- **Semantic card patterns** for knowledge representation
- **Temporal knowledge graph** operations with validity periods
- **Memory layer hierarchy** optimized for daemon coordination
- **Retrieval patterns** that preserve relationship structure
- **Benchmark reference** for architecture selection

The core insight: Memory is not a database feature—it's an **arterial system** that carries knowledge through the cognitive architecture. The substrate is alive; it pulses with accumulated understanding.

## Dual Substrate Architecture

The exocortex operates on two complementary substrates:

```
┌─────────────────────────────────────────┐
│         SEMANTIC SUBSTRATE              │
│  (Graph: Neo4j, semantic cards, links)  │
│  Authority: Morphognome                 │
│  Content: Claims, relationships, memory │
└─────────────────────────────────────────┘
                    +
┌─────────────────────────────────────────┐
│        MECHANICAL SUBSTRATE             │
│  (Git: versioning, code, config)        │
│  Authority: Operator                    │
│  Content: System artifacts, deployments │
└─────────────────────────────────────────┘
```

| Substrate | Storage | Authority | Content Type |
|-----------|---------|-----------|--------------|
| **Semantic** | Graph DB (Neo4j) | Morphognome | Semantic cards, relationships, claims |
| **Mechanical** | Git repository | Operator | Code, config, system artifacts |

**Critical constraint**: Only Morphognome has graph write authority. All other daemons are read-only during evaluation phases.

---

## Semantic Card Architecture

### Card Structure

Semantic cards are the atomic units of knowledge in the graph substrate:

```yaml
semantic_card:
  id: "card-deterministic-uuid"  # Hash-based, not random
  type: "claim | entity | relationship | refusal"
  content:
    title: "Human-readable title"
    body: "The semantic content"
    source: "Provenance attribution"
  metadata:
    created: "ISO-timestamp"
    modified: "ISO-timestamp"
    valid_from: "ISO-timestamp"
    valid_until: "ISO-timestamp | null"
    confidence: 0.0-1.0
    domain: "self | knowledge | memory"
  relationships:
    - type: "supports | contradicts | refines | supersedes"
      target: "card-id"
      strength: 0.0-1.0
```

### Card Types

| Type | Purpose | Example |
|------|---------|---------|
| **Claim** | Factual assertion | "X is true because Y" |
| **Entity** | Thing with identity | "User preferences for ZK" |
| **Relationship** | Connection between entities | "X depends on Y" |
| **Refusal** | Recorded rejection | "Pattern Z rejected for reason W" |

### Domain Hierarchy

Cards exist in domains with different friction levels:

```
Self Domain (High Friction)
├── Identity claims
├── Preference overrides
└── Protected patterns
    ↓
Knowledge Domain (Medium Friction)
├── Learned facts
├── Accumulated context
└── Entity properties
    ↓
Memory Domain (Immutable)
├── Session transcripts
├── Decision trails
└── Archival snapshots
```

| Domain | Friction | Mutation Policy |
|--------|----------|-----------------|
| **Self** | High | Requires explicit operator approval |
| **Knowledge** | Medium | Morphognome can mutate post-triquetra |
| **Memory** | Immutable | Append-only, no modifications |

---

## Temporal Knowledge Graph

### Why Temporal Structure Matters

Vector stores lose relationship information and temporal validity. If the substrate learns "Customer X purchased Product Y on Date Z," a vector store cannot answer "What products did customers who purchased Y also buy?" because relationship structure is not preserved.

Temporal knowledge graphs add validity periods to facts:

```cypher
// Temporal relationship with validity period
CREATE (user:Entity {id: "user-zk"})
       -[r:PREFERS {
           valid_from: datetime("2025-01-01"),
           valid_until: null,
           confidence: 0.95
       }]->
       (theme:Entity {id: "catppuccin-mocha"})
```

### Temporal Query Patterns

**Point-in-time query**:
```cypher
// What was the user's preference on specific date?
MATCH (user)-[r:PREFERS]->(theme)
WHERE user.id = $user_id
  AND r.valid_from <= $query_time
  AND (r.valid_until IS NULL OR r.valid_until > $query_time)
RETURN theme
```

**Validity range query**:
```cypher
// What preferences were active during time range?
MATCH (user)-[r:PREFERS]->(theme)
WHERE user.id = $user_id
  AND r.valid_from <= $range_end
  AND (r.valid_until IS NULL OR r.valid_until >= $range_start)
RETURN theme, r.valid_from, r.valid_until
```

**Supersession detection**:
```cypher
// Find facts that supersede older facts
MATCH (new:Card)-[s:SUPERSEDES]->(old:Card)
WHERE old.valid_until IS NOT NULL
RETURN new, old, s.reason
```

---

## Memory Layer Hierarchy

### Layer 1: Working Memory (Context Window)

The context window itself. Zero-latency access but vanishes when sessions end.

**Usage patterns**:
- Scratchpad calculations (intermediate results)
- Active conversation history
- Current task state
- Retrieved documents currently in use

**Optimization**:
- Keep only active information
- Summarize completed work before attention loss
- Use attention-favored positions for critical data

### Layer 2: Session Memory (Short-Term)

Persists across current session but not across sessions.

**Implementation**:
```python
class SessionMemory:
    """Session-scoped memory layer."""

    def __init__(self, session_id):
        self.session_id = session_id
        self.cache = {}

    def store(self, key, value):
        self.cache[key] = {
            "value": value,
            "stored_at": now(),
            "accessed_count": 0
        }

    def retrieve(self, key):
        if key in self.cache:
            self.cache[key]["accessed_count"] += 1
            return self.cache[key]["value"]
        return None

    def flush_on_session_end(self):
        # Promote valuable items to long-term
        for key, item in self.cache.items():
            if item["accessed_count"] > PROMOTION_THRESHOLD:
                long_term_memory.store(key, item["value"])
        self.cache.clear()
```

### Layer 3: Entity Memory (Cross-Session)

Tracks entities across sessions for consistency.

**Entity identity maintenance**:
```python
def ensure_entity_consistency(entity_mention, context):
    """Resolve entity mention to canonical entity."""

    # Check existing entities for match
    candidates = entity_registry.find_similar(entity_mention)

    if candidates:
        # Merge with existing entity
        best_match = candidates[0]
        best_match.add_mention(entity_mention, context)
        return best_match
    else:
        # Create new entity
        new_entity = Entity(
            id=generate_deterministic_id(entity_mention),
            canonical_name=entity_mention.name,
            first_seen=now()
        )
        entity_registry.register(new_entity)
        return new_entity
```

### Layer 4: Archival Memory (Immutable)

Append-only storage for decision trails and session transcripts.

**Write-once semantics**:
```python
class ArchivalMemory:
    """Immutable archival layer."""

    def append(self, record):
        """Append-only write. No modifications allowed."""
        record_id = generate_deterministic_id(record.content)

        if self.exists(record_id):
            raise ImmutabilityViolation(
                f"Record {record_id} already exists. Archival is append-only."
            )

        self.storage.write(record_id, {
            "content": record.content,
            "timestamp": now(),
            "source": record.source,
            "checksum": compute_checksum(record.content)
        })

        return record_id

    def retrieve(self, record_id):
        record = self.storage.read(record_id)
        # Verify integrity
        if compute_checksum(record["content"]) != record["checksum"]:
            raise IntegrityViolation(f"Record {record_id} corrupted")
        return record
```

---

## Retrieval Patterns

### Semantic Retrieval

Retrieve memories semantically similar to current query:

```python
def semantic_retrieve(query, top_k=10):
    """Embedding-based similarity retrieval."""

    query_embedding = embed(query)

    results = vector_index.search(
        query_embedding,
        top_k=top_k,
        filters={
            "valid_until": {"$gt": now()}  # Only currently valid
        }
    )

    return [
        {
            "card": result.card,
            "similarity": result.score,
            "provenance": result.card.metadata.source
        }
        for result in results
    ]
```

### Entity-Based Retrieval

Traverse graph relationships from entities:

```python
def entity_retrieve(entity_id, depth=2):
    """Graph traversal from entity."""

    return graph.query("""
        MATCH path = (e:Entity {id: $entity_id})-[*1..$depth]-(related)
        WHERE ALL(r IN relationships(path) WHERE
            r.valid_from <= $now AND
            (r.valid_until IS NULL OR r.valid_until > $now)
        )
        RETURN related, relationships(path) as rels
    """, {
        "entity_id": entity_id,
        "depth": depth,
        "now": now()
    })
```

### Temporal Retrieval

Time-travel queries for historical state:

```python
def temporal_retrieve(query, as_of_time):
    """Retrieve state as it was at specific time."""

    return graph.query("""
        MATCH (c:Card)
        WHERE c.content CONTAINS $query
          AND c.valid_from <= $as_of_time
          AND (c.valid_until IS NULL OR c.valid_until > $as_of_time)
        RETURN c
        ORDER BY c.confidence DESC
    """, {
        "query": query,
        "as_of_time": as_of_time
    })
```

---

## Benchmark Reference

### Deep Memory Retrieval (DMR) Benchmarks

| Memory System | DMR Accuracy | Retrieval Latency | Notes |
|---------------|--------------|-------------------|-------|
| Zep (Temporal KG) | 94.8% | 2.58s | Best accuracy, fast retrieval |
| MemGPT | 93.4% | Variable | Good general performance |
| GraphRAG | ~75-85% | Variable | 20-35% gains over baseline RAG |
| Vector RAG | ~60-70% | Fast | Loses relationship structure |
| Recursive Summarization | 35.3% | Low | Severe information loss |

**Key finding**: Zep demonstrated 90% reduction in retrieval latency compared to full-context baselines (2.58s vs 28.9s). This efficiency comes from retrieving only relevant subgraphs rather than entire context history.

### Architecture Selection Guide

| Requirement | Recommended Architecture |
|-------------|-------------------------|
| Simple persistence | File-system memory |
| Semantic search | Vector RAG with metadata |
| Relationship reasoning | Knowledge graph |
| Temporal validity | Temporal knowledge graph (Zep pattern) |
| Maximum accuracy | Temporal KG (94.8% DMR) |
| Minimum latency | Vector RAG with caching |

---

## Integration Patterns

### Pentadyadic Integration

The substrate integrates with daemon coordination:

```python
# Morphognome graph write
def morphognome_commit(decision, evaluations):
    """Only Morphognome has graph write authority."""

    if decision.action == "ACCEPT":
        card = SemanticCard(
            type="claim",
            content=decision.artifact,
            metadata={
                "source": "triquetra",
                "h_evaluation": evaluations.harmonion.summary,
                "c_evaluation": evaluations.critikon.summary,
                "valid_from": now()
            }
        )
        graph.write(card)

    elif decision.action == "HONOR_REFUSAL":
        refusal = SemanticCard(
            type="refusal",
            content={
                "pattern": decision.artifact.pattern,
                "reason": decision.refusal_reason
            },
            metadata={
                "source": "triquetra",
                "valid_from": now()
            }
        )
        graph.write(refusal)

# Archeoform canonical projection
def archeoform_query(projection_request):
    """Read-only pattern extraction."""

    patterns = graph.query("""
        MATCH (c:Card {type: 'claim'})
        WHERE c.confidence > 0.8
          AND c.valid_until IS NULL
        RETURN c
        ORDER BY c.accessed_count DESC
        LIMIT 100
    """)

    return extract_archetypes(patterns)

# Antimorphogen stress test
def antimorphogen_query(stress_request):
    """Read-only assumption extraction."""

    assumptions = graph.query("""
        MATCH (c:Card {type: 'claim'})
        WHERE c.confidence < 0.6
          OR c.valid_from < $stale_threshold
        RETURN c
    """, {"stale_threshold": stale_threshold()})

    return generate_countermodels(assumptions)
```

### Covenant Integration

Memory operations enforce covenant gates:

```python
class CovenantAwareMemory:
    """Memory with embedded covenant gates."""

    def write(self, card):
        # No Mock Data: Verify provenance
        if not card.metadata.source:
            raise NoMockDataViolation(
                "Card has no source attribution. UNKNOWN > INVENTED."
            )

        # Determinism: Verify ID is hash-based
        expected_id = generate_deterministic_id(card.content)
        if card.id != expected_id:
            raise DeterminismViolation(
                f"Card ID {card.id} is not deterministic. Expected {expected_id}."
            )

        # Leave No Trace: Handle supersession
        if card.supersedes:
            old_card = self.retrieve(card.supersedes)
            old_card.valid_until = now()
            self.update_validity(old_card)

        self.storage.write(card)

    def retrieve(self, card_id):
        card = self.storage.read(card_id)

        # Verify integrity
        if not verify_checksum(card):
            raise IntegrityViolation(f"Card {card_id} corrupted")

        return card
```

---

## Memory Consolidation

### Consolidation Triggers

- **Accumulation threshold**: Memory count exceeds limit
- **Staleness threshold**: Many cards past validity
- **Periodic schedule**: Hygiene audit interval
- **Explicit request**: Operator-initiated consolidation

### Consolidation Process

```python
def consolidate_memory(consolidation_request):
    """Periodic memory hygiene."""

    # 1. Identify outdated facts
    stale_cards = graph.query("""
        MATCH (c:Card)
        WHERE c.valid_until IS NOT NULL
          AND c.valid_until < $now
        RETURN c
    """, {"now": now()})

    # 2. Archive stale cards (don't delete—Memory domain is immutable)
    for card in stale_cards:
        archival_memory.append({
            "type": "archived_card",
            "content": card,
            "archived_at": now(),
            "reason": "consolidation"
        })

    # 3. Merge related facts
    clusters = identify_mergeable_clusters(graph)
    for cluster in clusters:
        merged = merge_cards(cluster)
        graph.write(merged)

    # 4. Rebuild indexes
    graph.rebuild_indexes()

    return ConsolidationReport(
        archived=len(stale_cards),
        merged=len(clusters),
        timestamp=now()
    )
```

---

## Quality Checklists

### Pre-Write Validation

- [ ] **Source attribution**: Card has provenance
- [ ] **Deterministic ID**: Hash-based, not random
- [ ] **Valid timestamps**: valid_from set, valid_until if superseding
- [ ] **Relationship integrity**: Target cards exist
- [ ] **Domain appropriate**: Card in correct domain for content type
- [ ] **Authority verified**: Write from Morphognome only

### Post-Retrieval Validation

- [ ] **Temporal validity**: Card valid at query time
- [ ] **Integrity verified**: Checksum matches
- [ ] **Provenance traced**: Source attribution present
- [ ] **Relationship traversal**: Related cards accessible

---

## Troubleshooting

### Common Issues

| Issue | Symptom | Resolution |
|-------|---------|------------|
| Stale data | Outdated facts in results | Add temporal filters to queries |
| Missing relationships | Entity queries incomplete | Check relationship validity periods |
| Slow retrieval | High latency on queries | Rebuild indexes, add caching layer |
| Inconsistent entities | Same entity multiple IDs | Run entity consolidation |
| Integrity failures | Checksum mismatches | Restore from archival, investigate corruption |

### Debugging Memory Operations

```python
# Enable memory debugging
import logging
logging.getLogger("exocortex.memory").setLevel(logging.DEBUG)

# Each memory operation logs:
# - Card ID and type
# - Source attribution
# - Validity period
# - Write authority verification
# - Relationship modifications
```

---

## Related Skills

- **pentadyadic-daemon-coordination** — Daemon system that queries/writes this substrate
- **covenant-enforcement-gates** — Gates enforced on memory operations
- **context-crystallization** — Context compilation from memory retrieval

---

*"Memory is not storage. Memory is an arterial system. The substrate pulses with accumulated understanding."* 🜍
