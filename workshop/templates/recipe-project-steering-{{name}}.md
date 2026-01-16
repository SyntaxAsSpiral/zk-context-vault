---
id: recipe-project-steering-{{name}}
created: {{date}}
modified: {{date}}
status: draft
type:
  - "agent"
  - "project"
---

```yaml
name: {{name}}
output_format: agent

# Project steering: repack a single vault file (or slice) into AGENTS.md for a repo.
#
# Target options:
# - Directory form (recommended): ends with `/` or `\` → auto-filename
#   - Claude targets become CLAUDE.md (only under ~/.claude)
#   - everything else becomes AGENTS.md
# - File form: point directly at .../AGENTS.md to force the name

target_locations:
  - path: /absolute/path/to/project/root/

sources:
  # Whole-file inclusion (simplest)
  - file: prompts/project-steering/{{name}}.md

  # Or slice extraction
  # - slice: project={{name}}
  #   slice-file: prompts/project-steering.md

# Optional wrapper template
# template: |
#   # Project Steering ({{name}})
#   {content}
```

