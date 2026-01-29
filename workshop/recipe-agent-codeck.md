---
id: recipe-agent-codeck
created: 2026-01-29
modified: 2026-01-29
status: active
type:
  - agent
---

```yaml
name: Codeck
output_format: agent

target_locations:
  - path: deck@amexsomnemon:~/.codex/AGENTS.md

sources:
  - slice: agent=codeck
    slice-file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-mesh.md
  - file: agents/steering-global-principles.md
```
