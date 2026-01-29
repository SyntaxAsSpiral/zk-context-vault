AT---
name: zk-mesh
description: Workflow for managing ZRRH/Deck NixOS flakes, remote rebuilds, and mesh SSH from ZRRH or amexsomnemon. Use for NixOS rebuilds, channel repair, and flake deploys across the mesh.
---

# zk-mesh

Use this skill when working on NixOS config or rebuild/deploy across ZRRH (Windows + WSL) and amexsomnemon (Deck NixOS).

## Guardrails

- Only run `nixos-rebuild` when explicitly asked.
- On the Deck, prefer tmux for long-running operations.
- Avoid running Nix builds from `/mnt/c` in WSL. Use `/home/<user>/...`.
- Use `/run/wrappers/bin/sudo` and `/run/current-system/sw/bin` on the Deck if PATH is broken.
- Keep commands in Unix-style paths with forward slashes.
- **NEVER write Linux config files from Windows filesystem**—CRLF line endings will corrupt shell scripts and break PATH. Always write/edit within WSL or directly on the target.
- **NEVER run rebuilds without explicit operator request**—these are long-running and can't be safely interrupted.

## Paths and context

- WSL home: `/home/zk` (use Linux paths; never Windows paths in commands)
- Deck NixOS config: `/etc/nixos`
- WSL flakes:
  - `/home/zk/nix/flake-zk`
  - `/home/zk/nix/flake-deck`

## Deck (amexsomnemon) operations

### Safe shell PATH

```
/run/current-system/sw/bin/env PATH=/run/wrappers/bin:/run/current-system/sw/bin:/nix/var/nix/profiles/default/bin:$PATH
```

### Repair channels / NIX_PATH

```
/run/wrappers/bin/sudo /run/current-system/sw/bin/nix-channel --list
/run/wrappers/bin/sudo /run/current-system/sw/bin/nix-channel --remove nixos 2>/dev/null || true
/run/wrappers/bin/sudo /run/current-system/sw/bin/nix-channel --add https://nixos.org/channels/nixos-25.11 nixos
/run/wrappers/bin/sudo /run/current-system/sw/bin/nix-channel --update
```

### Rebuild (non-flake)

```
/run/wrappers/bin/sudo /run/current-system/sw/bin/nixos-rebuild switch
```

### Rebuild (flake)

```
/run/wrappers/bin/sudo /run/current-system/sw/bin/nixos-rebuild switch --flake /etc/nixos
```

### If rebuild fails with world-writable path

```
/run/wrappers/bin/sudo /run/current-system/sw/bin/stat -c "%A %a %U %G %N" / /nix /nix/var /nix/var/nix /nix/var/nix/builds
/run/wrappers/bin/sudo /run/current-system/sw/bin/chmod 755 /
```

### Check where /nix is mounted (SD vs SSD)

```
/run/current-system/sw/bin/findmnt /nix
```

### Increase Nix download buffer (if fetch/unpack is slow)

```
/run/current-system/sw/bin/nix show-config | /run/current-system/sw/bin/rg -i download-buffer
```

Add to `configuration.nix` and rebuild:

```
nix.settings.download-buffer-size = 33554432; # 32 MiB
```

### tmux session (recommended)

```
/run/current-system/sw/bin/tmux new -s codex
# detach: Ctrl-b d
# reattach:
/run/current-system/sw/bin/tmux attach -t codex
```

## ZRRH (Windows + WSL) operations

### Install Nix in WSL (single-user)

```
sudo apt update && sudo apt install -y curl
sh <(curl -L https://nixos.org/nix/install) --no-daemon
. ~/.nix-profile/etc/profile.d/nix.sh
mkdir -p ~/.config/nix
printf 'experimental-features = nix-command flakes\n' > ~/.config/nix/nix.conf
```

### Keep flakes on WSL filesystem

```
cd ~
mkdir -p ~/nix/flake-zk ~/nix/flake-deck
```

### Deploy Deck from WSL (build here, switch on Deck)

```
nix run nixpkgs#nixos-rebuild -- switch --flake /home/zk/nix/flake-deck#amexsomnemon --target-host deck@amexsomnemon --sudo
```

Note: `--use-remote-sudo` is deprecated, use `--sudo` instead.

**Prerequisites**: The Deck must have the `environment.shellInit` PATH fix applied locally first. See "PATH fix for remote deploys" section.

### Copy Deck config into WSL flake

```
ssh -i ~/.ssh/id_ed25519 deck@amexsomnemon '/run/current-system/sw/bin/env PATH=/run/current-system/sw/bin:/run/wrappers/bin /run/wrappers/bin/sudo -n /run/current-system/sw/bin/tar -C /etc -czf - nixos' | /bin/tar -C /home/zk/nix/flake-deck -xzf -
```

## Flake skeletons

### Deck flake (example)

```
{
  description = "NixOS config for amexsomnemon";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
  };

  outputs = { self, nixpkgs }:
  {
    nixosConfigurations.amexsomnemon = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [ ./nixos/configuration.nix ];
    };
  };
}
```

### ZRRH flake (template)

```
{
  description = "NixOS config for zrrh";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
  };

  outputs = { self, nixpkgs }:
  {
    nixosConfigurations.zrrh = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [ ./nixos/configuration.nix ];
    };
  };
}
```

## Troubleshooting quick hits

- If commands are missing on Deck, use the full paths in this file.
- If `nixos-rebuild` complains about NIX_PATH, repair channels.
- If `sudo` fails, call `/run/wrappers/bin/sudo` directly.
- If SSH drops, run builds inside tmux.
- If you see `$'\r': command not found`, CRLF line endings corrupted the file. Fix with:
  ```
  /run/wrappers/bin/sudo /run/current-system/sw/bin/sed -i 's/\r$//' /etc/nixos/configuration.nix
  ```
- If `nix-copy-closure` fails with `nix-store: command not found`, the Deck's PATH isn't set for non-interactive SSH. See "PATH fix for remote deploys" below.

## PATH fix for remote deploys

Remote deploys via `nix-copy-closure` run commands in non-interactive SSH sessions where `profile.local`, `bashrc.local`, and `interactiveShellInit` don't apply. Add this to `configuration.nix`:

```nix
# Force PATH for ALL shell invocations (including non-interactive SSH commands)
environment.shellInit = ''
  export PATH="/run/wrappers/bin:/run/current-system/sw/bin:/nix/var/nix/profiles/default/bin:$PATH"
'';
```

**Bootstrap problem**: You must apply this fix locally on the Deck first before remote deploys will work:

```
/run/wrappers/bin/sudo /run/current-system/sw/bin/nixos-rebuild switch
```

## Garbage collection

Build garbage accumulates fast during iteration. Clean up periodically:

```bash
# Remove dead store paths (keeps all generations)
/run/wrappers/bin/sudo /run/current-system/sw/bin/nix-collect-garbage

# Delete ALL old generations + garbage (nuclear option, loses rollback)
/run/wrappers/bin/sudo /run/current-system/sw/bin/nix-collect-garbage -d

# Check how much garbage exists before cleaning
/run/current-system/sw/bin/nix-store --gc --print-dead | /run/current-system/sw/bin/wc -l
```

When building remotely from ZRRH, build garbage stays in WSL's `/nix/store` instead of the Deck. Generation garbage still accumulates on the Deck with each `switch`.