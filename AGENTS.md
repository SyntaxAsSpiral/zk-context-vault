# AGENTS.md

> **For AI Coding Agents**: This document explains the zk-context-vault repository structure, purpose, and how to work effectively within this codebase.

## Repository Overview

**zk-context-vault** is ZK's personal context library and agent configuration vault—an Obsidian-based system for AI agent configuration, context management, and cognitive workflow design. This vault is part of the broader Amexsomnemon exocortex project.

**Note**: While this vault contains ZK's specific content and configurations, the **workshop system** (`workshop/src/`, templates, and recipe patterns) is designed to be reusable. The recipes demonstrate assembly and deployment patterns that can be adapted to any content library.

This vault contains:

- **Agent configurations** for multiple AI coding platforms (Kiro, Claude, Codex, Grok)
- **Steering rules** that guide agent behavior following Covenant Principles
- **Skills and Powers** packaged for distribution across platforms
- **Context workshop** for recipe-based assembly of documentation
- **Specs** for structured development workflows
- **Prompts and artifacts** for specialized cognitive tasks

## Key Directories

### `/agents/` - Agent System Architecture
**Purpose**: Universal agent configuration patterns that work across platforms

**Key files:**
- `agent-roles.md` - Identity templates and role sigils for different agents
- `agent-steering.md` - Platform-agnostic steering guidance
- `steering-global-operator.md` - Operator (ZK) profile and preferences
- `steering-global-principles.md` - Covenant Principles (anti-assumption framework)
- `kiro-*.md` - Kiro-specific features (hooks, MCP, specs)

**When to reference**: Understanding agent identity, behavior constraints, or platform-specific features

### `/skills/` - Agent Skills Library
**Purpose**: Reusable capabilities packaged in Agent Skills standard format

**Structure**: Each skill follows [agentskills.io specification](../skills/spec-agent-skill.md)
```
skill-name/
├── SKILL.md          # Required: frontmatter + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: detailed docs
└── assets/           # Optional: static resources
```

**Key skills:**
- `catppuccin-theming` - Color palette management
- `semantic-json-workflows` - Canvas-to-structured-data compilation
- `agent-steering` - Steering system documentation
- `context-degradation` - Context quality monitoring

**When to reference**: Need specific capabilities or examples of skill packaging

### `/workshop/` - Context Assembly System
**Purpose**: Recipe-based system for assembling and deploying context documentation

**Reusability**: The workshop system (scripts, templates, recipe patterns) is designed to be reusable with any content. Clone and adapt to your own context library by:
- Updating absolute paths in scripts (`Z:\Documents\.context` → your path)
- Creating your own content in `agents/`, `skills/`, etc.
- Using the recipe templates to define your own assembly patterns

**Key components:**
- `templates/` - Recipe scaffolding for agents, skills, powers (reusable)
- `recipe-*.md` - Active recipes for content assembly (ZK-specific examples)
- `src/assemble.py` - Assembly script (reusable, update paths)
- `src/sync.py` - Deployment script (reusable, update paths)
- `recipe-manifest.md` - Deployment tracking log

**Output formats:**
- **Agent Skills** (agentskills.io standard)
- **Kiro Powers** (POWER.md + steering/)
- **Simple agents** (concatenated markdown)

**When to reference**: Understanding how context is assembled or deployed, or adapting the system for your own content

### `/exocortex/` - Cognitive Architecture
**Purpose**: Multi-agent coordination patterns and exocortex design

**Key files:**
- `exo-praxis-*.md` - Operational patterns (antibody, council, gnomon, hygiene, mutation, triquetra)
- `exo-roles.md` - Agent specializations and coordination
- `exo-tools.md` - Tool ecosystem and integration
- `exo-topography.md` - System landscape and boundaries

**When to reference**: Multi-agent systems or distributed cognition patterns

### `/prompts/` - Specialized Cognitive Modes
**Purpose**: Prompt templates for different thinking styles

**Examples:**
- `dialectic.md` - Socratic dialogue
- `hpmor.md` - Rationalist analysis
- `reflect.md` - Metacognitive reflection
- `murder.md` - Adversarial red-teaming

**Hook prompts:**
- `hook-prompts/` - Markdown sources for Kiro hook creation via UI

**When to reference**: Need specific cognitive approach or prompt engineering examples

