---
id: recipe-tm20
created: 2026-09-05
modified: 2026-09-08
status: active
type:
  - "skill"
---

```yaml
name: tm20
output_format: skill

target_locations:
  - path: ~/.claude/skills/tm20/
  - path: ~/.codex/skills/tm20/
  - path: ~/.pi/agent/skills/tm20/
  - path: zk@adeck:~/.claude/skills/tm20/
  - path: zk@adeck:~/.codex/skills/tm20/
  - path: zk@adeck:~/.hermes/skills/user/tm20/
  - path: ~/.gemini/skills/tm20/
  - path: ~/.grok/skills/tm20/
  - path: zk@adeck:~/.grok/skills/tm20/
  - path: zk@zrrh:~/.grok/skills/tm20/
  - path: zk@zrrh:~/.claude/skills/tm20/
  - path: zk@zrrh:~/.codex/skills/tm20/
  - path: /mnt/repository/context-vault/.grok/skills/tm20/

sources:
  skill_md:
    frontmatter:
      name: tm20
      description: >-
        Print 80 mm thermal slips and receipts on the mesh Epson TM-T20III via tm20/tm20-set
        or the quita print receiver. Use when designing or printing tape, item listings,
        logos, QR, ESC/POS, 1-bit art, or when the user mentions tm20, TM-T20III, thermal
        printer, 80 mm receipts, or the mesh print receiver. Slash: /tm20
      compatibility: USB and tm20 binaries are quita only. Scripted jobs from other hosts POST the print receiver. No CUPS. Paper must be loaded.
      metadata:
        author: zk
        version: "0.4.0"
        category: print

    body:
      - file: skills/tm20/SKILL.md

  references:
    - file: skills/tm20/references/motifs.md
      output_name: motifs.md

validate_agentskills_spec: true
```
