---
inclusion: always
---

# Mesh Infrastructure

## Tailscale Mesh — tail293e98.ts.net (SyntaxAsSpiral)

| Host | Tailscale IP | MAC Address | OS | Status |
|------|--------------|-------------|-------|--------|
| nxiz | 100.115.135.104 | FC:34:97:3B:6E:99 (enp10s0) | NixOS 26.05 (Yarara) | online |
| zrrh | 100.126.60.24 | 60:CF:84:61:D8:00 (ethernet), B0:DC:EF:2F:7B:0F (wifi, active) | Garuda Linux | online |
| adeck | 100.89.32.9 | 80:6D:97:AB:3A:FC (dock, DOWN), 50:5A:65:1F:84:9D (wifi, active) | NixOS 26.05 (Yarara) | online |
| zdeck | 100.64.136.57 | - | SteamOS | offline |
| zk-pixel | 100.96.213.111 | - | Android | online |
| zk-note | 100.105.239.55 | - | Android | online |

## nxiz — FC:34:97:3B:6E:99 — 100.115.135.104

**Role:** Primary Workstation  
**OS:** NixOS 26.05 (Yarara)  
**GPU:** NVIDIA RTX 3070

### Storage

| Device | Size | Type | UUID/Label | Mount | Taildrive Share |
|--------|------|------|------------|-------|-----------------|
| nvme0n1p1 | 512M | vfat | - | /boot | - |
| nvme0n1p2 | 476.4G | btrfs | - | / (subvols) | - |
| sdb1 | 838.2G | btrfs | - | /mnt/repository | `repository` |
| sda1 | 931.5G | btrfs | - | /mnt/archive | - |

**Context vault:** `/mnt/repository/context-vault`

## zrrh — 100.126.60.24

**Role:** Couch PC / Local Inference  
**OS:** Garuda Linux  
**GPU:** NVIDIA RTX 4090 (primary inference GPU)

### Storage

| Device | Size | Type | UUID/Label | Mount | Taildrive Share |
|--------|------|------|------------|-------|-----------------|
| nvme0n1p1 | 512M | vfat | 5996-AD7F | /boot/efi | - |
| nvme0n1p2 | 1.8T | btrfs | ZRRH (a94ba4f7) | / (subvols: @, @home, @root, @srv, @cache, @log, @tmp) | - |
| nvme1n1p1 | 1.3T | btrfs | Media (112f1862) | /mnt/media | `media` |
| nvme1n1p2 | 2T | btrfs | Games (7b93a14d) | /mnt/games | - |
| zram | 61.9G | swap | - | - | - |

### Services

**llmster (LM Studio headless daemon):**
- Endpoint: `http://zrrh:1234` (accessible via Tailscale mesh)
- API: OpenAI-compatible (`/v1/models`, `/v1/chat/completions`, `/v1/embeddings`)
- Available models: gpt-oss-20b, seed-oss-36b, qwen3-30b-a3b-thinking distill, granite-4-h-tiny, olmo-3-32b-think, ernie-4.5-21b-a3b, dolphin-mistral-24b, phi4-trader, lfm2-1.2b, financial-gpt-oss-20b
- Embedding models: nomic-embed-text-v1.5, qwen3-embedding-4b, mxbai-embed-large-v1

## adeck — 100.89.32.9

**Role:** Headless Agentic Server / Relay (always on)  
**OS:** NixOS 26.05 (Yarara)

### Storage

| Device | Size | Type | UUID/Label | Mount | Taildrive Share |
|--------|------|------|------------|-------|-----------------|
| mmcblk0p1 | 512M | vfat | 0F7B-533B | /boot | - |
| mmcblk0p2 | 237.9G | ext4 | 43631aea | / | - |
| nvme0n1 | 476.9G | - | - | unmounted (legacy SteamOS) | - |
| sda | 1.8T | btrfs | vault (b802e750) | /mnt/vault | `vault` |

### Taildrive Mounts

| Remote Share | Local Mount |
|--------------|-------------|
| nxiz/repository | /mnt/taildrive/repository |
| zrrh/media | /mnt/taildrive/media |

### Services

**pulse-generator (systemd timer):**
- Schedule: Daily at 02:24 PST
- Script: `src/github_status_rotator.py` from `/home/zk/pulse-log/` venv
- Domain: lexemancy.com (GitHub Pages)
- LLM backends: OpenRouter (kimi-k2 primary), fallback chain → deepseek-v3.2, local llmster (gpt-oss-20b-heretic via localhost:1234), gemini-3-flash
- Local copy: `zk@adeck:~/pulse-log/` (synced via git)

**Other services:**
- Docker
- SSH
- Tailscale

## zdeck — 100.64.136.57

**Role:** Gaming  
**OS:** SteamOS  
**Status:** offline

## Taildrive Mesh Summary

**Shares:**
- `nxiz/repository` → `/mnt/repository` (838.2G btrfs) - Context vault and development repositories
- `zrrh/media` → `/mnt/media` (1.3T btrfs) - Media library
- `adeck/vault` → `/mnt/vault` (1.8T btrfs) - Backup vault

**Consumers:**
- `adeck` mounts: `nxiz/repository`, `zrrh/media`
