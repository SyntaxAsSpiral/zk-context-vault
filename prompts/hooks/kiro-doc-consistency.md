---
id: kiro-doc-consistency
source: agents/kiro-hooks.md
---

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

