# Context Engineering Skills

*A ZK-specific library of agent system capabilities with dual-format documentation for multiple deployment targets.*

## What This Is

This is not a generic skill collection. It's a **bespoke capability library** for the ZK context vault—each skill maps to a core system (Principles, Agents, Prompts, Artifacts, Workshop, Exocortex) and provides practical patterns rather than theoretical frameworks.

Think of it as "the skills ZK actually uses" with dual-format deployment.

## The Architecture

Skills follow a standardized structure supporting multiple compilation targets:

```
Skill Source → Workshop Recipes → Target-Specific Packages
```

### Skill Structure

Each skill directory contains:

| Component | Purpose | Compilation Target |
|-----------|---------|-------------------|
| **SKILL.md** | Core technical documentation | Claude Code, Codex skills |
| **POWER.md** | User-friendly power documentation | Kiro Powers |
| **power.json** | Power metadata and configuration | Kiro Powers |
| **references/** | Supporting documentation | All targets |
| **assets/** | Resources and data files | Kiro Powers |

### Core System Mapping

Skills map to the 7 core systems:

| Core System | Primary Skill | Coverage |
|-------------|--------------|----------|
| **Principles** | covenant-patterns | ✅ Full |
| **Agents** | agent-steering | ✅ Full |
| **Prompts** | epistemic-rendering | ✅ Full |
| **Artifacts** | semantic-json-workflows | ✅ Full |
| **Workshop** | recipe-assembly | ✅ Full |
| **Exocortex** | multi-agent-coordination | ✅ Full |
| **Skills** | (this library) | META |

## Skills Catalog

### Foundations

| Skill | Purpose | Core System | Power |
|-------|---------|-------------|-------|
| **[covenant-patterns](covenant-patterns/SKILL.md)** | Thirteen principles as design constraints | Principles | ✅ |

### Agent Configuration

| Skill | Purpose | Core System | Power |
|-------|---------|-------------|-------|
| **[agent-steering](agent-steering/SKILL.md)** | Universal agent configuration (Kiro, Claude, Codex) | Agents | ✅ |
| **[multi-agent-coordination](multi-agent-coordination/SKILL.md)** | Pentadyadic and multi-agent patterns | Exocortex | ✅ |

### Cognitive Tools

| Skill | Purpose | Core System | Power |
|-------|---------|-------------|-------|
| **[epistemic-rendering](epistemic-rendering/SKILL.md)** | Eight cognitive lenses for different understanding | Prompts | ✅ |

### Context Management

| Skill | Purpose | Core System | Power |
|-------|---------|-------------|-------|
| **[recipe-assembly](recipe-assembly/SKILL.md)** | Slice architecture and deployment | Workshop | ✅ |
| **[context-degradation](context-degradation/SKILL.md)** | Detecting and preventing context failures | Reference | ❌ |

### Visual & Integration

| Skill | Purpose | Core System | Power |
|-------|---------|-------------|-------|
| **[semantic-json-workflows](semantic-json-workflows/SKILL.md)** | Canvas-to-structured-data anticompiler | Artifacts | ✅ |
| **[catppuccin-theming](catppuccin-theming/SKILL.md)** | Consistent color palette application | Aesthetic | ✅ |
| **[mcp-builder](mcp-builder/SKILL.md)** | Model Context Protocol server creation | Integration | ❌ |

## Skill Dependencies

```
covenant-patterns (foundation)
    ↓
├── agent-steering (depends on covenant)
│       ↓
│   └── multi-agent-coordination (depends on agent-steering)
├── epistemic-rendering (depends on covenant)
├── recipe-assembly (depends on covenant)
└── semantic-json-workflows (standalone)
```

## Workshop Integration

Skills integrate with the [Context Workshop](../workshop/README.md) through recipe-based compilation:

### Example Recipe

```yaml
name: skill-bundle
target_locations:
  - path: ~/.claude/skills/covenant-bundle.md
sources:
  - slice: skill=covenant-patterns
    file: skills/covenant-patterns/SKILL.md
  - slice: skill=agent-steering
    file: skills/agent-steering/SKILL.md
template: |
  # Skills Bundle
  {content}
```

### Slice Architecture

Skills use HTML comment markers for extraction:

```markdown
<!-- slice:skill=covenant-patterns -->
Content to extract
<!-- /slice -->
```

## Documentation Standards

### SKILL.md Structure

```markdown
---
name: skill-identifier
description: Brief description for activation context
---

# Skill Title

## Overview
What is this, why it exists

## Core Concepts
Fundamental principles

## Detailed Topics
Implementation patterns

## Practical Guidance
Concrete examples

## Integration
Related skills, system connections
```

### POWER.md Structure

```markdown
# Power Title 🎯

**One-line value proposition**

## Overview
User-focused description

## Features
### Feature Categories
- Specific capabilities

## Quick Start
Immediate value examples
```

### power.json Schema

```json
{
  "name": "identifier",
  "displayName": "Human Name",
  "description": "User-facing description",
  "version": "1.0.0",
  "author": "ZK",
  "keywords": ["searchable", "terms"],
  "category": "classification",
  "mcpServers": {},
  "steeringFiles": ["POWER.md", "SKILL.md"],
  "dependencies": {},
  "assets": []
}
```

## Quality Standards

### Covenant Alignment

All skills embody covenant principles:
- **Bespokedness**: ZK-specific patterns, not generic frameworks
- **Data Fidelity**: No invented examples or presumed outputs
- **Determinism**: Reproducible patterns with stable identifiers
- **Context Hygiene**: Skills compile per-recipient, not dump everything

### Documentation Requirements

- **Activation Context**: Clear triggers for when to use
- **Implementation Depth**: Sufficient detail for practical application
- **System Integration**: How skill connects to core systems
- **Cross-References**: Links to related skills

### Dual-Format Consistency

- **Content Alignment**: SKILL.md and POWER.md cover same capabilities
- **Appropriate Depth**: Technical vs. user-friendly presentation
- **Metadata Sync**: Consistent naming across formats

## Archive

Generic context-engineering skills have been archived to `archive/`. These contain valuable theoretical content that may be referenced when building new skills:

- context-fundamentals (foundational theory)
- context-optimization (token allocation findings)
- context-compression (compression metrics)
- memory-systems (DMR benchmarks)
- multi-agent-patterns (telephone game research)
- tool-design (reduction case studies)
- evaluation (basic frameworks)
- advanced-evaluation (LLM-as-judge patterns)
- project-development (case studies)

## Integration

This skills library connects to the broader context ecosystem:

- **[Principles](steering-global-principles.md)** — Foundation that skills operationalize
- **[Agents](../agents/README.md)** — Agent configuration using skills
- **[Prompts](../prompts/README.md)** — Epistemic lenses documented as skill
- **[Artifacts](../artifacts/README.md)** — Visual workflows documented as skill
- **[Workshop](../workshop/README.md)** — Recipe-based skill compilation
- **[Exocortex](../exocortex/README.md)** — Multi-agent patterns as skill

---

*Skills are capabilities mapped to core systems. Bespoke, not generic.*
