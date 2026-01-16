---
id: recipe-{{name}}
created: {{date}}
modified: {{date}}
status: draft
type:
  - "agent"
---

```yaml
name: {{name}}
output_format: agent

# Agent output is a single markdown file (staged under `workshop/staging/agent/<name>/`).
# If `target_locations.path` is a directory (ends with `/` or `\`), the filename is auto-selected:
# - under `~/.claude/` → `CLAUDE.md`
# - otherwise → `AGENTS.md`

target_locations:
  - path: # Target file path OR directory (e.g. ~/.codex/AGENTS.md or ~/.codex/)
sources:
  # Slice extraction:
  - slice: # e.g. agent=claudi-claude-code
    slice-file: # e.g. agents/agent-roles.md

  # Whole file inclusion:
  # - file: agents/steering-global-principles.md

# Multi-section: inside this YAML block, separate additional output sections with `---`.
template: |
  # {{name}} Agent
  {content}
# Agent-specific fields
agent_format: # claude | kiro | openai | custom
output_type: # system_prompt | config_file | both
persona_elements:
  - role_sigils: true    # Include role sigils from slices
  - voiceprint: true     # Include voiceprint/tone
  - constraints: true    # Include behavioral constraints
  - bindu: false         # Include bindu/anchor elements (optional)
```
