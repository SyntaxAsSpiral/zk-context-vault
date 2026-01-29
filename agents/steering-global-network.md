---
inclusion: always
---

# Network Topology

ZK operates a Tailscale mesh:

| Host | OS | Role |
|------|----|------|
| zrrh | Win11 | Primary workstation |
| zrrh-wsl | WSL2 | Linux subsystem (zrrh) |
| nix | NixOS | NixOS partition (zrrh) |
| smnm | Win11 | Secondary workstation |
| amexsomnemon | NixOS | Relay node (Steam Deck) |
| zdeck | SteamOS | Gaming (offline when amexsomnemon) |
| zk-pixel | Android | Mobile (Pixel, primary w/ SIM) |
| zk-note | Android | Control surface (home/network via Termius) |

**amexsomnemon** runs AI CLIs (claude-code, gemini-cli, codex-cli). Agents on client machines (zrrh/smnm) focus on local project work; mesh orchestration happens on the deck.

When paths reference `deck@amexsomnemon:`, that's an SSH target on the relay node.
