---
name: nix-manager
description: Manage Nix packages, flakes, and configurations using Determinate Nix installer patterns. Use when installing/updating packages, creating flakes, troubleshooting Nix issues, or optimizing Nix workflows. Keywords: nix, flake, package, nixpkgs, nix profile, flake.nix, flake.lock, determinate, nix-installer
---

# Nix Package & Configuration Manager

Comprehensive Nix management following Determinate Systems best practices and this repository's patterns.

## Core Architecture Components

### 1. agent-skills-nix (Framework)
**The primary orchestrator for Declarative Skill Management.**

- **The Concept**: Skills are self-contained directories with a `SKILL.md` (instructions/YAML frontmatter).
- **The Mechanism**: Uses a Home Manager module to "sync" selected skills into agent configuration directories (e.g., `~/.claude/skills`).
- **Key Feature**: Supports **Markdown Transformations**. You can inject local paths to binaries (like `jq` or `curl`) directly into the `SKILL.md` so the agent doesn't have to guess where they are or download them, saving context tokens.

### 2. llm-agents.nix (Distribution)
**A daily-updated collection of Nix packages for AI agents.**

- Provides ready-to-use derivations for `claude-code`, `codex`, `amp`, and more.
- This is your source for the actual agent binaries.

### 3. khanelinix (System-Level context engine)
**Beyond just "skills," this repo is a masterclass in Nix Meta-Programming for AI context.**

- **The Transformation Engine**: Uses custom Nix logic (`lib.importSubdirs` + `mapAttrs`) to translate a single source of truth for agents and commands into:
    - **Claude Code**: Multi-part Markdown with YAML frontmatter.
    - **Gemini CLI**: JSON-friendly descriptors and prompt blocks.
    - **OpenCode**: Specialized frontmatter for tool permissions (bash, edit, write).
- **MCP Integration**: Directly imports `mcp-servers-nix`, treats MCP tools as system-level resources available across all host archetypes.
- **Flake-Parts Partitioning**: The entire system is modularly partitioned. You can swap neovim flavors (`khanelivim`) or shell environments without breaking the core system logic.

## Instructions

### 0. Required Workflow

Every config change follows this sequence — no shortcuts:

1. **Discover** — use `mcp-nixos` to find correct package attr or option path. Never guess.
2. **Inspect** — read the target file before editing (`inspect_state` or Read tool).
3. **Patch** — edit the module. Minimal diff.
4. **Validate** — targeted eval before deploying (see §3).
5. **Apply** — `zcli deploy <host>` for system switches.
6. **Report** — surface `rollback_generation` so user can recover: `sudo nixos-rebuild switch --rollback`.

On validation failure: extract the first `error:` line, surface it, stop. Don't retry blind.

**System config vs Home Manager:**
- System modules (`/mnt/repository/nix-os/hosts/`, `modules/`) → `zcli deploy <host>`
- Home Manager config → `home-manager build` then `home-manager switch` (no sudo)

### 1. Understand Repository Context

Check current Nix setup:
- **Flake location**: `/mnt/repository/nix-os/`
- **Package management**: Declarative NixOS configuration via flakes.
- **Update mechanism**: `zcli deploy <host>`

Read current `flake.nix` to understand:
- Input sources (currently: `nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable"`)
- Package definitions (buildEnv with ~60+ packages)
- Outputs: `packages`, `devShells`, `formatter`
- Supported systems: x86_64-linux

### 2. Package Management Operations

#### Install New Package

**Process:**
1. Query `mcp-nixos` for correct package attribute name
2. Add package to appropriate module in `/mnt/repository/nix-os/`
3. Validate (§3)
4. Run `zcli deploy <host>` to apply
5. Verify package availability

#### Update All Packages

**Process:**
```bash
# Update flake inputs
nix flake update -C /mnt/repository/nix-os

# Apply updates to mesh host
zcli deploy <host>
```

#### Remove Package

**Process:**
1. Remove from flake configuration
2. Run `zcli deploy <host>` or `nh os switch`
3. Old package remains in store but not in PATH

**Note**: Garbage collection removes unreferenced packages:
```bash
nh clean all
```

### 3. Flake Configuration

#### Modify flake.nix

**Common operations:**

