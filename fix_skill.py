import re

with open('skills/nix-os/SKILL.md', 'r') as f:
    content = f.read()

# 1. Context block
content = content.replace(
"""Check current Nix setup:
- **Flake location**: `/Users/wcygan/Development/dotfiles/flake.nix`
- **Installation script**: `scripts/install-packages.sh`
- **Package management**: `nix profile` (user-scoped, modern approach)
- **Installer**: Determinate Systems installer (macOS/Linux)
- **Update mechanism**: `make update` or `nix flake update && nix profile upgrade`""",
"""Check current Nix setup:
- **Flake location**: `/mnt/repository/nix-os/`
- **Package management**: Declarative NixOS configuration via flakes.
- **Update mechanism**: `zcli deploy <host>` or `nh os switch`"""
)

# 2. Supported systems
content = content.replace("- Supported systems: x86_64-linux, aarch64-linux, x86_64-darwin, aarch64-darwin", "- Supported systems: x86_64-linux")

# 3. Package Management Operations
old_pkg_mgmt = """### 2. Package Management Operations

#### Install New Package

**Process:**
1. Add package to `flake.nix` in appropriate category
2. Run `nix flake check` to validate
3. Run `nix profile upgrade dotfiles` to apply changes
4. Test package availability

**Example:**
```nix
# flake.nix packages section
paths = [
  # ... existing packages ...

  # New package
  cowsay  # Fun terminal tool
];
```

```bash
# Validate and install
nix flake check
nix profile upgrade dotfiles
which cowsay  # Verify installation
```

#### Update All Packages

**Process:**
```bash
# Update flake inputs (updates nixpkgs revision)
nix flake update

# Apply updates to installed profile
nix profile upgrade dotfiles

# Verify no breakage
nix profile list
```

Or use Makefile shortcut:
```bash
make update  # Runs both commands above
```

#### Remove Package

**Process:**
1. Remove from `flake.nix`
2. Run `nix flake check`
3. Run `nix profile upgrade dotfiles`
4. Old package remains in store but not in PATH

**Note**: Garbage collection removes unreferenced packages:
```bash
make clean  # or: nix-collect-garbage -d
```"""

new_pkg_mgmt = """### 2. Package Management Operations

#### Install New Package

**Process:**
1. Add package to appropriate module in `/mnt/repository/nix-os/`
2. Validate changes
3. Run `zcli deploy <host>` or `nh os switch` to apply changes
4. Test package availability

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
```"""

content = content.replace(old_pkg_mgmt, new_pkg_mgmt)

# 4. Darwin packages
content = content.replace("""**Add platform-specific packages:**
```nix
paths = [
  # Universal packages
  git gh lazygit
] ++ lib.optionals stdenv.isDarwin [
  # macOS-only
  darwin.apple_sdk.frameworks.Security
] ++ lib.optionals stdenv.isLinux [
  # Linux-only
  libnotify
];
```""", """**Add host-specific packages:**
```nix
paths = [
  # Universal packages
  git gh lazygit
] ++ lib.optionals (config.networking.hostName == "nxiz") [
  # nxiz-only
  nvidia-vaapi-driver
];
```""")

# 5. Make test-pre
content = content.replace('echo "Run: make test-pre"', 'echo "Ready for development."')

# 6. Profile issues
old_profile_issues = """#### Profile Issues

**List installed profiles:**
```bash
nix profile list
```

**Output format:**
```
Index:              0
Flake attribute:    legacyPackages.aarch64-darwin.dotfiles
Original flake URL: git+file:///Users/wcygan/Development/dotfiles
Locked flake URL:   git+file:///Users/wcygan/Development/dotfiles?rev=...
Store paths:        /nix/store/...-system-packages
```

**Rollback to previous generation:**
```bash
nix profile rollback
```

**Remove specific profile:**
```bash
nix profile remove <index-number>
```"""

new_gen_issues = """#### Generation Issues

**Rollback to previous generation:**
Use the boot menu on restart, or temporarily switch:
```bash
/nix/var/nix/profiles/system-*-link/bin/switch-to-configuration test
```"""

content = content.replace(old_profile_issues, new_gen_issues)

# 7. CI/CD
old_ci_cd = """### 5. CI/CD Integration

This repository uses **Determinate Systems GitHub Actions** for CI.

**GitHub Actions setup** (`.github/workflows/ci.yml`):
```yaml
- name: Setup Nix cache
  uses: DeterminateSystems/magic-nix-cache-action@v2

- name: Install Nix
  uses: DeterminateSystems/nix-installer-action@v14
  with:
    extra-conf: |
      experimental-features = nix-command flakes

- name: Run install script
  run: ./install.sh
```

**Benefits:**
- Magic Nix Cache: ~90% faster CI (uses GitHub Actions cache)
- Automatic cache population
- No configuration required

**Local equivalent:**
```bash
# Test installation in Docker
make test-docker

# Test idempotency
./install.sh && ./install.sh  # Should succeed twice
```"""

