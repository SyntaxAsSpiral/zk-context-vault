---
id: agent-system-readme
title: "Agent System Architecture"
type: 
  - "documentation"
  - "readme"
category: "agents"
tags:
  - "agents"
  - "architecture"
  - "universal"
  - "steering"
  - "single-agent"
created: 2026-01-11
modified: 2026-01-15
status: "active"
glyph: "🧭"
lens: "system-architecture"
---

# Agent System Architecture

*Universal patterns for single-agent steering across AI coding platforms.*

## What This Is

This is not multi-agent coordination. It's **single-agent steering**—universal patterns for configuring individual AI coding agents (Kiro, Claude Code, Codex, Charm) through explicit context management and modular documentation.

The directory documents platform-agnostic patterns that work across different AI coding environments. While each platform has unique features, the core steering principles remain consistent.

Think of it as "universal agent configuration" - explicit, modular, assumption-hostile.

## The Shift: Single-Agent Focus

This vault previously documented multi-agent coordination patterns. Those have moved to:
- **[Exocortex](../exocortex/README.md)** - Pentadyadic multi-agent architecture
- **[Multi-Agent Coordination Skill](../skills/multi-agent-coordination/SKILL.md)** - Coordination patterns and frameworks

This directory now focuses exclusively on **single-agent steering** - how to configure one AI coding agent effectively, regardless of platform.

## Core Architecture

```
Global Steering → Workspace Steering → Project Steering → Agent Behavior
       ↓                  ↓                   ↓
  Principles         AGENTS.md          .kiro/steering/
```

### The Steering Hierarchy

**Three-tier context system** that works across all platforms:

| Tier | Scope | Implementation | Example |
|------|-------|----------------|---------|
| **Global** | Universal principles | `~/.kiro/steering/` or platform config | Covenant Principles, Operator profile |
| **Workspace** | Multi-project coordination | Workspace root `AGENTS.md` | Project-agnostic guidance |
| **Project** | Specific codebase context | `.kiro/steering/*.md` | Tech stack, structure, product |

**Key insight**: Later tiers override earlier ones. Project steering takes precedence over workspace, workspace over global.

## The .kiro/ Canonical Source

**For Kiro users**: `.kiro/` is the **canonical modular context system**. It provides:

### Modular Steering Files
```
.kiro/steering/
├── product.md     # What this project is
├── structure.md   # Directory organization
├── tech.md        # Technology stack
└── custom-*.md    # Additional context
```

**How it works:**
- Kiro auto-loads all `.md` files in `.kiro/steering/`
- Each file becomes a workspace-level steering rule
- Modular design = add/remove context by adding/removing files
- Appears in Kiro UI as "Included Rules"

**Automatic inclusions:**
- `AGENTS.md` at workspace root is automatically loaded
- Provides project-specific agent guidance
- No need to duplicate in `.kiro/steering/`

### Structured Development (Specs)
```
.kiro/specs/{feature}/
├── requirements.md  # User stories, acceptance criteria
├── design.md        # Architecture, approach
└── tasks.md         # Implementation breakdown
```

**3-phase workflow**: Design → Requirements → Tasks → Implementation

### Automated Workflows (Hooks)
```
.kiro/hooks/
└── *.kiro.hook      # JSON configurations for event triggers
```

**Hook types**: `fileEdited`, `fileCreated`, `userTriggered`, `promptSubmit`, `agentStop`

See [.kiro/README.md](../.kiro/README.md) for complete documentation.

## Universal Patterns (All Platforms)

### Explicit Context Management

**Principle**: No assumptions about what the agent knows.

**Implementation**:
- **Kiro**: `.kiro/steering/*.md` files
- **Claude Code**: `CLAUDE.md` or project documentation
- **Codex**: `AGENTS.md` or inline documentation
- **Charm**: Configuration files or project docs

**Pattern**: Provide explicit context through structured markdown files that the agent can reference.

### Hierarchical Steering

**Principle**: Context flows from general to specific.

**Implementation**:
- **Global**: Universal principles (Covenant, operator profile)
- **Workspace**: Multi-project coordination (`AGENTS.md`)
- **Project**: Codebase-specific context (`.kiro/steering/` or equivalent)

**Pattern**: Later context overrides earlier. Project-specific guidance takes precedence.

### Modular Composition

**Principle**: Add/remove context without editing monolithic files.

**Implementation**:
- **Kiro**: Multiple `.md` files in `.kiro/steering/`
- **Claude Code**: Separate documentation files
- **Codex**: Modular markdown documents
- **Charm**: Composable configuration

**Pattern**: One concern per file. Easy to add, remove, or update specific context.

### Assumption-Hostile Design

**Principle**: Guard against presumptive behavior.

**Implementation**: Follow [Covenant Principles](steering-global-principles.md):
- 👁️ **Dotfile Visibility** - No bare `ls`, treat dotfolders as first-class
- 🗣️ **Data Fidelity** - UNKNOWN > INVENTED, never invent data
- ⛔ **Work Preservation** - Never discard work without explicit instruction
- 🚮 **Final-State Surgery** - Remove old world entirely unless transition requested

