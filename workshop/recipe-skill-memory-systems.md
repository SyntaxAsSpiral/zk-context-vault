---
id: recipe-memory-systems
created: 2025-01-22
modified: 2025-01-22
status: active
type:
  - "skill"
---

```yaml
name: memory-systems
output_format: skill

# Agent Skills standard structure:
# memory-systems/
# ├── SKILL.md (required - with YAML frontmatter + markdown body)
# ├── scripts/ (optional - executable code)
# │   └── memory_store.py
# └── references/ (optional - additional docs loaded on demand)
#     └── implementation.md

target_locations:
  - path: ~/.claude/skills/memory-systems/
  - path: ~/.codex/skills/memory-systems/
  - path: deck@amexsomnemon:~/.claude/skills/memory-systems/
  - path: deck@amexsomnemon:~/.codex/skills/memory-systems/

# Source mapping to skill structure
sources:
  skill_md:
    # SKILL.md with required frontmatter
    frontmatter:
      name: memory-systems
      description: This skill should be used when the user asks to "implement agent memory", "persist state across sessions", "build knowledge graph", "track entities", or mentions memory architecture, temporal knowledge graphs, vector stores, entity memory, or cross-session persistence.
      license: MIT
      compatibility: Requires Python 3.8+ for scripts. Graph database optional (Neo4j, etc.). Vector store optional (Pinecone, Weaviate, etc.).
      metadata:
        version: "1.0.0"
        author: "Agent Skills for Context Engineering Contributors"
        created: "2025-12-20"
        last_updated: "2025-12-20"
    
    body:
      - file: skills/memory-systems/SKILL.md
  
  scripts:
    - file: skills/memory-systems/memory-store.py.md
      output_name: memory_store.py
  
  references:
    - file: skills/memory-systems/implementation.md
      output_name: implementation.md

# Validation
validate_agentskills_spec: true
```
