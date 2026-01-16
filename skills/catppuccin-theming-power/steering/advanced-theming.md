# Advanced Catppuccin Theming

Master advanced techniques for creating cohesive, beautiful color schemes across your entire development ecosystem.

## Custom Palette Creation

### Interactive Palette Mutator

For visual palette exploration, use `assets/palette-mutator.html` - an interactive tool for:
- Hue shifting, saturation, lightness, and contrast adjustments
- Live preview of mutations across the 16-color grid
- Export to CSS variables, JSON, or Terminal theme formats
- Loading custom palette JSONs via file input

### Blending Official Flavors

Create hybrid palettes by mixing colors from different Catppuccin flavors:

```python
from catppuccin import PALETTE

# Create a custom blend
mocha = PALETTE.mocha
frappe = PALETTE.frappe

custom_blend = {
    'name': 'mocha-frappe-blend',
    'colors': {
        # Use Mocha accents with Frappé backgrounds
        'red': mocha.colors.red.hex,
        'green': mocha.colors.green.hex,
        'blue': mocha.colors.blue.hex,
        'background': frappe.colors.base.hex,
        'surface': frappe.colors.surface0.hex,
        'text': mocha.colors.text.hex
    }
}
```

### ZK Variant Analysis

Study ZK's custom variants to understand palette design principles:

```python
# Analyze color relationships in ZK variants
import json

with open('references/🩷Catppuccin.pure.json') as f:
    zk_palettes = json.load(f)

# Extract palette data from Canvas nodes
for node in zk_palettes['nodes']:
    if node.get('type') == 'palette':
        # Parse JSON from text content
        # Analyze color harmony, contrast ratios
        pass
```

## Application-Specific Theming

### VS Code Theme Generation

Create complete VS Code color themes:

```python
def generate_vscode_theme(palette_name, colors):
    theme = {
        "name": f"Catppuccin {palette_name}",
        "type": "dark",
        "colors": {
            "editor.background": colors['base'],
            "editor.foreground": colors['text'],
            "activityBar.background": colors['mantle'],
            "statusBar.background": colors['crust'],
            "sideBar.background": colors['surface0'],
            # ... complete theme definition
        },
        "tokenColors": [
            {
                "scope": ["comment"],
                "settings": {
                    "foreground": colors['overlay1'],
                    "fontStyle": "italic"
                }
            },
            {
                "scope": ["keyword"],
                "settings": {
                    "foreground": colors['mauve']
                }
            }
            # ... syntax highlighting rules
        ]
    }
    return theme
```

### Browser Extension Themes

Generate CSS for browser extension theming:

```python
def generate_browser_css(colors):
    return f"""
/* Catppuccin Browser Theme */
:root {{
    --bg-primary: {colors['base']};
    --bg-secondary: {colors['surface0']};
    --text-primary: {colors['text']};
    --text-secondary: {colors['subtext1']};
    --accent-primary: {colors['blue']};
    --accent-success: {colors['green']};
    --accent-warning: {colors['yellow']};
    --accent-danger: {colors['red']};
}}

/* Apply to common elements */
body {{ background: var(--bg-primary); color: var(--text-primary); }}
.button {{ background: var(--accent-primary); }}
.success {{ background: var(--accent-success); }}
.warning {{ background: var(--accent-warning); }}
.danger {{ background: var(--accent-danger); }}
"""
```

## Consistency Management

### Color Usage Validation

Ensure consistent color usage across projects:

```python
def validate_color_usage(css_file, allowed_palette):
    """Check if CSS file only uses approved Catppuccin colors"""
    import re
    
    with open(css_file) as f:
        content = f.read()
    
    # Extract hex colors
    hex_colors = re.findall(r'#[0-9a-fA-F]{6}', content)
    
    # Check against allowed palette
    violations = []
    for color in hex_colors:
        if color.lower() not in [c.lower() for c in allowed_palette.values()]:
            violations.append(color)
    
    return violations
```

### Automated Theme Updates

Create scripts to update themes across multiple applications:

```bash
#!/bin/bash
# update-catppuccin-themes.sh

# Generate fresh palettes
python generate_css_vars.py > ~/.config/themes/catppuccin.css
python generate_terminal_theme.py > ~/.config/alacritty/catppuccin.yml
python generate_starship_config.py >> ~/.config/starship.toml

# Reload applications
pkill -USR1 alacritty  # Reload Alacritty
# ... other reload commands
```

## Accessibility Considerations

### Contrast Ratio Checking

Ensure WCAG compliance while maintaining Catppuccin aesthetics:

```python
def check_contrast_ratio(fg_hex, bg_hex):
    """Calculate WCAG contrast ratio between two colors"""
    def luminance(hex_color):
        # Convert hex to RGB, then calculate relative luminance
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        rgb_norm = [c/255.0 for c in rgb]
        rgb_linear = [c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4 for c in rgb_norm]
        return 0.2126*rgb_linear[0] + 0.7152*rgb_linear[1] + 0.0722*rgb_linear[2]
    
    l1 = luminance(fg_hex)
    l2 = luminance(bg_hex)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

# Test Catppuccin combinations
mocha = PALETTE.mocha
ratio = check_contrast_ratio(mocha.colors.text.hex, mocha.colors.base.hex)
print(f"Text on base contrast: {ratio:.2f} ({'PASS' if ratio >= 4.5 else 'FAIL'})")
```

### Alternative Color Suggestions

Provide accessible alternatives when needed:

```python
def suggest_accessible_alternative(fg_color, bg_color, target_ratio=4.5):
    """Suggest color adjustments to meet contrast requirements"""
    current_ratio = check_contrast_ratio(fg_color, bg_color)
    
    if current_ratio >= target_ratio:
        return fg_color  # Already accessible
    
    # Suggest lighter/darker alternatives from palette
    # Implementation would test other Catppuccin colors
    pass
```

## Integration Patterns

### Configuration File Templates

Create reusable templates for common applications:

```python
# Template system for generating configs
templates = {
    'starship': """
[directory]
style = "bold {blue}"
[git_branch] 
style = "bold {green}"
[character]
success_symbol = "[>]({mauve})"
""",
    
    'tmux': """
set -g status-bg '{base}'
set -g status-fg '{text}'
set -g window-status-current-bg '{blue}'
""",
    
    'vim': """
hi Normal guifg={text} guibg={base}
hi Comment guifg={overlay1}
hi Keyword guifg={mauve}
"""
}

def generate_config(template_name, colors):
    return templates[template_name].format(**colors)
```

## Performance Optimization

### Lazy Loading Palettes

For applications with many themes, implement lazy loading:

```python
class CatppuccinPalettes:
    def __init__(self):
        self._palettes = {}
    
    def get_palette(self, name):
        if name not in self._palettes:
            self._palettes[name] = self._load_palette(name)
        return self._palettes[name]
    
    def _load_palette(self, name):
        # Load palette data on demand
        pass
```

### Caching Generated Themes

Cache expensive theme generation operations:

```python
import hashlib
import pickle
import os

def cached_theme_generation(palette_data, theme_type):
    # Create cache key from palette data
    cache_key = hashlib.md5(str(palette_data).encode()).hexdigest()
    cache_file = f".theme_cache/{theme_type}_{cache_key}.pkl"
    
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    
    # Generate theme if not cached
    theme = generate_theme(palette_data, theme_type)
    
    # Cache result
    os.makedirs(".theme_cache", exist_ok=True)
    with open(cache_file, 'wb') as f:
        pickle.dump(theme, f)
    
    return theme
```

Master these advanced techniques to create a truly cohesive, beautiful, and accessible Catppuccin-themed development environment! 🎨✨