**Add new input:**
```nix
inputs = {
  nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  # Add new input
  home-manager.url = "github:nix-community/home-manager";
  home-manager.inputs.nixpkgs.follows = "nixpkgs";  # Prevent duplicate nixpkgs
};
```

**Add host-specific packages:**
```nix
paths = [
  # Universal packages
  git gh lazygit
] ++ lib.optionals (config.networking.hostName == "nxiz") [
  # nxiz-only
  nvidia-vaapi-driver
];
```

**Modify devShell:**
```nix
devShells = forAllSystems ({ pkgs }: {
  default = pkgs.mkShell {
    packages = with pkgs; [
      fish
      nixpkgs-fmt
      shellcheck
      # Add development tools here
    ];
    inputsFrom = [ self.packages.${pkgs.system}.default ];
    shellHook = ''
      echo "🐠 Dotfiles development environment"
      echo "Ready for development."
    '';
  };
});
```

#### Validate Before Applying

Choose the right tool for the scope of change:

```bash
# Dry-run full host eval (standard gate before deploy)
zcli deploy <host> --dry

# Evaluate a specific attribute without building
nix eval /mnt/repository/nix-os#nixosConfigurations.<host>.config.<attr.path>

# Check a specific package is resolvable
nix eval /mnt/repository/nix-os#nixosConfigurations.<host>.config.environment.systemPackages --json

# Build only the system closure, no switch
nix build /mnt/repository/nix-os#nixosConfigurations.<host>.config.system.build.toplevel --dry-run

# Fast syntax+eval check without building anything
nix flake check /mnt/repository/nix-os --no-build

# Quick metadata check (no eval)
nix flake metadata /mnt/repository/nix-os
```

On error: extract the first `error:` line and surface it. Stop. Don't retry blind.

**Common issues:**
- Package renamed in nixpkgs (e.g., `du-dust` → `dust`)
- Missing comma in package list
- Invalid attribute path
- Syntax errors in Nix expressions

#### Update Lock File

**When to update:**
- Regular maintenance (weekly/monthly)
- Security updates needed
- Specific package version required

**How:**
```bash
# Update all inputs
nix flake update

# Update specific input only
nix flake lock --update-input nixpkgs

# Verify changes
git diff flake.lock
```

### 4. Troubleshooting

#### Slow Nix Operations

**Diagnosis:**
```bash
nix store info             # Check store size
nix store gc --dry-run     # See what can be cleaned
```

**Solutions:**
- Run `nix-collect-garbage -d` to remove old generations
- Run `nix store optimise` to deduplicate files
- Check network connectivity (binary cache downloads)

#### Package Not Found

**Error**: `error: attribute 'package-name' missing`

**Solutions:**
1. Check nixpkgs version: some packages only in unstable
2. Search for package: `nix search nixpkgs package-name`
3. Check if package was renamed
4. Try alternative package names

#### Evaluation Errors

**Error**: `error: ... while evaluating ...`

**Common causes:**
- Syntax error in `flake.nix`
- Recursive attribute access
- Type mismatch (string vs list)

**Debug:**
```bash
nix eval .#packages.aarch64-darwin.default.name  # Test specific attribute
nix repl                                          # Interactive REPL
:lf .                                             # Load flake in REPL
packages.aarch64-darwin.default.name              # Evaluate in REPL
```

#### Lock File Conflicts

**Error**: `error: flake.lock is dirty`

**Solutions:**
```bash
# Regenerate lock file
rm flake.lock
nix flake update

# Or accept uncommitted changes
nix flake check --impure  # NOT recommended for reproducibility
```

#### Generation Issues

**Rollback to previous generation:**
Use the boot menu on restart, or temporarily switch:
```bash
/nix/var/nix/profiles/system-*-link/bin/switch-to-configuration test
```



### 6. Best Practices (Determinate Nix Patterns)

#### Use nixos-unstable Instead of master

**Reasoning:**
- `nixos-unstable`: Tested, passes Hydra CI
- `master`: Untested, may have broken packages

**Current setup:**
```nix
inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
```

#### Never Use --impure

**Problem:** Breaks reproducibility by allowing environment variable access

**Correct:**
```bash
nix flake check                # Pure evaluation
```

