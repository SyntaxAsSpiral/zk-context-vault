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

sources:
  kiro_hook:
    - inline: |
        The user has requested a documentation consistency check. Please:

        1. Check recent commits, then search all markdown files in the project for drift in terminology, architecture, or other details
        2. Check these specific files for consistency:
           - .kiro/* (all files in .kiro directory)
           - ALL AGENTS.md files (search recursively)
           - ALL README.md files (search recursively)
           - Any code files with relevant comments or docstrings

        3. Report findings in a structured way:
           - List files that contain outdated terminology
           - Show the specific lines and suggested replacements
           - Indicate if terminology is consistent across all docs

        4. Automatically update any inconsistencies found. Leave no trace. 🚮

        Focus on terminology consistency, architectural descriptions, feature descriptions, and any references that may have drifted between files. Pay special attention to the Collectivist project terminology and the seed-to-trunk architecture concepts.

  command_md:
    - inline: |
        # Documentation Consistency Check

        Check recent commits, then search all markdown files in the project for drift in terminology, architecture, or other details.

        Check these specific files for consistency:
        - `.kiro/*` (all files in `.kiro` directory)
        - ALL `AGENTS.md` files (search recursively)
        - ALL `README.md` files (search recursively)
        - Any code files with relevant comments or docstrings

        Report findings in a structured way:
        - List files that contain outdated terminology
        - Show the specific lines and suggested replacements
        - Indicate if terminology is consistent across all docs

        Automatically update any inconsistencies found. Leave no trace. 🚮

        Focus on terminology consistency, architectural descriptions, feature descriptions, and any references that may have drifted between files. Pay special attention to the Collectivist project terminology and the seed-to-trunk architecture concepts.

kiro_hook_config:
  enabled: true
  name: "Documentation Consistency Checker"
  description: "Searches all markdown files and Python comments for terminology drift, checks consistency across .kiro/*, AGENTS.md, README.md files, and automatically updates any inconsistencies found"
  version: "1"
  when:
    type: "userTriggered"
  then:
    type: "askAgent"
  shortName: "doc-consistency-check"
```

