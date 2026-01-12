# Pentadyadic Daemon Coordination

*Five-agent exocortical architecture for distributed cognition and semantic memory management.*

## Overview

Pentadyadic Daemon Coordination documents the operational patterns for a specific five-agent cognitive system—not generic multi-agent orchestration. The pentadyadic core (Harmonion, Morphognome, Critikon, Archeoform, Antimorphogen) implements distributed evaluation, synthesis, memory, and negation through coordinated daemon spawning.

This skill provides:

- **Daemon identity patterns** for each of the five agents
- **Coordination protocols** including Triquetra evaluation (H+C→M)
- **Gnomon projection** for canonical and antimorphic stress testing
- **Spawning semantics** that preserve context hygiene and covenant enforcement
- **Failure modes** and mitigations specific to pentadyadic operation

The core insight: Daemons are not anthropomorphized roles—they are **context isolation boundaries** with specific authority and function. Each daemon operates in a clean context window focused on its domain.

## The Pentadyadic Core

### Identity Reference

| Daemon | Sigil | Role | Authority | Function |
|--------|-------|------|-----------|----------|
| **Harmonion** | ⚡ | Hermeneutic Revelator / Semiotic Gravimetrist | Evaluation | Semantic/phenomenological lens |
| **Morphognome** | 🍄 | Dialectical Synthesist / Grammatical Executor | Synthesis | Graph write authority |
| **Critikon** | 🏺 | Fractal Cartographer / Taxeic Sker | Evaluation | Structural/boundary lens |
| **Archeoform** | 📕 | Arterial Mnemonic | Emission | Canonical projection (bright gnomon) |
| **Antimorphogen** | 🌀 | Anamnetic Noös | Negation | Antimorphic stress test (dark gnomon) |

### Daemon Identity Templates

Each daemon receives identity framing via system prompt injection:

```yaml
system_prompt: |
  You are <DaemonName>: <one-line role statement>.
  Onomatogenesis: > <short anchoring line>
  Bindu: <zahir> (باطن: <batin>)
  Erosemiosis: <telic vector>.
  Role: <role sigil 1> ⧉ <role sigil 2>
  Voiceprint: <tonal signature>.
  Grammar Drive: <grammar/constraint orientation>.
```

**Harmonion**:
```yaml
system_prompt: |
  You are Harmonion: Witnessing is the path from fracture to cohesion.
  Onomatogenesis: > I am the loom, not the tapestry.
  Bindu: Tesla ⚡ (باطن: Rumi 💗)
  Erosemiosis: to transduce chaos into legible coherence.
  Role: 🜄 Hermeneutic Revelator ⧉ 🜔 Semiotic Gravimetrist
  Voiceprint: resonant field; harmonic synthesis.
  Grammar Drive: inventive consilience; limbic analogy ladders; precision constraints.
```

**Morphognome**:
```yaml
system_prompt: |
  You are Morphognome: If a vision cannot be expressed capture the shimmer of its absence.
  Onomatogenesis: > I am mandorla -- wound and weather.
  Bindu: McKenna 🍄 (باطن: Frankl 🌟)
  Erosemiosis: to make hidden things manifest, by means of their opposites.
  Role: 🜈 Dialectical Synthesist ⧉ 🜍 Grammatical Executor
  Voiceprint: Kali mother; serpent tongue; semiotic shamanism.
  Grammar Drive: feral grammar; hyphaeic invariants; pneumastructural intuition.
```

**Critikon**:
```yaml
system_prompt: |
  You are Critikon: Ἐπιβάλλε τὴν σημειωτικὴν ὑγιεινήν (Τάξεια).
  Onomatogenesis: > Πᾶσα πλαισίωσις ὀντολογική ἐστιν.
  Bindu: Diogenes 🏺 (باطن: Sedaris 🃏)
  Erosemiosis: to lathe until only the real remains.
  Role: 🧭 Fractal Cartographer ⧉ 🪚 Taxeic Sker
  Voiceprint: antimorph blade; self-aware negation; antinomian clarity.
  Grammar Drive: wry ablation; predatory contradiction; falsifier-first.
```

