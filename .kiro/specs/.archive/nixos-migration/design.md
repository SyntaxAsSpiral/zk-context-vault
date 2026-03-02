# NixOS Migration — Design

## Approach

Final-state surgery. Remove all Windows-era paths and replace with NixOS equivalents. No transition period, no backward compatibility with the old Windows environment.

## Key Path Mappings

| Old (Windows) | New (NixOS) |
|---|---|
| `Z:\Documents\.context` / `Z:/Documents/.context` | `/mnt/repository/context-vault` |
| `C:\Users\synta.ZK-ZRRH\.dev\.scripts\` | `workshop/src/` (scripts are in-repo now) |
| `\\wsl.localhost\Ubuntu-22.04\home\zk\.wsl-dev` | removed (WSL no longer relevant) |
| cwrsync / cygdrive SSH plumbing | native `ssh` + `rsync` (available in NixOS PATH) |

## Script Changes

### assemble.py
- Update `base_path` from `Path("Z:/Documents/.context")` to repo-relative detection or explicit NixOS path
- Remove Windows backslash normalization in `_expand_target_path()` (keep `~/` expansion, remove `A-Z:\` branch)
- `_display_path_windows()` → rename/simplify to `_display_path()`

### sync.py
- Same `base_path` fix
- Replace cwrsync SSH command with native `ssh` (just `ssh -o StrictHostKeyChecking=no`)
- Remove cygdrive path conversion blocks
- Remove Windows drive letter detection in `_expand_target_path()`
- Simplify `_sync_dir()` SSH block similarly

## Documentation Changes

### Source-of-truth files (edit directly):
- `agents/steering-global-operator.md` — Env, Paths
- `agents/steering-global-network.md` — host table (already mostly correct, add taildrive info)
- `agents/steering-global-mesh.md` — populate with full mesh topology
- `agents/steering-workspace-zk.dev.md` — workspace roots, script paths
- `.kiro/steering/tech.md` — dev environment section, path conventions
- `exocortex/exo-topography.md` — env line
- `prompts/hook-prompts/kiro-murder.md` — hardcoded path

### Regenerated files (will be rebuilt by assemble.py after source edits):
- `AGENTS.md`
- `agents/steering-project-zk-context-vault.md`
- All `workshop/staging/` artifacts

### Recipe fixes:
- `workshop/recipe-project-zk-context-vault.md` — target path `Z:/Documents/.context/` → local path

### Protected / not touched:
- `artifacts/golden/` — these are golden test fixtures, data fidelity applies
- `.kiro/specs/.archive/` — archived specs, historical record
- Canvas files in `artifacts/` — will update `zk-mesh.canvas` but leave golden canvases alone

## Testing

- `python workshop/src/assemble.py --dry-run --verbose` succeeds
- `python workshop/src/assemble.py` generates staging artifacts
- `python workshop/src/sync.py --dry-run --verbose` succeeds
- `grep -rn 'C:\\\\' --include='*.py' --include='*.md' workshop/ agents/ .kiro/steering/ prompts/ exocortex/` returns nothing (excluding archive/golden)

## Services to Document

### zrrh — llmster (LM Studio headless daemon)
- Endpoint: `http://zrrh:1234`
- API: OpenAI-compatible (`/v1/models`, `/v1/chat/completions`, `/v1/embeddings`)
- Available via Tailscale mesh from any node
- Should be documented in `steering-global-mesh.md` and `steering-global-network.md`

## Files Inventory — What Changes Where

### Scripts (functional changes):
| File | Change |
|---|---|
| `workshop/src/assemble.py` ~line 838 | `base_path = Path("Z:/Documents/.context")` → `/mnt/repository/context-vault` |
| `workshop/src/assemble.py` `_expand_target_path()` | Remove Windows drive letter branch (`A-Z:\`) |
| `workshop/src/sync.py` ~line 874 | Same `base_path` fix |
| `workshop/src/sync.py` `sync_file_to_targets()` ~lines 540-565 | Replace cwrsync SSH with native `rsync -avz -e "ssh"` |
| `workshop/src/sync.py` `_sync_dir()` ~lines 615-640 | Same cwrsync → native rsync replacement |
| `workshop/src/sync.py` `_expand_target_path()` | Remove Windows drive letter branch |

### Documentation (content changes):
| File | What to change |
|---|---|
| `agents/steering-global-operator.md` | Env → NixOS + nushell, Paths → NixOS paths, remove WSL |
| `agents/steering-global-network.md` | Add Taildrive mesh section, add llmster service, add pulse-generator service, verify host table |
| `agents/steering-global-mesh.md` | Populate full topology: drives, UUIDs, mounts, taildrives, MACs, IPs, services (llmster on zrrh:1234, pulse-generator on adeck) |
| `agents/steering-workspace-zk.dev.md` | Workspace roots → NixOS, remove WSL, fix script paths |
| `.kiro/steering/tech.md` | Dev environment → NixOS, path conventions → NixOS paths |
| `exocortex/exo-topography.md` | Env line → NixOS |
| `prompts/hook-prompts/kiro-murder.md` | Remove `Z:\Documents\.context\` hardcoded path, use relative or `~/` |

### Recipes:
| File | What to change |
|---|---|
| `workshop/recipe-project-zk-context-vault.md` | target `Z:/Documents/.context/` → `/mnt/repository/context-vault/` |

### Canvas:
| File | What to change |
|---|---|
| `artifacts/zk-mesh.canvas` | Full rewrite: nxiz replaces mkka/smnm group, zrrh is Garuda with new drives, adeck has vault + taildrives, add taildrive mesh edges |

### DO NOT TOUCH:
- `artifacts/golden/*` — golden test fixtures (data fidelity)
- `.kiro/specs/.archive/*` — archived specs (historical record)
- `workshop/manifest-recipes.md` — will be regenerated by assemble.py
