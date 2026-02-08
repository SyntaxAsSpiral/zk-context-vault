# NixOS Migration — Requirements

## Context

The primary development environment has shifted from Windows 11 (zrrh) to NixOS (nxiz). The machine previously known as mkka/smnm is now nxiz — same hardware (FC:34:97:3B:6E:99), new OS and hostname. zrrh has been reimaged to Garuda Linux and serves as couch PC. adeck has gained a 1.8T vault drive and consumes taildrives from the mesh.

All Windows-era paths (`Z:\Documents\.context`, WSL references, cwrsync plumbing) are dead. The vault now lives at `/mnt/repository/context-vault` on nxiz.

## Source of Truth (polled 2026-02-07)

### nxiz — FC:34:97:3B:6E:99 — 100.115.135.104
- OS: NixOS 26.05 (Yarara), Primary Workstation
- GPU: NVIDIA RTX 3070
- nvme0n1 (476.9G): p1 vfat /boot, p2 btrfs / (subvols)
- sdb1 (838.2G btrfs) → /mnt/repository — Taildrive share: `repository`
- sda1 (931.5G btrfs) → /mnt/archive
- Ethernet: enp10s0 FC:34:97:3B:6E:99

### zrrh — 100.126.60.24
- OS: Garuda Linux, Couch PC / Local Inference
- GPU: NVIDIA RTX 4090 (primary inference GPU for llmster)
- Ethernet: 60:CF:84:61:D8:00, WiFi (active): B0:DC:EF:2F:7B:0F
- Services: Tailscale, llmster (LM Studio headless daemon) at `zrrh:1234` — OpenAI-compatible API
  - Available models: gpt-oss-20b, seed-oss-36b, qwen3-30b-a3b-thinking distill, granite-4-h-tiny, olmo-3-32b-think, ernie-4.5-21b-a3b, dolphin-mistral-24b, phi4-trader, lfm2-1.2b, financial-gpt-oss-20b
  - Embedding models: nomic-embed-text-v1.5, qwen3-embedding-4b, mxbai-embed-large-v1
- nvme0n1 (1.8T): p1 vfat /boot/efi (5996-AD7F), p2 btrfs ZRRH (a94ba4f7) — subvols @, @home, @root, @srv, @cache, @log, @tmp
- nvme1n1 (3.6T): p1 btrfs Media 1.3T (112f1862) → /mnt/media — Taildrive share: `media`, p2 btrfs Games 2T (7b93a14d) → /mnt/games
- 61.9G zram swap

### adeck — 100.89.32.9
- OS: NixOS 26.05 (Yarara), Headless Agentic Server / Relay (always on)
- Dock ethernet: 80:6D:97:AB:3A:FC (DOWN), WiFi (active): 50:5A:65:1F:84:9D
- mmcblk0 (238.4G): p1 vfat boot (0F7B-533B), p2 ext4 root (43631aea)
- nvme0n1 (476.9G): legacy SteamOS partitions, unmounted
- sda (1.8T btrfs "vault" b802e750) → /mnt/vault — Taildrive share: `vault`
- Taildrive mounts: nxiz/repository → /mnt/taildrive/repository, zrrh/media → /mnt/taildrive/media
- Services: Docker, SSH, Tailscale, pulse-generator (systemd timer)
  - pulse-generator: daily at 02:24 PST, runs `src/github_status_rotator.py` from `/home/zk/pulse-log/` venv
  - Domain: lexemancy.com (GitHub Pages)
  - LLM backends: OpenRouter (kimi-k2 primary), fallback chain → deepseek-v3.2, local llmster (gpt-oss-20b-heretic via localhost:1234), gemini-3-flash
  - Local copy of project at `zk@adeck:~/pulse-log/`, synced via git

### Tailnet — tail293e98.ts.net (SyntaxAsSpiral)

| Host | Tailscale IP | OS | Role | Status |
|---|---|---|---|---|
| nxiz | 100.115.135.104 | NixOS 26.05 | Primary Workstation | online |
| zrrh | 100.126.60.24 | Garuda Linux | Couch PC / Local Inference | online |
| adeck | 100.89.32.9 | NixOS 26.05 | Headless Agentic Server/Relay | online (always) |
| zdeck | 100.64.136.57 | SteamOS | Gaming | offline |
| zk-pixel | 100.96.213.111 | Android | Mobile (Pixel, primary w/ SIM) | online |
| zk-note | 100.105.239.55 | Android | Control surface (Termius) | online |

### zdeck — offline
- SteamOS, Gaming

### zk-pixel — Android, Mobile (Pixel, primary w/ SIM)
### zk-note — Android, Control surface (home/network via Termius)

### Taildrive Mesh
- nxiz → shares `repository` (/mnt/repository)
- zrrh → shares `media` (/mnt/media)
- adeck → shares `vault` (/mnt/vault)
- adeck consumes: nxiz/repository, zrrh/media

## Acceptance Criteria

1. Workshop scripts (`assemble.py`, `sync.py`) run successfully on nxiz with no Windows path references
2. All steering/operator docs reflect NixOS as primary environment
3. Mesh topology docs and canvas match polled reality
4. Recipe target paths use `~/` or SSH notation (no drive letters)
5. Assembled artifacts regenerate cleanly after all changes
6. No `C:\`, `Z:\`, `\\wsl.localhost`, cwrsync, or cygdrive references remain in active (non-archived, non-golden-artifact) files
