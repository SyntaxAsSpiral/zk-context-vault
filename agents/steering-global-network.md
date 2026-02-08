---
inclusion: always
---

# Network Topology

ZK operates a Tailscale mesh (tail293e98.ts.net - SyntaxAsSpiral):

| Host | Tailscale IP | OS | Role | Status |
|------|--------------|----|----|--------|
| nxiz | 100.115.135.104 | NixOS 26.05 (Yarara) | Primary Workstation | online |
| zrrh | 100.126.60.24 | Garuda Linux | Couch PC / Local Inference | online |
| adeck | 100.89.32.9 | NixOS 26.05 (Yarara) | Headless Agentic Server/Relay | online (always) |
| zdeck | 100.64.136.57 | SteamOS | Gaming | offline |
| zk-pixel | 100.96.213.111 | Android | Mobile (Pixel, primary w/ SIM) | online |
| zk-note | 100.105.239.55 | Android | Control surface (Termius) | online |

## Taildrive Mesh

Taildrive shares provide cross-device filesystem access over the Tailscale mesh:

**Shared drives:**
- `nxiz/repository` - `/mnt/repository` (838.2G btrfs) - Context vault and development repositories
- `zrrh/media` - `/mnt/media` (1.3T btrfs) - Media library
- `adeck/vault` - `/mnt/vault` (1.8T btrfs) - Backup vault

**Consumers:**
- `adeck` mounts: `nxiz/repository` → `/mnt/taildrive/repository`, `zrrh/media` → `/mnt/taildrive/media`

## Services

### zrrh — llmster (LM Studio headless daemon)
- **Endpoint:** `http://zrrh:1234` (accessible via Tailscale mesh)
- **API:** OpenAI-compatible (`/v1/models`, `/v1/chat/completions`, `/v1/embeddings`)
- **Available models:** gpt-oss-20b, seed-oss-36b, qwen3-30b-a3b-thinking distill, granite-4-h-tiny, olmo-3-32b-think, ernie-4.5-21b-a3b, dolphin-mistral-24b, phi4-trader, lfm2-1.2b, financial-gpt-oss-20b
- **Embedding models:** nomic-embed-text-v1.5, qwen3-embedding-4b, mxbai-embed-large-v1

### adeck — pulse-generator
- **Schedule:** Daily at 02:24 PST (systemd timer)
- **Script:** `src/github_status_rotator.py` from `/home/zk/pulse-log/` venv
- **Domain:** lexemancy.com (GitHub Pages)
- **LLM backends:** OpenRouter (kimi-k2 primary), fallback chain → deepseek-v3.2, local llmster (gpt-oss-20b-heretic via localhost:1234), gemini-3-flash
- **Local copy:** `zk@adeck:~/pulse-log/` (synced via git)

### adeck — nanoclaw (WhatsApp AI assistant)
- **Service:** `nanoclaw.service` (systemd, enabled, always running)
- **Runtime:** Node.js (`dist/index.js`)
- **Path:** `zk@adeck:~/nanoclaw/`
- **Interface:** WhatsApp (via Anthropic Agents SDK / Claude)
- **Isolation:** Docker-based container sandboxing

