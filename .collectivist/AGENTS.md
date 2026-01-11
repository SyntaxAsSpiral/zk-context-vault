# Repository Index System

## Overview

Automated repository indexing with deterministic git tracking, AI-generated descriptions with category tagging, and auto-generated README documentation.

## Architecture

```
.repos/
├── .collectivist/
│   ├── repo-index.yaml             # Generated index data
│   ├── repo-index-task.xml         # Task Scheduler (every 3 days)
│   ├── AGENTS.md                   # This file
│   └── src/
│       ├── repo-index.nu           # Core pipeline (chains describe → readme)
│       ├── repo-describe.py        # AI description + category generator
│       └── generate-readme.nu      # README generator from YAML
├── README.md                       # Auto-generated documentation
└── [repositories...]
```

## YAML Schema

```yaml
- short_name: repo-name
  git_status: up_to_date    # not_a_repo | no_remote | up_to_date | updates_available | error
  description: "AI-generated one-sentence summary from README."
  category: ai_llm_agents   # Category assigned by LLM
  always_pull: false        # Set to true to auto-pull updates on every index run
  git_error: null           # only if git_status == 'error'
  size: 640763117
  type: dir
  created: 2025-10-21 04:46:05.849563300 -07:00
  modified: 2025-10-21 04:46:13.203395400 -07:00
  accessed: 2026-01-09 14:26:50.526557100 -08:00
  name: ..\repo-name
  target: null
  readonly: false
```

## Usage

### Command

```bash
nu .collectivist/src/repo-index.nu
```

This runs the full pipeline:
1. Scan repos and check git status
2. Generate AI descriptions + categories for new repos
3. Auto-generate categorized README

### Individual Components

```bash
python ./src/repo-describe.py    # Descriptions + categories only
nu ./src/generate-readme.nu      # README generation only
```

## Git Status Logic

**Accurate** - fetches latest remote state:
1. Check `.git` exists → `not_a_repo` if missing
2. Check `remote.origin.url` → `no_remote` if missing
3. Check upstream tracking `@{u}` → `error` if missing
4. Run `git fetch --quiet` to update remote refs (doesn't modify local files)
5. Count commits: `git rev-list HEAD..@{u} --count`
6. Result: `updates_available` if count > 0, else `up_to_date`
7. **Auto-pull**: If `always_pull: true` and `updates_available`, runs `git pull --quiet`

**Status Symbols:**
- ✓ up-to-date
- ⬆ updates available
- ⚠ error (fetch/pull failed)
- ◌ no remote configured
- ○ not a git repo

## Auto-Pull Feature

**Enable for specific repos:**
```yaml
always_pull: true  # Change from false to true in repo-index.yaml
```

When enabled:
- Index checks for updates via `git fetch`
- If updates available, automatically runs `git pull`
- Updates status to `up_to_date` (or `error` if pull fails)
- Preserves `always_pull` setting across re-indexes

**Use case**: Pristine reference repos you want to keep current automatically

## AI Description Generator

**Requirements:**
- Python 3.x with `pyyaml` and `requests` packages
- LMStudio running on `localhost:1234`
- Model: `gpt-oss-20b-heretic` (JIT loaded)
- Server-side max_tokens: 16k (set in LMStudio)

**Process:**
1. Loads existing index, finds repos with `description == null`
2. Scans for README (README.md, readme.md, README, Readme.md)
3. Sends first 3000 chars + 5 example descriptions to LLM
4. LLM returns JSON: `{"description": "...", "category": "..."}`
5. Updates YAML incrementally (saves after each success)
6. Uses ThreadPoolExecutor with 5 concurrent workers

**Output:**
- Description: One-sentence technical summary (max 150 chars)
- Category: Assigned from fixed taxonomy based on README analysis

## README Generation

**Process:**
1. Reads `repo-index.yaml`
2. Generates summary stats
3. Creates sortable table: Status | Name | Description | Category | Created
4. Auto-generates categorized sections from YAML categories
5. Saves to `README.md` at repo root

**Table Columns:**
- Status: Git status emoji
- Name: Repository name (bolded)
- Description: Full description text
- Category: Category tag in backticks
- Created: Creation date (YYYY-MM-DD)

## Task Scheduler

**Full Pipeline:** Every 3 days at 2:00 AM

Import command:
```powershell
schtasks /Create /XML "C:\Users\synta.ZK-ZRRH\.dev\.repos\.collectivist\repo-index-task.xml" /TN "RepoIndex\Every3Days"
```

Runs complete pipeline (index → describe → readme) with 2 hour timeout.

## Directory Filtering

**Excluded from indexing:**
- Hidden directories (starting with `.`)
- The `.collectivist` directory itself

**Result:** Clean separation of infrastructure from indexed content

## Self-Healing

- Index regenerated from scratch each run (no merge logic)
- Deleted repos automatically disappear
- Incremental saves enable resumable operation
- Category assignments preserved across re-indexes

## Notes for Agents

- **Fast-fail methodology**: LLM unreachable → exit immediately
- **No mock data**: Real git status only, `null` for missing values
- **Deterministic**: Same filesystem + git state = same output
- **Context compilation**: YAML → README transformation, not raw data dumps
- **Hybrid architecture**: Nushell for git/filesystem, Python for concurrent LLM processing
- **ThreadPoolExecutor pattern**: Maintains exactly 5 concurrent workers
- **Recursive structure**: `.dev\.repos\.collectivist\` - each dot marks a visibility boundary
- **Leave no trace**: Clean final-state surgery, no legacy artifacts

## Anagoglyph Path

```
C:\Users\synta.ZK-ZRRH\.dev\.repos\.collectivist\
```

Nested dot-paths creating recursive containment:
- `.dev` - development workspace (hidden from user-space)
- `.repos` - reference archive (nested hidden context)
- `.collectivist` - indexing machinery (meta-layer, compilation artifact)

Infrastructure as palimpsest, data as compiled breath 🜍
