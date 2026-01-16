---
name: "catppuccin-theming"
displayName: "🩷Catppuccin Theming"
description: "The Catppuccin Theming Power provides comprehensive color palette management for the beloved Catppuccin aesthetic. Generate CSS variables, terminal themes, configuration files, and custom color schemes using both official Catppuccin flavors and ZK's bespoke variants."
keywords: ["css", "ui", "color", "catppuccin", "theme", "style"]
---

# Catppuccin Theming Power 🎨

**Apply beautiful Catppuccin color palettes consistently across your entire development workflow**

## Overview

The Catppuccin Theming Power provides comprehensive color palette management for the beloved Catppuccin aesthetic. Generate CSS variables, terminal themes, configuration files, and custom color schemes using both official Catppuccin flavors and ZK's bespoke variants.

## Features

### 🌈 Complete Palette Access
- **Official Flavors**: Latte, Frappé, Macchiato, Mocha
- **ZK Custom Variants**: Rose, Sage, Grape, Honey, Blueberry, MochaFrappé
- **Programmatic Access**: Python catppuccin package integration
- **16-Color Terminal**: Standard ANSI color mapping

### 🎯 Format Generation
- **CSS Variables**: Custom properties for web projects
- **JSON Configs**: Terminal emulators, applications
- **TOML/YAML**: Configuration files (Starship, etc.)
- **Code Constants**: Language-specific color definitions

### 🛠️ Development Integration
- **Theme Generation**: Automated color scheme creation
- **Consistency Checking**: Validate color usage across projects
- **Semantic Mapping**: UI element to color recommendations
- **Live Preview**: See colors in context

## Quick Start

### Generate CSS Variables
```bash
# Using Python package
python -c "
from catppuccin import PALETTE
mocha = PALETTE.mocha
print(':root {')
for color in mocha.colors:
    css_name = color.name.lower().replace(' ', '-')
    print(f'  --ctp-{css_name}: {color.hex};')
print('}')
"
```

### Create Terminal Theme
```bash
# Generate 16-color JSON for terminal
python -c "
import json
from catppuccin import PALETTE
mocha = PALETTE.mocha
# ... (see SKILL.md for full example)
"
```

### Apply to Starship Prompt
```toml
[directory]
style = "bold #89b4fa"  # Catppuccin blue

[git_branch] 
style = "bold #a6e3a1"  # Catppuccin green

[character]
success_symbol = "[>](#cba6f7)"  # Catppuccin mauve
```

## ZK Aesthetic Integration

This power includes ZK's custom Catppuccin variants designed for specific moods and contexts:

- **MochaFrappé**: ZK's signature blend (`#f38ba8 #fab387 #f9e2af #a6e3a1 #74c7ec #b4befe #cba6f7`)
- **Rose**: Soft pink palette for gentle interfaces
- **Sage**: Earthy green tones for natural themes  
- **Grape**: Rich purples for luxurious aesthetics
- **Honey**: Warm amber for cozy environments
- **Blueberry**: Cool blues for focused work

## Semantic Color Guidelines

| UI Element | Recommended Colors |
|------------|-------------------|
| Primary Actions | `blue`, `sapphire` |
| Success States | `green`, `teal` |
| Warnings | `yellow`, `peach` |
| Errors | `red`, `maroon` |
| Links | `blue`, `mauve` |
| Code/Syntax | `pink`, `flamingo` |
| Headings | `lavender`, `mauve` |

## Advanced Usage

### Custom Palette Creation
Blend official flavors or create entirely new variants following Catppuccin's design principles.

### Batch Theme Generation  
Apply consistent theming across multiple applications and configuration files.

### Color Accessibility
Ensure proper contrast ratios while maintaining the Catppuccin aesthetic.

## Resources

- **Palette Reference**: Complete color tables and hex values
- **Example Configs**: Real-world usage in Starship, CSS, terminals
- **ZK Variants**: Custom palettes in Semantic JSON format
- **Python Integration**: Programmatic palette access and generation

Transform your entire development environment into a cohesive, beautiful Catppuccin experience! 🌸