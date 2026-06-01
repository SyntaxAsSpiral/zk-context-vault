---
id: recipe-semantic-json
created: 2026-05-31
modified: 2026-05-31
status: active
type:
  - "skill"
---

```yaml
name: semantic-json
output_format: skill

# semantic-json/
# ├── SKILL.md
# └── references/
#     ├── getting-started.md
#     └── advanced-workflows.md

target_locations:
  - path: ~/.claude/skills/semantic-json/
  - path: ~/.codex/skills/semantic-json/
  - path: ~/.pi/agent/skills/semantic-json/
  - path: zk@adeck:~/.claude/skills/semantic-json/
  - path: zk@adeck:~/.codex/skills/semantic-json/
  - path: zk@adeck:~/.hermes/skills/user/semantic-json/
  - path: ~/.gemini/antigravity/skills/semantic-json/
  - path: ~/.gemini/skills/semantic-json/
  - path: ~/.grok/skills/semantic-json/
  - path: zk@adeck:~/.grok/skills/semantic-json/
  - path: /mnt/repository/context-vault/.grok/skills/semantic-json/

sources:
  skill_md:
    frontmatter:
      name: semantic-json
      description: Use when working with Obsidian Canvas files as cognitive modeling tools — compiling spatial/visual structure into deterministic JSON, designing canvas layouts with semantic color and edge conventions, exporting structured data from canvas, or importing JSON into canvas form.
      metadata:
        author: zk
        version: "1.0"
        category: obsidian

    body:
      - file: skills/semantic-json/SKILL.md

  references:
    - file: skills/semantic-json/getting-started.md
      output_name: getting-started.md
    - file: skills/semantic-json/advanced-workflows.md
      output_name: advanced-workflows.md

validate_agentskills_spec: true
```
