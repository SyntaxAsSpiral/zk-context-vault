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
target_locations:
  - path: # Target file path for skill output (e.g., ~/.kiro/skills/{{name}}.md)
sources:
  - slice: # Slice identifier for skill content
    file: # Source file path (e.g., .context/skills/{{name}}/SKILL.md)
  # Add more sources as needed for skill bundles
template: |
  # {{name}} Skill
  {content}
# Skill-specific fields
skill_type: # individual | bundle
bundle_options:
  combine_skills: []     # List of skill names to bundle together
  create_catalog: true   # Generate searchable skill catalog
  include_metadata: true # Include skill metadata in output
skill_metadata:
  extract_frontmatter: true    # Extract YAML frontmatter from skills
  include_examples: true       # Include example sections
  include_references: true     # Include reference sections
  resolve_references: true     # Resolve and include referenced slices
output_formats:
  - markdown              # Standard markdown format
  # - json                # JSON format for programmatic use
  # - yaml                # YAML format for configuration
cross_references:
  auto_resolve: true      # Automatically resolve skill cross-references
  include_related: false  # Include related skills in output
```