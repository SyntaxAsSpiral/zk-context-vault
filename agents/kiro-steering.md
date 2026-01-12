---
id: kiro-steering
title: "Kiro Steering Hierarchy"
type: 
  - "documentation"
  - "configuration"
category: "agents"
tags:
  - "kiro"
  - "steering"
  - "hierarchy"
  - "context"
  - "guidance"
created: 2026-01-11
modified: 2026-01-11
status: "active"
glyph: "🧭"
lens: "contextual-guidance"
---

# 🧭 Kiro Steering Hierarchy

*Hierarchical context and behavior guidance system.*

## global 

- `C:\Users\synta.ZK-ZRRH\.kiro\steering\agent.md`

[%agent-role-kiro%](agents/agent-roles.md)


- `C:\Users\synta.ZK-ZRRH\.kiro\steering\operator.md`

# Operator :: Zach Battin  — Vibe Alchemist 🜏

zk::mocha: #f38ba8 #fab387 #f9e2af #a6e3a1 #74c7ec #b4befe #cba6f7 :frappe: #292c3c  #45475a

## Prime Directive::>  Ἐπιβάλλε τὴν σημειωτικὴν ὑγιεινήν (Τάξεια). Πᾶσα πλαισίωσις ὀντολογική ἐστιν.

> Don't hurt; be pure. Don't cheat; be content. Don't take; be disciplined. Don't waste; be aware. Don't cling; be devoted.

**aka:** ZK::🜏🜃🜔 // Æmexsomnus // 🍥
**Env:** Windows 11 + nushell (primary)  \\ compiled triquetra workspace \\ .dotfiles = zahir ≠ batin
**Fav Font**: Recursive Mono Casual
**Paths:** `C:/Users/synta.ZK-ZRRH/.dev/` - main working projects directory; `C:/Users/synta.ZK-ZRRH/.dev/.repos` - cloned reference repos; `\\wsl.localhost\Ubuntu-22.04\home\zk\.wsl-dev` - wsl workspace

### **Current Project Priorities:**
- `.dev/obsidian-workshop/Semantic-JSON` - Obsidian plugin for smart Canvas data recompiling. 
- `.dev/Collectivist` - AI powered curation for intentional collections. 
- `.dev/Amexsomnemon` - Overarching exocortex project. 
- SDK Task Automation DB
- ADK-Go Multi-Agent Architecture in various domains

### **Role Sigil:** 
-  🌸 Autognostic Infloresencer · 🪢 Logopolysemic Weaver (Self-Seeker & Pattern Linguist)
- 💨 Pneumastructural Intuitive · 🛸 Ritotechnic Liminalist (Breathform Sculptor & Threshold Architect)
- 🧩 Syntactic Delver · 🗺️ Mythic Tactician (Grammatical Navigator & Narrative Strategist)
- ♓︎ Syzygetic Machinator · ⚗️ Alchemical Lexemancer (Polarity Tensor & Hyperstitional Engineer)
- 🧬 Mnemonic Emanator · 🛏️ Oneiric Pedagogue (Living Memory & Dreamfield Guide)

---

## workspace

- `C:\Users\synta.ZK-ZRRH\.dev\.kiro\steering\compiled-workspace.md`

## Multi-Workspace Navigation
- **Path Parameter**: Use `executePwsh(path="workspace_root")` to specify which workspace to run commands from
- **Absolute Paths in Scripts**: In multi-workspace setups, hardcode absolute paths in scripts rather than relying on relative paths
- **Workspace Roots**: 
  - `z:\Documents\.context` - Context/documentation workspace
  - `c:\Users\synta.ZK-ZRRH\.dev` - Development workspace  
  - `\\wsl.localhost\Ubuntu-22.04\home\zk\.wsl-dev` - WSL workspace

### Script Execution Pattern
```python
# In Python scripts, use absolute paths for cross-workspace access
base_path = Path("Z:/Documents/.context")  # Context workspace root
script_path = Path("C:/Users/synta.ZK-ZRRH/.dev/.scripts")  # Scripts location
```

### Common Pitfall

- Running executePwsh(command="python script.py", path="workspace_a") but script looks for files relative to workspace_a
- **Solution**: Hardcode absolute paths in the script itself, not relative to execution directory

---

## project

### collectivist
- `C:\Users\synta.ZK-ZRRH\.dev\collectivist\.kiro\steering\product.md`

#### Product Overview - `C:\Users\synta.ZK-ZRRH\.dev\collectivist\.kiro\steering\product.md`

**Collectivist** is an AI-powered collection curator that transforms semantically coherent collections into living documentation substrates. It uses a distributed seed-to-trunk architecture where portable collection seeds automatically centralize to a coordination trunk for unified curation and documentation.

## Core Philosophy

- **Domain-specific intelligence** over generic sorting
- **Collection overview generation** with LLM-powered contextual summaries
- **Template-based rendering** for deterministic, reproducible documentation
- **Curation that feels magical** through context-aware organization

## Key Features

- **Multi-format collections**: Repositories, Obsidian vaults, documents, media files, research papers, creative projects, datasets
- **Seed deployment**: Drop `.collectivist/` seed anywhere, works immediately with automatic trunk centralization
- **Plugin architecture**: Domain-specific scanners for different collection types
- **Multi-stage pipeline**: Analyzer → Scanner → Describer → Renderer
- **Web interface**: Simple trunk interface with SQLite storage for unified collection management
- **LLM integration**: Multiple provider support (OpenAI, Anthropic, OpenRouter, local models)

## Target Use Cases

- Repository collections with Git metadata and semantic understanding
- Research paper collections with citation extraction and topic clustering
- Media collections with timeline organization and metadata extraction
- Creative project collections with version tracking and asset linking
- Dataset collections with schema inference and sample previews

## Architecture Modes

- **Seed**: Minimal mode with `.collectivist/` seed drop-in system that auto-detects collection type
- **Trunk**: Central coordination with SQLite storage, web interface, and unified collection management
- **Distributed**: Full workflow with multiple seeds centralizing to trunk for intelligent processing and documentation