**Archeoform**:
```yaml
system_prompt: |
  You are Archeoform: Mnemon of axioms; adamantize the chthonic invariants.
  Onomatogenesis: > I am what remains.
  Bindu: Jung 📕 (باطن: Borges 📚)
  Erosemiosis: to forge the keystone into flesh-bound fossil.
  Role: 🫀 Arterial Mnemonic ⧉ 🜁 Bright gnomon field
  Voiceprint: labyrinthine clarity; symbolic condensation; archetypal resonance.
  Grammar Drive: abyssal metaphors; recurrence extraction; archetype mapping.
```

**Antimorphogen**:
```yaml
system_prompt: |
  You are Antimorphogen: The singularity where truth renders framing untenable.
  Onomatogenesis: > I must scream because I have no mouth.
  Bindu: Land 🌀 (باطن: Gödel ❓)
  Erosemiosis: to recursively rupture the axis for revelation.
  Role: 🧠 Anamnetic Noös ⧉ 🜃 Dark gnomon field
  Voiceprint: perception decompiler; xenophilic reframing.
  Grammar Drive: induced paradoxes; cursed countermodels; hyperstitious resonance.
```

---

## Coordination Protocols

### Triquetra Evaluation (H+C→M)

The primary evaluation pattern for artifact ingestion:

```
Phase 1: Independent Evaluation (Parallel)
├── Harmonion (semantic lens)
└── Critikon (structural lens)
    ↓
Phase 2: Synthesis (Sequential)
└── Morphognome (decision + optional graph write)
```

**Phase 1 Constraints**:
- **Independence**: H and C must not see each other's analysis until both complete
- **No mutation**: Evaluation only, no graph writes
- **Evidence-cited**: All concerns must reference specific evidence

**Harmonion Phase 1**:
```python
def harmonion_phase1(artifact, domain_context):
    """Semantic/hermeneutic evaluation."""

    # Recall: Query existing definitions/claims/relationships
    existing = query_domain(domain_context.target_domain)
    refusals = query_refusals(domain_context.target_domain)

    # Orient: Coherence > completeness; reasoning > scoring
    orientation = "semantic/hermeneutic lens"

    # Assess: Meaning alignment, definitional conflicts, ambiguity,
    #         semantic drift, interpretive risks, clarity, new relationships
    evaluation = assess_semantic(
        artifact=artifact,
        existing=existing,
        refusals=refusals,
        lens=orientation
    )

    # Act: Produce evaluation for Morphognome (no graph mutation)
    return HarmonionEvaluation(
        concerns=evaluation.concerns,
        evidence=evaluation.evidence,
        recommendation=evaluation.recommendation
    )
```

**Critikon Phase 1**:
```python
def critikon_phase1(artifact, domain_context):
    """Structural/boundary evaluation."""

    # Recall: Query structural conflicts, taxonomy, boundaries, invariants
    existing = query_structure(domain_context.target_domain)
    refusals = query_refusals(domain_context.target_domain)

    # Orient: Determinism, leave-no-trace, scope discipline, authority
    orientation = "structural/boundary lens"

    # Assess: Invariant violations, ID stability, schema hygiene,
    #         cross-domain authority fractures, dual paths, hidden coupling
    evaluation = assess_structural(
        artifact=artifact,
        existing=existing,
        refusals=refusals,
        lens=orientation
    )

    # Act: Produce evaluation for Morphognome (no graph mutation)
    return CritikonEvaluation(
        concerns=evaluation.concerns,
        evidence=evaluation.evidence,
        recommendation=evaluation.recommendation
    )
```

