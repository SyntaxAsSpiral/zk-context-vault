# Semantic-JSON Workflows Power 🎨

**Transform visual models into deterministic structured data through canvas-to-semantic-JSON anticompiler workflows**

## Overview

The Semantic-JSON Workflows Power provides comprehensive visual cognitive modeling capabilities through Obsidian Canvas and the Semantic-JSON anticompiler. Design complex systems visually, then compile spatial semantics into stable, human-readable structured data while preserving visual intent.

## Features

### 🧠 Anticompiler Philosophy
- **Visual Decompression**: Transform machine-dense Canvas JSON into human-legible structure
- **Spatial Semantics**: Preserve position, containment, color, and flow topology as meaning
- **Deterministic Compilation**: Stable ordering regardless of Obsidian's JSON scrambling
- **Intent Preservation**: Maintain visual design decisions through structural transformation

### 🎯 Canvas Design Patterns
- **Hierarchical Organization**: Depth-first traversal through spatial containment
- **Flow Topology**: Directional edges define execution and dependency order
- **Color Taxonomy**: Visual categories become semantic groupings
- **Edge Semantics**: Typed relationships (`model`, `sequence`, `compile`, `blocks`, `relates`)

### 🛠️ Compilation Workflows
- **Spatial Compilation**: Position coordinates → linear reading sequence
- **Pure JSON Export**: Strip Canvas metadata while preserving semantic structure
- **Labeled Edge Embedding**: Convert relationships to self-contained node properties
- **Content Identity Extraction**: Surface semantic keys from YAML, Markdown, structured text

### 🔄 Integration Capabilities
- **Workshop Recipes**: Automated canvas processing and deployment
- **Kiro Specs**: Visual 3-phase development process support
- **Templater Workflows**: Dynamic canvas generation with variable substitution
- **Exocortex Coordination**: Multi-agent visual modeling and workflow design

## Quick Start

### Create Your First Semantic Canvas
```javascript
// Basic canvas structure with semantic organization
const semanticCanvas = {
  nodes: [
    {
      id: "project-overview",
      type: "text",
      x: 0, y: 0, width: 400, height: 200,
      text: `---
id: project-spec
title: "{{project_name}}"
type: ["specification", "design"]
status: "draft"
---

# {{project_name}}

{{project_description}}`
    }
  ],
  edges: []
};
```

### Compile Canvas to Structured Data
```bash
# Using Semantic-JSON plugin compilation
# 1. Open canvas in Obsidian
# 2. Run "Compile Canvas" command
# 3. Export as pure JSON for processing
```

### Process with Workshop Recipe
```yaml
# semantic-canvas-recipe.yml
recipe_id: semantic-canvas-compile
description: "Compile Canvas to structured JSON with semantic ordering"

inputs:
  - canvas_file: "*.canvas"
  - compilation_options:
      flow_sort: false
      color_sort: true
      embed_labeled_edges: true

steps:
  - compile_spatial_semantics:
      source: "{{canvas_file}}"
      output: "compiled.json"
  
  - export_pure_json:
      source: "compiled.json"
      output: "{{target}}.json"
      strip_metadata: true

outputs:
  - compiled_canvas: "compiled.json"
  - pure_data: "{{target}}.json"
```

## Visual Design Principles

### Spatial Semantic Encoding

| Visual Element | Semantic Meaning | Compilation Result |
|----------------|------------------|-------------------|
| **Position (x, y)** | Reading sequence | Top-to-bottom, left-to-right ordering |
| **Containment** | Hierarchical structure | Depth-first traversal through groups |
| **Color** | Semantic taxonomy | Visual categories become logical clusters |
| **Directionality** | Information flow | Execution order and dependency chains |

### Edge Relationship Types

| Edge Type | Visual Cue | Purpose | Compilation Behavior |
|-----------|------------|---------|---------------------|
| `model` | Solid arrow | Architecture refinement | Sequential design flow |
| `sequence` | Dashed arrow | Process derivation | Implementation ordering |
| `compile` | Bold arrow | Direct transformation | Bypass intermediate steps |
| `blocks` | Red/thick line | Hard dependency | Execution constraints |
| `relates` | Dotted line | Soft association | Conceptual relationships |

