---
id: recipe-agent-claudeck
created: 2026-01-28
modified: 2026-01-28
status: active
type:
  - agent
---

```yaml
name: Claudeck
output_format: agent

target_locations:
  - path: deck@amexsomnemon:~/.claude/CLAUDE.md

sources:
  - slice: agent=claudeck
    slice-file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-mesh.md
  - file: agents/steering-global-principles.md
```
