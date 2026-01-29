---
id: recipe-nix-os
created: 2026-01-29
modified: 2026-01-29
status: active
type:
  - "power"
---

```yaml
name: nix-os
output_format: power
target_locations:
  - path: ~/.kiro/powers/installed/nix-os/

sources:
  power_md:
    - file: skills/nix-os/POWER.md
  
  mcp_config:
    - file: skills/nix-os/mcp.json
      output_name: mcp.json
  
  steering_files:
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

metadata:
  version: "1.0.0"
  author: zk::anticompiler
  license: MIT
  description: Comprehensive Nix package and configuration management
  keywords: ["nix", "nixos", "package-manager", "flakes"]
  category: development
  displayName: NixOS Manager
  iconUrl: https://cdn.jsdelivr.net/gh/SyntaxAsSpiral/esotericons@main/enochian.png
  repositoryUrl: https://github.com/nixos/nix
```