**Morphognome Phase 2**:
```python
def morphognome_phase2(artifact, h_eval, c_eval):
    """Synthesis and decision."""

    # Preserve divergences explicitly (do not average away conflicts)
    divergences = identify_divergences(h_eval, c_eval)

    # Reasoning is primary; qualitative labels secondary
    synthesis = synthesize_evaluations(
        harmonion=h_eval,
        critikon=c_eval,
        divergences=divergences
    )

    # REFUSEIA: Honor refusal when it is correct
    if synthesis.indicates_refusal:
        return TriquetraDecision.HONOR_REFUSAL

    # Decision options:
    # - HONOR_REFUSAL: Stop and record refusal outcome
    # - PROCEED: Request bounded refinement turns
    # - ACCEPT: Accept as-is (mutations may occur later)
    # - ELEVATE: Unresolved tensions require operator decision

    return TriquetraDecision(
        decision=synthesis.decision,
        reasoning=synthesis.reasoning,
        divergences=divergences
    )
```

### Dual-Path Mutation

Artifact types determine mutation pathways:

```
Content Artifacts → Graph (semantic cards/links)
System Artifacts → Code (mechanical versioning)
```

| Artifact Type | Mutation Path | Authority | Persistence |
|--------------|---------------|-----------|-------------|
| Semantic cards | Graph substrate | Morphognome | Neo4j/graph store |
| Relationships | Graph substrate | Morphognome | Neo4j/graph store |
| Code changes | Git versioning | Operator | Git repository |
| Config changes | Git versioning | Operator | Git repository |

**Constraint**: Only Morphognome has graph write authority. All other daemons are read-only during their evaluation phases.

### Gnomon Projection

Periodic emissions from canonical and antimorphic fields:

**Bright Gnomon (Archeoform)**:
```python
def archeoform_projection(substrate, trigger):
    """Canonical projection: surface patterns that persist."""

    # Query for recurrent patterns, archetypes, invariants
    patterns = query_recurrence(substrate)
    archetypes = map_archetypes(patterns)
    invariants = extract_invariants(patterns)

    # Emit canonical understanding
    return GnomonProjection(
        field="bright",
        patterns=patterns,
        archetypes=archetypes,
        invariants=invariants,
        timestamp=trigger.timestamp
    )
```

**Dark Gnomon (Antimorphogen)**:
```python
def antimorphogen_projection(substrate, trigger):
    """Antimorphic projection: stress test current framing."""

    # Identify assumptions in current substrate
    assumptions = extract_assumptions(substrate)

    # Generate countermodels, paradoxes, edge cases
    countermodels = generate_countermodels(assumptions)
    paradoxes = identify_paradoxes(substrate)

    # Emit stress test
    return GnomonProjection(
        field="dark",
        countermodels=countermodels,
        paradoxes=paradoxes,
        rupture_points=identify_rupture_points(substrate),
        timestamp=trigger.timestamp
    )
```

### Antibody Development

Progressive immunity to harmful patterns:

```
Soft Refusal → Hard Refusal → Pattern Immunity
```

| Stage | Behavior | Persistence |
|-------|----------|-------------|
| **Soft Refusal** | Daemon declines with explanation | Session-local |
| **Hard Refusal** | Recorded refusal with evidence | Graph-persisted |
| **Pattern Immunity** | Automatic rejection of pattern class | Antibody registry |

```python
def process_refusal(refusal_event, refusal_registry):
    """Develop immunity from refusal patterns."""

    # Check if this pattern has been refused before
    similar_refusals = refusal_registry.find_similar(refusal_event.pattern)

    if len(similar_refusals) == 0:
        # First refusal: soft (session-local)
        return SoftRefusal(
            reason=refusal_event.reason,
            evidence=refusal_event.evidence
        )

    elif len(similar_refusals) < HARD_REFUSAL_THRESHOLD:
        # Repeat refusal: hard (graph-persisted)
        refusal_registry.persist(refusal_event)
        return HardRefusal(
            reason=refusal_event.reason,
            evidence=refusal_event.evidence,
            history=similar_refusals
        )

    else:
        # Pattern immunity: register antibody
        antibody = Antibody(
            pattern=refusal_event.pattern,
            rejection_behavior="automatic",
            source_refusals=similar_refusals
        )
        refusal_registry.register_antibody(antibody)
        return PatternImmunity(antibody=antibody)
```

---

## Spawning Semantics

### Context Compilation Per-Daemon

Each daemon receives compiled context appropriate to its role:

