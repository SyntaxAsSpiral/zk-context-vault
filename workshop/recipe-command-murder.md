---
id: recipe-command-murder
created: 2026-01-15
modified: 2026-01-15
status: active
type:
  - "command"
---

```yaml
name: murder
output_format: command  # Multi-platform deployment

# Deploy murder cogitator prompt to all platforms
# Using global scope (~/) so it's available across all projects

target_locations:
  - path: ~/.kiro/hooks/murder.kiro.hook      # Kiro uses hooks (JSON)
  - path: ~/.claude/commands/murder.md        # Claude uses commands (MD)
  - path: ~/.codex/prompts/murder.md         # Codex uses prompts (MD)

# Source mapping
sources:
  # Kiro hook format (JSON wrapper around prompt)
  kiro_hook:
    - file: prompts/murder.md
      output_name: murder.kiro.hook
      format: kiro_hook
  
  # Other platforms (direct markdown)
  command_md:
    - file: prompts/murder.md
      output_name: murder.md

# Kiro hook configuration
kiro_hook_config:
  enabled: true
  name: "Murder Cogitator"
  description: "Adversarial red-teaming persona for assumption-hostile review and critique"
  version: "1"
  when:
    type: "userTriggered"  # Manual trigger - invoke on demand
  then:
    type: "askAgent"
    # prompt content loaded from prompts/murder.md
  workspaceFolderName: ""
  shortName: "murder"
```

# Murder Cogitator Command Recipe

Deploys the murder cogitator prompt (adversarial red-teaming persona) to all AI platforms.

## Platform-Specific Formats

- **Kiro**: Deployed as a user-triggered hook (`.kiro.hook` JSON format)
- **Claude/Codex/Cursor**: Deployed as direct markdown commands

## Usage

Invoke with platform-specific command syntax:
- **Kiro**: Trigger via hooks UI or command palette
- **Claude**: Loads as slash command (ie /murder)
- **Codex**: Loads as slash command (ie /murder)

The murder cogitator provides adversarial analysis and assumption-hostile review.

## Hook Structure

The Kiro hook wraps the prompt content in a JSON structure:
```json
{
  "enabled": true,
  "name": "Murder Cogitator",
  "description": "Adversarial red-teaming persona...",
  "version": "1",
  "when": {"type": "userTriggered"},
  "then": {"type": "askAgent", "prompt": "<content from prompts/murder.md>"},
  "workspaceFolderName": "",
  "shortName": "murder"
}
```
