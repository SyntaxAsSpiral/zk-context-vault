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
  - "kiro"
  - "claude-code"
  - "codex"
  - "charm"
created: 2026-01-11
modified: 2026-01-11
status: "active"
glyph: "🧭"
lens: "system-architecture"
---

# Agent System Architecture

*Comprehensive documentation for AI coding agent integration, modular context assembly, and structured development processes.*

## What This Is

This is not just agent configuration. It's a **universal agent ecosystem**—documenting patterns that work across different AI coding environments: Kiro, Claude Code, Codex, Charm, and others. While Kiro-specific features like hooks and MCP integration are documented here, the core patterns (steering, specs, modular context) are platform-agnostic.

The directory captures operational patterns that transform any AI coding agent from a simple assistant into a true cognitive partner.

Think of it as "AI agents as they should be" - fully configured, context-aware, and systematically organized.

## Why This Architecture Works

The agent system design philosophy aligns with the [Covenant Principles](../principles.md) and works across different AI coding environments:

- **Assumption-hostile**: Explicit context management prevents presumptive behavior (works in any agent)
- **Bespoke-first**: Modular system optimizes for operator workflow over enterprise patterns (universal principle)
- **Context hygiene**: Progressive disclosure and explicit boundaries maintain clean cognitive load (platform-agnostic)
- **Work preservation**: Specs and structured processes ensure nothing gets lost in translation (universal need)

The patterns documented here work whether you're using **Kiro** (with full hook/MCP integration), **Claude Code** (with steering and specs), **Codex** (with context assembly), or **Charm** (with modular configuration).

## The Architecture

The agent system operates through integrated components that work across different AI coding environments:

```
Steering → Specs → Context Assembly → Agent Experience
```

### Universal Components

| Component | Purpose | Platform Support | Integration |
|-----------|---------|------------------|-------------|
| **[Steering](kiro-steering.md)** | Context and behavior guidance | All agents via markdown files | Contextual intelligence |
| **[Specs](kiro-specs.md)** | 3-phase development process | All agents via structured docs | Structured development |
| **[Agent Roles](agent-roles.md)** | Identity templates and sigils | All agents via slice architecture | Persona management |

### Platform-Specific Components

| Component | Purpose | Platform Support | Integration |
|-----------|---------|------------------|-------------|
| **[Hooks](kiro-hooks.md)** | Automated workflow triggers | Kiro only | Event-driven automation |
| **[MCP Integration](kiro-mcp.md)** | Model Context Protocol servers | Kiro, Claude Code (limited) | External tool access |

## Universal Capabilities

### 🧭 Steering System - Contextual Intelligence

Steering provides layered context that adapts to different scopes and works with any AI coding agent:

| Scope | Purpose | Implementation | Platform Support |
|-------|---------|----------------|------------------|
| **Global** | Universal agent behavior | `~/.kiro/steering/` or project docs | All agents |
| **Workspace** | Multi-project coordination | Workspace-level steering files | All agents |
| **Project** | Specific project context | Project-specific documentation | All agents |

**Hierarchy**: Global → Workspace → Project (later overrides earlier)

### 📋 3-Phase Spec Process - Structured Development

The spec system provides structured development workflows that prevent scope creep across any platform:

#### Phase Structure
1. **Design** - Architecture and approach definition
2. **Requirements** - Concrete specifications and constraints  
3. **Tasks** - Implementation breakdown and execution

This pattern works whether you're using Kiro's native spec system, Claude Code's project files, or simple markdown documentation.

### 🎭 Agent Roles - Identity Management

The slice architecture enables modular identity composition across platforms:

```markdown
<!-- slice:agent=kiro -->
System prompt template for Kiro persona
<!-- /slice -->

<!-- slice:agent=claude -->
System prompt template for Claude Code persona
<!-- /slice -->
```

## Platform-Specific Features

### 🪝 Kiro Hook System - Automated Cognitive Workflows

Hooks transform Kiro from reactive to proactive, automatically triggering behaviors based on context:

| Hook Type | Purpose | Example Use Case |
|-----------|---------|------------------|
| **Persona Switching** | Dynamic identity adoption | `murder` → Kharon-9 persona |
| **Documentation Consistency** | Automated drift detection | Terminology sync across projects |
| **Dotfile Visibility** | Covenant principle enforcement | Remind about `ls -a` usage |

### 🔌 MCP Server Integration - External Cognitive Extensions

MCP servers extend capabilities beyond the base agent (primarily Kiro, limited Claude Code support):

- **Task Management**: SDK task automation database
- **Web Access**: Fetch server for external content
- **Custom Tools**: Project-specific integrations

## Cross-Platform Usage

### Using with Different Agents

**Kiro** (Full Integration)
- Native hooks and MCP server support
- Built-in spec system with 3-phase workflow
- Hierarchical steering with automatic context loading
- Complete slice architecture support

**Claude Code** (Core Patterns)
- Steering via project documentation and context files
- Specs as structured markdown in project folders
- Agent roles via system prompts and context assembly
- Limited MCP support for external tools

**Codex** (Documentation-Based)
- Steering through comprehensive project documentation
- Specs as structured development guides
- Context assembly via markdown includes and references
- Agent roles via prompt engineering patterns

**Charm** (Configuration-Driven)
- Steering via configuration files and documentation
- Specs as structured project templates
- Context assembly through modular configuration
- Agent roles via persona configuration files

### Universal Implementation Patterns

All platforms benefit from:
- **Explicit Context Management**: No assumptions about what the agent knows
- **Structured Development**: 3-phase approach prevents scope creep
- **Modular Identity**: Slice-based persona management
- **Hierarchical Guidance**: Global → Workspace → Project context inheritance

## Operational Patterns

### Hook Development Workflow

1. **Identify Trigger**: What event should activate the hook?
2. **Define Action**: What should Kiro do when triggered?
3. **Test Behavior**: Verify the hook works as expected
4. **Deploy Globally**: Move successful hooks to appropriate scope

### Spec Development Process

1. **Design Phase**: Architecture, approach, and high-level decisions
2. **Requirements Phase**: Concrete specifications and constraints
3. **Tasks Phase**: Implementation breakdown and execution plan

### MCP Server Integration

1. **Server Selection**: Choose appropriate MCP server for capability
2. **Configuration**: Add to `.kiro/settings/mcp.json`
3. **Testing**: Verify server connectivity and functionality
4. **Documentation**: Update this system for future reference

## Future Expansion

This agents directory will grow to include:

- **Advanced Hook Patterns**: Complex workflow automation
- **Custom MCP Servers**: Bespoke cognitive extensions
- **Multi-Agent Coordination**: Kiro + external agent integration
- **Evaluation Frameworks**: Measuring agent effectiveness
- **Deployment Automation**: Streamlined configuration management

## The Universal Agent Advantage

This agent architecture solves fundamental problems in AI-augmented work across all platforms:

- **No Black Boxes**: Every behavior is explicitly configured and documented
- **Assumption Resistance**: Principles prevent presumptive failures regardless of agent
- **Modular Composition**: Slice architecture enables flexible assembly across platforms
- **Multiple Deployment**: Write once, adapt to different agent environments
- **Cognitive Flexibility**: Multiple approaches work with different agent capabilities
- **Workflow Integration**: Systems work together rather than in isolation

Whether you're using Kiro's advanced features, Claude Code's project integration, Codex's documentation focus, or Charm's configuration approach, these patterns create AI assistance that enhances rather than replaces human cognition.

---

*Agent-agnostic cognitive architecture. Choose your platform, keep your patterns.* 🧭