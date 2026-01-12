# Context Workshop

*A minimal context management system using recipe-based assembly and deployment of documentation slices.*

## What This Is

This is not a complex build system. It's a **context workshop**—a bespoke tool for assembling context documentation from distributed sources using YAML recipes embedded in Obsidian markdown. The system follows the principle of disposable software optimized for operator workflow rather than enterprise scalability.

Think of it as "make for context" with Obsidian integration.

## The Architecture

The workshop operates through a simple two-script pipeline: assembly and synchronization:

```
Obsidian Context Vault → Workshop Recipes → assemble.py → Workshop Output → sync.py → Target Locations
```

### Core Components

| Component | Purpose | Location | Authority |
|-----------|---------|----------|-----------|
| **[Templates](templates/)** | Recipe scaffolding | `.context/workshop/templates/` | Obsidian |
| **[Recipes](.)** | Assembly instructions | `.context/workshop/*.md` | Operator |
| **[Output](output/)** | Assembled artifacts | `.context/workshop/output/` | System |
| **[Manifest](recipe-manifest.md)** | Deployment tracking | `.context/workshop/recipe-manifest.md` | System |

### Script Pipeline

| Script | Function | Location | Responsibility |
|--------|----------|----------|----------------|
| **[assemble.py](../../.dev/.scripts/assemble.py)** | Extract slices, apply templates | `C:/Users/synta.ZK-ZRRH/.dev/.scripts/` | Assembly |
| **[sync.py](../../.dev/.scripts/sync.py)** | Deploy outputs, clean orphans | `C:/Users/synta.ZK-ZRRH/.dev/.scripts/` | Synchronization |

### VSCode Integration

The system integrates with VSCode through [task configurations](../../.dev/.scripts/README-vscode-tasks.md):

- **Ctrl+Shift+B** - Run full workflow (assemble + sync)
- **Ctrl+Shift+P** → "Tasks: Run Task" - Individual operations
- **Dry run modes** - Preview operations without file changes
- **Verbose modes** - Detailed output for debugging

## Recipe Structure

Recipes combine Obsidian frontmatter with embedded YAML configuration:

### Recipe Schema
```yaml
name: recipe-identifier
target_locations:
  - path: /deployment/target/file.md
sources:
  - slice: slice-identifier
    file: source/file/path.md
template: |
  Template with {content} substitution
```

### Recipe Types

The workshop provides specialized templates for different context types:

| Template | Purpose | Specialized Fields |
|----------|---------|-------------------|
| **[recipe-agent-{{name}}.md](templates/recipe-agent-{{name}}.md)** | Agent system prompts | `agent_format`, `persona_elements` |
| **[recipe-kiro-{{name}}.md](templates/recipe-kiro-{{name}}.md)** | Kiro IDE configurations | IDE-specific settings |
| **[recipe-power-{{name}}.md](templates/recipe-power-{{name}}.md)** | Power system bundles | Power-specific metadata |
| **[recipe-skill-{{name}}.md](templates/recipe-skill-{{name}}.md)** | Skill documentation | `skill_type`, `bundle_options` |

## Slice Architecture

The system uses HTML comment markers for content extraction:

```markdown
<!-- slice:agent=claudi-claude-code -->
Content to extract and assemble
<!-- /slice -->
```

This enables:
- **Targeted extraction** from source documents
- **Modular composition** of context artifacts
- **Version tracking** through Obsidian frontmatter
- **Deployment automation** via sync scripts

## Processing Flow

### Assembly Phase (assemble.py)
1. **Discovery**: Find recipe files in `.context/workshop/` (excluding templates)
2. **Parsing**: Extract Obsidian frontmatter and YAML configuration blocks
3. **Extraction**: Pull content from slice markers in source files
4. **Templating**: Apply string substitution to templates
5. **Output**: Write assembled artifacts to `output/`
6. **Logging**: Update manifest with assembly results

### Synchronization Phase (sync.py)
1. **Tracking**: Read deployment history from manifest
2. **Deployment**: Copy outputs to target locations with path expansion
3. **Cleanup**: Remove orphaned files from previous deployments
4. **Logging**: Update manifest with sync results

### Error Handling
The Python implementation includes gothic-themed error messages and graceful degradation:
- Missing YAML blocks trigger "HERETEK·PROTOCOL·VIOLATION" warnings
- File access errors report "MACHINE·SPIRIT·CORRUPTION"
- Processing continues with remaining recipes on individual failures

## Integration

This workshop system connects to the broader context ecosystem:

- **[Context Engineering Skills](../skills/README.md)** - Source material for skill bundles
- **[Epistemic Rendering](../prompts/README.md)** - Templates for different cognitive approaches
- **[Exocortex Architecture](../exocortex/README.md)** - Agent configurations and slice sources
- **[Covenant Principles](../principles.md)** - Bespoke design philosophy

The workshop serves as the deployment mechanism for translating vault knowledge into operational context.

## Correctness Properties

Simple validation for disposable software:

1. **Recipe Processing Completeness** - All valid recipes generate output
2. **Slice Extraction Accuracy** - Content matches slice markers exactly  
3. **Template Substitution** - Placeholders replaced correctly
4. **Sync Completeness** - All outputs deployed to targets
5. **Orphan Cleanup** - Removed files cleaned from targets

## Usage Patterns

### Creating New Recipes
1. Use Obsidian template to create recipe from template
2. Configure sources, targets, and template
3. Run `assemble.nu` to generate output
4. Run `sync.nu` to deploy to targets

### Monitoring Deployments
- Check [recipe-manifest.md](recipe-manifest.md) for assembly/sync status
- Review deployment logs for troubleshooting
- Track file changes through Obsidian frontmatter

---

*Simple tools for simple problems. The workshop explains itself through its recipes.*