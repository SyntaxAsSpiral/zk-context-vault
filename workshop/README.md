# Context Workshop

*A minimal context management system using recipe-based assembly and deployment of markdown slices/files.*

## What This Is

This is not a complex build system. It's a **context workshop**—a bespoke tool for assembling context documentation from distributed sources using YAML recipes embedded in Obsidian markdown. The system follows the principle of disposable software optimized for operator workflow rather than enterprise scalability.

Think of it as "make for context" with Obsidian integration.

## The Architecture

The workshop operates through a simple two-script pipeline: assembly and synchronization:

```
Context Vault → Workshop Recipes → assemble.py → Workshop Staging → sync.py → Target Locations
```

### Core Components

| Component | Purpose | Location | Authority |
|-----------|---------|----------|-----------|
| **[Templates](templates/)** | Recipe scaffolding | `workshop/templates/` | Obsidian |
| **[Recipes](.)** | Assembly instructions | `workshop/recipe-*.md` | Operator |
| **[Staging](staging/)** | Assembled artifacts | `workshop/staging/` | System |
| **[Manifest](recipe-manifest.md)** | Deployment tracking | `workshop/recipe-manifest.md` | System |

### Script Pipeline

| Script | Function | Location | Responsibility |
|--------|----------|----------|----------------|
| `workshop/src/assemble.py` | Parse recipes, assemble artifacts | `workshop/src/` | Assembly |
| `workshop/src/sync.py` | Deploy artifacts, purge orphans | `workshop/src/` | Synchronization |

### IDE Integration

The system can be wired into IDE tasks (paths in this repo may differ from older `.dev/.scripts` setups):

- **Ctrl+Shift+B** - Run full workflow (assemble + sync)
- **Ctrl+Shift+P** → "Tasks: Run Task" - Individual operations
- **Dry run modes** - Preview operations without file changes
- **Verbose modes** - Detailed output for debugging

## Recipe Structure

Recipes combine Obsidian frontmatter with embedded YAML configuration:

### Simple Agent Recipe (no template)
```yaml
name: Claudi
output_format: agent
target_locations:
  - path: ~/.claude/CLAUDE.md
sources:
  - slice: agent=claudi-claude-code
    slice-file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
```

### Agent Skills Standard Recipe (SKILL.md folder)
```yaml
name: catppuccin-theming
output_format: skill  # Creates Agent Skills standard structure
target_locations:
  - path: ~/.claude/skills/catppuccin-theming/
sources:
  skill_md:
    frontmatter:
      name: catppuccin-theming
      description: Apply Catppuccin color palettes...
    body:
      - file: skills/catppuccin-theming/SKILL.md
  references:
    - file: skills/catppuccin-theming/🩷Catppuccin.md
      output_name: 🩷Catppuccin.md
```

### Kiro Power Recipe
```yaml
name: semantic-json-workflows
output_format: power  # Creates Kiro Power structure
target_locations:
  - path: ~/.kiro/powers/installed/semantic-json-workflows/
sources:
  power_md:
    - file: skills/semantic-json-workflows/POWER.md
  steering_files:
    - file: skills/semantic-json-workflows/getting-started.md
      output_name: getting-started.md
```

### Command / Prompt / Hook Recipe (MD + Kiro hook JSON)
```yaml
name: murder
output_format: command
target_locations:
  - path: ~/.kiro/hooks/murder.kiro.hook
  - path: ~/.claude/commands/murder.md
  - path: ~/.codex/prompts/murder.md
sources:
  kiro_hook:
    - file: prompts/murder.md
  command_md:
    - file: prompts/murder.md
kiro_hook_config:
  enabled: true
  name: "Murder Cogitator"
  description: "Adversarial review persona"
  version: "1"
  when: { type: "userTriggered" }
  then: { type: "askAgent" }
  shortName: "murder"
```

### Source Types

- **`slice` + `slice-file`**: Extract content between `<!-- slice:id -->` markers
- **`file` only**: Include entire file content
- **Source roles**: Group sources by purpose (skill_md, power_md, steering_files, references, assets)

### Multi-Section Recipes (one recipe, multiple outputs)
Inside the YAML code block, separate documents with `---` to emit multiple outputs from one recipe file.

### Recipe Types

The workshop provides specialized templates for different context types:

| Template | Purpose | Output Format |
|----------|---------|---------------|
| **[recipe-agent-{{name}}.md](templates/recipe-agent-{{name}}.md)** | Agent system prompts | Simple concatenation |
| **[recipe-skill-{{name}}.md](templates/recipe-skill-{{name}}.md)** | Agent Skills standard | SKILL.md + scripts/ + references/ + assets/ |
| **[recipe-power-{{name}}.md](templates/recipe-power-{{name}}.md)** | Kiro Power packages | POWER.md + mcp.json + steering/ |
| **[recipe-command-{{name}}.md](templates/recipe-command-{{name}}.md)** | Prompts/commands/hooks | `.md` + optional `.kiro.hook` |
| **[recipe-project-steering-{{name}}.md](templates/recipe-project-steering-{{name}}.md)** | Project AGENTS.md | `.md` (directory targets supported) |
| `recipe-kiro-modular-{{name}}.md` | Future expansion (not wired up) | n/a |
| `exo-praxis-{{cmd}}.md` | Exo/Praxis scratchpad | n/a |

## Output Formats

