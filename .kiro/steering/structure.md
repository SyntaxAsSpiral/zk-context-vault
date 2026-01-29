---
inclusion: manual
---


# Project Structure

## Directory Organization

### `/agents/` - Agent System Architecture
Universal agent configuration patterns that work across platforms (Kiro, Claude Code, Codex, Charm).

**Key files:**
- `agent-roles.md` - Identity templates and role sigils (slice-based)
- `steering-global-operator.md` - Operator (ZK) profile and preferences
- `steering-global-principles.md` - Covenant Principles (anti-assumption framework)
- `steering-global-mesh.md` - Tailnet device topology and SSH configuration
- `steering-project-*.md` - Project-specific steering (e.g., zk-context-vault, deck)

### `/skills/` - Agent Skills Library
Reusable capabilities packaged in Agent Skills standard format. Each skill follows agentskills.io specification.

**Structure per skill:**
```
skill-name/
├── SKILL.md          # Required: frontmatter + instructions
├── POWER.md          # Optional: Kiro Power documentation
├── power.json        # Optional: Kiro Power metadata
├── scripts/          # Optional: executable code
├── references/       # Optional: detailed docs
└── assets/           # Optional: static resources
```

**Active skills:**
- `covenant-patterns/` - Thirteen principles as design constraints
- `agent-steering/` - Universal agent configuration
- `multi-agent-coordination/` - Pentadyadic and multi-agent patterns
- `epistemic-rendering/` - Eight cognitive lenses
- `recipe-assembly/` - Slice architecture and deployment
- `semantic-json-workflows/` - Canvas-to-structured-data anticompiler
- `catppuccin-theming/` - Color palette management
- `context-degradation/` - Context quality monitoring
- `mcp-builder/` - Model Context Protocol server creation

**Archived skills:** `skills/archive/` contains theoretical content for reference.

### `/workshop/` - Context Assembly System
Recipe-based system for assembling and deploying context documentation.

**Key components:**
- `templates/` - Recipe scaffolding (reusable)
- `recipe-*.md` - Active recipes for content assembly
- `src/assemble.py` - Assembly script (generates staging/)
- `src/sync.py` - Deployment script (staging/ → targets)
- `staging/` - Generated artifacts (gitignored except README)
- `recipe-manifest.md` - Deployment tracking log

**Output structure:**
```
staging/
├── agent/          # Simple concatenated markdown
├── skill/          # Agent Skills standard structure
├── power/          # Kiro Power structure
└── command/        # Prompts/hooks (md + optional .kiro.hook)
```

### `/exocortex/` - Cognitive Architecture
Multi-agent coordination patterns and exocortex design.

**Key files:**
- `exo-praxis-*.md` - Operational patterns (antibody, council, gnomon, hygiene, mutation, triquetra)
- `exo-roles.md` - Agent specializations and coordination
- `exo-tools.md` - Tool ecosystem and integration
- `exo-topography.md` - System landscape and boundaries
- `exo-config.md` - System configuration
- `exo-snapshot.md` - State preservation

### `/prompts/` - Specialized Cognitive Modes
Prompt templates for different thinking styles.

**Examples:**
- `dialectic.md` - Socratic dialogue
- `hpmor.md` - Rationalist analysis
- `reflect.md` - Metacognitive reflection
- `murder.md` - Adversarial red-teaming
- `hook-prompts/` - Markdown sources for Kiro hook creation

### `/artifacts/` - Visual Models and Examples
Canvas files and golden examples.

**Key artifacts:**
- `golden/` - Reference implementations and examples
- `*.canvas` - Obsidian Canvas visual models

### `/.kiro/` - Kiro Canonical Sources
Canonical hooks and specs that deploy to project-specific `.kiro/` directories.

**Structure:**
- `.kiro/hooks/*.kiro.hook` - Hook JSON configurations (canonical source)
- `.kiro/specs/*/` - Spec templates (requirements.md, design.md, tasks.md)
- `.kiro/steering/` - Project-specific steering rules

**Archived specs:**
- `.archive/context-management/` - Context workshop system specification (archived)

**Deployment pattern:** This vault's `.kiro/` serves as the canonical source. Workshop recipes deploy hooks and specs from here to project-specific `.kiro/` directories.

### `/.obsidian/` - Obsidian Configuration
Obsidian workspace configuration (mostly gitignored).

**Tracked files:**
- `plugins/` - Community plugins (Semantic-JSON, Style Settings, BRAT)
- `themes/Catppuccin/` - Catppuccin theme
- Core configuration files (app.json, appearance.json, etc.)

**Gitignored:**
- `workspace.json` - Personal workspace state
- `workspace-mobile.json` - Mobile workspace state

### `/.collectivist/` - Repository Indexing
AI-powered curation system for intentional collections (gitignored - contains personal data).

### `/dashboards/` - Task Dashboards
Task tracking and dashboard views.

## File Naming Conventions

### Markdown Files
- **Lowercase with hyphens**: `agent-roles.md`, `steering-global-principles.md`
- **Frontmatter required**: All markdown files have YAML frontmatter with metadata
- **Slice markers**: Use `<!-- slice:type=identifier -->` for modular extraction

### Recipe Files
- **Pattern**: `recipe-{type}-{name}.md` (e.g., `recipe-agent-kiro.md`)
- **Types**: agent, skill, power, command, project-steering, kiro-modular
- **Location**: `workshop/` directory only

### Spec Files
- **Pattern**: `.kiro/specs/{feature-name}/`
- **Required files**: `requirements.md`, `design.md`, `tasks.md`
- **Feature name format**: kebab-case (e.g., "user-authentication")

### Hook Files
- **Pattern**: `{name}.kiro.hook` (JSON format)
- **Location**: `.kiro/hooks/` (canonical) or project-specific `.kiro/hooks/`

## Important Constraints

### Protected Paths
**Do not edit unless explicitly requested:**
- `docs/**` - May drift or be incomplete

### Dotfolders Are First-Class Citizens
- Always use `ls -a` or include `.*` in searches
- Dotfolders are organizational, not hidden
- `.kiro/`, `.obsidian/`, `.collectivist/` are primary structural elements

### Git Semantics
- "Commit" = `git add -A` then `git commit` as instructed
- No amending, reordering, or curating unless asked
- Never discard work without explicit instruction

## Cross-References

- **Architecture overview**: See `README.md`
- **Workshop details**: See `workshop/README.md`
- **Skills catalog**: See `skills/README.md`
- **Agent patterns**: See `agents/README.md`
- **Exocortex design**: See `exocortex/README.md`
- **AI agent guidance**: See `AGENTS.md`
