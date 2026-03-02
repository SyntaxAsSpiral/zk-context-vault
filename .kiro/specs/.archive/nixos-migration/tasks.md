# NixOS Migration — Tasks

- [x] 1. Fix workshop scripts for NixOS
  - [x] 1.1 Update `assemble.py` base_path to `/mnt/repository/context-vault` and remove Windows path logic
  - [x] 1.2 Update `sync.py` base_path and replace cwrsync/cygdrive SSH plumbing with native rsync/ssh
  - [x] 1.3 Clean up Windows-specific path helpers in both scripts (`_expand_target_path`, `_display_path_windows`, backslash normalization)

- [x] 2. Update source-of-truth documentation
  - [x] 2.1 Update `agents/steering-global-operator.md` — Env line (NixOS + nushell), Paths (NixOS paths), remove WSL references
  - [x] 2.2 Update `agents/steering-global-network.md` — fix host table (zrrh=Garuda, nxiz=NixOS Workstation), add Taildrive mesh section
  - [x] 2.3 Populate `agents/steering-global-mesh.md` with full mesh topology (drives, UUIDs, mounts, taildrives, MACs, tailscale IPs)
  - [x] 2.4 Update `agents/steering-workspace-zk.dev.md` — workspace roots, script paths, remove WSL
  - [x] 2.5 Update `.kiro/steering/tech.md` — dev environment section, path conventions
  - [x] 2.6 Update `exocortex/exo-topography.md` — env line
  - [x] 2.7 Fix `prompts/hook-prompts/kiro-murder.md` — remove hardcoded `Z:\` path

- [x] 3. Fix recipe target paths
  - [x] 3.1 Update `workshop/recipe-project-zk-context-vault.md` target from `Z:/Documents/.context/` to repo-local path

- [x] 4. Update mesh canvas
  - [x] 4.1 Rewrite `artifacts/zk-mesh.canvas` to reflect current topology (nxiz replaces mkka/smnm, zrrh is Garuda, adeck has vault drive, taildrive mesh)

- [x] 5. Regenerate and validate
  - [x] 5.1 Run `python workshop/src/assemble.py --dry-run --verbose` and verify no errors
  - [x] 5.2 Run `python workshop/src/assemble.py` to regenerate all staging artifacts
  - [x] 5.3 Verify no stale Windows paths remain in active files (grep check excluding archive/golden)
