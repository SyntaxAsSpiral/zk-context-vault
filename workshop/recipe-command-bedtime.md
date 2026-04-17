---
id: recipe-command-bedtime
created: 2026-04-17
modified: 2026-04-17
status: active
type:
  - "command"
---

```yaml
name: bedtime
output_format: command

target_locations:
  - path: ~/.kiro/hooks/bedtime.kiro.hook
  - path: ~/.claude/commands/bedtime.md
  - path: ~/.codex/prompts/bedtime.md
  - path: ~/.cursor/commands/bedtime.md
  - path: ~/.gemini/prompts/bedtime.md

sources:
  kiro_hook:
    - file: prompts/bedtime.md
  
  command_md:
    - file: prompts/bedtime.md

kiro_hook_config:
  enabled: true
  name: "bedtime"
  description: "Explain complex concepts through gentle bedtime story format"
  version: "1"
  when:
    type: "userTriggered"
  then:
    type: "askAgent"
  workspaceFolderName: ""
  shortName: "bedtime"
```

# bedtime Command Recipe

This recipe deploys the `bedtime` prompt/command to multiple AI platforms.

## Usage

1. Update `target_locations` with desired deployment paths
2. Verify source file exists in `prompts/bedtime.md`
3. Run `python workshop/src/assemble.py` to generate artifacts under `workshop/staging/command/bedtime/`
4. Run `python workshop/src/sync.py` to deploy to targets

## Notes

- Commands/prompts are flexible - no strict frontmatter requirements
- All platforms accept `.md` files for commands
- Use this template for any prompt you want available across multiple agents
