---
id: recipe-{{name}}
created: {{date}}
modified: {{date}}
status: draft
type:
  - "kiro"
---

```yaml
name: {{name}}
target_locations:
  - path: # Target file path for Kiro output (e.g., ~/.kiro/config/{{name}}.md)
sources:
  - slice: # Slice identifier for Kiro-specific content
    file: # Source file path
  # Add more sources as needed
template: |
  # {{name}} Kiro Configuration
  {content}
# Kiro-specific fields
kiro_type: # power | skill | agent | config
integration_points:
  - mcp_servers: []      # List of MCP server integrations
  - steering_files: []   # List of steering file references
  - hooks: []            # List of hook configurations
metadata:
  version: "1.0.0"
  author: # Author name
  description: # Brief description
  keywords: []           # Search keywords
dependencies: []         # List of dependencies
```