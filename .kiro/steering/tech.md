# Technology Stack

## Core Technologies

- **Obsidian** - Primary knowledge management platform with Canvas support
- **Python 3** - Workshop assembly and sync scripts
- **Markdown** - Universal documentation format with YAML frontmatter
- **YAML** - Configuration and recipe definitions
- **JSON** - Structured data (MCP configs, Kiro hooks, power metadata)

## Key Libraries

- `pyyaml` - YAML parsing for recipe processing
- `python-frontmatter` - Obsidian frontmatter handling
- `pathlib` - Cross-platform path operations

## File Formats

- **`.md`** - Markdown with YAML frontmatter for all documentation
- **`.canvas`** - Obsidian Canvas files for visual modeling
- **`.kiro.hook`** - JSON configuration for Kiro hooks
- **`mcp.json`** - Model Context Protocol server configuration
- **`power.json`** - Kiro Power metadata

## Workshop System

The workshop uses a two-script pipeline for context assembly and deployment:

### Assembly Script
```bash
# Preview assembly without writing files
python workshop/src/assemble.py --dry-run --verbose

# Generate artifacts in workshop/staging/
python workshop/src/assemble.py
```

### Sync Script
```bash
# Preview deployment without copying files
python workshop/src/sync.py --dry-run --verbose

# Deploy staged artifacts to target locations
python workshop/src/sync.py
```

### Full Workflow
```bash
# Run both assembly and sync
python workshop/src/assemble.py && python workshop/src/sync.py
```

## Path Conventions

- **Context library**: `Z:\Documents\.context` (absolute path in scripts)
- **Workshop**: `.context/workshop/` (recipes, staging, manifest)
- **Staging**: `.context/workshop/staging/` (generated artifacts)
- **Specs**: `.kiro/specs/{feature-name}/` (requirements, design, tasks)
- **Hooks**: `.kiro/hooks/` (canonical hook configurations)
- **Steering**: `.kiro/steering/` (project-specific context)

## Slice Architecture

Content extraction uses HTML comment markers:

```markdown
<!-- slice:agent=kiro -->
Content to extract for Kiro agent
<!-- /slice -->

<!-- slice:skill=covenant-patterns -->
Content to extract for covenant-patterns skill
<!-- /slice -->
```

This enables:
- Targeted extraction from source documents
- Modular composition of context artifacts
- Write once, deploy everywhere pattern

## Output Formats

### Agent Skills Standard (agentskills.io)
```
skill-name/
├── SKILL.md          # YAML frontmatter + markdown body
├── scripts/          # Executable code
├── references/       # Additional docs
└── assets/           # Static resources
```

### Kiro Power Format
```
power-name/
├── POWER.md          # Main documentation with frontmatter
├── mcp.json          # Optional: MCP server config
└── steering/         # Required: all guides as .md
```

## Development Environment

- **Primary OS**: Windows 11
- **Primary Shell**: nushell
- **WSL**: Ubuntu 22.04 (available)
- **Docker**: Available
- **Favorite Font**: Recursive Mono Casual

## Testing

The workshop system includes basic validation:
- Recipe parsing completeness
- Source processing accuracy (slice extraction, file inclusion)
- Structure generation (Agent Skills, Kiro Power formats)
- Frontmatter validation (required fields)
- Sync completeness and orphan cleanup
