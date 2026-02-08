# Agent Steering 🧭

**Universal patterns for AI coding agent configuration. Works with Kiro, Claude Code, Codex, Charm.**

## Overview

This power documents patterns that transform any AI coding agent into a cognitive partner. Platform-agnostic principles with platform-specific deployment.

Key insight: Agents fail through presumption. Explicit context prevents presumptive behavior.

## Features

### 📊 Steering Hierarchy

| Layer | Scope | Purpose |
|-------|-------|---------|
| **Global** | All sessions | Universal patterns, identity |
| **Workspace** | Multi-project | Shared context |
| **Project** | Single project | Specific constraints |

Later layers override earlier. Hierarchy: Global → Workspace → Project.

### 📋 3-Phase Spec Process

```
Design → Requirements → Tasks
(lock)      (lock)      (execute)
```

Once a phase completes, decisions are locked. No reopening Design in Tasks.

### 🧩 Context Assembly

Progressive disclosure, not context stuffing:
- Turn 0: Minimal (identity + task)
- Turn N: Extended (only if needed)

### 🔀 Slice Architecture

```markdown
<!-- slice:agent=kiro -->
Kiro-specific configuration
<!-- /slice -->

<!-- slice:agent=claude -->
Claude Code-specific configuration
<!-- /slice -->
```

## Quick Start

### Steering Setup

```
~/.kiro/steering/      → Global steering
workspace/.kiro/       → Workspace steering
project/.kiro/         → Project steering
```

### Spec Workflow

1. **Design Phase**: Architecture, approach, decisions
2. **Requirements Phase**: Specifications, constraints
3. **Tasks Phase**: Implementation, execution

### Context Boundaries

```markdown
## Known Context
- [Explicitly provided information]

## Unknown Context (must query)
- [Information agent cannot assume]
```

## Platform Deployment

| Pattern | Kiro | Claude Code | Codex |
|---------|------|-------------|-------|
| Steering | `.kiro/steering/` | `CLAUDE.md` | Project docs |
| Specs | Native system | Markdown files | Inline docs |
| Identity | `agent.md` | Global config | System prompt |

## Hierarchy Resolution

```python
context = {}
context.update(global_steering)   # Foundation
context.update(workspace_steering) # Extends
context.update(project_steering)   # Overrides
```

## Spec Phase Boundaries

| Phase | Locks | Cannot Reopen |
|-------|-------|---------------|
| Design | Architecture, approach | — |
| Requirements | Specifications | Design decisions |
| Tasks | Implementation order | Design, requirements |

## Context Engineering

**Token Allocation**:
- First 20%: Highest attention
- Middle 70%: Attention valley
- Last 10%: Recency boost

**Degradation Thresholds**:
- <50K: Optimal
- 50-100K: Good
- 100-200K: Degraded
- >200K: Unreliable

## Covenant Integration

- **Bespokedness**: Operator-specific configuration
- **Decision Integrity**: Locked spec phases
- **Context Hygiene**: Layered steering
- **Data Fidelity**: No presumed preferences

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Agent assumes context | Add explicit boundaries |
| Scope creep | Enforce spec phases |
| Context bloat | Use progressive disclosure |
| Wrong platform behavior | Check slice markers |

## Integration

Works with:
- **covenant-patterns** — Principles steering enforces
- **epistemic-rendering** — Cognitive lenses for agents
- **recipe-assembly** — Slice deployment
- **multi-agent-coordination** — Multi-agent steering

---

*"Platform-agnostic principles, platform-specific deployment."* 🧭
