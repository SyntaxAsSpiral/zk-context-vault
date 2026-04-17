---
id: recipe-command-reflect
created: 2026-04-17
modified: 2026-04-17
status: active
type:
  - "command"
---

```yaml
name: reflect
output_format: command

target_locations:
  - path: ~/.kiro/hooks/reflect.kiro.hook
  - path: ~/.claude/commands/reflect.md
  - path: ~/.codex/prompts/reflect.md
  - path: ~/.cursor/commands/reflect.md
  - path: ~/.gemini/prompts/reflect.md

sources:
  kiro_hook:
    - file: prompts/reflect.md
  
  command_md:
    - file: prompts/reflect.md

kiro_hook_config:
  enabled: true
  name: "reflect"
  description: "Generate reflective dev diary entries with philosophical depth"
  version: "1"
  when:
    type: "userTriggered"
  then:
    type: "askAgent"
  workspaceFolderName: ""
  shortName: "reflect"
```

# reflect Command Recipe

This recipe deploys the `reflect` prompt/command to multiple AI platforms.

## Usage

1. Update `target_locations` with desired deployment paths
2. Verify source file exists in `prompts/reflect.md`
3. Run `python workshop/src/assemble.py` to generate artifacts under `workshop/staging/command/reflect/`
4. Run `python workshop/src/sync.py` to deploy to targets

## Notes

- Commands/prompts are flexible - no strict frontmatter requirements
- All platforms accept `.md` files for commands
- Use this template for any prompt you want available across multiple agents
