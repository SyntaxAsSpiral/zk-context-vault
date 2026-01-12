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

- [x] 2. Create assemble.py script
  - Create `C:/Users/synta.ZK-ZRRH/.dev/.scripts/assemble.py`
  - Parse Obsidian frontmatter and extract YAML code blocks from recipe files
  - Extract slices from source files using existing slice markers
  - Apply template substitution and generate outputs
  - Update recipe-manifest.md with run logs
  - _Requirements: 1.1, 2.1, 2.2, 3.1_

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

- [ ] 5. Test with existing templates and manifest
  - Verify script works with existing Obsidian templates
  - Test slice extraction from real context files
  - Validate manifest updates work correctly
  - Test end-to-end assembly and sync workflow
  - _Requirements: 9.1, 9.2, 9.3_

## Notes

- Scripts will be ~50-100 lines each in Python
- Use `pyyaml` for YAML parsing and `frontmatter` for Obsidian frontmatter
- Focus on simple, readable code over complex error handling
- Leverage existing Obsidian template structure and slice markers