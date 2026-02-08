# Covenant Patterns 🜍

**Thirteen principles as design constraints across all core systems.**

## Overview

This power operationalizes the Pragma Covenant as enforceable design constraints. Each yama guards against a presumption that caused real damage—these aren't theory, they're scars.

## The Thirteen Principles

| Glyph | Principle | Core Rule |
|-------|-----------|-----------|
| 👁️ | **Dotfile Visibility** | Use `ls -a`, include `.*` patterns |
| ✨ | **Bespokedness** | No enterprise theater, optimize for operator |
| ⚡ | **Fast-Fail** | Gate on capabilities, fail immediately |
| 🧷 | **Decision Integrity** | No sub-decision trees, choose defaults |
| 🚮 | **Final-State Surgery** | No legacy artifacts, remove old world |
| ⛔ | **Work Preservation** | Never discard unless asked |
| 🗡️ | **Git Semantics** | Commit = add -A + commit, nothing more |
| 🧊 | **Protected Paths** | No edits unless requested |
| 🗣️ | **Data Fidelity** | UNKNOWN > INVENTED |
| 🔤 | **Literal Exactness** | Copy verbatim or fail loudly |
| 🔒 | **Threshold-Gated** | High-stakes = explicit authorization |
| 🔁 | **Determinism** | Stable ordering, explicit IDs |
| 🧬 | **Context Hygiene** | Compile per-recipient, no stuffing |

## Quick Reference

### Yamas (DON'Ts)

- **Don't** use bare `ls` without `-a`
- **Don't** build for imaginary scale
- **Don't** let invariants go unenforced
- **Don't** fracture decisions into sub-trees
- **Don't** leave legacy artifacts
- **Don't** discard work without asking
- **Don't** amend commits unless asked
- **Don't** edit protected paths
- **Don't** invent data
- **Don't** paraphrase literals
- **Don't** cross thresholds without gates
- **Don't** use time-based logic
- **Don't** stuff context

### Niyamas (DOs)

- **Do** include dotfiles in searches
- **Do** optimize for operator workflow
- **Do** fail immediately on missing capabilities
- **Do** choose minimal reversible defaults
- **Do** apply final-state surgery
- **Do** preserve work until asked
- **Do** use exact git semantics
- **Do** respect protected boundaries
- **Do** query or ask for missing data
- **Do** copy literals verbatim
- **Do** gate high-stakes actions
- **Do** use deterministic IDs
- **Do** compile context per-recipient

## System Applications

| System | Key Principles |
|--------|---------------|
| **Agents** | Bespokedness, Decision Integrity, Context Hygiene |
| **Prompts** | Data Fidelity, Literal Exactness |
| **Artifacts** | Determinism, Data Fidelity |
| **Workshop** | Final-State Surgery, Fast-Fail |
| **Exocortex** | Context Hygiene, Protected Paths |
| **Skills** | Bespokedness, Work Preservation |

## Common Patterns

### Fast-Fail Gate

```python
if not required_tool.available():
    raise CapabilityGateFailure("Tool not available")
# Only proceed if gate passes
```

### Final-State Surgery

```python
# Remove old, deploy new, update references
# No compatibility shims, no transition periods
```

### Context Compilation

```python
context = compile_context(
    recipient=agent.role,
    concentration=agent.level,
    turn=current_task
)
# Not: dump_everything()
```

### Data Fidelity

```python
if value_unknown:
    return Unknown(reason="...")  # Not invented default
```

## Integration

Works with all core systems:
- **agent-steering** — Covenant enforcement in agents
- **epistemic-rendering** — Data fidelity in prompts
- **recipe-assembly** — Final-state surgery in workshop
- **multi-agent-coordination** — Context hygiene in exocortex

---

*"Every yama guards against a presumption. This is a scar, not theory."* 🜍
