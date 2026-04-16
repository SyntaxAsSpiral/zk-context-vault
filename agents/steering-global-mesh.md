---
inclusion: always
---

# Mesh Infrastructure

## Tailscale Mesh — tail293e98.ts.net (SyntaxAsSpiral)

| Host | Tailscale IP | MAC Address | OS | Status |
|------|--------------|-------------|-------|--------|
| nxiz | 100.115.135.104 | FC:34:97:3B:6E:99 (enp10s0) | NixOS 26.05 (Yarara) | online |
| zrrh | 100.77.90.79 | 60:CF:84:61:D8:00 (eno1, DOWN), B0:DC:EF:2F:7B:0F (wlp9s0, active) | NixOS 26.05 (Yarara) | offline |
| adeck | 100.89.32.9 | 10:82:86:2A:E0:00 (enp4s0f3u1u4c2, DOWN), 50:5A:65:26:0F:CD (wlo1, active) | NixOS 26.05 (Yarara) | online |
| zdeck | 100.64.136.57 | - | SteamOS | online |
| quita | 100.82.51.63 | - | Linux Mint | offline |
| zk-pixel | 100.96.213.111 | - | Android | offline |
| zk-note | 100.105.239.55 | - | Android | online |

## nxiz — FC:34:97:3B:6E:99 — 100.115.135.104

**Role:** Workstation  
**OS:** NixOS 26.05 (Yarara)  
**GPU:** NVIDIA RTX 3070

### Storage

| Device | Size | Type | UUID/Label | Mount | Taildrive Share |
|--------|------|------|------------|-------|-----------------|
| nvme0n1p1 | 1G | vfat | boot (90B6-5EC8) | /boot | - |
| nvme0n1p2 | 325.9G | btrfs | NXIZ (b3821fe9) | / (subvols) | - |
| sda1 | 838.2G | btrfs | Repository (0d00b77b) | /mnt/repository | `repository` |
| sdb1 | 931.5G | btrfs | Archive (619e6bb2) | /mnt/archive | `archive` |

**Context vault:** `/mnt/repository/context-vault`

### Services

**LM Studio (local + mesh-accessible):**
- Endpoint: `http://localhost:1234` (mesh-accessible for trusted peers)
- Usage: Handles embeddings and small-model inference tasks; shared inference split across nxiz + zrrh depending on workload

## zrrh — 100.77.90.79

**Role:** Daemon Forge  
**OS:** NixOS 26.05 (Yarara)  
**GPU:** NVIDIA RTX 4090 (primary inference GPU)

### Storage

| Device | Size | Type | UUID/Label | Mount | Taildrive Share |
|--------|------|------|------------|-------|-----------------|
| nvme0n1p1 | 1G | vfat | boot (C5FA-F364) | /boot | - |
| nvme0n1p2 | 1.5T | btrfs | ZRRH (43b13d4c) | / , /home, /nix/store | - |
| nvme1n1p1 | 1.3T | btrfs | Media (112f1862) | /mnt/media | `media` |
| nvme1n1p2 | 2T | btrfs | Games (7b93a14d) | /mnt/games | `games` |
| zram | 31G | swap | - | - | - |

## adeck — 100.89.32.9

**Role:** Agentic Server / Relay (always on)  
**OS:** NixOS 26.05 (Yarara)
**Hardware:** Valve Jupiter (Steam Deck)
**Note:** This device carries memorial significance. 🕯️

### Storage

| Device | Size | Type | UUID/Label | Mount | Taildrive Share |
|--------|------|------|------------|-------|-----------------|
| mmcblk0p1 | 1G | vfat | boot (0F7B-533B) | /boot | - |
| mmcblk0p2 | 150G | ext4 | ADECK (43631aea) | / , /nix/store | - |
| sda1 | 931.5G | btrfs | Echo (ba0a8294) | /mnt/echo | `echo` |
| sdb | 1.8T | btrfs | vault (b802e750) | /mnt/vault | `vault` |
| nvme0n1p8 | 466.3G | ext4 | 67dcc5ae | /mnt/adam-steam | - |

### Taildrive Mounts

| Remote Share | Local Mount |
|--------------|-------------|
| nxiz/repository | /mnt/taildrive/repository |
| zrrh/media | /mnt/taildrive/media |

### Services

**pulse-generator (systemd timer):**
- Schedule: Daily at 02:24 PST
- Script: `src/github_status_rotator.py` from `/home/zk/lexemancy-site/` venv
- Domain: lexemancy.com (GitHub Pages)
- Local copy: `zk@adeck:~/lexemancy-site/` (synced via git)

