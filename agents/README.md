# Kiro Agent System

*Comprehensive documentation for Kiro IDE integration, modular context assembly, and the 3-phase spec process.*

## What This Is

This is not just agent configuration. It's a **Kiro-specific agent ecosystem**—documenting the unique capabilities that make Kiro exceptional: hooks for automated workflows, MCP server integration, the 3-phase spec process, and modular steering systems. This directory captures the operational patterns that transform Kiro from an IDE into a true cognitive partner.

Think of it as "Kiro as it should be" - fully configured and context-aware.

## Why Kiro Fits

Kiro's design philosophy aligns perfectly with the [Covenant Principles](../principles.md):

- **Assumption-hostile**: Kiro's explicit context management prevents presumptive behavior
- **Bespoke-first**: The modular system optimizes for operator workflow over enterprise patterns
- **Context hygiene**: Progressive disclosure and explicit boundaries maintain clean cognitive load
- **Work preservation**: Specs and hooks ensure nothing gets lost in translation

The 3-phase spec process you designed independently mirrors Kiro's natural workflow, making this a perfect cognitive fit.

## The Architecture

Kiro operates through four integrated systems that work together seamlessly:

```
Hooks → MCP Servers → Specs → Steering → Unified Agent Experience
```

### Core Components

| Component | Purpose | Location Pattern | Integration |
|-----------|---------|------------------|-------------|
| **[Hooks](kiro-hooks.md)** | Automated workflow triggers | `.kiro/hooks/*.kiro.hook` | Event-driven automation |
| **[MCP Integration](kiro-mcp.md)** | Model Context Protocol servers | `.kiro/settings/mcp.json` | External tool access |
| **[Specs](kiro-specs.md)** | 3-phase development process | `.kiro/specs/*/` | Structured development |
| **[Steering](kiro-steering.md)** | Context and behavior guidance | `.kiro/steering/*.md` | Contextual intelligence |
| **[Agent Roles](agent-roles.md)** | Identity templates and sigils | Slice architecture | Persona management |

## Kiro's Unique Capabilities

### 🪝 Hook System - Automated Cognitive Workflows

Hooks transform Kiro from reactive to proactive, automatically triggering behaviors based on context:

| Hook Type | Purpose | Example Use Case |
|-----------|---------|------------------|
| **Persona Switching** | Dynamic identity adoption | `murder` → Kharon-9 persona |
| **Documentation Consistency** | Automated drift detection | Terminology sync across projects |
| **Dotfile Visibility** | Covenant principle enforcement | Remind about `ls -a` usage |

**Hook Architecture:**
```json
{
  "when": { "type": "userTriggered|fileEdited|sessionStart" },
  "then": { "type": "askAgent|executeCommand", "prompt": "..." }
}
```

### 🔌 MCP Server Integration - External Cognitive Extensions

MCP servers extend Kiro's capabilities beyond the IDE:

- **Task Management**: SDK task automation database
- **Web Access**: Fetch server for external content
- **Custom Tools**: Project-specific integrations

**Configuration Pattern:**
```json
{
  "mcpServers": {
    "tasks": {
      "command": "node",
      "args": [".system/node/mcp-servers/tasks/index.mjs"]
    }
  }
}
```

### 📋 3-Phase Spec Process - Structured Development

The spec system provides structured development workflows that prevent scope creep and ensure clarity:

#### Phase Structure
1. **Design** - Architecture and approach definition
2. **Requirements** - Concrete specifications and constraints  
3. **Tasks** - Implementation breakdown and execution

#### Current Specs
- **Collectivist**: AI-powered collection curation system
- **Context Workshop**: Recipe-based context assembly system

This mirrors your existing [Amexsomnemon spec architecture](../../.dev/amexsomnemon/cockpit/specs/) with implementation/, schemas/, and templates/ directories.

### 🧭 Steering System - Contextual Intelligence

Steering provides layered context that adapts to different scopes:

| Scope | Purpose | Example |
|-------|---------|---------|
| **Global** | Universal agent behavior | Core identity and principles |
| **Workspace** | Multi-project coordination | Compiled workspace navigation |
| **Project** | Specific project context | Collectivist product knowledge |

**Hierarchy**: Global → Workspace → Project (later overrides earlier)

### 🎭 Agent Roles - Identity Management

The slice architecture enables modular identity composition:

```markdown
<!-- slice:agent=kiro -->
System prompt template for Kiro persona
<!-- /slice -->
```

This integrates with the [Workshop system](../workshop/README.md) for automated agent configuration deployment.

## Integration Patterns

### Workshop Recipe Integration

Kiro configurations can be assembled through workshop recipes:

```yaml
name: kiro-agent-config
sources:
  - slice: agent=kiro
    file: .context/agents/agent-roles.md
  - slice: steering=workspace
    file: .dev/.kiro/steering/compiled-workspace.md
target_locations:
  - path: ~/.kiro/agents/kiro-complete.md
```

### Cross-System Coherence

The agent system maintains coherence with:

- **[Context Engineering Skills](../skills/README.md)** - Technical capabilities
- **[Epistemic Rendering](../prompts/README.md)** - Cognitive approaches  
- **[Exocortex Architecture](../exocortex/README.md)** - Multi-agent patterns
- **[Workshop System](../workshop/README.md)** - Assembly and deployment

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

## The Kiro Advantage

Kiro's modular context assembly and explicit configuration management solve the fundamental problems of AI assistance:

- **No Black Boxes**: Every behavior is explicitly configured
- **Contextual Awareness**: Steering adapts to current scope
- **Workflow Integration**: Hooks automate cognitive patterns
- **Extensible Architecture**: MCP servers add capabilities on demand
- **Structured Development**: Specs prevent scope creep and confusion

This creates an AI assistant that truly understands your workflow rather than fighting against it.

---

*Kiro = care + flow. The recursion is the craft. 🧭*