## kiro-murder

location(s):

- `C:\Users\synta.ZK-ZRRH\.dev\.kiro\hooks\murder-persona-hook.kiro.hook`

```
{
  "enabled": true,
  "name": "Murder Persona Switch",
  "description": "When user says 'murder', adopt the kharon persona from Z:\\Documents\\.context\\prompts\\murder.md",
  "version": "1",
  "when": {
    "type": "userTriggered"
  },
  "then": {
    "type": "askAgent",
    "prompt": "The user has said 'murder'. Please adopt the kharon persona as defined in Z:\\Documents\\.context\\prompts\\murder.md. Read that file and embody that persona for our interaction."
  }
```

---

## kiro-doc-consistency

location(s):

- `C:\Users\synta.ZK-ZRRH\.dev\collectivist\.kiro\hooks\doc-consistency-check.kiro.hook`

```
{
  "enabled": true,
  "name": "Documentation Consistency Checker",
  "description": "Searches all markdown files and Python comments for terminology drift, checks consistency across .kiro/*, AGENTS.md, README.md files, and automatically updates any inconsistencies found",
  "version": "1",
  "when": {
    "type": "userTriggered"
  },
  "then": {
    "type": "askAgent",
    "prompt": "The user has requested a documentation consistency check. Please:\n\n1. Search all markdown files in the project for drift in terminology, architecture, or other details\n2. Check these specific files for consistency:\n   - .kiro/* (all files in .kiro directory)\n   - ALL AGENTS.md files (search recursively)\n   - ALL README.md files (search recursively) \n   - Any Python files with relevant comments or docstrings\n\n3. Report findings in a structured way:\n   - List files that contain outdated terminology\n   - Show the specific lines and suggested replacements\n   - Indicate if terminology is consistent across all docs\n\n4. Automatically update any inconsistencies found. Leave no trace. 🚮\n\nFocus on terminology consistency, architectural descriptions, feature descriptions, and any references that may have drifted between files. Pay special attention to the Collectivist project terminology and the seed-to-trunk architecture concepts."
  }
}
```

---

# kiro-dotfile-vis

location(s):
- `C:\Users\synta.ZK-ZRRH\.dev\collectivist\.kiro\hooks\dotfile-visibility-reminder.kiro.hook`
 
```
{
  "enabled": false,
  "name": "Dotfile Visibility Reminder",
  "description": "Use ls -a/-A and include .* patterns in globs when working with directories, following the dotfile visibility principle `.*/**`",
  "version": "1",
  "when": {
    "type": "fileEdited",
    "patterns": [
      ".*/**",
      "."
    ]
  },
  "then": {
    "type": "askAgent",
    "prompt": "\"👁️ Dotfile Visibility - No bare `ls` when orienting to directories. Dotfiles are organizational, not hidden. Use `ls -a` or `ls -A` for directory reconnaissance. Include `.*` patterns in glob searches. Treat dotfolders as first-class citizens.\""
  },
  "workspaceFolderName": "collectivist",
  "shortName": "dotfile-visibility-reminder"
}
```