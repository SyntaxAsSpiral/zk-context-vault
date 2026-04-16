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
