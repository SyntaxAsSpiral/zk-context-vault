# Context Engineering Skills

*A comprehensive library of agent system capabilities with dual-format documentation for multiple deployment targets.*

## What This Is

This is not just a skill collection. It's a **dual-format documentation system**—each skill provides complete technical documentation that can be compiled into different schemas for various deployment targets: Claude Code skills, Codex skills, and Kiro Powers. The workshop system assembles these into target-specific packages with appropriate formatting and frontmatter.

Think of it as "write once, deploy everywhere" for agent capabilities.

## The Architecture

Skills follow a standardized structure that supports multiple compilation targets:

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
| **examples/** | Self-documenting conformance tests | All targets |
| **scripts/** | Implementation code and examples | All targets |
| **references/** | Supporting documentation | All targets |
| **assets/** | Resources and data files | Kiro Powers |

### Dual-Format Requirements

Different deployment targets require different schemas:

| Target | Format | Frontmatter | Focus |
|--------|--------|-------------|-------|
| **Claude Code** | Technical SKILL.md | `name`, `description` | Implementation details |
| **Codex Skills** | Technical SKILL.md | Extended metadata | Integration patterns |
| **Kiro Powers** | User-friendly POWER.md + power.json | Rich metadata, dependencies | User experience |

## Skills Catalog

### Context Engineering Core

| Skill | Purpose | Complexity | Power Available |
|-------|---------|------------|-----------------|
| **[context-fundamentals](context-fundamentals/SKILL.md)** | Understanding context mechanics and constraints | Foundational | ❌ |
| **[context-optimization](context-optimization/SKILL.md)** | Extending effective context capacity | Intermediate | ❌ |
| **[context-compression](context-compression/SKILL.md)** | Intelligent context summarization | Advanced | ❌ |
| **[context-degradation](context-degradation/SKILL.md)** | Detecting and preventing context failures | Advanced | ❌ |

### Agent Architecture

| Skill | Purpose | Complexity | Power Available |
|-------|---------|------------|-----------------|
| **[multi-agent-patterns](multi-agent-patterns/SKILL.md)** | Designing multi-agent architectures | Advanced | ❌ |
| **[memory-systems](memory-systems/SKILL.md)** | Persistent memory for agent systems | Advanced | ❌ |
| **[tool-design](tool-design/SKILL.md)** | Creating effective agent tools | Intermediate | ❌ |

### Evaluation & Quality

| Skill | Purpose | Complexity | Power Available |
|-------|---------|------------|-----------------|
| **[evaluation](evaluation/SKILL.md)** | Building evaluation frameworks | Intermediate | ❌ |
| **[advanced-evaluation](advanced-evaluation/SKILL.md)** | Sophisticated evaluation techniques | Advanced | ❌ |

### Development & Integration

| Skill | Purpose | Complexity | Power Available |
|-------|---------|------------|-----------------|
| **[project-development](project-development/SKILL.md)** | Agent-powered development workflows | Intermediate | ❌ |
| **[mcp-builder](mcp-builder/SKILL.md)** | Model Context Protocol integration | Advanced | ❌ |
| **[catppuccin-theming](catppuccin-theming/SKILL.md)** | Consistent color palette application | Beginner | ✅ |

## Workshop Integration

The skills integrate with the [Context Workshop](../workshop/README.md) through recipe-based compilation:

### Recipe Types

- **skill-bundle**: Combine multiple skills for Claude Code
- **power-package**: Generate Kiro Power from POWER.md + power.json
- **codex-skill**: Format for Codex integration

### Compilation Process

1. **Source Analysis**: Workshop analyzes skill structure and metadata
2. **Target Selection**: Recipe specifies compilation target (Claude/Codex/Kiro)
3. **Schema Transformation**: Content reformatted for target requirements
4. **Asset Bundling**: Scripts, references, and assets packaged appropriately
5. **Deployment**: Assembled packages deployed to target locations

### Example Recipe Structure

```yaml
name: claude-context-skills
target_locations:
  - path: ~/.config/claude/skills/context-bundle.md
sources:
  - slice: skill=context-fundamentals
    file: .context/skills/context-fundamentals/SKILL.md
  - slice: skill=context-optimization
    file: .context/skills/context-optimization/SKILL.md
template: |
  # Context Engineering Skills Bundle
  {content}
```

## Implementation Patterns

### Self-Documenting Examples Pattern

Inspired by the [Semantic JSON Examples](https://github.com/SyntaxAsSpiral/semantic-json/tree/main/examples) methodology, skills should include examples that literally describe their expected behavior—files that document themselves.

#### Example Structure
- **Primary test file**: Core demonstration that describes its own expected state
- **Exported artifacts**: Clean versions showing transformation results  
- **Visual references**: Screenshots or diagrams showing expected outcomes
- **Real-world samples**: Practical applications using actual data

#### Conformance Testing Pattern
```
skill-example.canvas  →  skill-example.json
         ↓                        ↓
   Full skill format         Pure data artifact
   (implementation details)  (semantic content only)
   (context metadata)        (core capabilities)
```

### SKILL.md Structure

All skills follow a consistent documentation pattern:

```markdown
---
name: skill-identifier
description: Brief description for activation context
---

# Skill Title

## When to Activate
- Specific trigger conditions
- Use case scenarios

## Core Concepts
- Fundamental principles
- Key insights

## Detailed Topics
- Implementation details
- Advanced patterns

## Practical Guidance
- Concrete examples
- Best practices

## Integration
- Related skills
- External dependencies
```

### POWER.md Structure

Powers provide user-friendly documentation:

```markdown
# Power Title 🎯

**One-line value proposition**

## Overview
User-focused description

## Features
### 🎯 Feature Categories
- Specific capabilities
- User benefits

## Quick Start
Immediate value examples

## Advanced Usage
Power user features
```

### power.json Schema

```json
{
  "name": "identifier",
  "displayName": "Human Name",
  "description": "User-facing description",
  "version": "semver",
  "author": "creator",
  "keywords": ["searchable", "terms"],
  "category": "classification",
  "mcpServers": {},
  "steeringFiles": ["guides.md"],
  "dependencies": {},
  "assets": ["resources"]
}
```

## Quality Standards

### Documentation Requirements

- **Activation Context**: Clear triggers for when to use the skill
- **Implementation Depth**: Sufficient detail for practical application
- **Self-Documenting Examples**: Following the [conformance test pattern](https://github.com/SyntaxAsSpiral/semantic-json/blob/main/examples/conformance-test-card.canvas) where examples describe their expected behavior
- **Transformation Artifacts**: Before/after examples showing skill application results
- **Integration Guidance**: How skills connect to broader systems
- **Code Examples**: Working implementations in scripts/
- **Cross-References**: Links to related skills and external resources

### Dual-Format Consistency

- **Content Alignment**: SKILL.md and POWER.md cover same capabilities
- **Appropriate Depth**: Technical vs. user-friendly presentation
- **Metadata Sync**: Consistent naming and descriptions across formats
- **Asset Management**: Proper resource organization for different targets

## Integration

This skills library connects to the broader context ecosystem:

- **[Context Workshop](../workshop/README.md)** - Recipe-based compilation system
- **[Epistemic Rendering](../prompts/README.md)** - Different cognitive approaches to skill application
- **[Exocortex Architecture](../exocortex/README.md)** - Agent system implementation patterns
- **[Covenant Principles](../principles.md)** - Bespoke design philosophy

The skills serve as the technical foundation for implementing sophisticated agent systems while maintaining the flexibility to deploy across different platforms and use cases.

---

*Skills are capabilities. Powers are experiences. The workshop bridges the gap.*