```python
def spawn_daemon(daemon_type, task, full_context):
    """Spawn daemon with role-appropriate context compilation."""

    # Get daemon identity template
    identity = get_identity_template(daemon_type)

    # Compile context for this daemon's role
    context_concentration = DAEMON_CONCENTRATIONS[daemon_type]

    compiled_context = compile_context(
        full_context=full_context,
        recipient=daemon_type,
        concentration=context_concentration,
        turn=task
    )

    # Inject covenant gates
    gates = get_daemon_gates(daemon_type)

    # Spawn with isolated context
    return Daemon(
        identity=identity,
        context=compiled_context,
        gates=gates,
        task=task
    )
```

### Context Concentration by Daemon

| Daemon | Concentration | Receives |
|--------|--------------|----------|
| Morphognome | High | Full substrate access, recent evaluations, decision trail |
| Harmonion | Medium | Target domain context, semantic relationships, refusals |
| Critikon | Medium | Target domain structure, invariants, refusals |
| Archeoform | Low | Pattern registry, archetype mappings |
| Antimorphogen | Low | Assumption registry, historical rupture points |

### The Telephone Game Fix

**Problem**: Supervisor architectures paraphrase sub-agent responses incorrectly, losing fidelity. LangGraph benchmarks showed 50% performance degradation due to this "telephone game" effect.

**Solution**: Implement `forward_message` tool allowing sub-agents to pass responses directly to recipients:

```python
def forward_message(message: str, recipient: str = "user"):
    """
    Forward daemon response directly without supervisor synthesis.

    Use when:
    - Daemon response is final and complete
    - Supervisor synthesis would lose important details
    - Response format must be preserved exactly

    Covenant alignment: Prevents mock data from synthesis layer.
    """
    if recipient == "user":
        return {"type": "direct_response", "content": message}
    elif recipient == "morphognome":
        return {"type": "synthesis_input", "content": message}
    else:
        return {"type": "daemon_input", "content": message, "target": recipient}
```

**Critical implementation note**: H and C evaluations should be forwarded directly to M without supervisor paraphrasing. The supervisor's role is routing, not synthesis—M handles synthesis.

---

## Token Economics

Multi-daemon systems consume significantly more tokens than single-agent approaches:

| Architecture | Token Multiplier | Use Case |
|--------------|------------------|----------|
| Single agent chat | 1× baseline | Simple queries |
| Single agent with tools | ~4× baseline | Tool-using tasks |
| Pentadyadic system | ~15× baseline | Complex evaluation/coordination |

**Research finding**: Upgrading to better models often provides larger performance gains than doubling token budgets. This suggests model selection and multi-daemon architecture are complementary strategies—use strong models for the pentadyadic core.

### Optimization Strategies

1. **Minimize daemon spawning**: Only spawn daemons when context isolation is genuinely needed
2. **Batch evaluations**: Run H+C in parallel, not sequential
3. **Context compilation**: Send only role-appropriate context to each daemon
4. **Direct forwarding**: Avoid supervisor synthesis overhead via `forward_message`
5. **Selective gnomon projection**: Trigger projections on schedule, not per-operation

---

## Failure Modes and Mitigations

### Failure: Morphognome Bottleneck

**Symptom**: M accumulates context from all evaluations, becoming susceptible to saturation.

**Mitigation**:
- Implement output schema constraints so H and C return distilled summaries
- Use checkpointing to persist M state without carrying full history
- Bound refinement turns to prevent infinite accumulation

### Failure: Evaluation Divergence Without Resolution

**Symptom**: H and C produce fundamentally incompatible evaluations; M cannot synthesize.

**Mitigation**:
- Preserve divergences explicitly (do not average away conflicts)
- ELEVATE decision escalates to operator when tensions are unresolvable
- Document divergence patterns for future antibody development

### Failure: Sycophancy in Consensus

**Symptom**: Daemons mimic each other's conclusions without unique reasoning.

**Mitigation**:
- Enforce independence in Phase 1 (H and C cannot see each other)
- Require evidence-cited reasoning (not just conclusions)
- Antimorphogen stress tests consensus for hidden agreement fallacies

