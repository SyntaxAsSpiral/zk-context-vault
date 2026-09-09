---
id: recipe-agent-codex
created: 2026-01-15
modified: 2026-09-08
status: active
type:
  - agent
---

```yaml
name: Codex
output_format: agent  # Simple concatenation, no template
output_name: AGENTS.md

target_locations:
  - path: ~/.codex/AGENTS.md
  - path: zk@zrrh:~/.codex/AGENTS.md
  - path: zk@quita:~/.codex/AGENTS.md

sources:
  - slice: agent=gpt-codex
    slice-file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-mesh.md
  - file: agents/steering-global-principles.md
```
