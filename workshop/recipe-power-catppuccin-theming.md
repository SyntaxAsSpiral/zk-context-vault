---
id: recipe-power-catppuccin-theming
created: 2026-01-16
modified: 2026-01-16
status: active
type:
  - "power"
---

```yaml
name: catppuccin-theming
output_format: power  # Creates power folder structure

# Power folder structure:
# power-name/
# ├── POWER.md (from power_md source)
# ├── mcp.json (optional, from mcp_config source)
# └── steering/ (all steering_files go here as .md)

target_locations:
  - path: ~/.kiro/powers/installed/catppuccin-theming/

# Source mapping to power structure
sources:
  power_md:
    - file: skills/catppuccin-theming/POWER.md
  
  steering_files:  # All go to steering/ folder as .md
    - file: skills/catppuccin-theming/getting-started.md
      output_name: getting-started.md
    - file: skills/catppuccin-theming/advanced-theming.md
      output_name: advanced-theming.md
    - file: skills/catppuccin-theming/🩷Catppuccin.md
      output_name: 🩷Catppuccin.md
    - file: skills/catppuccin-theming/palette-mutator.md
      output_name: palette-mutator.md
# Optional metadata
metadata:
  version: "1.0.0"
  author: zk::chromasorix
  license: MIT
  displayName: 🩷Catppuccin Theming
  description: The Catppuccin Theming Power provides comprehensive color palette management for the beloved Catppuccin aesthetic. Generate CSS variables, terminal themes, configuration files, and custom color schemes.
  keywords: ["css", "ui", "color", "catppuccin", "theme", "style"]
  iconUrl: https://cdn.jsdelivr.net/gh/SyntaxAsSpiral/esotericons@main/cottagecore.png
  repositoryUrl: https://github.com/catppuccin/catppuccin
  category: theming
```
