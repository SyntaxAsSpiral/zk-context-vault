---
id: recipe-command-cave
created: 2026-04-17
modified: 2026-04-17
status: default
type:
  - "command"
---

```yaml
name: cave
output_format: command

target_locations:
  - path: ~/.kiro/hooks/cave.kiro.hook
  - path: ~/.claude/commands/cave.md
  - path: ~/.codex/prompts/cave.md
  - path: ~/.cursor/commands/cave.md
  - path: ~/.gemini/prompts/cave.md

sources:
  kiro_hook:
    - file: prompts/cave.md
  
  command_md:
    - file: prompts/cave.md

kiro_hook_config:
  enabled: true
  name: "cave"
  description: "Ultra-compressed communication mode — caveman grammar, bear kaomoji expression, emoji shorthand"
  version: "1"
  when:
    type: "userTriggered"
  then:
    type: "askAgent"
  workspaceFolderName: ""
  shortName: "cave"
```

# cave Command Recipe

This recipe deploys the `cave` prompt/command to multiple AI platforms.

## Usage

1. Update `target_locations` with desired deployment paths
2. Verify source file exists in `prompts/cave.md`
3. Run `python workshop/src/assemble.py` to generate artifacts under `workshop/staging/command/cave/`
4. Run `python workshop/src/sync.py` to deploy to targets

## Notes

- Commands/prompts are flexible - no strict frontmatter requirements
- All platforms accept `.md` files for commands
- Use this template for any prompt you want available across multiple agents
