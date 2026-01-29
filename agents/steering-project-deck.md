# amexsomnemon (Deck) Project Steering

## Critical Constraints

**DECK AGENTS ARE FORBIDDEN FROM INITIATING REBUILDS.**

Rebuilds must be initiated from client-side agents (zrrh/smnm) via remote deploy. This prevents long-running operations from blocking the deck's limited resources and ensures rebuilds can be monitored from a stable workstation.

If a rebuild is needed, tell the operator to initiate it from a client machine.

## Safe Operations (Deck agents may perform)

- Edit `/etc/nixos/configuration.nix` and related config files
- Channel repairs and NIX_PATH fixes
- Garbage collection
- tmux session management
- File operations and general development work

## Paths

- NixOS config: `/etc/nixos`
- Safe shell PATH prefix: `/run/wrappers/bin:/run/current-system/sw/bin:/nix/var/nix/profiles/default/bin`

## Safe Shell PATH

When PATH is broken, prefix commands with:
```
/run/current-system/sw/bin/env PATH=/run/wrappers/bin:/run/current-system/sw/bin:/nix/var/nix/profiles/default/bin:$PATH
```

## Channel Repair

```bash
/run/wrappers/bin/sudo /run/current-system/sw/bin/nix-channel --list
/run/wrappers/bin/sudo /run/current-system/sw/bin/nix-channel --remove nixos 2>/dev/null || true
/run/wrappers/bin/sudo /run/current-system/sw/bin/nix-channel --add https://nixos.org/channels/nixos-25.11 nixos
/run/wrappers/bin/sudo /run/current-system/sw/bin/nix-channel --update
```

## tmux (for long operations)

```bash
/run/current-system/sw/bin/tmux new -s deck
# detach: Ctrl-b d
# reattach: /run/current-system/sw/bin/tmux attach -t deck
```

## Garbage Collection

```bash
# Remove dead store paths (keeps generations)
/run/wrappers/bin/sudo /run/current-system/sw/bin/nix-collect-garbage

# Nuclear option (loses rollback)
/run/wrappers/bin/sudo /run/current-system/sw/bin/nix-collect-garbage -d
```

## Troubleshooting

- Missing commands → use full paths from this file
- `sudo` fails → `/run/wrappers/bin/sudo`
- NIX_PATH errors → repair channels
- CRLF corruption (`\r': command not found`) → `sed -i 's/\r$//' <file>`
