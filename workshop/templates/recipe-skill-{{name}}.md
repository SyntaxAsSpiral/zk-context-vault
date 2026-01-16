---
id: recipe-{{name}}
created: {{date}}
modified: {{date}}
status: draft
type:
  - "skill"
---

```yaml
name: {{name}}
output_format: skill  # Creates Agent Skills standard structure

# Agent Skills standard structure:
# skill-name/
# ├── SKILL.md (required - with YAML frontmatter + markdown body)
# ├── scripts/ (optional - executable code)
# │   ├── script1.py
# │   └── script2.sh
# ├── references/ (optional - additional docs loaded on demand)
# │   ├── guide-1.md
# │   └── guide-2.md
# └── assets/ (optional - static resources)
#     └── data.json

target_locations:
  - path: ~/.kiro/skills/{{name}}/
  - path: ~/.claude/skills/{{name}}/  # Multi-platform deployment

# Source mapping to skill structure
sources:
  skill_md:
    # SKILL.md with required frontmatter
    frontmatter:
      name: {{name}}  # Required: lowercase, numbers, hyphens only
      description: # Required: max 1024 chars, what skill does and when to use it
      license: # Optional: license name or reference to bundled file
      compatibility: # Optional: max 500 chars, environment requirements
      metadata: {}  # Optional: arbitrary key-value pairs
      allowed-tools: # Optional: space-delimited list of pre-approved tools
    
    body:  # Markdown instructions for agents
      - slice: # Slice identifier for main skill instructions
        slice-file: # Source file path
  
  scripts:  # Optional - go to scripts/ folder
    - file: # Path to Python/Bash/JS script
      output_name: script1.py
    - slice: # Slice containing script code
      slice-file: # Source file
      output_name: script2.sh
  
  references:  # Optional - go to references/ folder (loaded on demand)
    - slice: # Slice identifier for reference doc
      slice-file: # Source file
      output_name: guide-1.md
    - file: # Whole file reference
      output_name: api-reference.md
  
  assets:  # Optional - go to assets/ folder
    - file: # Path to static resource
      output_name: data.json

# Optional: Also output as Kiro power format
also_output_as_power: false  # Set to true to generate both skill and power formats

# Validation
validate_agentskills_spec: true  # Ensure compliance with agentskills.io standard
```