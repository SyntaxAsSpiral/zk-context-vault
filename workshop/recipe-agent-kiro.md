---
id: recipe-agent-kiro
created: 2026-01-15
modified: 2026-01-15
status: active
type:
  - agent
---

```yaml
name: Kiro
output_format: agent  # Multi-section recipe for related outputs

target_locations:
  - path: ~/.kiro/steering/agent.md
sources:
  - slice: agent=kiro
    slice-file: agents/agent-roles.md

---
   
target_locations:
  - path: ~/.kiro/steering/operator.md
sources:
  - file: agents/steering-global-operator.md

---

target_locations:
  - path: ~/.kiro/steering/principles.md
sources:
  - file: agents/steering-global-principles.md
```