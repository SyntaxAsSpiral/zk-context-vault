# Specification

> The complete format specification for Kiro Powers.

This document defines the Kiro Power format.

## Directory structure

A power is a directory containing at minimum a `POWER.md` file:

```
power-name/
├── POWER.md          # Required
└── steering/         # Required (can be empty)
```

<Tip>
  You can optionally include `mcp.json` at the root if your power provides MCP (Model Context Protocol) tools.
</Tip>

## POWER.md format

The `POWER.md` file must contain YAML frontmatter followed by Markdown content.

### Frontmatter (required)

```yaml  theme={null}
---
name: power-name
displayName: Power Display Name
description: A description of what this power does and when to use it.
version: "1.0.0"
keywords: []
---
```

With optional fields:

```yaml  theme={null}
---
name: semantic-json-workflows
displayName: Semantic-JSON Workflows
description: Canvas-to-structured-data anticompiler workflows for visual cognitive modeling
version: "1.0.0"
author: zk::anticompiler
license: MIT
keywords: ["semantic-json", "canvas", "anticompiler", "obsidian", "visual-modeling"]
category: visual-modeling
iconUrl: https://.../icon.png
repositoryUrl: https://github.com/...
mcpServers: {}
steeringFiles: ["getting-started.md", "advanced-workflows.md"]
dependencies:
  obsidian: ">=1.0.0"
  plugins:
    semantic-json: ">=0.2.0"
---
```

| Field            | Required | Constraints                                                                                                |
| ---------------- | -------- | ---------------------------------------------------------------------------------------------------------- |
| `name`           | Yes      | Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen.      |
| `displayName`    | Yes      | Max 128 characters. Human-readable name with proper capitalization and spacing.                            |
| `description`    | Yes      | Max 1024 characters. Non-empty. Describes what the power does and when to use it.                          |
| `version`        | Yes      | Semantic version string (e.g., "1.0.0").                                                                   |
| `keywords`       | Yes      | Array of strings. Search terms for power discovery. Empty array allowed.                                   |
| `author`         | No       | Author name or identifier.                                                                                 |
| `license`        | No       | License identifier (e.g. MIT).                                                                             |
| `category`       | No       | Power category (e.g., "development", "productivity", "visual-modeling").                                   |
| `iconUrl`        | No       | URL to 128x128 png icon.                                                                                   |
| `repositoryUrl`  | No       | URL to source repository.                                                                                  |
| `mcpServers`     | No       | Object mapping MCP server names to configurations. Empty object if no MCP servers.                         |
| `steeringFiles`  | No       | Array of steering file names (relative to steering/ directory).                                            |
| `dependencies`   | No       | Object specifying required dependencies (applications, plugins, packages).                                 |

#### `name` field

The required `name` field:

* Must be 1-64 characters
* May only contain unicode lowercase alphanumeric characters and hyphens (`a-z` and `-`)
* Must not start or end with `-`
* Must not contain consecutive hyphens (`--`)
* Must match the parent directory name

Valid examples:

```yaml  theme={null}
name: semantic-json-workflows
```

```yaml  theme={null}
name: catppuccin-theming
```

```yaml  theme={null}
name: agent-steering
```

Invalid examples:

```yaml  theme={null}
name: Semantic-JSON  # uppercase not allowed
```

```yaml  theme={null}
name: -semantic  # cannot start with hyphen
```

```yaml  theme={null}
name: semantic--json  # consecutive hyphens not allowed
```

#### `displayName` field

The required `displayName` field:

* Must be 1-128 characters
* Human-readable name with proper capitalization
* Can include spaces and special characters
* Used for UI display and documentation

Examples:

```yaml  theme={null}
displayName: Semantic-JSON Workflows
```

```yaml  theme={null}
displayName: Catppuccin Theming Power 🎨
```

#### `description` field

The required `description` field:

* Must be 1-1024 characters
* Should describe both what the power does and when to use it
* Should include specific keywords that help with power discovery

Good example:

```yaml  theme={null}
description: Canvas-to-structured-data anticompiler workflows for visual cognitive modeling and spatial semantic compilation. Use when designing complex systems visually in Obsidian Canvas.
```

Poor example:

```yaml  theme={null}
description: Helps with canvas stuff.
```

#### `version` field

The required `version` field:

* Must follow semantic versioning (MAJOR.MINOR.PATCH)
* Indicates the power version for compatibility tracking

Example:

```yaml  theme={null}
version: "1.2.3"
```

#### `keywords` field

The required `keywords` field:

* Array of strings used for power discovery
* Can be empty array if no specific keywords
* Should include relevant terms that users might search for

Example:

```yaml  theme={null}
keywords: ["css", "ui", "color", "catppuccin", "theme", "style"]
```

#### `author` field

The optional `author` field:

* Specifies the power creator
* Can be a name, organization, or identifier

Example:

```yaml  theme={null}
author: zk::anticompiler
```

#### `category` field

The optional `category` field:

* Categorizes the power for organization and discovery
* Common categories: "development", "productivity", "visual-modeling", "theming", "workflow"

Example:

```yaml  theme={null}
category: visual-modeling
```

#### `mcpServers` field

The optional `mcpServers` field:

* Object mapping MCP server names to their configurations
* Empty object `{}` if power has no MCP servers
* If present, corresponding `mcp.json` file should exist at power root

Example:

```yaml  theme={null}
mcpServers:
  weather-api:
    command: "uvx"
    args: ["weather-mcp-server"]
```

#### `steeringFiles` field

The optional `steeringFiles` field:

* Array of markdown filenames in the steering/ directory
* Lists available workflow guides and documentation
* Files are loaded on demand by agents

Example:

```yaml  theme={null}
steeringFiles: ["getting-started.md", "advanced-workflows.md", "troubleshooting.md"]
```

#### `dependencies` field

The optional `dependencies` field:

* Object specifying required software, plugins, or packages
* Can include version constraints
* Helps users understand power requirements

Example:

```yaml  theme={null}
dependencies:
  obsidian: ">=1.0.0"
  plugins:
    semantic-json: ">=0.2.0"
  node: ">=16.0.0"
  packages:
    js-yaml: ">=4.0.0"
```

### Body content

The Markdown body after the frontmatter contains the power documentation. Recommended sections:

* **Overview**: High-level description of capabilities
* **Features**: Key functionality and use cases
* **Quick Start**: Getting started examples
* **Integration**: How to use with other systems
* **Resources**: Links to steering files and additional documentation

Note that agents will load this entire file when activating a power. Keep it focused on essential information and reference steering files for detailed guides.

## Required directories

### steering/

Contains all additional documentation and workflow guides as Markdown files:

* `getting-started.md` - Initial setup and basic usage
* `advanced-workflows.md` - Complex use cases and patterns
* `troubleshooting.md` - Common issues and solutions
* Domain-specific guides

**Important constraints:**

* All files must be `.md` (Markdown) format
* JSON and HTML content should be embedded in Markdown code blocks
* Files are loaded on demand by agents
* Keep individual files focused (< 500 lines recommended)

Example steering file structure:

```
steering/
├── getting-started.md
├── advanced-workflows.md
├── api-reference.md
└── examples.md
```

## Optional files

### mcp.json

Contains MCP (Model Context Protocol) server configuration if the power provides MCP tools:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "uvx",
      "args": ["package-name"],
      "env": {
        "ENV_VAR": "value"
      }
    }
  }
}
```

**Constraints:**

* Only include if power provides MCP tools
* Must be valid JSON
* Must match `mcpServers` field in POWER.md frontmatter

## Progressive disclosure

Powers should be structured for efficient use of context:

1. **Metadata** (~200 tokens): The frontmatter fields are loaded for power discovery and selection
2. **Overview** (< 3000 tokens recommended): The POWER.md body is loaded when the power is activated
3. **Detailed guides** (as needed): Steering files are loaded on demand when specific workflows are needed

Keep your main `POWER.md` under 300 lines. Move detailed workflow documentation to steering files.

## File references

When referencing steering files in your POWER.md, use relative paths:

```markdown  theme={null}
See [Getting Started](steering/getting-started.md) for initial setup.

For advanced patterns, consult [Advanced Workflows](steering/advanced-workflows.md).
```

## Embedding non-Markdown content

Since steering files must be `.md` format, embed JSON, HTML, or other content in code blocks:

**JSON configuration:**

````markdown  theme={null}
## Configuration Example

```json
{
  "setting": "value",
  "options": ["a", "b", "c"]
}
```
````

**HTML templates:**

````markdown  theme={null}
## HTML Template

```html
<div class="component">
  <h1>{{title}}</h1>
  <p>{{content}}</p>
</div>
```
````

## Validation

Powers should validate:

* `name` follows naming conventions
* `version` is valid semantic version
* `POWER.md` has required frontmatter fields
* All `steeringFiles` exist in steering/ directory
* If `mcpServers` is non-empty, `mcp.json` exists
* All steering files are `.md` format

## Example power structure

**Minimal power:**

```
my-power/
├── POWER.md
└── steering/
    └── getting-started.md
```

**Full-featured power:**

```
semantic-json-workflows/
├── POWER.md
├── mcp.json
└── steering/
    ├── getting-started.md
    ├── advanced-workflows.md
    ├── api-reference.md
    └── troubleshooting.md
```

---

> This specification defines the Kiro Power format for packaging and distributing agent capabilities with comprehensive documentation and optional MCP tool integration.