**Pattern**: Explicit constraints prevent common failure modes across all agents.

## Platform-Specific Features

### Kiro
- **Modular steering**: `.kiro/steering/*.md` auto-loaded
- **Hooks**: Event-driven automation (`.kiro/hooks/*.kiro.hook`)
- **Specs**: 3-phase structured development (`.kiro/specs/*/`)
- **MCP integration**: External tool servers

### Claude Code
- **CLAUDE.md**: Global steering file (`~/.claude/CLAUDE.md`)
- **Project docs**: Markdown files in project root

### Codex
- **AGENTS.md**: Project-level steering
- **Documentation**: Inline and separate markdown files

## Key Files in This Directory

### [agent-roles.md](agent-roles.md)
**Purpose**: Identity templates and role sigils for different agents

**Contains**:
- Slice-based agent personas (Kiro, Claude, Codex, Grok)
- System prompt templates
- Role-specific guidance

**Usage**: Extract slices via workshop recipes for platform-specific deployment

### [steering-global-operator.md](steering-global-operator.md)
**Purpose**: Operator (ZK) profile and preferences

**Contains**:
- Identity and role sigils
- Environment details (Windows, nushell, paths)
- Current project priorities
- Aesthetic preferences (Catppuccin colors, Recursive Mono font)

**Usage**: Global-level context for all agents

### [steering-global-principles.md](steering-global-principles.md)
**Purpose**: Covenant Principles - anti-assumption framework

**Contains**:
- 13 principles (yamas) with niyamas (practices)
- Each principle guards against a specific assumption
- Operational guidance for assumption-hostile design

**Usage**: Foundation for all agent behavior across platforms

## Deployment Patterns

### Workshop Assembly

The [workshop system](../workshop/README.md) uses slice architecture to deploy agent configurations:

```yaml
# Example: Deploy to Claude Code
name: Claudi
target_locations:
  - path: ~/.claude/CLAUDE.md
sources:
  - slice: agent=claudi-claude-code
    slice-file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-principles.md
```

**Pattern**: Extract slices from this directory, assemble into platform-specific files.

### Slice Architecture

Content marked with HTML comments for modular extraction:

```markdown
<!-- slice:agent=kiro -->
Kiro-specific system prompt content
<!-- /slice -->

<!-- slice:agent=claudi-claude-code -->
Claude Code-specific system prompt content
<!-- /slice -->
```

**Benefit**: Write once, deploy to multiple platforms with platform-specific customization.

## Integration with Broader Ecosystem

### Skills Library
Agent configurations reference [skills](../skills/README.md) for technical capabilities:
- **[agent-steering](../skills/agent-steering/SKILL.md)** - Steering system documentation
- **[covenant-patterns](../skills/covenant-patterns/SKILL.md)** - Principles as design constraints

### Workshop System
[Workshop recipes](../workshop/README.md) assemble agent configurations from this directory.

### Exocortex
For multi-agent coordination, see [exocortex](../exocortex/README.md) - this directory focuses on single-agent steering only.

## Best Practices

### For Kiro Users

1. **Use .kiro/steering/ for project context**
   - Create modular files (one concern per file)
   - Let Kiro auto-load them
   - Update as project evolves

2. **Leverage AGENTS.md at workspace root**
   - Automatically loaded by Kiro
   - Provides project-specific guidance
   - No duplication needed

3. **Create specs for features**
   - Use 3-phase workflow (Design → Requirements → Tasks)
   - Prevents scope creep
   - Maintains clear acceptance criteria

4. **Use hooks for automation**
   - Event-driven workflows
   - Consistency checks
   - Principle enforcement

### For Other Platforms

1. **Leverage AGENTS/CLAUDE.md in global + project scopes**
   - Automatically loaded by Codex and Claude harnesses respectively.
   - Cursor IDE auto-imports CLAUDE.md
   - Most harness will auto load AGENTS.md 
   - Provides project-specific guidance
   - No duplication needed

2. **Use slice architecture**
   - Mark content with HTML comments
   - Enable platform-specific extraction
   - Maintain single source of truth

## The Single-Agent Advantage

This architecture solves fundamental problems in AI-augmented work:

- **No Black Boxes**: Every behavior explicitly configured
- **Assumption Resistance**: Principles prevent presumptive failures
- **Modular Composition**: Add/remove context without monolithic files
- **Platform Agnostic**: Same patterns work across different agents
- **Progressive Disclosure**: Context loads per-turn, not all at once
- **Work Preservation**: Nothing gets lost, changes are explicit

The result is AI assistance that enhances rather than replaces human cognition, maintaining transparency and control while providing sophisticated capabilities.

---

*Single-agent steering. Universal patterns. Explicit behavior.* 🧭
