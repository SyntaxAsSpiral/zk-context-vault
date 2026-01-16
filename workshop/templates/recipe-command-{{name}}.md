---
id: recipe-command-{{name}}
created: {{date}}
modified: {{date}}
status: draft
type:
  - "command"
---

```yaml
name: {{name}}
output_format: command  # Simple markdown file deployment

# Command/Prompt deployment to multiple platforms
# Commands are flexible .md files with optional frontmatter

# Scope is determined by target path:
# - Global scope: ~/.kiro/hooks/, ~/.claude/commands/, etc.
# - Project scope: .kiro/hooks/, .claude/commands/, etc. (relative paths)

# Platform-specific formats:
# - Kiro: Uses hooks (JSON format with .kiro.hook extension)
# - Claude/Codex/Cursor: Direct .md files

target_locations:
  # Global scope (available across all projects)
  - path: ~/.kiro/hooks/{{name}}.kiro.hook     # Kiro uses hooks
  - path: ~/.claude/commands/{{name}}.md       # Claude uses commands
  - path: ~/.codex/prompts/{{name}}.md         # Codex uses prompts
  - path: ~/.cursor/commands/{{name}}.md       # Cursor uses commands
  
  # Project scope (only available in current project)
  # - path: .kiro/hooks/{{name}}.kiro.hook
  # - path: .claude/commands/{{name}}.md
  
  # Add more target locations as needed

# Source mapping
sources:
  # Kiro hook: the prompt content embedded into the JSON wrapper.
  kiro_hook:
    - file: prompts/{{name}}.md
  
  # Other platforms (direct markdown).
  command_md:
    - file: prompts/{{name}}.md

# Kiro hook configuration
kiro_hook_config:
  enabled: true
  name: "{{name}}"
  description: "{{description}}"
  version: "1"
  when:
    type: "userTriggered"  # Hook trigger type - see options below
    # patterns: ["*.ts", "*.tsx"]  # Required for file-based triggers
  then:
    type: "askAgent"  # or "runCommand"
    # prompt will be loaded from prompts/{{name}}.md for askAgent
    # command: "npm run lint"  # for runCommand type
  workspaceFolderName: ""  # Optional: specific workspace
  shortName: "{{name}}"

# Hook trigger types:
# - userTriggered: Manual execution (on-demand)
# - promptSubmit: When user submits a prompt (USER_PROMPT env var available)
# - agentStop: When agent completes its turn
# - fileCreated: When files matching patterns are created
# - fileSaved: When files matching patterns are saved
# - fileDeleted: When files matching patterns are deleted
#
# Action types:
# - askAgent: Send prompt to agent (use with any trigger)
# - runCommand: Execute shell command (use with promptSubmit or agentStop only)
```

# {{name}} Command Recipe

This recipe deploys the `{{name}}` prompt/command to multiple AI platforms.

## Usage

1. Update `target_locations` with desired deployment paths
2. Verify source file exists in `prompts/{{name}}.md`
3. Run `python workshop/src/assemble.py` to generate artifacts under `workshop/staging/command/{{name}}/`
4. Run `python workshop/src/sync.py` to deploy to targets

## Notes

- Commands/prompts are flexible - no strict frontmatter requirements
- All platforms accept `.md` files for commands
- Use this template for any prompt you want available across multiple agents
