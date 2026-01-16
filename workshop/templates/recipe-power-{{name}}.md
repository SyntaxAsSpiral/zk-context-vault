---
id: recipe-{{name}}
created: {{date}}
modified: {{date}}
status: draft
type:
  - "power"
---

```yaml
name: {{name}}
output_format: power  # Creates power folder structure

# Power folder structure:
# power-name/
# ├── POWER.md (from power_md source)
# ├── mcp.json (optional, from mcp_config source)
# └── steering/ (all steering_files go here as .md)

target_locations:
  - path: ~/.kiro/powers/{{name}}/

# Source mapping to power structure
sources:
  power_md:
    - slice: # Slice identifier for main POWER.md content
      slice-file: # Source file path
  
  mcp_config:  # Optional - only if MCP tools included
    - file: # Path to mcp.json or slice containing JSON
  
  steering_files:  # All go to steering/ folder as .md
    - slice: # Slice identifier for guide 1
      slice-file: # Source file
      output_name: getting-started.md
    - slice: # Slice identifier for guide 2
      slice-file: # Source file
      output_name: advanced-usage.md
    # Add more steering files as needed

# Optional metadata
metadata:
  version: "1.0.0"
  author: # Author name
  description: # Brief description
  keywords: []           # Search keywords for power discovery
  category: # Power category (e.g., "development", "productivity")
```