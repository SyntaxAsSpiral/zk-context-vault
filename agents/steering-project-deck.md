# adeck Project Steering

## Critical Constraints

**DECK AGENTS ARE FORBIDDEN FROM INITIATING REBUILDS.**

**SSH is Tailscale IP only.** adeck runs Mullvad; MagicDNS / hostnames (`adeck`, `adeck.tail293e98.ts.net`, other mesh names) do not work for SSH from this host. Use IPs (`adeck` = `100.89.32.9`).

## Safe Operations (Deck agents may perform)

- Edit `/etc/nixos/configuration.nix` and related config files
- Channel repairs and NIX_PATH fixes
- Garbage collection
- tmux session management
- File operations and general development work

```
