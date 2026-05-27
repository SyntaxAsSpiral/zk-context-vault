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

target_locations:
  - path: ~/.grok/agents/grok-vault.md
  - path: zk@adeck:~/.grok/agents/grok-vault.md   # Grok on adeck (Steam Deck agentic server)
  # Project-local agent profile (add when .grok/ harness is active in this vault):
  # - path: /mnt/repository/context-vault/.grok/agents/grok-vault.md

sources:
  - slice: agent=grok
    slice-file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-mesh.md
  - file: agents/steering-global-principles.md
```
