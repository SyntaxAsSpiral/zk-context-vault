---
id: recipe-agent-gemini
created: 2026-01-24
modified: 2026-01-24
status: active
type:
  - agent
---

```yaml
name: Gemini
output_format: agent

target_locations:
  - path: ~/.gemini/GEMINI.md
  - path: deck@amexsomnemon:~/.gemini/GEMINI.md

sources:
  - slice: agent=gemini-cli
    slice-file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-mesh.md
  - file: agents/steering-global-principles.md
```
