---
id: recipe-sideriod
created: 2026-05-01
modified: 2026-05-01
status: active
type:
  - "skill"
---

```yaml
name: sideriod
output_format: skill  # Creates Agent Skills standard structure

# Agent Skills standard structure:
# sideriod/
# ├── SKILL.md (required - with YAML frontmatter + markdown body)
# ├── mcp/ (MCP server — deploy to ~/sideriod/mcp/ on host running the daemon)
# │   ├── server.py
# │   └── pyproject.toml
# └── README.md (asset)

target_locations:
  - path: ~/.claude/skills/sideriod/
  - path: ~/.codex/skills/sideriod/
  - path: ~/.pi/agent/skills/sideriod/
  - path: zk@adeck:~/.claude/skills/sideriod/
  - path: zk@adeck:~/.codex/skills/sideriod/
  - path: zk@adeck:~/.hermes/skills/user/sideriod/
  - path: ~/.gemini/antigravity/skills/sideriod/
  - path: ~/.gemini/skills/sideriod/

# Source mapping to skill structure
sources:
  skill_md:
    frontmatter:
      name: sideriod
      description: Use when the user asks for astrology readings, celestial timing, planetary hours, tattwa cycles, moon sign, biorhythms, or symbolic timing weather. Requires sideriod installed locally — if not present, run the setup guide.
      license: MIT
      compatibility: Requires Python 3.10+ and Nix. Sideriod uses kerykeion, flatlib, and pyswisseph for full-precision ephemeris. MCP server (mcp/server.py) connects via HTTP to the running daemon on adeck:8765.
      metadata:
        author: zk
        version: "0.1.0"
        category: chronographic-oracle
        mcp_transport: streamable-http
        mcp_default_port: "8765"

    body:
      - file: skills/sideriod/SKILL.md

  scripts:
    - file: skills/sideriod/mcp/server.py
      output_name: mcp/server.py

  assets:
    - file: skills/sideriod/README.md
      output_name: README.md
    - file: skills/sideriod/mcp/pyproject.toml
      output_name: mcp/pyproject.toml

# Validation
validate_agentskills_spec: true
```