**Incorrect:**
```bash
nix flake check --impure     # BAD: non-reproducible
```

**Exception:** Only use `--impure` if flake explicitly uses `getEnv` or similar

#### Pin Dependencies in Lock File

**Why:**
- Ensures reproducible builds across machines
- Prevents "works on my machine" issues
- Required for CI/CD reliability

**How:**
```bash
# Always commit flake.lock
git add flake.lock
git commit -m "chore: update flake lock"
```

#### Use buildEnv for Package Groups

**Pattern in this repo:**
```nix
packages.default = pkgs.buildEnv {
  name = "system-packages";
  paths = [ git gh lazygit ... ];
};
```

**Benefits:**
- Single derivation for all packages
- Atomic updates (all packages succeed or fail together)

#### Enable Flakes in Config

**User-level config** (`~/.config/nix/nix.conf`):
```
experimental-features = nix-command flakes
```



### 7. Development Workflows

#### Create New Project Flake

**Use repository root as template:**
```bash
# Copy flake structure
cp flake.nix /path/to/new-project/

# Customize for project needs
cd /path/to/new-project
$EDITOR flake.nix
```

**Or use templates directory:**
```bash
# Use template (if available in .claude/skills/nix-manager/templates/)
nix flake init -t .#template-name
```

#### Test Flake Locally

**Without installing:**
```bash
# Enter dev shell
nix develop

# Build without installing
nix build

# Run specific package
nix run .#package-name
```

#### Format Nix Code

**Using formatter output:**
```bash
nix fmt  # Uses nixpkgs-fmt (defined in flake.nix)
```

**Manual formatting:**
```bash
nixpkgs-fmt flake.nix
```



### 8. Transient Agent Tooling (Daemon Profile)

This skill enables agents to maintain a local Nix profile in a user-provided directory, allowing dynamic installation of tools without requiring system-wide package management or sudo access.

#### Quick Start: Setting Up a Local Profile
The `DAEMON_PROFILE` env var is automatically set to `~/.local/state/daemon-profile` and its `bin` directory is added to the `$PATH` via Home Manager. The agent can use:

```bash
nix profile add --profile "$DAEMON_PROFILE" "nixpkgs#git"
```
The `--profile` flag stores the profile metadata in that location. 
*(Note: on older Nix versions, the `add` sub-command was called `install`).*

#### Essential Commands for Agents

**Search for Packages:**
```bash
# Search in nixpkgs flake
nix search nixpkgs git

# Search in specific (fully qualified) flake
nix search "github:user/repo[/branch]" <package-name>

# Get detailed JSON output
nix search nixpkgs python3 --json | jq '.[].pname'
```

**Manage Daemon Profile:**
```bash
# Add package
nix profile add --profile "$DAEMON_PROFILE" "<flake>#<package>"

# List installed packages
nix profile list --profile "$DAEMON_PROFILE"

# Remove by index or element number
nix profile remove --profile "$DAEMON_PROFILE" 0

# Upgrade packages
nix profile upgrade --profile "$DAEMON_PROFILE" <package_name>
nix profile upgrade --profile "$DAEMON_PROFILE" --all
```

#### General Agent Workflow
```bash
# 1. Verify profile path
echo $DAEMON_PROFILE

# 2. Search for the package
nix search nixpkgs git

# 3. Add it
nix profile add --profile "$DAEMON_PROFILE" "nixpkgs#git"

# 4. Use it!
git --version
```

**Important Details:**
- **Path**: The directory containing the profile (`$DAEMON_PROFILE/bin`) is automatically in `$PATH`.
- **Immutability**: `nixpkgs#git` resolves to the current nixpkgs version. Use `github:user/repo/ref#package` to pin.
- **Locking**: Only one agent should modify a profile at a time; locking is not automatic.

### 9. Output Format

When modifying flake.nix:

**Use Edit tool** for existing files:
- Modify specific sections
- Preserve comments and formatting
- Minimize diff size

**Use Write tool** for new files:
- Complete flake.nix from scratch
- Include comments explaining choices
- Follow repository formatting style

**After changes, always:**
1. Validate: targeted `nix eval` or `zcli deploy <host> --dry`
2. Apply: `zcli deploy <host>`
3. Report rollback generation to user

