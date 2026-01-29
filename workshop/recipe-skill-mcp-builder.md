---
id: recipe-mcp-builder
created: 2025-01-22
modified: 2025-01-22
status: active
type:
  - "skill"
---

```yaml
name: mcp-builder
output_format: skill

# Agent Skills standard structure:
# mcp-builder/
# ├── SKILL.md (required - with YAML frontmatter + markdown body)
# ├── scripts/ (optional - executable code)
# │   ├── connections.py
# │   └── evaluation.py
# ├── references/ (optional - additional docs loaded on demand)
# │   ├── evaluation.md
# │   ├── example-evaluation.xml.md
# │   ├── mcp_best_practices.md
# │   ├── node_mcp_server.md
# │   └── python_mcp_server.md
# └── assets/ (optional - static resources)
#     ├── LICENSE.txt
#     ├── mcp.json
#     └── requirements.txt

target_locations:
  - path: ~/.claude/skills/mcp-builder/
  - path: ~/.codex/skills/mcp-builder/
  - path: deck@amexsomnemon:~/.claude/skills/mcp-builder/
  - path: deck@amexsomnemon:~/.codex/skills/mcp-builder/
  - path: ~/.gemini/antigravity/skills/mcp-builder/
  - path: ~/.gemini/skills/mcp-builder/

# Source mapping to skill structure
sources:
  skill_md:
    # SKILL.md with required frontmatter
    frontmatter:
      name: mcp-builder
      description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
      license: Complete terms in LICENSE.txt
      compatibility: Requires Python 3.8+ for Python servers, Node.js 18+ for TypeScript servers. MCP Inspector for testing.
      metadata:
        version: "1.0.0"
        author: "ZK"
        frameworks: "FastMCP (Python), MCP SDK (TypeScript)"
    
    body:
      - file: skills/mcp-builder/SKILL.md
  
  scripts:
    - file: skills/mcp-builder/connections.py.md
      output_name: connections.py
    - file: skills/mcp-builder/evaluation.py.md
      output_name: evaluation.py
  
  references:
    - file: skills/mcp-builder/evaluation.md
      output_name: evaluation.md
    - file: skills/mcp-builder/example-evaluation.xml.md
      output_name: example-evaluation.xml.md
    - file: skills/mcp-builder/mcp_best_practices.md
      output_name: mcp_best_practices.md
    - file: skills/mcp-builder/node_mcp_server.md
      output_name: node_mcp_server.md
    - file: skills/mcp-builder/python_mcp_server.md
      output_name: python_mcp_server.md
  
  assets:
    - file: skills/mcp-builder/LICENSE.txt
      output_name: LICENSE.txt
    - file: skills/mcp-builder/requirements.txt
      output_name: requirements.txt

# Validation
validate_agentskills_spec: true
```
