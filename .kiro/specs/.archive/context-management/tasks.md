# Implementation Plan: Context Management

## Overview

Two Python scripts for assembling and syncing context documentation using Obsidian-based recipes with frontmatter and YAML blocks.

## Tasks

- [x] 1. Define recipe schemas for templates
  - Fill in the `{{agent recipe schema}}`, `{{kiro recipe schema}}`, `{{power recipe schema}}`, and `{{skill recipe schema}}` placeholders in existing templates
  - Define YAML structure for each recipe type based on their specific needs
  - Include required fields: name, target_locations, sources, template
  - Add type-specific fields as needed (e.g., agent format, skill bundle options)
  - _Requirements: 1.2, 1.3_

- [x] 2. Create assemble.py script (draft implementation exists)
  - Update `C:/Users/synta.ZK-ZRRH/.dev/.scripts/assemble.py` to match requirements
  - Support both `slice` + `slice-file` for slice extraction AND `file` only for whole file inclusion
  - Support multi-section recipes by splitting on `---` separators
  - Parse type-specific fields (agent_format, skill_type, power_structure) for future use
  - Default template to `{content}` if not provided
  - Update recipe-manifest.md with run logs
  - _Requirements: 1.1, 1.4, 1.5, 2.1, 2.2, 2.4, 2.5, 3.1, 12.1, 12.2_

- [x] 3. Create sync.py script  
  - Create `C:/Users/synta.ZK-ZRRH/.dev/.scripts/sync.py`
  - Parse recipe-manifest.md for deployment tracking
  - Copy outputs to target locations specified in recipes
  - Clean up orphaned files that were previously synced
  - Update recipe-manifest.md with sync results
  - _Requirements: 3.2, 3.3, 8.2, 8.4, 8.5_

- [x] 4. Create IDE task configurations
  - Create task definitions for running assemble.py and sync.py
  - Configure tasks to run from workspace root with proper Python paths
  - Add task arguments for dry-run and verbose modes
  - _Requirements: 3.4_

- [x] 5. Test with existing recipes and validate against requirements
  - Test simple agent recipes (Claudi, Codex) with slice + whole file sources
  - Test multi-section recipe (Kiro) with multiple outputs
  - Test skill recipe with type-specific fields
  - Validate slice extraction from real context files
  - Validate manifest updates work correctly
  - Test end-to-end assembly and sync workflow
  - Verify orphan cleanup removes old synced files
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

## Notes

- Draft assemble.py exists (~300 lines) but needs updates to match requirements
- Use `pyyaml` for YAML parsing and `frontmatter` for Obsidian frontmatter
- Focus on simple, readable code - bespoke over enterprise
- Type-specific fields parsed but not processed yet (reserved for future)
- Multi-section recipes enable related outputs in one file (e.g., Kiro's 3 steering files)