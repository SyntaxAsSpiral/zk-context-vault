---
inclusion: always
---

# Mesh Infrastructure — amexsomnemon relay

**CRITICAL:** When writing commands or scripts, NEVER use Windows paths (C:/, backslashes). Always use Unix-style paths with forward slashes, even on Windows machines. SSH commands handle path translation automatically.

## Role & Principles (amexsomnemon)
- Relay/orchestration node for the mesh.
- Keep OS minimal; prefer remote storage for bulk data.
- Treat automation as non-interactive; prefer deterministic, minimal-diff changes.
- Use forward-slash paths everywhere; avoid backslashes in commands/scripts.

## Tailnet Devices
| Host | IP | OS | Role |
|------|----|----|------|
| zrrh | 100.70.89.47 | Win11 | Primary workstation |
| zrrh-wsl | 100.96.87.95 | WSL2 | Linux subsystem (zrrh) |
| nix | 100.80.244.38 | NixOS | NixOS partition (zrrh) |
| smnm | 100.95.254.19 | Win11 | Secondary workstation |
| amexsomnemon | 100.113.87.50 | NixOS | Exocortex relay (Steam Deck) |
| zdeck | 100.64.136.57 | SteamOS | Gaming (offline when amexsomnemon) |
| zk-pixel | 100.96.213.111 | Android | Mobile (Pixel, primary w/ SIM) |
| zk-note | 100.105.239.55 | Android | Control surface (home/network via Termius) |

## SSH Quick Reference
**From amexsomnemon:** `ssh zk@zrrh` or `ssh zk@smnm`
**From Windows hosts:** `ssh deck@amexsomnemon`

**Keys:**
- ZRRH/SMNM inbound: `C:/ProgramData/ssh/administrators_authorized_keys`
- amexsomnemon outbound: `~/.ssh/id_ed25519`
- amexsomnemon inbound: `~/.ssh/authorized_keys`

## amexsomnemon (NixOS/Steam Deck)
**Boot:** Insert microSD, hold Vol Down + Power, select microSD
**Login:** deck/deck | **Timezone:** America/Los_Angeles
**Storage:** Root: microSD (~59GB)
**Config:** `/etc/nixos/configuration.nix` → `sudo nixos-rebuild switch`
**Packages:** git, curl, wget, htop, neovim, nodejs_22, npm, pnpm, tailscale, ntfs3g, vscode
**AI CLIs:** claude-code (native), gemini-cli, codex-cli

**Screen control:**
```bash
# Off: ssh deck@amexsomnemon "sudo sh -c 'echo 1 > /sys/class/graphics/fb0/blank'"
# On:  ssh deck@amexsomnemon "sudo sh -c 'echo 0 > /sys/class/graphics/fb0/blank' && echo 100 | sudo tee /sys/class/backlight/amdgpu_bl1/brightness"
```

## Topology
```
        Tailscale Tailnet
    ┌────────┼────────┐
  ZRRH  amexsomnemon  SMNM
(Win11)  (NixOS)    (Win11)
          relay
```

**Notes:** zdeck/amexsomnemon share hardware (boot select). amexsomnemon is the relay host for mesh orchestration.
