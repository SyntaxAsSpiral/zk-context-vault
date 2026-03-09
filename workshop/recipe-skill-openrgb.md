---
id: recipe-openrgb
created: 2026-03-09
modified: 2026-03-09
status: draft
type:
  - "skill"
---

```yaml
name: openrgb
output_format: skill

# Agent Skills standard structure:
# openrgb/
# ├── SKILL.md (required - with YAML frontmatter + markdown body)

target_locations:
  - path: ~/.claude/skills/openrgb/
  - path: ~/.codex/skills/openrgb/
  - path: zk@adeck:~/.claude/skills/openrgb/
  - path: zk@adeck:~/.codex/skills/openrgb/
  - path: zk@zrrh:~/.claude/skills/openrgb/
  - path: zk@zrrh:~/.codex/skills/openrgb/
  - path: zk@zrrh:~/.gemini/skills/openrgb/
  - path: zk@zrrh:~/.pi/agent/skills/openrgb/
  - path: ~/.gemini/antigravity/skills/openrgb/
  - path: ~/.gemini/skills/openrgb/
  - path: ~/.pi/agent/skills/openrgb/

sources:
  skill_md:
    frontmatter:
      name: openrgb
      description: Advanced OpenRGB integration for ambient computing — SDK server automation, remote display surfaces, presence indicators, notification channels, and event-driven effects using openrgb-python. Use when building RGB as an ambient interface layer, presence/notification systems, multi-host lighting coordination, or system-event-driven effects.
      compatibility: Requires OpenRGB with SDK server enabled, openrgb-python (pip). Network features require hosts reachable over TCP. Linux recommended; partial Windows/macOS support.
      metadata:
        version: "0.2"
        author: zk
        category: integration

    body:
      - file: skills/openrgb/SKILL.md

validate_agentskills_spec: true
```