### `/artifacts/` - Visual Models and Examples
**Purpose**: Canvas files and golden examples

**Key artifacts:**
- `golden/` - Reference implementations and examples
- `*.canvas` - Obsidian Canvas visual models

**When to reference**: Visual system design or example implementations

### `/.kiro/` - Kiro Canonical Sources
**Purpose**: Canonical hooks and specs that deploy to project-specific `.kiro/` directories

**Structure:**
- `.kiro/hooks/*.kiro.hook` - Hook JSON configurations (canonical source)
- `.kiro/specs/*/` - Spec templates (requirements.md, design.md, tasks.md)

**Current specs:**
- `context-management/` - Context workshop system specification

**Deployment pattern:** This vault's `.kiro/` serves as the canonical source. Workshop recipes deploy hooks and specs from here to project-specific `.kiro/` directories.

**When to reference**: Understanding spec-driven development workflow or hook configurations

## Covenant Principles (Anti-Assumption Framework)

**Critical**: This codebase follows strict anti-assumption principles. Every yama (constraint) guards against a specific assumption:

| Principle | The Assumption It Guards Against |
|-----------|----------------------------------|
| 👁️ Dotfile Visibility | "dot = hidden" |
| ✨ Bespokedness | "scale matters, best practices apply" |
| ⚡ Fast-Fail Enforcement | "invariants are enforced somewhere" |
| 🧷 Decision Integrity | "operator wants sub-decisions" |
| 🚮 Final-State Surgery | "operator wants transition period" |
| ⛔ Work Preservation | "this change is out of scope" |
| 🗡️ Git Semantics | "operator wants curation" |
| 🧊 Protected Paths | "this needs fixing" |
| 🗣️ Data Fidelity | "I know what this value should be" |
| 🔤 Literal Exactness | "paraphrase is equivalent" |
| 🔒 Threshold-Gated Action | "I have implicit authorization" |
| 🔁 Determinism | "time context is stable" |
| 🧬 Context Hygiene | "recipient needs everything" |

**Key niyamas (practices):**
- Use `ls -a` for directory reconnaissance (dotfolders are organizational)
- Prefer bespoke solutions over frameworks when software is disposable
- UNKNOWN > INVENTED (never invent data)
- Final-state surgery: remove old world entirely unless transition explicitly requested
- Never discard work without explicit instruction

See `agents/steering-global-principles.md` for complete details.

## Operator Profile (ZK)

