---
id: recipe-agent-grok
created: 2026-05-26
modified: 2026-05-26
status: active
type:
  - agent
---
```yaml
name: Grok
output_format: agent
output_name: AGENTS.md

target_locations:
  - path: ~/.grok/AGENTS.md
  - path: zk@adeck:~/.grok/AGENTS.md   # Global rules on adeck (applies to all sessions)
  # Optional named agent profile (for explicit --agent-profile use of the full exocortex context):
  # - path: ~/.grok/agents/grok-vault.md
  # - path: zk@adeck:~/.grok/agents/grok-vault.md
  # Project-local (inside this vault):
  # - path: /mnt/repository/context-vault/.grok/AGENTS.md

sources:
  - slice: agent=grok
    slice-file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-mesh.md
  - file: agents/steering-global-principles.md
```
