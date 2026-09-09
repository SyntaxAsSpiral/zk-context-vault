---
id: steering-global-mesh
title: "Tailscale Mesh Infrastructure"
type:
  - steering
  - infrastructure
category: agents
tags:
  - mesh
  - tailscale
  - nixos
  - infrastructure
  - hardware
  - global
created: 2026-03-02
modified: 2026-09-08
status: active
glyph: "🕸️"
lens: infrastructure
---

# Mesh Infrastructure

## Tailscale Mesh — tail293e98.ts.net (SyntaxAsSpiral)

| Host | IP | Role | OS | GPU |
|------|----|------|----|-----|
| nxiz | 100.115.135.104 | Primary Workstation | NixOS 26.05 | RTX 3070 |
| zrrh | 100.77.90.79 | Inference Node | NixOS 26.05 | RTX 4090 |
| adeck | 100.89.32.9 | Agentic Server / Relay (always on) | NixOS 26.05 | AMD Vangogh (Vulkan, 5.5 GiB) |
| zdeck | 100.64.136.57 | Gaming | SteamOS | AMD Vangogh (Vulkan) |
| quita | 100.82.51.63 | Family laptop / mesh print host | Linux Mint | — |
| zk-pixel | 100.96.213.111 | Android phone | Android | — |
| zk-note | 100.105.239.55 | Android phone | Android | — |

**Host faces** ([esotericons](https://github.com/SyntaxAsSpiral/esotericons)): `lotus` → nxiz · `meso` → zrrh · `sufi` → adeck. Fetch that stem when a slip is for a host.

## Key Mounts

| Host | Path | Purpose |
|------|------|---------|
| nxiz | `/mnt/repository` | Context vault + dev repos |
| nxiz | `/mnt/archive` | Archive storage |
| zrrh | `/mnt/media` | Media library |
| zrrh | `/mnt/games` | Game storage |
| adeck | `/mnt/vault` | Data lake (msgvault, memory substrate) |
| adeck | `/mnt/echo` | Hot storage for processed knowledge |

## Services

**Inference Gateway (`adeck:1234`):** All inference requests target `adeck:1234`. Adeck routes via `lmlink` — large models to `zrrh`, small models/embeddings local or to `nxiz`. OpenAI-compatible API (`/v1/chat/completions`, `/v1/embeddings`).

**Holliday Table (`adeck`):** Kitchen app at `https://adeck.tail293e98.ts.net`. Authoritative tree `/mnt/echo/family-cookbook`. Quita is not the app host.

**tm20 thermal (`quita`):** Epson TM-T20III USB (`04b8:0e28`, 24V brick, USB-B). USB execution is **quita only** — `tm20` / `tm20-set` in `/usr/local/bin`, source `~/src/tm20`. udev `/etc/udev/rules.d/99-tm20-epson.rules` (`plugdev`, unbinds `usblp`). No CUPS. CLIs open USB only (library TCP :9100 is unused). Paper: generic 80 mm / 3-1/8" thermal. Do not share via router USB. Linux faces: Liberation Sans/Mono (local `kit.rs`); macOS Helvetica/Menlo otherwise. How to compose and when to use USB vs the receiver: skill **tm20**.

**Mesh print receiver (`quita:8766`):** Shared USB gate for Holliday Table, holliday-estate, and sideriod. Live tree `~/src/print-receiver` (not inside any project checkout). systemd user unit `print-receiver.service`. Token `PRINT_TOKEN` (alias `HOLIDAY_PRINT_TOKEN`). POST `http://quita:8766/print` a unique `job_id` plus a 576px PNG (`image`) or markdown (`markdown`). Duplicate ids are not reprinted. One USB lock. Prefer this from other hosts and from long-running services. Direct `tm20` / `tm20-set` is for sitting at quita: design, preview, hello, status, recovering a jammed job.

**Other services on adeck:** Docker, qBittorrent, SSH, Tailscale, msgvault, Hermes agent, sideriod gnomon, pulse-generator (daily site rotation at 02:24 PST), Bitburner (MCP + sync server).

## Development Mandates

- **Nix-First:** Prefer Nix for all package management. No `pip`, `npm`, `cargo` for global installs.
- **Root Flakes:** Use per-project `flake.nix` for reproducible envs (`nix develop` / `direnv`).
- **Transient Tooling:** Agents should use `nix shell` / `nix run` for ad-hoc tools.
- **Declarative:** Minimize non-declarative state. Reproducibility over convenience.

## Taildrive Mesh

**Shares:**
- `nxiz/repository` → `/mnt/repository`
- `nxiz/archive` → `/mnt/archive`
- `zrrh/media` → `/mnt/media`
- `zrrh/games` → `/mnt/games`
- `adeck/vault` → `/mnt/vault`
- `adeck/echo` → `/mnt/echo`

**Consumers:** `adeck` mounts `nxiz/repository` and `zrrh/media`.

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
