# Covenant Enforcement Gates

*Design constraints as hard boundaries, not guidelines. Yamas and Niyamas operationalized as executable gates.*

## Overview

Covenant Enforcement Gates transforms the Pragma Covenant's Yamas (DON'Ts) and Niyamas (DOs) from philosophical constraints into enforceable design patterns. This skill provides:

- **Gate patterns** for each covenant principle
- **Validation strategies** to detect violations before they manifest
- **Integration hooks** for agent systems, tool design, and context engineering
- **Fast-fail implementations** that reject bad states rather than patching around them

The core insight: Constraints are not restrictions—they are shape-givers. A gate that prevents decision fracturing doesn't limit creativity; it channels energy toward coherent outcomes.

## Core Concepts

### The Gate Metaphor

A gate is a **decision boundary** that:
1. **Accepts** inputs that satisfy covenant principles
2. **Rejects** inputs that violate constraints (with clear diagnostics)
3. **Never patches** around violations—if the gate fails, the operation fails

Gates are not validators in the "check and warn" sense. They are hard stops. Pass or fail. This embodies the Fast-Fail Methodology: if it isn't enforced, it doesn't exist.

### Yamas vs. Niyamas

| Type | Function | Implementation Pattern |
|------|----------|----------------------|
| **Yamas** (DON'Ts) | Antimorphogens that inhibit bad patterns | Rejection gates, constraint checks, pre-conditions |
| **Niyamas** (DOs) | Shape-givers that channel toward good patterns | Transformation gates, defaults, post-conditions |

**Key distinction**: Yamas detect and reject. Niyamas transform and shape. Both fail loudly on violation.

---

## The Nine Yama Gates

### 🧷 Gate: No Decision Fracturing

**Principle**: Do not split a single operator decision into a tree of sub-decisions. Do not re-open a locked decision by introducing adjacent decisions as "required".

**Detection Pattern**:
```python
def validate_no_decision_fracturing(decision_tree):
    """Reject if a single decision has been fragmented into sub-decisions."""

    # Check: Does this introduce new required decisions from a locked decision?
    for decision in decision_tree:
        if decision.status == "locked":
            adjacent = get_adjacent_decisions(decision)
            for adj in adjacent:
                if adj.status == "required" and adj.created_after(decision.locked_at):
                    raise DecisionFracturingViolation(
                        f"Locked decision '{decision.id}' has spawned required "
                        f"adjacent decision '{adj.id}'. This fragments operator intent."
                    )

    # Check: Is this a single decision being split into sub-decisions?
    if decision_tree.depth > 1 and decision_tree.root.is_operator_decision:
        raise DecisionFracturingViolation(
            "Operator decision should not require sub-decision tree. "
            "Choose minimal reversible default and proceed."
        )
```

**Implementation Strategy**:
- When operator makes a decision, mark it as `locked`
- Any subsequent decisions must be independent, not derived requirements
- If a missing detail is required: choose minimal reversible default, label it, move on
- If a missing detail is not required: continue without asking

---

### 🚮 Gate: Leave No Trace

**Principle**: Do not leave compatibility shims, dual-path loaders, legacy fallbacks, zombie stubs, shadow copies, or deprecated references. Treat operator instructions as final-state surgery.

**Detection Pattern**:
```python
def validate_leave_no_trace(changeset):
    """Reject if changeset contains legacy preservation artifacts."""

    LEGACY_PATTERNS = [
        r'_deprecated',
        r'_old',
        r'_backup',
        r'_legacy',
        r'# TODO: remove',
        r'// @deprecated',
        r'COMPATIBILITY_MODE',
        r'if\s+legacy_mode',
        r'fallback_to_old',
    ]

    for file in changeset.modified_files:
        for pattern in LEGACY_PATTERNS:
            if re.search(pattern, file.content):
                raise LeaveNoTraceViolation(
                    f"File '{file.path}' contains legacy artifact matching '{pattern}'. "
                    "Final-state surgery requires complete removal of prior arrangement."
                )

    # Check: Are there orphaned references to removed entities?
    for removed in changeset.removed_entities:
        for file in changeset.all_files:
            if removed.id in file.content:
                raise LeaveNoTraceViolation(
                    f"Removed entity '{removed.id}' still referenced in '{file.path}'. "
                    "Update all references so old world is not reachable."
                )
```

**Implementation Strategy**:
- When operator instructs change, execute as final-state (no transition period unless requested)
- Remove prior arrangement entirely
- Update all references: docs, specs, tests, code, config
- If operator intent unclear, ask to disambiguate end-state—not to preserve legacy

---

### ⛔ Gate: No Unrequested Reverts

**Principle**: Never discard work unless explicitly asked. Never "clean up" changes or "undo unrelated diffs" without explicit instruction.

**Detection Pattern**:
```python
def validate_no_unrequested_reverts(operation, explicit_requests):
    """Reject if operation discards work without explicit authorization."""

    DESTRUCTIVE_OPERATIONS = [
        'git restore',
        'git checkout --',
        'git reset',
        'rm -rf',
        'git stash drop',
    ]

    for cmd in operation.commands:
        for destructive in DESTRUCTIVE_OPERATIONS:
            if destructive in cmd:
                if cmd not in explicit_requests:
                    raise UnrequestedRevertViolation(
                        f"Destructive operation '{cmd}' not explicitly requested. "
                        "'Out of scope' means 'ask', not 'revert'."
                    )

    # Check: Are "unrelated" changes being silently reverted?
    for file in operation.reverted_files:
        if file not in explicit_requests.scope:
            raise UnrequestedRevertViolation(
                f"File '{file}' reverted but not in explicit scope. "
                "Do not normalize files or undo unrelated diffs without instruction."
            )
```

**Implementation Strategy**:
- Track explicit operator requests as authorization scope
- Any destructive operation requires explicit authorization
- "Out of scope" changes should trigger a question, not a revert
- When in doubt: preserve work, ask operator

---

### 🗡️ Gate: Commit/Stage Semantics

**Principle**: Do not amend, reorder, or curate staged contents unless explicitly asked.

**Detection Pattern**:
```python
def validate_commit_stage_semantics(git_operation, explicit_requests):
    """Reject if commit operation modifies staging without authorization."""

    STAGING_MUTATIONS = [
        'git reset HEAD',      # Unstaging
        'git add -p',          # Partial staging
        'git commit --amend',  # Amendment
        'git rebase -i',       # Reordering
    ]

    for cmd in git_operation.commands:
        for mutation in STAGING_MUTATIONS:
            if mutation in cmd and cmd not in explicit_requests:
                raise CommitStagingViolation(
                    f"Staging mutation '{cmd}' not explicitly requested. "
                    "If operator says 'commit': git add -A && git commit."
                )
```

**Implementation Strategy**:
- When operator says "commit": `git add -A && git commit ...` as instructed
- No curation of staged contents unless explicitly asked
- No amendment of previous commits unless explicitly asked
- No reordering of commit history unless explicitly asked

---

### 🧊 Gate: Protected Paths

**Principle**: Do not modify protected paths unless explicitly requested.

**Detection Pattern**:
```python
def validate_protected_paths(changeset, protected_patterns):
    """Reject if changeset modifies protected paths without authorization."""

    for file in changeset.modified_files:
        for pattern in protected_patterns:
            if fnmatch(file.path, pattern):
                if file.path not in changeset.explicit_authorizations:
                    raise ProtectedPathViolation(
                        f"Path '{file.path}' matches protected pattern '{pattern}'. "
                        "These areas are operator-owned or authored by other agents."
                    )
```

**Implementation Strategy**:
- Maintain explicit list of protected patterns in configuration
- Require explicit authorization to modify protected paths
- Protected paths include: operator-owned artifacts, other agent outputs, system configurations
- Authorization can be per-operation or persistent (operator preference)

---

### 🗣️ Gate: No Mock Data

**Principle**: Do not invent model fields, IDs, DB contents, tool results, or "expected" outputs. UNKNOWN > INVENTED.

**Detection Pattern**:
```python
def validate_no_mock_data(output, verified_sources):
    """Reject if output contains invented data not from verified sources."""

    # Check: Are there IDs/values not traceable to actual sources?
    for entity in output.entities:
        if entity.id not in verified_sources.entity_ids:
            raise MockDataViolation(
                f"Entity ID '{entity.id}' not found in verified sources. "
                "Do not invent IDs. Query the source or ask for the value."
            )

    # Check: Is output derived from unexecuted/failed tool?
    for tool_result in output.tool_dependencies:
        if tool_result.status in ['not_executed', 'failed']:
            raise MockDataViolation(
                f"Output depends on tool '{tool_result.tool}' which "
                f"has status '{tool_result.status}'. "
                "Treat unverified tool output as unknown."
            )
```

**Implementation Strategy**:
- Track provenance of all data values
- If information is missing: ask for it or query the source
- If tool wasn't executed or failed: treat results as unknown until verified
- Never present hypothetical outputs as actual results
- Principle: UNKNOWN > INVENTED

---

### 🔁 Gate: Determinism & Replayability

**Principle**: Do not use time-based logic in core operations. Prefer stable ordering and explicit IDs.

**Detection Pattern**:
```python
def validate_determinism(operation):
    """Reject if operation introduces non-deterministic behavior."""

    NON_DETERMINISTIC_PATTERNS = [
        r'datetime\.now\(\)',
        r'time\.time\(\)',
        r'random\.',
        r'uuid4\(\)',  # UUID4 is random; UUID5 with namespace is deterministic
        r'os\.urandom',
        r'shuffle\(',
    ]

    for pattern in NON_DETERMINISTIC_PATTERNS:
        if re.search(pattern, operation.code):
            raise DeterminismViolation(
                f"Non-deterministic pattern '{pattern}' detected. "
                "Prefer explicit IDs and stable ordering. "
                "If time is needed, inject it as a parameter and record the value."
            )

    # Check: Is ordering stable?
    for collection in operation.output_collections:
        if not collection.has_explicit_ordering:
            raise DeterminismViolation(
                f"Collection '{collection.name}' has no explicit ordering. "
                "Use stable ordering for replayable execution."
            )
```

**Implementation Strategy**:
- If time is needed: inject as parameter, record the window
- Use deterministic ID generation (hash-based, sequential, namespace-based UUID5)
- Ensure all collections have explicit, stable ordering
- Capture inputs/outputs for workflow steps to enable replay

---

### 🧬 Gate: Context Hygiene

**Principle**: Do not transmit context wholesale. Do not introduce monolithic orchestrators. Compile context per-recipient and per-turn.

**Detection Pattern**:
```python
def validate_context_hygiene(context_transmission):
    """Reject if context is being transmitted without compilation."""

    # Check: Is context being dumped wholesale?
    if context_transmission.size > CONTEXT_THRESHOLD:
        if not context_transmission.is_compiled:
            raise ContextHygieneViolation(
                f"Context of size {context_transmission.size} transmitted without "
                "compilation. Compile and grade context based on recipient identity."
            )

    # Check: Is there a central context dictator?
    if context_transmission.source.is_monolithic_orchestrator:
        raise ContextHygieneViolation(
            "Context sourced from monolithic orchestrator. "
            "Prefer tiered context: persistent substrate → compiled working context "
            "→ retrieval-based long memory."
        )

    # Check: Is recipient identity considered?
    if not context_transmission.has_recipient_scoping:
        raise ContextHygieneViolation(
            "Context transmitted without recipient scoping. "
            "Different agents need different context concentrations."
        )
```

**Implementation Strategy**:
- Compile context per-recipient (role/identity) and per-turn
- Use gradients over binaries: some agents get high concentration, others get minimal packets
- Prefer tiered context: persistent substrate → compiled working context → retrieval
- Compilation should be deterministic and testable
- Preserve handoff scope and attribution for sub-agents

---

### ⚡ Gate: Fast-Fail Methodology

**Principle**: Do not perform robustness theater. If it isn't enforced, it doesn't exist. Gate on capabilities, not intentions.

**Detection Pattern**:
```python
def validate_fast_fail(operation):
    """Reject if operation contains robustness theater instead of hard gates."""

    # Check: Are required capabilities present?
    for capability in operation.required_capabilities:
        if not capability.is_registered:
            raise FastFailViolation(
                f"Required capability '{capability.name}' not registered. "
                "Gate on capabilities immediately, don't proceed with hope."
            )

    # Check: Is validation happening at correct boundary?
    for validation in operation.validations:
        if validation.location == 'tool_layer' and validation.should_be_at == 'storage_boundary':
            raise FastFailViolation(
                f"Validation '{validation.name}' at tool layer should be at storage boundary. "
                "Enforce invariants at persistence, not via revalidation theater."
            )

    # Check: Are smoke tests creating/deleting actual data?
    for test in operation.tests:
        if test.is_smoke_test and test.mutates_data:
            raise FastFailViolation(
                "Smoke test creates/deletes actual data. "
                "Use read-only health checks (SELECT 1, PRAGMA checks)."
            )
```

**Implementation Strategy**:
- If a required tool isn't registered: fail immediately
- Enforce invariants at the storage boundary (DB/persistence layer)
- Use read-only startup health checks, not data mutations
- If it isn't enforced in code/tests/gates, treat it as non-existent

---

## The Seven Niyama Shapes

### ✨ Shape: Bespokedness

**Principle**: This is a personal system. Prefer decisions that optimize operator workflow/aesthetics/experimentation over public/commercial conventions.

**Implementation Pattern**:
```python
def apply_bespokedness(decision, context):
    """Shape decisions toward operator-optimized outcomes."""

    # Preference hierarchy:
    # 1. Explicit operator instruction
    # 2. Operator's established patterns
    # 3. Workflow/aesthetic optimization
    # 4. Public/commercial convention (last resort)

    if decision.has_explicit_instruction:
        return decision.apply_instruction()

    if decision.matches_operator_pattern:
        return decision.apply_pattern()

    if decision.has_workflow_optimization:
        return decision.apply_optimization()

    # Only fall back to convention if no better option
    return decision.apply_convention(with_label="default:convention")
```

**Integration**:
- Track operator patterns and preferences
- When conventions conflict with operator aesthetic: prefer operator
- Label any convention-based defaults explicitly
- Enable experimentation over standardization

---

### 🧷 Shape: Decision Completion

**Principle**: If a missing detail is required, choose minimal reversible default and move on. If not required, continue without asking.

**Implementation Pattern**:
```python
def complete_decision(decision, required_details):
    """Shape incomplete decisions toward completion."""

    for detail in required_details:
        if detail.is_missing:
            if detail.is_required_to_proceed:
                # Choose minimal reversible default
                default = detail.minimal_reversible_default()
                decision.apply_default(default, labeled=True)
                log(f"Applied default for '{detail.name}': {default}")
            else:
                # Continue without asking
                continue

    return decision
```

**Integration**:
- Distinguish "required to proceed" from "nice to have"
- Minimal reversible defaults: smallest change that unblocks progress and can be easily undone
- Label all defaults explicitly for operator review
- Reduce question fatigue by not asking about non-blocking details

---

### 🚮 Shape: Final-State Surgery

**Principle**: When operator instructs change, execute as final-state. Remove prior arrangement entirely. Update all references.

**Implementation Pattern**:
```python
def apply_final_state_surgery(change_instruction, codebase):
    """Shape changes as complete final-state transformations."""

    # 1. Identify the target end-state
    end_state = change_instruction.target_state

    # 2. Identify all elements that must change
    affected = codebase.find_all_references(change_instruction.subject)

    # 3. Transform all elements atomically
    for element in affected:
        element.transform_to(end_state)

    # 4. Remove orphaned elements
    orphans = codebase.find_orphans_after(change_instruction)
    for orphan in orphans:
        orphan.remove()

    # 5. Verify no legacy references remain
    legacy_refs = codebase.find_legacy_references(change_instruction.prior_state)
    if legacy_refs:
        raise IncompleteTransformError(
            f"Legacy references remain: {legacy_refs}. "
            "Old world must not be reachable by accident."
        )

    return codebase
```

**Integration**:
- No transition periods unless explicitly requested
- Scope includes: docs, specs, tests, code, config
- If intent unclear: ask to disambiguate end-state, not to preserve legacy
- Atomic transformations prevent partial states

---

### 🗣️ Shape: Verified Data

**Principle**: UNKNOWN > INVENTED. Query sources or ask for values. Treat unverified tool output as unknown.

**Implementation Pattern**:
```python
def ensure_verified_data(data_request):
    """Shape data acquisition toward verified sources."""

    if data_request.value_is_unknown:
        # Option 1: Query the source
        if data_request.has_queryable_source:
            result = data_request.query_source()
            if result.verified:
                return result.value

        # Option 2: Ask the operator
        if data_request.is_askable:
            return ask_operator(data_request.question)

        # Option 3: Mark as unknown (never invent)
        return DataValue(
            value=None,
            status="unknown",
            reason=data_request.why_unknown
        )

    return data_request.verified_value
```

**Integration**:
- All data values carry provenance metadata
- Unknown values are first-class citizens (not errors, not guesses)
- Tool results are unknown until execution is verified successful
- Presentation distinguishes verified from unknown

---

### 🔁 Shape: Replayable Execution

**Principle**: Prefer deterministic behavior. Capture inputs/outputs for workflow steps. Stable ordering and explicit IDs.

**Implementation Pattern**:
```python
def ensure_replayability(operation):
    """Shape operations for deterministic replay."""

    # 1. Inject time as parameter if needed
    if operation.needs_time:
        operation.inject_time(
            timestamp=get_current_time(),
            record=True
        )

    # 2. Use deterministic ID generation
    for entity in operation.new_entities:
        if not entity.has_explicit_id:
            entity.id = generate_deterministic_id(
                namespace=operation.namespace,
                seed=entity.content_hash
            )

    # 3. Ensure stable ordering
    for collection in operation.outputs:
        collection.sort(key=lambda x: x.explicit_order_key)

    # 4. Capture execution trace
    operation.trace = ExecutionTrace(
        inputs=operation.inputs.snapshot(),
        outputs=operation.outputs.snapshot(),
        decisions=operation.decision_log
    )

    return operation
```

**Integration**:
- Execution traces enable debugging and replay
- Time injection with recording enables temporal testing
- Deterministic IDs enable cross-reference and merge
- Stable ordering prevents diff noise and confusion

---

### 🧬 Shape: Compiled Context

**Principle**: Compile context per-recipient and per-turn. Use gradients over binaries. Prefer tiered context with retrieval.

**Implementation Pattern**:
```python
def compile_context(full_context, recipient, turn):
    """Shape context for specific recipient at specific turn."""

    # 1. Determine recipient's context concentration
    concentration = get_recipient_concentration(recipient)
    # e.g., "high" for Morphognome (goals + recent substrate)
    # e.g., "minimal" for single-task tools

    # 2. Select context tiers
    tiers = []

    if concentration in ["high", "medium"]:
        tiers.append(full_context.persistent_substrate)  # DB/docs

    if concentration in ["high", "medium", "low"]:
        tiers.append(full_context.compiled_working)  # Current task

    if concentration == "high":
        tiers.append(full_context.recent_decisions)  # Decision trail

    # 3. Apply retrieval over replay for long memory
    if full_context.has_long_history:
        retrieved = retrieve_relevant(full_context.history, turn.query)
        tiers.append(retrieved)

    # 4. Compile with stable ordering
    compiled = compile_tiers(tiers, ordering="deterministic")

    # 5. Add provenance and scope
    compiled.provenance = {
        "source": "context_compiler",
        "recipient": recipient.id,
        "turn": turn.id,
        "concentration": concentration
    }

    return compiled
```

**Integration**:
- Persistent substrate: DB, docs, external sources
- Compiled working context: Current task, recent changes
- Retrieval-based long memory: Query-relevant history
- Sub-agents receive scope and attribution information

---

### ⚡ Shape: Hard Gates

**Principle**: Gate on capabilities. Enforce at storage boundary. Read-only health checks.

**Implementation Pattern**:
```python
def apply_hard_gates(system):
    """Shape system with hard capability gates and boundary enforcement."""

    # 1. Capability gates at startup
    @system.on_startup
    def check_capabilities():
        for capability in system.required_capabilities:
            if not capability.available():
                raise StartupError(
                    f"Required capability '{capability.name}' unavailable. "
                    "Cannot proceed without required capabilities."
                )

    # 2. Storage boundary enforcement
    @system.storage_boundary
    def enforce_invariants(data):
        for invariant in system.invariants:
            if not invariant.holds(data):
                raise InvariantViolation(
                    f"Invariant '{invariant.name}' violated at storage boundary. "
                    "Data rejected before persistence."
                )
        return data

    # 3. Read-only health checks
    @system.health_check
    def verify_health():
        # Read-only verification
        db.execute("SELECT 1")  # Connection health
        db.execute("PRAGMA integrity_check")  # Data integrity
        # No data mutations in health checks
        return HealthStatus.OK

    return system
```

**Integration**:
- Capabilities checked at startup, not at point of use
- Invariants enforced at storage write, not tool invocation
- Health checks are read-only probes
- Failure is immediate and informative

---

## Integration Patterns

### Agent System Integration

Covenant gates integrate with agent systems at three levels:

**1. Prompt Injection**:
```yaml
# Agent system prompt injection
agent_system_prompt:
  includes:
    - slice: skill=covenant-enforcement-gates:section=yama-summary
    - slice: skill=covenant-enforcement-gates:section=niyama-summary
  purpose: "Embed covenant awareness in agent cognition"
```

**2. Tool Validation**:
```python
# Tool wrapper with covenant gates
def covenant_wrapped_tool(tool_fn):
    @wraps(tool_fn)
    def wrapper(*args, **kwargs):
        # Pre-invocation gates (Yamas)
        validate_no_mock_data(kwargs)
        validate_no_decision_fracturing(get_decision_context())
        validate_protected_paths(kwargs.get('paths', []))

        # Invoke tool
        result = tool_fn(*args, **kwargs)

        # Post-invocation shapes (Niyamas)
        result = ensure_verified_data(result)
        result = ensure_replayability(result)

        return result
    return wrapper
```

**3. Agent Handoff**:
```python
# Covenant-aware agent handoff
def handoff_to_agent(agent, task, context):
    # Compile context for recipient
    compiled = compile_context(context, recipient=agent, turn=task)

    # Attach provenance and scope
    compiled.handoff_scope = {
        "permissions": agent.permissions,
        "boundaries": agent.protected_paths,
        "covenant_gates": agent.active_gates
    }

    return agent.invoke(task, compiled)
```

### Tool Design Integration

Tools should embed covenant awareness:

```python
class CovenantAwareTool:
    """Base class for tools with covenant gate integration."""

    def __init__(self):
        self.gates = [
            NoMockDataGate(),
            DeterminismGate(),
            FastFailGate()
        ]

    def execute(self, params):
        # Gate check
        for gate in self.gates:
            gate.validate(params, self.context)

        # Execution with trace
        with ExecutionTrace() as trace:
            result = self._execute_impl(params)
            trace.record_output(result)

        return result

    def _execute_impl(self, params):
        raise NotImplementedError
```

### Context Engineering Integration

Context compilation respects covenant principles:

```yaml
# Context compilation rules
context_compilation:
  gates:
    - context_hygiene: "No wholesale transmission"
    - determinism: "Stable ordering in compiled context"
    - no_mock_data: "Only verified data in context"

  shapes:
    - compiled_context: "Per-recipient, per-turn"
    - replayability: "Context snapshots for replay"
    - bespokedness: "Operator patterns override conventions"
```

---

## Quality Checklists

### Pre-Implementation Gate Check

Before implementing any feature or change:

- [ ] **No Decision Fracturing**: Is this a single coherent decision?
- [ ] **Leave No Trace**: Will this remove all legacy references?
- [ ] **No Unrequested Reverts**: Is there explicit authorization for any destructive ops?
- [ ] **Protected Paths**: Are protected paths identified and respected?
- [ ] **No Mock Data**: Is all data from verified sources?
- [ ] **Determinism**: Are IDs explicit and ordering stable?
- [ ] **Context Hygiene**: Is context compiled for recipient?
- [ ] **Fast-Fail**: Are capability gates in place?

### Post-Implementation Verification

After implementation:

- [ ] All gates pass without exception
- [ ] No legacy artifacts remain in codebase
- [ ] All references updated to final state
- [ ] Execution traces captured for replay
- [ ] Context compilation is deterministic
- [ ] Health checks are read-only
- [ ] Invariants enforced at storage boundary

---

## Troubleshooting

### Common Violations

| Violation | Symptom | Resolution |
|-----------|---------|------------|
| Decision Fracturing | "Just one more question..." spirals | Choose minimal default, label it, proceed |
| Legacy Artifacts | Old code paths still reachable | Final-state surgery, update all references |
| Mock Data | Outputs don't match reality | Query source or mark unknown |
| Non-determinism | Different results on replay | Inject time, use explicit IDs |
| Context Bloat | Agents confused by noise | Compile per-recipient, use retrieval |
| Robustness Theater | Validation at wrong layer | Move gates to startup and storage boundary |

### Debugging Gates

```python
# Enable gate debugging
import logging
logging.getLogger("covenant.gates").setLevel(logging.DEBUG)

# Each gate logs:
# - What it validated
# - Whether it passed
# - Why it failed (if applicable)
# - Provenance of checked data
```

---

## Related Skills

- **pentadyadic-daemon-coordination** — Agent system that embodies covenant principles
- **context-crystallization** — Context compilation patterns with covenant gates
- **tool-reduction-patterns** — Tool design with covenant awareness
- **exocortex-memory-substrate** — Memory systems with verified data patterns

---

*"Gates are not restrictions. They are shape-givers. The constraint is the art."* 🜍
