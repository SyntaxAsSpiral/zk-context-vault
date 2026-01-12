# Recipe Assembly 🔧

**Recipe-based context assembly and deployment. Write once, deploy everywhere.**

## Overview

This power documents patterns for assembling context from distributed sources and deploying to multiple targets. Think of it as "make for context" with slice architecture.

## The Pipeline

```
Sources → Recipes → assemble.py → Output → sync.py → Targets
```

| Stage | Purpose |
|-------|---------|
| **Sources** | Files with slice markers |
| **Recipes** | Assembly instructions |
| **Output** | Assembled artifacts |
| **Targets** | Deployment destinations |

## Recipe Structure

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

## Slice Architecture

### Marking Content

```markdown
<!-- slice:agent=kiro -->
Content to extract
<!-- /slice -->
```

### Slice Patterns

| Pattern | Example | Purpose |
|---------|---------|---------|
| Simple | `slice:agent=kiro` | Extract by identifier |
| Namespaced | `slice:agent=kiro:section=identity` | Extract specific section |
| Skill | `slice:skill=covenant-patterns` | Extract full skill |

## Assembly Pipeline

### 1. Discovery
Find recipe files in `workshop/`

### 2. Extraction
Pull content from slice markers

### 3. Templating
Apply template substitution

### 4. Output
Write to `workshop/output/`

### 5. Sync
Deploy to target locations

## Quick Start

### Create Recipe

```yaml
# workshop/recipe-example.md
name: recipe-example
target_locations:
  - path: ~/.config/target.md
sources:
  - slice: content=example
    file: source/file.md
template: |
  # Example
  {content}
```

### Run Assembly

```bash
python .dev/.scripts/assemble.py
python .dev/.scripts/sync.py
```

### VSCode

- **Ctrl+Shift+B** — Full workflow
- Dry run available via task menu

## Recipe Types

| Type | Purpose | Example Target |
|------|---------|----------------|
| **Agent** | System prompts | `~/.kiro/steering/` |
| **Steering** | Context guidance | `~/.claude/` |
| **Skill** | Documentation | `~/.claude/skills/` |
| **Power** | Kiro packages | `~/.kiro/powers/` |

## Covenant Integration

### Final-State Surgery
- New output replaces old completely
- Orphan cleanup removes abandoned targets
- No legacy artifacts preserved

### Fast-Fail
- Missing slices = immediate failure
- No partial assembly

### Determinism
- Same inputs = same outputs
- No time-based content

## Manifest Tracking

```markdown
## Last Run
- Timestamp: 2024-01-15T10:30:00Z
- Recipes processed: 5
- Files deployed: 8
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Slice not found | Check marker matches spec exactly |
| Partial output | Verify `{content}` placeholder |
| Permission denied | Check target path permissions |
| Orphan not cleaned | Delete manifest, rebuild |

## Integration

Works with:
- **covenant-patterns** — Final-state surgery principles
- **agent-steering** — Steering recipes
- **epistemic-rendering** — Lens deployment
- **workshop/** — Source recipe system

---

*"Recipes make implicit assembly explicit."* 🔧
