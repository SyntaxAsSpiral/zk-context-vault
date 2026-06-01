---
id: recipe-obsidian
created: 2026-05-31
modified: 2026-05-31
status: active
type:
  - "skill"
---

```yaml
name: obsidian
output_format: skill

# obsidian/
# ├── SKILL.md
# └── references/
#     ├── CALLOUTS.md
#     ├── EMBEDS.md
#     └── PROPERTIES.md

target_locations:
  - path: ~/.claude/skills/obsidian/
  - path: ~/.codex/skills/obsidian/
  - path: ~/.pi/agent/skills/obsidian/
  - path: zk@adeck:~/.claude/skills/obsidian/
  - path: zk@adeck:~/.codex/skills/obsidian/
  - path: zk@adeck:~/.hermes/skills/user/obsidian/
  - path: ~/.gemini/antigravity/skills/obsidian/
  - path: ~/.gemini/skills/obsidian/
  - path: ~/.grok/skills/obsidian/
  - path: zk@adeck:~/.grok/skills/obsidian/
  - path: /mnt/repository/context-vault/.grok/skills/obsidian/

sources:
  skill_md:
    frontmatter:
      name: obsidian
      description: Use when working with Obsidian vaults — creating or editing .md notes, wikilinks, callouts, frontmatter, embeds, tags, or Obsidian-specific syntax; or when interacting with a vault via the obsidian CLI to read, create, search, manage notes/tasks/properties, or develop and debug plugins and themes.
      metadata:
        author: zk
        version: "1.0"
        category: obsidian

    body:
      - file: skills/obsidian/SKILL.md

  references:
    - file: skills/obsidian/references/CALLOUTS.md
      output_name: CALLOUTS.md
    - file: skills/obsidian/references/EMBEDS.md
      output_name: EMBEDS.md
    - file: skills/obsidian/references/PROPERTIES.md
      output_name: PROPERTIES.md

validate_agentskills_spec: true
```