The workshop supports two standard output formats:

### Agent Skills Standard (agentskills.io)
```
skill-name/
├── SKILL.md          # Required: YAML frontmatter + markdown body
├── scripts/          # Optional: Python, Bash, JS executables
├── references/       # Optional: Additional docs (loaded on demand)
└── assets/           # Optional: Static resources
```

**Frontmatter requirements:**
- `name`: lowercase, numbers, hyphens only (max 64 chars)
- `description`: what skill does and when to use it (max 1024 chars)
- `license`, `compatibility`, `metadata`, `allowed-tools`: optional

### Kiro Power Format
```
power-name/
├── POWER.md          # Required: main documentation with frontmatter
├── mcp.json          # Optional: only if MCP tools included
└── steering/         # Required: all guides as .md (JSON/HTML embedded)
    ├── getting-started.md
    └── advanced-usage.md
```

**Frontmatter requirements:**
- `name`, `displayName`, `description`, `version`, `keywords`: required
- `author`, `category`, `mcpServers`, `steeringFiles`, `dependencies`: optional

## Platform-Specific Conventions

Different AI platforms have different file naming conventions:

### Steering/Agent Configuration Files

| Platform | File Name | Format | Notes |
|----------|-----------|--------|-------|
| **Kiro** | `modular` | Markdown | Standard agent configuration |
| **Claude** | `CLAUDE.md` | Markdown | Claude-specific naming |
| **Codex** | `AGENTS.md` | Markdown | Standard agent configuration |
| **Grok** | `AGENTS.md` | Markdown | Standard agent configuration |

### Skills/Capabilities Files

| Platform | File Name | Format | Notes |
|----------|-----------|--------|-------|
| **Kiro** | `POWER.md` | Kiro Power format | POWER.md + steering/ structure |
| **Claude** | `SKILL.md` | Agent Skills standard | SKILL.md + scripts/ + references/ + assets/ |
| **Codex** | `SKILL.md` | Agent Skills standard | SKILL.md + scripts/ + references/ + assets/ |
| **Grok** | `SKILL.md` | Agent Skills standard | SKILL.md + scripts/ + references/ + assets/ |

### Commands/Prompts Files

| Platform | File Name | Format | Notes |
|----------|-----------|--------|-------|
| **All** | `*.md` | Markdown | Flexible frontmatter, no strict naming |

**Key insight**: 
- **Steering**: Everyone uses `AGENTS.md` except Claude uses `CLAUDE.md` (auto-selected if `target_locations.path` is a directory)
- **Skills**: Everyone uses `SKILL.md` (Agent Skills standard) except Kiro uses `POWER.md` (Kiro Power format)
- **Prompts**: All platforms flexible with `.md` files and frontmatter

This is why the workshop system uses `output_format` and `target_locations` - it can generate the right format for each platform from the same source content.

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
1. **Discovery**: Find recipe files in `.context/workshop/recipe-*.md`
2. **Parsing**: Extract Obsidian frontmatter and 1+ YAML documents (split on `---` inside the YAML block)
4. **Source processing**:
   - `slice` + `slice-file`: Extract content between slice markers
   - `file` only: Include entire file content
   - Source roles: Group by purpose (skill_md, power_md, steering_files, etc.)
5. **Structure generation**: Create folder structures based on `output_format` (agent/skill/power/command)
6. **Output**: Write assembled artifacts to `staging/` with proper folder structure
7. **Logging**: Update manifest with assembly results

### Synchronization Phase (sync.py)
1. **Tracking**: Read deployment history from manifest
2. **Recipe parsing**: Compute expected artifacts + targets from recipes
3. **Deployment**: Copy/mirror staged artifacts to target locations (supports `~/` expansion)
4. **Cleanup**: Remove orphaned targets for removed deployments
5. **Logging**: Update manifest with sync results and cleaned target count

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
- **[Covenant Principles](../agents/steering-global-principles.md)** - Bespoke design philosophy

The workshop serves as the deployment mechanism for translating vault knowledge into operational context.

## Correctness Properties

Simple validation for disposable software:

1. **Recipe Processing Completeness** - All valid recipes generate output
2. **Source Processing Accuracy** - Slice extraction and whole file inclusion work correctly
3. **Structure Generation** - Agent Skills and Kiro Power formats created properly
4. **Frontmatter Validation** - SKILL.md and POWER.md have required fields
5. **Sync Completeness** - All outputs deployed to targets
6. **Orphan Cleanup** - Removed files cleaned from targets

## Specifications

See `.kiro/specs/context-management/` for the current spec + requirements.

## Usage Patterns

### Creating New Recipes
1. Use Obsidian template to create recipe from appropriate template
2. Configure `output_format`, sources, targets, and optional fields
3. Run `python workshop/src/assemble.py` to generate artifacts in `workshop/staging/`
4. Inspect staged content
5. Run `python workshop/src/sync.py` to deploy to target locations

### Dry Run Mode
```bash
python workshop/src/assemble.py --dry-run --verbose  # Preview assembly
python workshop/src/sync.py --dry-run --verbose      # Preview deployment
```

### Monitoring Deployments
- Check [recipe-manifest.md](recipe-manifest.md) for assembly/sync status
- Review deployment logs for troubleshooting
- Track file changes through Obsidian frontmatter

---

*Simple tools for simple problems. The workshop explains itself through its recipes.*