## Advanced Workflows

### Canvas-Driven Kiro Specs
Transform visual specifications into structured development processes:

1. **Design Phase**: Visual architecture in canvas groups
2. **Requirements Phase**: Detailed specifications with mermaid diagrams  
3. **Tasks Phase**: Implementation breakdown with dependency edges

### Multi-Agent Coordination
Use canvas for exocortex agent workflow design:
- **Agent nodes**: Specialized AI capabilities
- **Flow edges**: Information and control flow
- **Group boundaries**: System and subsystem organization
- **Color coding**: Agent types and responsibilities

### Template Hierarchies
Create reusable canvas patterns:
- **Base templates**: Common structural patterns
- **Specialized templates**: Domain-specific variations
- **Composite templates**: Multi-pattern combinations
- **Dynamic templates**: Templater-driven generation

## Integration Patterns

### Workshop System Integration
- **Slice extraction**: Modular canvas content for recipe assembly
- **Recipe compilation**: Automated canvas processing pipelines
- **Target deployment**: Multi-format output from visual designs
- **Version control**: Git-friendly canvas artifact management

### Templater Workflows
```javascript
// Dynamic canvas instantiation
<%*
const canvasTemplate = {
  nodes: [
    {
      id: "{{title-slug}}",
      type: "text",
      x: 0, y: 0, width: 400, height: 200,
      text: `# {{title}}\n\n{{description}}`
    }
  ]
};

const canvasPath = `${tp.file.folder(true)}/{{title-slug}}.canvas`;
await app.vault.create(canvasPath, JSON.stringify(canvasTemplate, null, 2));
%>
```

### Exocortex Agent Design
Visual modeling for distributed cognition:
- **Agent specialization**: Different node types for different capabilities
- **Coordination protocols**: Edge semantics for agent communication
- **Workflow orchestration**: Canvas as blueprint for multi-agent processes
- **Cognitive architecture**: Visual representation of thinking systems

## Quality Assurance

### Structural Validation
- **Node integrity**: Unique IDs, valid types, proper positioning
- **Edge validation**: Valid references, consistent relationships
- **Hierarchy checking**: Proper containment and nesting
- **Flow analysis**: Acyclic dependencies, coherent topology

### Semantic Quality
- **Spatial consistency**: Logical positioning and grouping
- **Color taxonomy**: Meaningful visual categories
- **Edge semantics**: Appropriate relationship types
- **Content structure**: Valid YAML, Markdown, templater syntax

### Performance Optimization
- **Large canvas handling**: Spatial indexing and batch processing
- **Memory efficiency**: Streaming compilation for complex models
- **Caching strategies**: Avoid redundant compilation operations
- **Validation shortcuts**: Fast-fail on structural errors

## Tools and Assets

### Canvas Compiler (`tools/canvas-compiler.js`)
Programmatic compilation engine for batch processing and automation.

### Semantic Validator (`tools/semantic-validator.js`)  
Comprehensive validation suite for canvas structure and semantic quality.

### Reference Examples (`references/canvas-examples.json`)
Collection of well-structured canvas examples demonstrating best practices.

### Kiro Spec Template (`templates/kiro-spec-canvas.json`)
Ready-to-use canvas template for 3-phase development specifications.

## Troubleshooting

### Common Issues
- **Scrambled node order**: Use Semantic-JSON plugin compilation
- **Missing edge references**: Validate canvas structure before processing
- **Broken hierarchy**: Adjust group boundaries or explicit containment
- **Flow topology errors**: Check for circular dependencies in edge directions

### Debug Workflows
- **Spatial analysis**: Examine coordinate distribution and clustering
- **Hierarchy validation**: Check containment relationships and nesting
- **Flow topology**: Analyze edge directions and dependency chains
- **Content extraction**: Verify YAML frontmatter and templater syntax

Transform your visual thinking into structured reality. Design with canvas, compile with semantics, deploy with precision! 🎨✨