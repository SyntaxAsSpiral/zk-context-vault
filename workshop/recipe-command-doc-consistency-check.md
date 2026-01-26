---
id: recipe-command-doc-consistency-check
created: 2026-01-16
modified: 2026-01-16
status: active
type:
  - "command"
---

```yaml
name: doc-consistency-check
output_format: command

target_locations:
  - path: ~/.kiro/hooks/doc-consistency-check.kiro.hook
  - path: ~/.claude/commands/doc-consistency-check.md
  - path: ~/.codex/prompts/doc-consistency-check.md
  - path: deck@amexsomnemon:~/.claude/commands/doc-consistency-check.md
  - path: deck@amexsomnemon:~/.codex/prompts/doc-consistency-check.md

sources:
  kiro_hook:
    - inline: |
        The user has requested a documentation consistency check. Please:

        1. Check recent commits for context on terminology changes

        2. Identify canonical sources for this project/workspace:
           - .kiro/specs/* (requirements.md, design.md, tasks.md)
           - AGENTS.md (project steering at repo root)
           - README.md (project overview)

        3. Search all markdown files in the project for drift in terminology, architecture, or other details (compare against canonical sources)

        4. Check these specific files for consistency:
           - .kiro/* (all files in .kiro directory)
           - ALL AGENTS.md files (search recursively)
           - ALL README.md files (search recursively)
           - Any code files with relevant comments or docstrings

        5. Report findings in a structured way:
           - List files that contain outdated terminology
           - Show the specific lines and suggested replacements based on canonical sources
           - Indicate if terminology is consistent across all docs

        6. Automatically update any inconsistencies found. Leave no trace. 🚮

        Focus on terminology consistency, architectural descriptions (validate against .kiro/specs/*/design.md), feature descriptions (validate against .kiro/specs/*/requirements.md), and any references that may have drifted between files.

  command_md:
    - inline: |
        # Documentation Consistency Check

        1. Check recent commits for context on terminology changes

        2. Identify canonical sources for this project/workspace:
           - `.kiro/specs/*` (requirements.md, design.md, tasks.md)
           - `AGENTS.md` (project steering at repo root)
           - `README.md` (project overview)

        3. Search all markdown files in the project for drift in terminology, architecture, or other details (compare against canonical sources)

        4. Check these specific files for consistency:
           - `.kiro/*` (all files in `.kiro` directory)
           - ALL `AGENTS.md` files (search recursively)
           - ALL `README.md` files (search recursively)
           - Any code files with relevant comments or docstrings

        5. Report findings in a structured way:
           - List files that contain outdated terminology
           - Show the specific lines and suggested replacements based on canonical sources
           - Indicate if terminology is consistent across all docs

        6. Automatically update any inconsistencies found. Leave no trace. 🚮

        Focus on terminology consistency, architectural descriptions (validate against `.kiro/specs/*/design.md`), feature descriptions (validate against `.kiro/specs/*/requirements.md`), and any references that may have drifted between files.

kiro_hook_config:
  enabled: true
  name: "Documentation Consistency Checker"
  description: "Searches all markdown files for terminology drift against canonical sources (.kiro/specs/*, AGENTS.md, README.md), checks consistency across all documentation, and automatically updates any inconsistencies found"
  version: "1"
  when:
    type: "userTriggered"
  then:
    type: "askAgent"
  shortName: "doc-consistency-check"
```

