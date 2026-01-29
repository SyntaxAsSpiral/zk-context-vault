---
name: nix-os
displayName: NixOS Manager ❄️
description: Comprehensive Nix package and configuration management following Determinate Systems best practices. Use when installing packages, managing flakes, or troubleshooting Nix issues.
version: "1.0.0"
keywords: ["nix", "nixos", "package-manager", "flakes", "system-configuration", "dev-environment"]
author: zk::anticompiler
category: development
mcpServers:
  nix.dev Docs:
    url: "https://gitmcp.io/NixOS/nix.dev"
  nixos:
    command: "uvx"
    args: ["mcp-nixos"]
steeringFiles: ["SKILL.md", "REFERENCE.md"]
---

# NixOS Manager ❄️

**Comprehensive Nix package and configuration management.**

## Overview
This power provides deep integration with the Nix ecosystem, allowing you to manage packages, flakes, and system configurations with precision. It follows Determinate Systems best practices and includes specific knowledge about the ZK-ZRRH architecture (Khanelinix, agent-skills-nix).

## Features
### Package Management
- Install, update, and remove packages using `nix profile`
- Manage flakes and lockfiles
- Troubleshoot dependency issues

### Architecture Integration
- **Khanelinix**: System-level context engine support
- **Agent Skills**: Integration with `agent-skills-nix` framework
- **MCP**: Management of Model Context Protocol servers via Nix

## Quick Start
```bash
# Update all packages
nix flake update && nix profile upgrade dotfiles

# Search for a package
nix search nixpkgs <package>
```

See [Skill Documentation](steering/SKILL.md) for detailed instructions.
