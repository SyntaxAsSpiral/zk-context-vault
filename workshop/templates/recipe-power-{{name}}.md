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
  - path: ~/.kiro/powers/installed/{{name}}/

# Source mapping to power structure
sources:
  power_md:
    - file: skills/{{name}}/POWER.md
    # Or slice extraction:
    # - slice: power={{name}}
    #   slice-file: skills/{{name}}/POWER.md
  
  mcp_config:  # Optional - only if MCP tools included
    - file: # Path to mcp.json (whole file)
      output_name: mcp.json
  
  steering_files:  # All go to steering/ folder as .md
    - file: skills/{{name}}/getting-started.md
      output_name: getting-started.md
    - file: skills/{{name}}/advanced-usage.md
      output_name: advanced-usage.md
    # Add more steering files as needed

# Optional metadata
# Optional metadata
metadata:
  version: "1.0.0"
  author: # Author name
  license: ""
  keywords: []
  displayName: # Human readable name
  description: # Brief description
  iconUrl: # Optional: URL to icon png
  repositoryUrl: # Optional: library source url
  category: # Power category (e.g., "development", "productivity")
```
