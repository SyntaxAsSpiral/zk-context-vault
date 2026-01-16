---
id: recipe-agent-codex
created: 2026-01-15
modified: 2026-01-15
status: active
type:
  - agent
---

```yaml
name: Codex
output_format: agent  # Simple concatenation, no template

target_locations:
  - path: ~/.codex/AGENTS.md

sources:
  - slice: agent=codex
    slice-file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-principles.md
```