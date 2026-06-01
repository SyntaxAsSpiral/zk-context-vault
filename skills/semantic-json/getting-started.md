# Getting Started with Semantic-JSON Workflows

Welcome to the Semantic-JSON Workflows Power! This guide will help you start transforming visual models into structured data through canvas-to-semantic-JSON anticompiler workflows.

## Prerequisites

1. **Install Obsidian** (>=1.0.0):
   - Download from [obsidian.md](https://obsidian.md)
   - Create or open a vault for your visual modeling work

2. **Install Semantic-JSON Plugin**:
   - Clone from [GitHub](https://github.com/SyntaxAsSpiral/Semantic-JSON)
   - Follow plugin installation instructions
   - Enable in Obsidian Community Plugins

3. **Verify Setup**:
   - Create a test canvas file
   - Run "Compile Canvas" command
   - Confirm semantic ordering in output

## Your First Semantic Canvas

### 1. Create a Basic Canvas

Start with a simple project specification canvas:

```json
{
  "nodes": [
    {
      "id": "project-title",
      "type": "text",
      "x": 200, "y": 0, "width": 400, "height": 120,
      "color": "#cba6f7",
      "text": "# My First Semantic Canvas\n\nA visual specification that compiles to structured data"
    },
    {
      "id": "overview-section",
      "type": "text", 
      "x": 100, "y": 200, "width": 300, "height": 180,
      "color": "#89b4fa",
      "text": "## Overview\n\n- Purpose: {{purpose}}\n- Scope: {{scope}}\n- Timeline: {{timeline}}"
    },
    {
      "id": "requirements-section",
      "type": "text",
      "x": 450, "y": 200, "width": 300, "height": 180, 
      "color": "#a6e3a1",
      "text": "## Requirements\n\n- FR1: {{functional_req_1}}\n- FR2: {{functional_req_2}}\n- NFR1: {{non_functional_req_1}}"
    }
  ],
  "edges": [
    {
      "id": "title-to-overview",
      "fromNode": "project-title",
      "toNode": "overview-section",
      "label": "defines"
    },
    {
      "id": "overview-to-requirements", 
      "fromNode": "overview-section",
      "toNode": "requirements-section",
      "label": "leads-to"
    }
  ]
}
```

### 2. Apply Semantic Compilation

Use the Semantic-JSON plugin to compile your canvas:

1. **Open canvas** in Obsidian
2. **Run compilation**: Command palette → "Compile Canvas"
3. **Review output**: Nodes now ordered by spatial semantics
4. **Export pure JSON**: Strip Canvas metadata for processing

**Before compilation** (scrambled):
```json
{
  "nodes": [
    {"id": "requirements-section", "x": 450, "y": 200, ...},
    {"id": "project-title", "x": 200, "y": 0, ...},
    {"id": "overview-section", "x": 100, "y": 200, ...}
  ]
}
```

**After compilation** (semantic order):
```json
{
  "nodes": [
    {"id": "project-title", "x": 200, "y": 0, ...},
    {"id": "overview-section", "x": 100, "y": 200, ...}, 
    {"id": "requirements-section", "x": 450, "y": 200, ...}
  ]
}
```

### 3. Process with Workshop Recipe

Create a recipe to automate canvas processing:

```yaml
# my-first-canvas-recipe.yml
recipe_id: first-canvas-compile
description: "Compile and process my first semantic canvas"

inputs:
  - canvas_file: "my-first-canvas.canvas"
  - template_vars:
      purpose: "Learn semantic canvas workflows"
      scope: "Single canvas with basic structure"
      timeline: "1 hour tutorial"

steps:
  - compile_canvas:
      source: "{{canvas_file}}"
      output: "compiled-canvas.json"
      options:
        spatial_sort: true
        embed_labeled_edges: true
  
  - extract_pure_data:
      source: "compiled-canvas.json" 
      output: "canvas-data.json"
      strip_metadata: true
  
  - generate_markdown:
      source: "canvas-data.json"
      template: "canvas-to-markdown.md"
      output: "specification.md"

outputs:
  - compiled_canvas: "compiled-canvas.json"
  - pure_data: "canvas-data.json"
  - specification: "specification.md"
```

### 4. Add Templater Integration

Make your canvas dynamic with templater variables:

```javascript
// Canvas instantiation script
<%*
const projectName = await tp.system.prompt("Project name:");
const projectType = await tp.system.suggester(
  ["Specification", "Architecture", "Workflow"], 
  ["spec", "arch", "workflow"]
);

const canvasTemplate = {
  nodes: [
    {
      id: `${projectType}-title`,
      type: "text",
      x: 200, y: 0, width: 400, height: 120,
      color: "#cba6f7",
      text: `# ${projectName}\n\nA ${projectType} canvas for visual modeling`
    },
    {
      id: `${projectType}-overview`,
      type: "text",
      x: 100, y: 200, width: 600, height: 200,
      color: "#89b4fa", 
      text: `## Overview\n\n{{description}}\n\n## Goals\n\n- {{goal_1}}\n- {{goal_2}}\n- {{goal_3}}`
    }
  ],
  edges: []
};

