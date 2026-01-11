---
id: context-tools
created: 2025-12-31T09:55:10.259-08:00
modified: 2026-01-01T21:52:08.213-08:00
status: draft
---

## Injection Targets

This file is intended to be sliced into minimal, per-agent tool lists and injected into request parameters (tools).

---

## Universal Agent Tools (Tier 1, Read-Only)
<!-- slice:shared -->

Call tools by exact name (no aliases).
<!-- /slice -->

---
## Agent Specific Tools (Tier 2, Graph Write, Artifact Emission)

Graph write authority is exclusive to Morphognome (M). Harmonion (H) and Critikon (C) MUST NOT call graph write tools directly.

### morphognome
<!-- slice:agent=morphognome tier=2 -->

<!-- /slice -->
### harmonion
<!-- slice:agent=harmonion tier=2 -->

<!-- /slice -->
### critikon
<!-- slice:agent=critikon tier=2 -->

<!-- /slice -->
### archeoform
<!-- slice:agent=archeoform tier=2 -->

<!-- /slice -->
### antimorphogen
<!-- slice:agent=antimorphogen tier=2 -->

<!-- /slice -->

---

## AS-NEEDED Tools (Tier 3)

### morphognome
<!-- slice:agent=morphognome tier=3 -->

<!-- /slice -->
### harmonion
<!-- slice:agent=harmonion tier=3 -->

<!-- /slice -->
### critikon
<!-- slice:agent=critikon tier=3 -->

<!-- /slice -->
### archeoform
<!-- slice:agent=archeoform tier=3 -->

<!-- /slice -->
### antimorphogen
<!-- slice:agent=antimorphogen tier=3 -->

<!-- /slice -->

___
