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
target_locations:
  - path: # Target file path for agent output (e.g., ~/.config/claude/system.md)
sources:
  - slice: # Slice identifier (e.g., agent=claudi-claude-code)
    file: # Source file path (e.g., .context/agents/assistant.md)
  # Add more sources as needed
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