**Include testing commands:**
```bash
# Validate changes
nix flake check

# Show what changed
nix flake show
```

## Repository Patterns

This NixOS mesh repository follows these conventions:

**File Structure:**
- `flake.nix` - Package definitions and outputs
- `flake.lock` - Pinned dependency versions
- `hosts/` - Host-specific configuration (`nxiz`, `zrrh`, `adeck`)
- `modules/` - Shared configuration modules

**Package Organization:**
Packages grouped by purpose with comments:
```nix
paths = [
  # Version control
  git gh lazygit

  # Build tools
  gnumake cmake pkg-config

  # Programming languages
  rustup go python3 deno

  # ... etc
];
```

**Common Commands:**
- `zcli deploy <host> --dry` - Dry-run eval without applying
- `zcli deploy <host>` - Build and apply to a host
- `nh clean all` - Garbage collect

## Mesh Flake Idioms

Patterns this flake uses that agents must recognize and preserve.

### Custom `my.*` Option Namespace

Host identity and opt-in features flow through `my.*` options defined in `modules/system.nix` and `modules/performance.nix`:

```nix
# modules/system.nix
options.my.host = lib.mkOption {
  type = lib.types.enum [ "nxiz" "adeck" "zrrh" ];
  description = "Host identifier — selects per-host blocks in shared modules";
};

# modules/performance.nix
options.my.performance.enable = lib.mkEnableOption "system-wide performance optimizations";
```

Each host's `configuration.nix` sets `my.host = "<name>";` — every shared module keys off this.

### `perHost` Lookup Tables

Instead of cascading `lib.mkIf` checks, shared modules declare a `perHost` attrset and select with `h = perHost.${config.my.host}`. Found in `modules/{boot,networking,storage,nh}.nix`:

```nix
let
  perHost = {
    nxiz  = { flake = "/mnt/repository/nix-os"; resolvedDns = true; };
    adeck = { flake = "/etc/nixos"; resolvedDns = false; };
    zrrh  = { flake = "/etc/nixos"; resolvedDns = true; };
  };
  h = perHost.${config.my.host};
in {
  programs.nh.flake = h.flake;
  services.resolved.enable = h.resolvedDns;
}
```

When adding host-divergent config, extend `perHost` rather than sprinkling conditionals.

### Home Manager Integrated into NixOS

HM is bound into each `nixosConfiguration` via `home-manager.nixosModules.home-manager` in `flake.nix`. Key settings:

```nix
home-manager.useGlobalPkgs = true;        # share nixpkgs with system
home-manager.useUserPackages = true;      # install to /etc/profiles/per-user/zk
home-manager.backupFileExtension = "hm-bak";
home-manager.overwriteBackup = true;      # resolves dotfile collisions on deploy
home-manager.extraSpecialArgs = { inherit inputs; };  # threads flake inputs into HM
```

HM modules live under `modules/home/**` and per-host HM entry is `hosts/<host>/home.nix`.

### Inline Derivations in `home.packages`

Ad-hoc derivations live next to their install site — avoid creating separate files for one-off packages. Found in `hosts/{nxiz,adeck,zrrh}/home.nix`:

```nix
# Prebuilt binary with ELF patch
pkgs.runCommand "nullclaw-2026.3.1" {
  src = pkgs.fetchurl { url = "..."; hash = "..."; };
  nativeBuildInputs = [ pkgs.autoPatchelfHook ];
} ''install -Dm755 $src $out/bin/nullclaw''

# Go module from GitHub
pkgs.buildGoModule {
  pname = "picoclaw";
  src = pkgs.fetchFromGitHub { owner = "..."; repo = "..."; rev = "..."; hash = "..."; };
  vendorHash = "...";
}

# Shell wrapper with runtime deps
pkgs.writeShellApplication {
  name = "fzf-emoji";
  runtimeInputs = [ fzf jq wl-clipboard curl coreutils ];
  text = ''...'';
}
```

Rule of thumb: if it's one derivation used in one place, inline it. If it's used across hosts, make it a module with `options.programs.<name>` (see `modules/home/msgvault.nix` for the reference pattern: `mkEnableOption` + `mkOption` + `lib.mkIf cfg.enable`).

### Overlays for Upstream Fixes

