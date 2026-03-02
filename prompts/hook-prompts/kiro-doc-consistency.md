---
id: kiro-doc-consistency
type: hook-prompt
---

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

