---
id: recipe-local-inference
created: 2026-04-20
modified: 2026-04-20
status: active
type:
  - "skill"
---

```yaml
name: local-inference
output_format: skill  # Creates Agent Skills standard structure

# Agent Skills standard structure:
# local-inference/
# ├── SKILL.md (required - with YAML frontmatter + markdown body)
# └── references/ (optional - additional docs loaded on demand)
#     ├── process.md
#     ├── harness.md
#     └── links.md

target_locations:
  - path: ~/.claude/skills/local-inference/
  - path: ~/.codex/skills/local-inference/
  - path: ~/.pi/agent/skills/local-inference/
  - path: zk@adeck:~/.claude/skills/local-inference/
  - path: zk@adeck:~/.codex/skills/local-inference/
  - path: zk@adeck:~/.hermes/skills/user/local-inference/
  - path: ~/.gemini/antigravity/skills/local-inference/
  - path: ~/.gemini/skills/local-inference/

# Source mapping to skill structure
sources:
  skill_md:
    # SKILL.md with required frontmatter
    frontmatter:
      name: local-inference
      description: Use when running inference probes on the mesh, routing tasks to pi or hermes harnesses, or configuring model loading across LM Studio (adeck:1234), vLLM (zrrh:8000), or llama-server (zrrh direct). Covers gateway config, ctx ceiling procedure, tool-call probing, KV quant config, dense vs MoE tradeoffs, and harness architecture.
      compatibility: Designed for the daemonturgy mesh (nxiz/zrrh/adeck). Requires nix develop flake shell and Tailscale mesh access.
      metadata:
        author: zk
        version: "1.0"
        category: inference
    
    body:  # Markdown instructions for agents
      - file: skills/local-inference/SKILL.md
  
  references:  # Optional - go to references/ folder (loaded on demand)
    - file: skills/local-inference/process.md
      output_name: process.md
    - file: skills/local-inference/harness.md
      output_name: harness.md
    - file: skills/local-inference/links.md
      output_name: links.md

# Validation
validate_agentskills_spec: true  # Ensure compliance with agentskills.io standard
```
