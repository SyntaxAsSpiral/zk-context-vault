---
id: recipe-mcp-builder
created: 2025-01-22
modified: 2025-01-22
status: active
type:
  - "power"
---

```yaml
name: mcp-builder
output_format: power

# Power folder structure:
# mcp-builder/
# ├── POWER.md
# ├── mcp.json
# └── steering/
#     ├── connections.py.md
#     ├── evaluation.md
#     ├── evaluation.py.md
#     ├── example-evaluation.xml.md
#     ├── mcp_best_practices.md
#     ├── node_mcp_server.md
#     └── python_mcp_server.md

target_locations:
  - path: ~/.kiro/powers/installed/mcp-builder/

# Source mapping to power structure
sources:
  power_md:
    - file: skills/mcp-builder/POWER.md
  
  mcp_config:
    - file: skills/mcp-builder/mcp.json
      output_name: mcp.json
  
  steering_files:
    - file: skills/mcp-builder/connections.py.md
      output_name: connections.py.md
    - file: skills/mcp-builder/evaluation.md
      output_name: evaluation.md
    - file: skills/mcp-builder/evaluation.py.md
      output_name: evaluation.py.md
    - file: skills/mcp-builder/example-evaluation.xml.md
      output_name: example-evaluation.xml.md
    - file: skills/mcp-builder/mcp_best_practices.md
      output_name: mcp_best_practices.md
    - file: skills/mcp-builder/node_mcp_server.md
      output_name: node_mcp_server.md
    - file: skills/mcp-builder/python_mcp_server.md
      output_name: python_mcp_server.md
  
  # Note: LICENSE.txt and requirements.txt are included in the skill format
  # but omitted from power format since steering/ only accepts .md files

# Optional metadata
metadata:
  version: "1.0.0"
  author: "muratcankoylan"
  license: MIT
  displayName: "MCP Server Builder"
  description: "Build high-quality MCP servers with comprehensive API coverage, clear tool design, and evaluation frameworks"
  keywords:
    - mcp
    - model-context-protocol
    - server
    - tools
    - api-integration
    - fastmcp
    - typescript
    - python
    - evaluation
  iconUrl: https://prod.download.desktop.kiro.dev/powers/icons/mcp.png
  repositoryUrl: https://github.com/model-context-protocol/servers
  category: "development"
```