`modules/overlays.nix` holds all `overrideAttrs` surgeries. Pattern is always `_final: prev: { pkg = prev.pkg.overrideAttrs (old: {...}); }`. Real examples:

- `tumbler` rebuilt without `libgepub` to drop webkitgtk dep
- `lmstudio` rebuilt with patchelf to fix Bun ELF layout corruption
- `yaziPlugins` namespace created from `flake = false` input source tree

Input-provided overlays are applied per-host in `flake.nix` via `nixpkgs.overlays = [ inputs.nix-cachyos-kernel.overlays.pinned ];`.

### agenix Secret Flow

Secrets encrypted with recipient SSH keys, decrypted at boot into `/run/secrets/`:

```nix
# modules/user.nix
age.identityPaths = [
  "/etc/ssh/ssh_host_ed25519_key"
  "/home/zk/.ssh/id_ed25519"
];

age.secrets.github-token = {
  file = ../secrets/github-token.age;
  owner = "zk"; group = "users"; mode = "0400";
  path = "/run/secrets/github-token";
};
```

Recipients declared in `secrets/secrets.nix` (per-file `publicKeys` list). To add a new secret: `agenix -e secrets/new.age` (after adding to `secrets.nix`), then reference via `config.age.secrets.new.path` in the module.

### Home Activation + DAG Ordering

HM activation scripts use `config.lib.dag.entryAfter [ "writeBoundary" ]` to run after file symlinks are in place:

```nix
home.activation.ensureLocalBin = config.lib.dag.entryAfter [ "writeBoundary" ] ''
  mkdir -p "$HOME/.local/bin"
'';
```

System activation uses `system.activationScripts.<name> = { text = "..."; deps = [ "etc" ]; }` — the `deps` list controls ordering (e.g. SSH host key staging runs after `/etc` is populated).

### `mkOutOfStoreSymlink` for Live Files

For dotfiles that point at mutable paths outside `/nix/store` (edited live, not baked into the system closure):

```nix
home.file.".pi".source = config.lib.file.mkOutOfStoreSymlink
  "/mnt/repository/daemonturgy/pi/.pi";
```

Use for editable config dirs, large data caches, or anything that shouldn't trigger a rebuild on change.

### Flake Outputs (Current)

- `nixosConfigurations.{nxiz,adeck,zrrh}` — host configs
- `formatter.x86_64-linux` — `nixfmt-rfc-style` (run `nix fmt`)
- `devShells.x86_64-linux.default` — includes `nixd`, `nil`, `nixfmt`, `statix`, `deadnix` (`nix develop`)
- `checks.x86_64-linux.{statix,deadnix}` — lint gates (`nix flake check`)

Run `nix fmt` before committing `.nix` changes. Run `nix flake check --no-build` to catch lint regressions cheaply.

## Reference Documentation

- Determinate Installer: https://determinate.systems/blog/determinate-nix-installer/
- Zero to Nix (Flakes): https://zero-to-nix.com/concepts/flakes/
- Nix.dev (Flakes): https://nix.dev/concepts/flakes.html
- NixOS Wiki: https://nixos.wiki/wiki/Flakes


## Quick Reference

**Essential Commands:**
```bash
# Deploy
zcli deploy <host>                   # Apply flake changes
zcli deploy <host> --dry             # Dry-run eval, no switch
zcli deploy all                      # Deploy all mesh hosts

# Targeted evaluation (prefer over full deploy for validation)
nix eval /mnt/repository/nix-os#nixosConfigurations.<host>.config.<attr>
nix build /mnt/repository/nix-os#nixosConfigurations.<host>.config.system.build.toplevel --dry-run
nix flake check /mnt/repository/nix-os --no-build

# Package discovery (use mcp-nixos first)
nix search nixpkgs <package>         # Fallback search

# Flake management
nix flake update /mnt/repository/nix-os   # Update all inputs
nix flake show /mnt/repository/nix-os     # Display outputs
nix flake metadata /mnt/repository/nix-os # Show metadata

# Garbage collection
nh clean all                         # Clean old generations
nix store gc --dry-run               # Preview cleanup

# Development
nix develop                          # Enter dev shell
nix fmt                              # Format Nix code
nix shell nixpkgs#<tool>             # Transient tool (one-shot)
```
