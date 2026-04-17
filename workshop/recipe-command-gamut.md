---
id: recipe-command-gamut
created: 2026-04-17
modified: 2026-04-17
status: active
type:
  - "command"
---

```yaml
name: gamut
output_format: command

target_locations:
  - path: ~/.kiro/hooks/gamut.kiro.hook
  - path: ~/.claude/commands/gamut.md
  - path: ~/.codex/prompts/gamut.md
  - path: ~/.cursor/commands/gamut.md
  - path: ~/.gemini/prompts/gamut.md

sources:
  kiro_hook:
    - file: prompts/gamut.md
  
  command_md:
    - file: prompts/gamut.md

kiro_hook_config:
  enabled: true
  name: "gamut"
  description: "Generate five distinct responses spanning entire solution space"
  version: "1"
  when:
    type: "userTriggered"
  then:
    type: "askAgent"
  workspaceFolderName: ""
  shortName: "gamut"
```

# gamut Command Recipe

This recipe deploys the `gamut` prompt/command to multiple AI platforms.

## Usage

1. Update `target_locations` with desired deployment paths
2. Verify source file exists in `prompts/gamut.md`
3. Run `python workshop/src/assemble.py` to generate artifacts under `workshop/staging/command/gamut/`
4. Run `python workshop/src/sync.py` to deploy to targets

## Notes

- Commands/prompts are flexible - no strict frontmatter requirements
- All platforms accept `.md` files for commands
- Use this template for any prompt you want available across multiple agents