content = content.replace(old_ci_cd, "")

# 8. Impure profile add
old_impure = """**Correct:**
```bash
nix profile add .              # Pure evaluation
nix profile upgrade dotfiles   # Pure evaluation
```"""
new_impure = """**Correct:**
```bash
nix flake check                # Pure evaluation
```"""
content = content.replace(old_impure, new_impure)

content = content.replace("""**Incorrect:**
```bash
nix profile add . --impure     # BAD: non-reproducible
```""", """**Incorrect:**
```bash
nix flake check --impure     # BAD: non-reproducible
```""")

# 9. buildEnv pattern repo reference
content = content.replace("""**Benefits:**
- Single derivation for all packages
- Atomic updates (all packages succeed or fail together)
- Easier to manage than individual `nix profile install` calls""", """**Benefits:**
- Single derivation for all packages
- Atomic updates (all packages succeed or fail together)""")

content = content.replace("**This is automatically set by `scripts/install-packages.sh`**", "")

# 11. Migration Guidance
old_migration = """### 8. Migration Guidance

#### From Homebrew

**Don't uninstall Homebrew**—it coexists peacefully. Fish PATH priority:
1. Homebrew (`/opt/homebrew/bin`) - highest priority
2. User bins (`~/.local/bin`, `~/bin`)
3. Language toolchains (`~/.cargo/bin`, `~/go/bin`)
4. **Nix** (`~/.nix-profile/bin`) - lowest priority

**Migration strategy:**
```bash
# 1. Install package via Nix
# (add to flake.nix and run nix profile upgrade)

# 2. Test package works
which package-name  # Should show Homebrew path (higher priority)

# 3. Uninstall from Homebrew
brew uninstall package-name

# 4. Verify Nix version now active
which package-name  # Should show /nix/store/... path
```

#### From apt/dnf

**Linux distros:**
- Nix coexists with system package managers
- System packages have priority over Nix (via PATH ordering)
- Use Nix for tools not in distro repos or needing newer versions"""
content = content.replace(old_migration, "")

# 12. Output Format
old_output_fmt = """3. Apply: `nix profile upgrade dotfiles`
4. Verify: `nix profile list`

**Include testing commands:**
```bash
# Validate changes
nix flake check

# Show what changed
nix flake show

# Apply updates
nix profile upgrade dotfiles
```"""
new_output_fmt = """3. Apply: `zcli deploy <host>` or `nh os switch`

**Include testing commands:**
```bash
# Validate changes
nix flake check

# Show what changed
nix flake show
```"""
content = content.replace(old_output_fmt, new_output_fmt)

# 13. Repository Patterns
old_repo_patterns = """## Repository Patterns

This dotfiles repository follows these conventions:

**File Structure:**
- `flake.nix` - Package definitions and outputs
- `flake.lock` - Pinned dependency versions
- `scripts/install-packages.sh` - Installation wrapper
- `scripts/link-config.sh` - Dotfile symlinking
- `config/` - Dotfile configurations (fish, starship, etc.)"""
new_repo_patterns = """## Repository Patterns

This NixOS mesh repository follows these conventions:

**File Structure:**
- `flake.nix` - Package definitions and outputs
- `flake.lock` - Pinned dependency versions
- `hosts/` - Host-specific configuration (`nxiz`, `zrrh`, `adeck`)
- `modules/` - Shared configuration modules"""
content = content.replace(old_repo_patterns, new_repo_patterns)

# 14. Testing and Commands
old_testing = """**Testing:**
- `make test-pre` - Pre-flight validation
- `make test-local` - Ephemeral HOME test
- `make test-docker` - Multi-distro Docker matrix

**Common Commands:**
- `make install` - Run full installation
- `make update` - Update flake + upgrade packages
- `make clean` - Garbage collect
- `make verify` - Check Nix installation health"""
new_testing = """**Common Commands:**
- `zcli build <host> --dry` - Verify evaluation without applying
- `zcli deploy <host>` - Build and apply to a host
- `nh clean all` - Garbage collect"""
content = content.replace(old_testing, new_testing)

# 15. Ref links
content = content.replace("- Repository: /Users/wcygan/Development/dotfiles/", "")
content = content.replace("- **Nix Manager**: https://github.com/wcygan/dotfiles/tree/main/.claude/skills/nix-manager", "")

# 16. Quick reference
old_quick_ref = """# Package management
nix search nixpkgs <package>     # Search for package
nix profile list                 # List installed packages
nix profile upgrade dotfiles     # Apply flake changes
nix-collect-garbage -d           # Clean old generations"""
new_quick_ref = """# Package management
nix search nixpkgs <package>     # Search for package
nh clean all                     # Clean old generations
zcli deploy <host>               # Apply flake changes"""
content = content.replace(old_quick_ref, new_quick_ref)
content = content.replace("nix profile rollback             # Revert to previous\n", "")

with open('skills/nix-os/SKILL.md', 'w') as f:
    f.write(content)
