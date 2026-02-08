---
id: recipe-skill-nix-os
created: 2026-01-29
modified: 2026-01-29
status: active
type:
  - "skill"
---

```yaml
name: nix-os
output_format: skill
target_locations:
  - path: ~/.claude/skills/nix-os/
  - path: ~/.codex/skills/nix-os/
  - path: zk@adeck:~/.claude/skills/nix-os/
  - path: zk@adeck:~/.codex/skills/nix-os/
  - path: ~/.gemini/antigravity/skills/nix-os/
  - path: ~/.gemini/skills/nix-os/

sources:
  skill_md:
    frontmatter:
      name: nix-os
      description: Comprehensive Nix package and configuration management following Determinate Systems best practices.
      metadata:
        version: "1.0.0"
        author: zk::anticompiler
        category: development
    
    body:
      - file: skills/nix-os/SKILL.md
  
  assets:
    - file: skills/nix-os/REFERENCE.md
      output_name: REFERENCE.md
    - file: skills/nix-os/module-enablement-matrix.md
      output_name: module-enablement-matrix.md
    - file: skills/nix-os/script-diagnose-nix.md
      output_name: script-diagnose-nix.md
    - file: skills/nix-os/script-update-flake.md
      output_name: script-update-flake.md
    - file: skills/nix-os/template-dotfiles-flake.md
      output_name: template-dotfiles-flake.md
    - file: skills/nix-os/template-minimal-flake.md
      output_name: template-minimal-flake.md
    - file: skills/nix-os/template-project-flake.md
      output_name: template-project-flake.md
    - file: skills/nix-os/template-skill-child-flake.md
      output_name: template-skill-child-flake.md

validate_agentskills_spec: true
```
