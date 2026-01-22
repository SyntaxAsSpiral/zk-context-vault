---
id: recipe-memory-systems
created: 2025-01-22
modified: 2025-01-22
status: active
type:
  - "power"
---

```yaml
name: memory-systems
output_format: power

# Power folder structure:
# memory-systems/
# ├── POWER.md
# └── steering/
#     ├── implementation.md
#     └── memory-store.py.md

target_locations:
  - path: ~/.kiro/powers/installed/memory-systems/

# Source mapping to power structure
sources:
  power_md:
    - file: skills/memory-systems/SKILL.md
  
  steering_files:
    - file: skills/memory-systems/implementation.md
      output_name: implementation.md
    - file: skills/memory-systems/memory-store.py.md
      output_name: memory-store.py.md

# Optional metadata
metadata:
  version: "1.0.0"
  author: "Agent Skills for Context Engineering Contributors"
  description: "Implement persistent agent memory with layered architectures from vector stores to temporal knowledge graphs"
  keywords:
    - memory
    - persistence
    - knowledge-graph
    - temporal
    - entity-tracking
    - vector-store
    - rag
  category: "agent-architecture"
```
