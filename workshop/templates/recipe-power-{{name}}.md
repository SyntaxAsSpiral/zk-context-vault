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
target_locations:
  - path: # Target directory for power package (e.g., ~/.kiro/powers/{{name}}/)
sources:
  - slice: # Slice identifier for power documentation
    file: # Source file path (e.g., .context/powers/{{name}}/POWER.md)
  - slice: # Slice identifier for power configuration
    file: # Source file path (e.g., .context/powers/{{name}}/config.json)
  # Add more sources as needed
template: |
  # {{name}} Power Package
  {content}
# Power-specific fields
power_structure:
  power_md: true         # Include POWER.md documentation
  config_json: true      # Include JSON configuration
  mcp_servers: []        # List of included MCP servers
  steering_files: []     # List of included steering files
  hooks: []              # List of included hooks
  spec_templates: []     # List of included spec templates
metadata:
  version: "1.0.0"
  author: # Author name
  description: # Brief description
  keywords: []           # Search keywords for power discovery
  category: # Power category (e.g., "development", "productivity")
dependencies:
  required: []           # Required dependencies
  optional: []           # Optional dependencies
validation:
  check_completeness: true    # Validate power structure
  check_dependencies: true    # Validate dependencies exist
```