**Other services:**
- **Inference Gateway (adeck:1234):** ALL inference requests must be directed to `adeck:1234`. `adeck` acts as the mesh-wide router/gateway; it uses `lmlink` to JIT-load and route models to the appropriate hardware (`zrrh` for large models, `nxiz`/ `adeck` local for small models/embeddings).
- Docker (enabled for agent/service workloads)
- qBittorrent
- SSH
- Tailscale
- msgvault
- Hermes agent
- zk data lake
- sideriod gnomon

## zdeck — 100.64.136.57

**Role:** Gaming  
**OS:** SteamOS  
**Note:** Verified online on the mesh alongside `adeck` at `100.64.136.57`. `zdeck` is Zach's Steam Deck and previously hosted the `adeck` partition before `adeck` moved onto Adam's former Steam Deck hardware.

## quita — 100.82.51.63

**Role:** Family laptop (remote support)  
**OS:** Linux Mint  
**Note:** Quita's old laptop, reimaged for family use. Tailscale mesh for remote access/support.

## Mesh Orchestration (zcli)

`zcli` is the primary wrapper for managing NixOS configurations across the mesh. It automates the distributed build process, ensuring that computationally expensive evaluations and builds are offloaded to `zrrh`.

### Distributed Build Logic

- **Control Host:** `zrrh` (Daemon Forge) acts as the central build server.
- **Evaluation:** Happens locally on the host where `zcli` is executed (e.g., `nxiz` or `adeck`).
- **Build:** Offloaded to `zrrh` via SSH/Tailscale when executed from remote hosts.
- **Deploy:** Updates the target host's configuration.

### Usage

```bash
# Dry-run eval to check for errors/changes
zcli deploy nxiz --dry

# Deploy (build + switch) configuration to a host
zcli deploy nxiz

# Deploy to all known mesh hosts
zcli deploy all
```

### Automation Details

- **Auto-Staging:** `zcli` automatically runs `git -C <flake> add -A` before execution to ensure all local changes (including new files) are included in the build.
- **Local Source:** Uses the local flake directory directly (`/mnt/repository/nix-os`); no manual git pushing is required for deployment.
- **Connectivity Check:** Verifies Tailscale connectivity to `zrrh` and target hosts before starting.

## Development Mandates

To maintain mesh integrity and reproducibility, the following principles apply:

- **Nix-First Tooling:** Prefer Nix for all package management. Avoid using imperative package managers (`pip`, `npm`, `cargo`, etc.) for global or user-profile installations.
- **Root Flakes for Projects:** If a project requires specific tooling or dependencies not provided by the global mesh configuration, use a root `flake.nix`. This ensures a declarative, reproducible environment via `nix develop` or `direnv`.
- **Transient Agent Tooling:** Agents should feel free to use `nix shell` (or `nix run`) to temporarily acquire any specialized tools or utilities needed for a specific task without modifying the permanent system configuration.
- **Declarative Preference:** Aim for reproducibility. Minimize operations that bypass the Nix store or introduce non-declarative state to the system.

## Taildrive Mesh Summary

**Shares:**
- `nxiz/repository` → `/mnt/repository` (838.2G btrfs) - Context vault and development repositories
- `nxiz/archive` → `/mnt/archive` (931.5G btrfs) - Archive storage
- `zrrh/media` → `/mnt/media` (1.3T btrfs) - Media library
- `zrrh/games` → `/mnt/games` (2T btrfs) - Game storage
- `adeck/vault` → `/mnt/vault` (1.8T btrfs) - Data lake staging + subvolume storage (@staging, @raw, @temp)
- `adeck/echo` → `/mnt/echo` (931.5G btrfs) - Hot storage for processed knowledge

**Consumers:**
- `adeck` mounts: `nxiz/repository`, `zrrh/media`

## Taildrop File Transfer

**Inbox:** `/tmp/taildrop-inbox/` on nxiz

Files sent from phones or other mesh nodes via Taildrop land here but require explicit retrieval:

```bash
# Retrieve pending files (requires sudo)
sudo tailscale file get /tmp/taildrop-inbox/

# Check inbox contents
ls -lt /tmp/taildrop-inbox/
```

**Notes:**
- Files are owned by root after retrieval
- The inbox is in `/tmp` — contents do not survive reboot
- Taildrop sends show as "delivered" on the sender before retrieval on the receiver — always run `sudo tailscale file get` to flush pending transfers
- `tailscale file get` without sudo will fail with "Access denied" unless `sudo tailscale set --operator=$USER` has been run
