---
id: recipe-factorio-modding
created: 2026-06-26
modified: 2026-06-26
status: active
type:
  - "skill"
---

```yaml
name: factorio-modding
output_format: skill

target_locations:
  - path: ~/.claude/skills/factorio-modding/
  - path: ~/.codex/skills/factorio-modding/
  - path: ~/.pi/agent/skills/factorio-modding/
  - path: ~/.gemini/skills/factorio-modding/
  - path: ~/.gemini/antigravity/skills/factorio-modding/
  - path: ~/.grok/skills/factorio-modding/
  - path: /mnt/repository/context-vault/.grok/skills/factorio-modding/

sources:
  skill_md:
    frontmatter:
      name: factorio-modding
      description: Use when creating, editing, or debugging Factorio mods — writing prototypes in data.lua, handling events in control.lua, defining mod settings, structuring info.json, writing locale files, or diagnosing desync and prototype errors.
      metadata:
        author: zk
        version: "1.0"
        category: gamedev

    body:
      - file: skills/factorio-modding/SKILL.md

validate_agentskills_spec: true
```
