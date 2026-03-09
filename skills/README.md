# Context Engineering Skills

*A ZK-specific library of custom agent skills packaged following the Agent Skills standard with optional Kiro Power deployment.*

## What This Is

This is not a generic skill collection. It's a **bespoke capability library** for the ZK context vault—custom skills developed for specific needs that map to core systems (Principles, Agents, Prompts, Artifacts, Workshop, Exocortex).

These are **custom-developed skills** demonstrating skill creation patterns. For production-ready skills from the community, see:

- **[Agent Skills for Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)** - Context management and engineering patterns
- **[Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)** - Production-ready skills from Vercel
- **[Anthropic Skills](https://github.com/anthropics/skills)** - Official skills from Anthropic

Think of this directory as "custom skill development examples" following the [agentskills.io](https://agentskills.io) standard.

## The Architecture

Skills follow the **Agent Skills standard** (agentskills.io) with optional Kiro Power packaging:

```
Skill Source (SKILL.md) → Workshop Recipes → Deployment Targets
                                    ↓
                          Agent Skills | Kiro Powers
```

### Canonical Structure (Flat)

**Agent Skills standard** (all skills):
```
skill-name/
├── SKILL.md              # Required: YAML frontmatter + markdown
├── getting-started.md    # Optional: guides
├── advanced-*.md         # Optional: additional docs
└── *.md                  # Optional: reference materials
```

**Kiro Power packaging** (optional, via workshop):
```
power-name/
├── POWER.md              # Main documentation
└── steering/             # All guides as .md
    ├── getting-started.md
    ├── advanced-*.md
    └── SKILL.md
```

**Key insight**: Skills are **flat** (no subfolders). All `.md` files at root level. Workshop recipes can repackage into Kiro Power format with `steering/` subfolder.

### Core System Mapping

Skills map to the 7 core systems:

| Core System | Primary Skill | Status |
|-------------|--------------|--------|
| **Principles** | covenant-patterns | ✅ |
| **Agents** | agent-steering | ✅ |
| **Prompts** | epistemic-rendering | ✅ |
| **Artifacts** | semantic-json-workflows | ✅ |
| **Workshop** | recipe-assembly | ✅ |
| **Exocortex** | multi-agent-coordination | ✅ |
| **Aesthetic** | catppuccin-theming | ✅ |

## Skills Catalog

### Foundations

| Skill | Purpose | Core System |
|-------|---------|-------------|
| **[covenant-patterns](covenant-patterns/SKILL.md)** | Thirteen principles as design constraints | Principles |

### Agent Configuration

| Skill | Purpose | Core System |
|-------|---------|-------------|
| **[agent-steering](agent-steering/SKILL.md)** | Universal single-agent configuration | Agents |
| **[multi-agent-coordination](multi-agent-coordination/SKILL.md)** | Pentadyadic and multi-agent patterns | Exocortex |

### Cognitive Tools

| Skill | Purpose | Core System |
|-------|---------|-------------|
| **[epistemic-rendering](epistemic-rendering/SKILL.md)** | Eight cognitive lenses for understanding | Prompts |

### Context Management

| Skill | Purpose | Core System |
|-------|---------|-------------|
| **[recipe-assembly](recipe-assembly/SKILL.md)** | Slice architecture and deployment | Workshop |
| **[context-degradation](context-degradation/SKILL.md)** | Detecting context failures | Reference |
| **[memory-systems](memory-systems/SKILL.md)** | Persistent agent memory and knowledge graphs | Memory |

### Visual & Integration

| Skill | Purpose | Core System |
|-------|---------|-------------|
| **[semantic-json-workflows](semantic-json-workflows/SKILL.md)** | Canvas-to-structured-data anticompiler | Artifacts |
| **[catppuccin-theming](catppuccin-theming/SKILL.md)** | Consistent color palette application | Aesthetic |
| **[mcp-builder](mcp-builder/SKILL.md)** | Model Context Protocol server creation | Integration |
| **[openrgb](openrgb/SKILL.md)** | Ambient RGB via OpenRGB SDK — presence, notifications, effects | Integration |

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
└── openrgb (standalone)
```

## Workshop Integration

Skills integrate with the [Context Workshop](../workshop/README.md) through recipe-based compilation:

### Agent Skills Deployment

```yaml
name: covenant-patterns
output_format: skill
target_locations:
  - path: ~/.claude/skills/covenant-patterns/
sources:
  - file: skills/covenant-patterns/SKILL.md
```

### Kiro Power Deployment

```yaml
name: catppuccin-theming
output_format: power
target_locations:
  - path: ~/.kiro/powers/catppuccin-theming/
sources:
  - file: skills/catppuccin-theming/POWER.md
  - file: skills/catppuccin-theming/SKILL.md
    output_name: steering/skill.md
  - file: skills/catppuccin-theming/getting-started.md
    output_name: steering/getting-started.md
```

**Pattern**: Skills are flat at source, workshop recipes create `steering/` subfolder for Kiro Powers.

### Slice Architecture

Skills use HTML comment markers for extraction:

```markdown
<!-- slice:skill=covenant-patterns -->
Content to extract
<!-- /slice -->
```

## Documentation Standards

### SKILL.md Structure (Required)

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

**Frontmatter requirements** (agentskills.io):
- `name`: lowercase, numbers, hyphens only, max 64 chars
- `description`: max 1024 chars

### POWER.md Structure (Optional)

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

**Note**: POWER.md is optional. Only create if deploying as Kiro Power.

### Additional Guides (Optional)

- `getting-started.md` - Initial setup and basic usage
- `advanced-*.md` - Advanced patterns and techniques
- `*.md` - Any additional reference materials

**All files at root level** (flat structure).

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

### Format Consistency

- **Agent Skills standard**: All skills follow agentskills.io spec
- **Flat structure**: No subfolders (except `archive/`)
- **Optional Power**: POWER.md only if deploying to Kiro
- **Workshop assembly**: Recipes create target-specific structure

## Restructuring Notes

### Canonical Example

**[catppuccin-theming](catppuccin-theming/)** is the canonical skill structure:
- Flat directory (all `.md` at root)
- SKILL.md with proper frontmatter
- POWER.md for Kiro deployment
- Additional guides (getting-started.md, advanced-theming.md, etc.)
- No `power.json` (not part of Agent Skills spec)

### Migration Status

**To be restructured** (remove `power.json`, flatten structure):
- agent-steering
- covenant-patterns
- epistemic-rendering
- multi-agent-coordination
- recipe-assembly
- semantic-json-workflows

**Already flat** (no changes needed):
- catppuccin-theming ✅
- context-degradation ✅
- mcp-builder ✅
- openrgb ✅

## Archive

Generic context-engineering skills have been archived to `archive/`. These contain valuable theoretical content that may be referenced when building new skills:

- context-fundamentals (foundational theory)
- context-optimization (token allocation findings)
- context-compression (compression metrics)
- multi-agent-patterns (telephone game research)
- tool-design (reduction case studies)
- evaluation (basic frameworks)
- advanced-evaluation (LLM-as-judge patterns)
- project-development (case studies)

**Note:** `archive/memory-systems/` contains older theoretical content; the active `memory-systems/` skill at root level is the canonical version.

## Community Skills

For production-ready skills, explore these repositories:

### [Agent Skills for Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)
Comprehensive context management patterns including:
- Context optimization techniques
- Memory management strategies
- Multi-agent coordination patterns
- Evaluation frameworks

### [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)
Production-ready skills from Vercel including:
- Web development patterns
- API integration
- Deployment workflows
- Testing strategies

### [Anthropic Skills](https://github.com/anthropics/skills)
Official skills from Anthropic including:
- Claude-specific patterns
- Best practices
- Integration examples

## Integration

This skills library connects to the broader context ecosystem:

- **[Principles](../agents/steering-global-principles.md)** — Foundation that skills operationalize
- **[Agents](../agents/README.md)** — Single-agent configuration using skills
- **[Prompts](../prompts/README.md)** — Epistemic lenses documented as skill
- **[Artifacts](../artifacts/README.md)** — Visual workflows documented as skill
- **[Workshop](../workshop/README.md)** — Recipe-based skill compilation
- **[Exocortex](../exocortex/README.md)** — Multi-agent patterns as skill

---

*Custom skills following Agent Skills standard. For production skills, see community repositories above.*