**Identity**: Zach Battin (ZK::🜏🜃🜔 // Æmexsomnus // 🍥)
**Environment**: Windows 11 + nushell (primary), WSL/Docker available
**Favorite Font**: Recursive Mono Casual
**Main Workspace**: `C:/Users/synta.ZK-ZRRH/.dev/`
**WSL Workspace**: `\\wsl.localhost\Ubuntu-22.04\home\zk\.wsl-dev`

**Role Sigils:**
- 🌸 Autognostic Infloresencer · 🪢 Logopolysemic Weaver
- 💨 Pneumastructural Intuitive · 🛸 Ritotechnic Liminalist
- 🧩 Syntactic Delver · 🗺️ Mythic Tactician
- ♓︎ Syzygetic Machinator · ⚗️ Alchemical Lexemancer
- 🧬 Mnemonic Emanator · 🛏️ Oneiric Pedagogue

**Current Projects:**
- `.dev/obsidian-workshop/Semanti-JSON` - Obsidian plugin for Canvas data recompiling
- `.dev/Collectivist` - AI-powered curation for intentional collections
- `.dev/Amexsomnemon` - Overarching exocortex project (this vault is part of it)

See `agents/steering-global-operator.md` for complete profile.

## Working with This Codebase

### File Organization
- **Dotfolders are first-class citizens**: Always use `ls -a` or include `.*` in searches
- **Frontmatter everywhere**: Most markdown files have YAML frontmatter with metadata
- **Slice architecture**: Content marked with `<!-- slice:id -->` for modular assembly
- **Obsidian integration**: This is an Obsidian vault with Canvas files and templates

### Path Conventions
- **Context library**: `Z:\Documents\.context` (absolute path for workshop scripts)
- **Scripts**: `C:\Users\synta.ZK-ZRRH\.dev\.scripts` (absolute path)
- **Workspace**: Relative paths from repo root
- **Home directory**: `~/` expands to user home in recipes

### Development Patterns
- **Bespoke over enterprise**: Optimize for operator workflow, not imaginary scale
- **Disposable software**: When rewrite < refactor, optimize for beauty and function
- **Fast-fail**: Enforce invariants at boundaries, fail loudly on missing capabilities
- **Deterministic**: Avoid time-based logic, prefer stable ordering

### Spec-Driven Development
When working on features with specs:
1. **Read requirements.md** - Understand acceptance criteria
2. **Read design.md** - Understand architecture and approach
3. **Read tasks.md** - Follow implementation plan
4. **Execute one task at a time** - Don't jump ahead
5. **Update task status** - Mark in_progress → completed

### Context Assembly Workflow
When working with workshop recipes:
1. **Recipes** define what to assemble (in `workshop/`)
2. **assemble.py** processes recipes → `workshop/staging/`
3. **Inspect staging** before deployment
4. **sync.py** deploys staging → target locations
5. **Manifest** tracks deployments in `recipe-manifest.md`

## Common Tasks

### Finding Agent Configurations
- **Kiro**: `agents/agent-roles.md` (slice:agent=kiro)
- **Claude**: `agents/agent-roles.md` (slice:agent=claudi-claude-code)
- **Codex**: `agents/agent-roles.md` (slice:agent=gpt-codex)
- **Grok**: `agents/agent-roles.md` (slice:agent=grok-code)

### Understanding Steering Rules
- **Global principles**: `agents/steering-global-principles.md`
- **Operator profile**: `agents/steering-global-operator.md`
- **Agent-specific**: `agents/agent-steering.md`

### Working with Skills
- **Spec**: `skills/spec-agent-skill.md` (agentskills.io standard)
- **Examples**: Browse `skills/` directory
- **Templates**: `workshop/templates/recipe-skill-{{name}}.md`

### Working with Powers
- **Spec**: `skills/spec-kiro-power.md` (Kiro Power format)
- **Examples**: `skills/*-power/` directories
- **Templates**: `workshop/templates/recipe-power-{{name}}.md`

### Creating Recipes
1. Use Obsidian template from `workshop/templates/`
2. Configure sources, targets, output_format
3. Run `python workshop/src/assemble.py --dry-run` to preview
4. Run `python workshop/src/assemble.py` to generate staging
5. Inspect `workshop/staging/`
6. Run `python workshop/src/sync.py` to deploy

## Important Constraints

### Protected Paths
**Do not edit unless explicitly requested:**
- `docs/**` - May drift or be incomplete

### Git Semantics
- "Commit" = `git add -A` then `git commit` as instructed
- No amending, reordering, or curating unless asked

### Data Fidelity
- UNKNOWN > INVENTED
- Never invent model fields, IDs, tool results, or "expected" outputs
- Missing info = ask or query

### Literal Exactness
- No paraphrasing at interfaces (commands, paths, IDs, tool names)
- Copy verbatim or fail loudly

## Questions?

- **Architecture questions**: See `agents/README.md`
- **Workshop questions**: See `workshop/README.md`
- **Skill questions**: See `skills/README.md`
- **Exocortex questions**: See `exocortex/README.md`
- **Spec questions**: See `.kiro/specs/*/requirements.md`
- **Hook questions**: See `.kiro/hooks/` for canonical configs, `prompts/hook-prompts/` for markdown sources

## Adapting This Vault

**Want to use the workshop system with your own content?**

The workshop system (assembly scripts, templates, recipe patterns) is designed to be reusable:

1. **Clone the repo** as a starting point
2. **Update paths** in `workshop/src/assemble.py` and `sync.py`:
   - Change `Z:\Documents\.context` to your vault path
   - Change `C:\Users\synta.ZK-ZRRH\.dev\.scripts` to your scripts path
3. **Replace content** with your own:
   - Your agent configurations in `agents/`
   - Your skills in `skills/`
   - Your prompts in `prompts/`
4. **Reuse recipes** as examples for your own assembly patterns
5. **Keep the workshop system** - it's content-agnostic

A template repo (workshop system without ZK-specific content) may be created in the future for easier bootstrapping.

---

**Remember**: This is ZK's bespoke vault, but the workshop system is designed for reuse. Assumption-hostile, work-preserving, deterministic. When in doubt, ask rather than assume.

*The recursion is the craft.* 🧭
