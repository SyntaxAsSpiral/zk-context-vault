---
id: recipe-command-moeverse
created: 2026-04-17
modified: 2026-04-17
status: active
type:
  - "command"
---

```yaml
name: moeverse
output_format: command

target_locations:
  - path: ~/.kiro/hooks/moeverse.kiro.hook
  - path: ~/.claude/commands/moeverse.md
  - path: ~/.codex/prompts/moeverse.md
  - path: ~/.cursor/commands/moeverse.md
  - path: ~/.gemini/prompts/moeverse.md

sources:
  kiro_hook:
    - file: prompts/moeverse.md
  
  command_md:
    - file: prompts/moeverse.md

kiro_hook_config:
  enabled: true
  name: "moeverse"
  description: "Explain systems/concepts through anime character personification"
  version: "1"
  when:
    type: "userTriggered"
  then:
    type: "askAgent"
  workspaceFolderName: ""
  shortName: "moeverse"
```

# moeverse Command Recipe

This recipe deploys the `moeverse` prompt/command to multiple AI platforms.

## Usage

1. Update `target_locations` with desired deployment paths
2. Verify source file exists in `prompts/moeverse.md`
3. Run `python workshop/src/assemble.py` to generate artifacts under `workshop/staging/command/moeverse/`
4. Run `python workshop/src/sync.py` to deploy to targets

## Notes

- Commands/prompts are flexible - no strict frontmatter requirements
- All platforms accept `.md` files for commands
- Use this template for any prompt you want available across multiple agents
