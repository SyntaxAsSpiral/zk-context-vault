---
id: exo-praxis-{{cmd}}
created: {{date}}
modified: {{date}}
status: draft
type:
  - "exocortex"
  - "praxis"
---

```yaml
name: exo-praxis-{{cmd}}
target_locations:
  - path: # Target file path for exocortex praxis (e.g., .context/exocortex/exo-praxis-{{cmd}}.md)
sources:
  - slice: shared
    file: # Source file with shared praxis content
  - slice: agent=harmonion
    file: # Source file with harmonion-specific overrides
  - slice: agent=critikon  
    file: # Source file with critikon-specific overrides
  - slice: agent=morphognome
    file: # Source file with morphognome-specific overrides
  - slice: agent=archeoform
    file: # Source file with archeoform-specific overrides
  - slice: agent=antimorphogen
    file: # Source file with antimorphogen-specific overrides
template: |
  # Exocortex Praxis: {{cmd}}
  
  ## Purpose
  Operational guidance for the {{cmd}} workflow within the pentadyadic agent architecture.
  
  {content}
# Exocortex-specific fields
command: {{cmd}}
agent_architecture: pentadyadic
coordination_pattern: # triquetra | dual-path | gnomon | antibody
phase_structure:
  - evaluation: true     # Include evaluation phase
  - synthesis: true      # Include synthesis phase  
  - execution: true      # Include execution phase
safety_gates:
  - determinism: true    # Enforce deterministic behavior
  - boundaries: true     # Enforce storage boundaries
  - refusal_honor: true  # Honor agent refusals
```

# Exocortex Praxis: {{cmd}}

*Operational guidance for the {{cmd}} workflow within the pentadyadic agent architecture.*

## Purpose

- Describe how to run the {{cmd}} workflow
- Define required inputs and expected outputs
- Provide agent-specific constraints and coordination patterns

---

## Shared Praxis

<!-- slice:shared -->

### Command

{{cmd}}:
- Goal: 
- Success criteria: 
- Non-goals: 

### Inputs (required)

- 

### Outputs (required)

- 

### Constraints

- Determinism: 
- Safety gates: 
- Storage boundaries: 

<!-- /slice -->

---

## Agent Overrides (optional)

### harmonion
<!-- slice:agent=harmonion -->

- Focus: 
- Failure modes to watch: 
- Output shape: 

<!-- /slice -->

### critikon
<!-- slice:agent=critikon -->

- Focus: 
- Invariants to enforce: 
- Output shape: 

<!-- /slice -->

### morphognome
<!-- slice:agent=morphognome -->

- Focus: 
- Allowed mutations / writes: 
- Output shape: 

<!-- /slice -->

### archeoform
<!-- slice:agent=archeoform -->

- Focus: 
- Canonicalization rules: 
- Output shape: 

<!-- /slice -->

### antimorphogen
<!-- slice:agent=antimorphogen -->

- Focus: 
- Stress tests / edge cases: 
- Output shape: 

<!-- /slice -->

---

## Notes (non-injected)

Keep any extra explanation here without slice tags so it never gets injected.
