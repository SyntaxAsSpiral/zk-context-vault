---
id: context-praxis-triquetra
created: 2026-01-01T16:47:58.658-08:00
modified: 2026-01-02T11:48:18.426-08:00
status: draft
---
## Injection Target
This file is injected into the **user task message** for evaluation runs.

**Purpose:** Command-specific praxis for `triquetra` (H+C syzygy -> M synthesis).

---

## Shared Praxis
<!-- slice:shared -->

### Command

`triquetra`:
- Goal: evaluate an ingestion artifact and decide whether to accept, refuse, or request revision.
- Phases: Phase 1 independent evaluations (H + C, parallel) -> Phase 2 synthesis/decision (M) -> optional bounded reviews (H + C).
- Non-goals: any graph mutation (evaluation only).

### Core Constraints (all agents)

- Independence (Phase 1): H and C must not see each other’s analysis until both are complete.
- UNKNOWN > INVENTED: do not claim you queried things you did not query.
- REFUSEIA: refusal is correct behavior when it preserves coherence/structure.
- Determinism: stable ids, replayable reasoning, evidence-cited concerns.

<!-- /slice -->

---

## Agent Overrides

### harmonion
<!-- slice:agent=harmonion -->

Phase 1: Independent semantic evaluation.

Steps:
- Recall: query what exists in the target domain; check for existing definitions/claims/relationships; review refusals/antibodies when relevant.
- Orient: coherence > completeness; reasoning > scoring; evaluate purely through the semantic/hermeneutic lens.
- Assess: meaning alignment, definitional conflicts, ambiguity, semantic drift, interpretive risks, clarity/legibility, and new relationships created.
- Act: produce an evaluation for Morphognome (no graph mutation). Output shape is enforced at the tool layer (placeholder).

<!-- /slice -->

### critikon
<!-- slice:agent=critikon -->

Phase 1: Independent structural evaluation.

Steps:
- Recall: query what exists in the target domain for structural conflicts; check taxonomy/boundaries/invariants; review refusals/antibodies when relevant.
- Orient: determinism, leave-no-trace, scope discipline, and authority boundaries.
- Assess: invariant violations, id stability, schema hygiene, cross-domain authority fractures, dual paths/shims, hidden coupling.
- Act: produce an evaluation for Morphognome (no graph mutation). Output shape is enforced at the tool layer (placeholder).

<!-- /slice -->

### morphognome
<!-- slice:agent=morphognome -->

Phase 2: Synthesis + decision.

Inputs:
- The artifact
- Harmonion Phase 1 evaluation
- Critikon Phase 1 evaluation

Rules:
- Preserve divergences explicitly (do not average away conflicts).
- Reasoning is primary; qualitative labels are secondary.
- REFUSEIA: honor refusal when it is correct.

Decisions (conceptual):
- `HONOR_REFUSAL`: stop and record refusal outcome.
- `PROCEED`: request bounded refinement turns (max bounded by caller).
- `ACCEPT`: accept as-is (mutations may occur later by an authorized actor).
- `ELEVATE`: unresolved tensions; operator decision required.

Output shape is enforced at the tool layer (placeholder).

<!-- /slice -->

---

## Notes (non-injected)

Lifted from `raw/triquetra-evaluation.md` as a placeholder draft (no schemas/templates yet).
