---
id: recipe-catppuccin-theming
created: 2026-01-15
modified: 2026-01-15
status: active
type:
  - "skill"
---

```yaml
name: catppuccin-theming
output_format: skill  # Creates Agent Skills standard structure

# Agent Skills standard structure:
# catppuccin-theming/
# ├── SKILL.md (required - with YAML frontmatter + markdown body)
# ├── references/ (optional - additional docs loaded on demand)
# │   └── 🩷Catppuccin.md
# └── assets/ (optional - static resources)
#     └── palette-mutator.md

target_locations:
  - path: ~/.claude/skills/catppuccin-theming/
  - path: ~/.codex/skills/catppuccin-theming/
  - path: deck@amexsomnemon:~/.claude/skills/catppuccin-theming/
  - path: deck@amexsomnemon:~/.codex/skills/catppuccin-theming/

# Source mapping to skill structure
sources:
  skill_md:
    # SKILL.md with required frontmatter
    frontmatter:
      name: catppuccin-theming
      description: Apply Catppuccin color palettes to configs, stylesheets, and terminal themes. This skill should be used when creating or modifying CSS themes, terminal color schemes, shell prompts (Starship, etc.), or any configuration that requires consistent Catppuccin colors. Covers all four official flavors (Latte, Frappe, Macchiato, Mocha) plus ZK's custom variants (rose, sage, grape, honey, blueberry).
      license: MIT
      compatibility: Requires Python catppuccin package for programmatic access
      metadata:
        author: zk
        version: "1.0"
        category: theming
    
    body:  # Markdown instructions for agents
      - file: skills/catppuccin-theming/SKILL.md
  
  references:  # Optional - go to references/ folder (loaded on demand)
    - file: skills/catppuccin-theming/🩷Catppuccin.md
      output_name: 🩷Catppuccin.md
  
  assets:  # Optional - go to assets/ folder
    - file: skills/catppuccin-theming/palette-mutator.md
      output_name: palette-mutator.md

# Validation
validate_agentskills_spec: true  # Ensure compliance with agentskills.io standard
```