const fileName = `${projectName.toLowerCase().replace(/\s+/g, '-')}-${projectType}.canvas`;
await app.vault.create(fileName, JSON.stringify(canvasTemplate, null, 2));
%>
```

## Understanding Spatial Semantics

### Position Encoding

Canvas coordinates encode reading order:
- **Y-axis**: Top-to-bottom sequence (primary sort)
- **X-axis**: Left-to-right within same row (secondary sort)
- **Containment**: Group membership creates hierarchy

### Color Taxonomy

Use colors to encode semantic categories:
- **Purple (#cba6f7)**: Titles, headers, primary concepts
- **Blue (#89b4fa)**: Information, details, descriptions  
- **Green (#a6e3a1)**: Requirements, specifications, actions
- **Red (#f38ba8)**: Warnings, errors, critical items
- **Yellow (#f9e2af)**: Notes, comments, temporary items

### Edge Semantics

Different edge types encode different relationships:
- **`defines`**: Conceptual definition or specification
- **`leads-to`**: Sequential flow or progression
- **`depends-on`**: Dependency relationship
- **`relates-to`**: General association
- **`implements`**: Implementation relationship

## Common Patterns

### Hierarchical Specifications

Use groups to create nested structure:

```json
{
  "nodes": [
    {
      "id": "system-architecture-group",
      "type": "group",
      "x": 0, "y": 0, "width": 800, "height": 600,
      "label": "System Architecture",
      "color": "6"
    },
    {
      "id": "frontend-component",
      "type": "text",
      "x": 50, "y": 50, "width": 300, "height": 200,
      "text": "## Frontend\n\n- React components\n- State management\n- API integration"
    },
    {
      "id": "backend-component", 
      "type": "text",
      "x": 450, "y": 50, "width": 300, "height": 200,
      "text": "## Backend\n\n- REST API\n- Database layer\n- Authentication"
    }
  ]
}
```

### Flow Processes

Model sequential workflows with directional edges:

```json
{
  "edges": [
    {
      "id": "step1-to-step2",
      "fromNode": "step-1",
      "toNode": "step-2", 
      "label": "sequence",
      "toEnd": "arrow"
    },
    {
      "id": "step2-to-step3",
      "fromNode": "step-2",
      "toNode": "step-3",
      "label": "sequence", 
      "toEnd": "arrow"
    }
  ]
}
```

### Template Structures

Create reusable patterns with templater syntax:

```markdown
---
id: {{id}}
title: "{{title}}"
type: ["{{type}}"]
status: "{{status}}"
created: {{date}}
---

# {{title}}

## Purpose
{{purpose}}

## Scope  
{{scope}}

## Acceptance Criteria
- {{criteria_1}}
- {{criteria_2}}
- {{criteria_3}}
```

## Next Steps

- **Advanced Workflows**: Learn complex canvas patterns and multi-phase processes
- **Integration Patterns**: Connect with Kiro specs, exocortex agents, and workshop recipes
- **Quality Assurance**: Validate canvas structure and semantic consistency
- **Performance Optimization**: Handle large canvases and batch processing

Ready to transform your visual thinking into structured reality! 🎨✨