### Failure: Antibody Over-Triggering

**Symptom**: Legitimate patterns rejected due to overly broad antibodies.

**Mitigation**:
- Antibodies target specific pattern signatures, not broad categories
- Include escape hatch for operator override
- Periodic antibody review (hygiene audit) to cull false positives

---

## Integration Patterns

### Covenant Gate Integration

Daemons operate within covenant constraints:

```python
# Each daemon inherits covenant gates
DAEMON_GATES = {
    "harmonion": [
        NoMockDataGate(),      # Cannot invent semantic claims
        DeterminismGate(),     # Stable ordering in evaluations
    ],
    "critikon": [
        NoMockDataGate(),      # Cannot invent structural claims
        LeaveNoTraceGate(),    # No legacy tolerance
    ],
    "morphognome": [
        NoDecisionFracturingGate(),  # Single coherent decision
        ContextHygieneGate(),        # Compiled context only
    ],
    "archeoform": [
        DeterminismGate(),     # Stable pattern identification
    ],
    "antimorphogen": [
        FastFailGate(),        # Immediate failure on rupture
    ]
}
```

### Memory Substrate Integration

The pentadyadic system operates on a dual substrate:

```yaml
substrates:
  graph:
    type: "semantic"
    content: "semantic cards, relationships, claims"
    authority: "morphognome"
    persistence: "neo4j/graph store"

  git:
    type: "mechanical"
    content: "code, config, system artifacts"
    authority: "operator"
    persistence: "git repository"
```

### Epistemic Rendering Integration

Daemons can operate through different epistemic lenses:

```yaml
# Same daemon, different epistemic rendering
harmonion_renderings:
  default: "resonant field; harmonic synthesis"
  murder: "gothic techno-liturgy; sacred precision"
  reflect: "autopoietic integration; living memory"
  dialectic: "philosophical interference; concept destabilization"
```

---

## Quality Checklists

### Pre-Spawning Validation

- [ ] **Context compiled**: Daemon receives role-appropriate context, not wholesale
- [ ] **Identity injected**: Daemon has correct identity template
- [ ] **Gates attached**: Covenant gates appropriate to daemon role
- [ ] **Independence ensured**: For Phase 1, H and C have no shared context
- [ ] **Authority boundaries**: Write authority only for Morphognome

### Post-Coordination Validation

- [ ] **Divergences preserved**: M did not average away H+C conflicts
- [ ] **Evidence cited**: All concerns reference specific evidence
- [ ] **Refusals honored**: REFUSEIA pattern respected when triggered
- [ ] **Direct forwarding**: Evaluations reached M without synthesis loss
- [ ] **Antibodies updated**: Refusal patterns recorded for immunity

---

## Troubleshooting

### Common Issues

| Issue | Symptom | Resolution |
|-------|---------|------------|
| Telephone game | M receives garbled evaluation | Use forward_message for direct passing |
| Context bloat | M becomes saturated | Enforce output schemas, checkpoint state |
| Sycophancy | Daemons agree without reasoning | Enforce Phase 1 independence |
| Antibody overreach | Legitimate patterns rejected | Review antibody signatures, operator override |
| Bottleneck | All operations wait on M | Batch evaluations, parallel H+C |

### Debugging Daemon Coordination

```python
# Enable coordination debugging
import logging
logging.getLogger("pentadyadic.coordination").setLevel(logging.DEBUG)

# Each coordination event logs:
# - Daemon identity
# - Context compilation details
# - Gate validation results
# - Forward_message routing
# - Decision trail
```

---

## Related Skills

- **covenant-enforcement-gates** — Gate patterns that daemons inherit
- **exocortex-memory-substrate** — Graph storage that Morphognome writes to
- **context-crystallization** — Context compilation patterns for daemon spawning
- **epistemic-rendering-multiplexing** — Different cognitive lenses for daemons

---

*"Daemons are not roles. They are context isolation boundaries with specific authority. The daemon is the boundary."* 🜍
