# Getting Started with Catppuccin Theming

Welcome to the Catppuccin Theming Power! This guide will help you start applying beautiful, consistent color palettes across your development environment.

## Prerequisites

1. **Install Python catppuccin package**:
   ```bash
   pip install catppuccin
   ```

2. **Verify installation**:
   ```bash
   python -c "from catppuccin import PALETTE; print('Catppuccin ready!')"
   ```

## Your First Theme

### 1. Generate CSS Variables

Create a complete CSS variable set for web projects:

```bash
python -c "
from catppuccin import PALETTE
mocha = PALETTE.mocha
print(':root {')
for color in mocha.colors:
    css_name = color.name.lower().replace(' ', '-')
    print(f'  --ctp-{css_name}: {color.hex};')
print('}')
" > catppuccin-mocha.css
```

### 2. Apply to Your Website

```css
body {
    background-color: var(--ctp-base);
    color: var(--ctp-text);
}

.button-primary {
    background-color: var(--ctp-blue);
    color: var(--ctp-base);
}

.button-success {
    background-color: var(--ctp-green);
    color: var(--ctp-base);
}

.button-danger {
    background-color: var(--ctp-red);
    color: var(--ctp-base);
}
```

### 3. Theme Your Terminal

Generate a 16-color terminal theme:

```bash
python -c "
import json
from catppuccin import PALETTE

mocha = PALETTE.mocha
terminal_theme = {
    'name': 'catppuccin-mocha',
    'color': [
        mocha.colors.base.hex,      # 0: black
        mocha.colors.red.hex,       # 1: red  
        mocha.colors.green.hex,     # 2: green
        mocha.colors.yellow.hex,    # 3: yellow
        mocha.colors.blue.hex,      # 4: blue
        mocha.colors.pink.hex,      # 5: magenta
        mocha.colors.teal.hex,      # 6: cyan
        mocha.colors.text.hex,      # 7: white
        mocha.colors.surface1.hex,  # 8: bright black
        mocha.colors.red.hex,       # 9: bright red
        mocha.colors.green.hex,     # 10: bright green  
        mocha.colors.yellow.hex,    # 11: bright yellow
        mocha.colors.sapphire.hex,  # 12: bright blue
        mocha.colors.pink.hex,      # 13: bright magenta
        mocha.colors.sky.hex,       # 14: bright cyan
        mocha.colors.subtext1.hex   # 15: bright white
    ],
    'foreground': mocha.colors.text.hex,
    'background': mocha.colors.base.hex
}

print(json.dumps(terminal_theme, indent=2))
" > terminal-catppuccin-mocha.json
```

### 4. Style Your Shell Prompt

Add Catppuccin colors to your Starship prompt:

```toml
# ~/.config/starship.toml
format = \"\"\"$directory$git_branch$git_status$character\"\"\"

[directory]
format = "[$path]($style) "
style = "bold #89b4fa"  # Catppuccin blue

[git_branch]
format = "[$symbol$branch]($style) "
symbol = " "
style = "bold #a6e3a1"  # Catppuccin green

[git_status]
format = "[$all_status$ahead_behind]($style) "
style = "bold #f38ba8"  # Catppuccin red

[character]
success_symbol = "[>](#cba6f7)"  # Catppuccin mauve
error_symbol = "[>](#f38ba8)"    # Catppuccin red
```

## ZK Custom Variants

Access ZK's bespoke Catppuccin variants from the included palette collection:

- **MochaFrappé**: ZK's signature blend
- **Rose**: Soft pink aesthetic  
- **Sage**: Earthy green tones
- **Grape**: Rich purple luxury
- **Honey**: Warm amber comfort
- **Blueberry**: Cool blue focus

These are available in the `references/🩷Catppuccin.pure.json` file.

## Next Steps

- **Advanced Theming**: Learn to create custom variants and blend palettes
- **Application Integration**: Theme VS Code, Discord, browsers, and more
- **Consistency Checking**: Validate color usage across projects
- **Accessibility**: Ensure proper contrast while maintaining aesthetics

Ready to make your entire development environment beautifully cohesive! 🎨