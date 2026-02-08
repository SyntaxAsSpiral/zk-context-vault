# Semantic-JSON Workflows

*Canvas-to-structured-data anticompiler workflows for visual cognitive modeling.*

## Overview

Semantic-JSON transforms Obsidian Canvas files from scrambled spatial data into deterministic, human-readable structures. This skill covers the complete workflow from visual design through semantic compilation to structured data export.

## Core Concepts

### The Anticompiler Philosophy

Semantic-JSON inverts traditional compilation:
- **Traditional compiler**: Human-legible → machine-legible (reduces ambiguity, increases constraints)
- **Anticompiler**: Machine-dense → human-legible (reduces opacity, increases semantic surface)

**Key insight**: Visual modeling preserves spatial semantics that linear text cannot capture. The anticompiler decompresses visual intent into stable, deterministic structure.

### Spatial Semantic Compilation

Canvas elements encode meaning through visual properties:
- **Position** (x, y coordinates) → Linear reading sequence (top-to-bottom, left-to-right)
- **Containment** (bounding boxes) → Hierarchical structure (depth-first traversal)
- **Color** (node/edge colors) → Semantic taxonomy and visual grouping
- **Directionality** (arrow endpoints) → Information flow topology and execution order

## Visual Design Patterns

### Canvas Structure Design

```yaml
# Recommended canvas organization
spatial_hierarchy:
  - orphan_nodes: "Metadata, references, standalone concepts"
  - root_groups: "Major system boundaries"
  - nested_groups: "Component hierarchies"
  - flow_chains: "Process sequences with directional edges"

node_content_patterns:
  - yaml_frontmatter: "Structured metadata with templater variables"
  - markdown_headers: "Semantic identity extraction"
  - templater_syntax: "{{variable}} for dynamic content"
  - mermaid_diagrams: "Embedded flow visualization"
```

### Edge Semantics

| Edge Type | Purpose | Visual Cue | Compilation Result |
|-----------|---------|------------|-------------------|
| `model` | Architecture refinement | Solid arrow | Sequential design flow |
| `sequence` | Process derivation | Dashed arrow | Implementation order |
| `compile` | Direct transformation | Bold arrow | Bypass intermediate steps |
| `blocks` | Hard dependency | Red/thick line | Execution constraints |
| `relates` | Soft association | Dotted line | Conceptual relationships |

### Color Taxonomy

```yaml
semantic_colors:
  red: "Urgent/error/critical path"
  orange: "Warning/alternative path"
  yellow: "In-progress/horizontal flow"
  green: "Success/complete/horizontal connections"
  blue: "Info/reference/vertical connections"
  purple: "Special/custom/unique relationships"
```

## Compilation Workflows

### Basic Canvas Compilation

```javascript
// Semantic-JSON plugin compilation process
const compileCanvas = (canvasData) => {
  // 1. Spatial analysis
  const spatialOrder = analyzeSpatialSemantics(canvasData.nodes);
  
  // 2. Hierarchical ordering
  const hierarchicalNodes = buildHierarchy(spatialOrder);
  
  // 3. Edge processing
  const processedEdges = compileEdgeTopology(canvasData.edges);
  
  // 4. Deterministic output
  return {
    nodes: hierarchicalNodes,
    edges: processedEdges
  };
};
```

### Flow Topology Compilation

```yaml
# Flow sorting configuration
flow_analysis:
  edge_direction_semantics:
    forward_arrow: "fromEnd: none, toEnd: arrow (default)"
    reverse_arrow: "fromEnd: arrow, toEnd: none (dependency)"
    bidirectional: "fromEnd: arrow, toEnd: arrow (chain connector)"
    non_directional: "fromEnd: none, toEnd: none (ignored)"
  
  flow_depth_assignment:
    source_nodes: "depth: 0 (only outgoing arrows)"
    intermediate_nodes: "depth: longest_path_from_source"
    sink_nodes: "depth: max_depth (only incoming arrows)"
```

### Pure JSON Export

```javascript
// Strip Canvas metadata while preserving semantic structure
const exportPureJSON = (compiledCanvas, options = {}) => {
  const stripped = {
    nodes: compiledCanvas.nodes.map(node => ({
      id: node.id,
      type: node.type,
      ...(node.text && { text: node.text }),
      ...(node.file && { file: node.file }),
      ...(node.url && { url: node.url }),
      ...(node.label && { label: node.label })
    }))
  };
  
  // Handle labeled edge embedding
  if (options.embedLabeledEdges) {
    embedRelationships(stripped.nodes, compiledCanvas.edges);
  }
  
  // Handle unlabeled edges based on flow context
  if (!options.stripEdges) {
    stripped.edges = compiledCanvas.edges.filter(edge => !edge.label);
  }
  
  return stripped;
};
```

## Advanced Patterns

### Labeled Edge Embedding

```javascript
// Convert labeled edges to directional node properties
const embedRelationships = (nodes, edges) => {
  const labeledEdges = edges.filter(edge => edge.label);
  
  labeledEdges.forEach(edge => {
    // Add to source node's 'to' array
    const fromNode = nodes.find(n => n.id === edge.fromNode);
    if (!fromNode.to) fromNode.to = [];
    fromNode.to.push({ node: edge.toNode, label: edge.label });
    
    // Add to target node's 'from' array
    const toNode = nodes.find(n => n.id === edge.toNode);
    if (!toNode.from) toNode.from = [];
    toNode.from.push({ node: edge.fromNode, label: edge.label });
  });
};
```

### Content Identity Extraction

```javascript
// Extract semantic identity from structured content
const extractContentIdentity = (node) => {
  switch (node.type) {
    case 'text':
      // YAML frontmatter extraction
      const yamlMatch = node.text.match(/^---\n(.*?)\n---/s);
      if (yamlMatch) {
        const yaml = parseYAML(yamlMatch[1]);
        return yaml.title || yaml.name || yaml.id;
      }
      
      // Markdown header extraction
      const headerMatch = node.text.match(/^#+\s+(.+)$/m);
      if (headerMatch) {
        return headerMatch[1];
      }
      
      return node.text.substring(0, 50).trim();
      
    case 'file':
      return path.basename(node.file);
      
    case 'link':
      return node.url;
      
    case 'group':
      return node.label || 'Group';
      
    default:
      return node.id;
  }
};
```

### Import Scaffolding

```javascript
// Create Canvas from pure JSON data
const importJSONToCanvas = (jsonData, options = {}) => {
  const canvas = { nodes: [], edges: [] };
  let nodeId = 0;
  let x = 0, y = 0;
  
  const processValue = (value, key = null, depth = 0) => {
    const id = `node-${nodeId++}`;
    const baseX = x + (depth * 300);
    const baseY = y;
    
    if (Array.isArray(value)) {
      // Array → Group with child nodes
      const groupNode = {
        id,
        type: 'group',
        x: baseX,
        y: baseY,
        width: 250,
        height: value.length * 100 + 50,
        label: key ? `[${key}]` : '[Array]',
        color: options.arrayColor || '4'
      };
      canvas.nodes.push(groupNode);
      
      value.forEach((item, index) => {
        y += 100;
        processValue(item, index, depth + 1);
      });
      
    } else if (typeof value === 'object' && value !== null) {
      // Object → Group with property nodes
      const groupNode = {
        id,
        type: 'group',
        x: baseX,
        y: baseY,
        width: 250,
        height: Object.keys(value).length * 80 + 50,
        label: key || '{Object}',
        color: options.objectColor || '6'
      };
      canvas.nodes.push(groupNode);
      
      Object.entries(value).forEach(([k, v]) => {
        y += 80;
        processValue(v, k, depth + 1);
      });
      
    } else {
      // Primitive → Text node
      const textNode = {
        id,
        type: 'text',
        x: baseX,
        y: baseY,
        width: 200,
        height: 60,
        text: `**${key || 'Value'}**: ${value}`,
        color: options.primitiveColor || '2'
      };
      canvas.nodes.push(textNode);
      y += 80;
    }
  };
  
  processValue(jsonData);
  return canvas;
};
```

## Integration Patterns

### Artifacts System Integration
Canvas workflows integrate with the [artifacts system](../../artifacts/README.md) through:
- **Visual modeling infrastructure**: Canvas-to-semantic-JSON anticompiler workflows
- **Template repositories**: Reusable canvas patterns for common design scenarios
- **Reference implementations**: Example canvases demonstrating best practices
- **Quality standards**: Validation patterns for semantic consistency and structural integrity

### Workshop Recipe Integration

```yaml
# Recipe for Semantic-JSON compilation
recipe_id: semantic-json-compile
description: "Compile Canvas to structured JSON with semantic ordering"

inputs:
  - canvas_file: "*.canvas"
  - compilation_options:
      flow_sort: false
      color_sort: true
      group_orphans: false
      embed_labeled_edges: true

steps:
  - compile_spatial_semantics:
      source: "{{canvas_file}}"
      output: "compiled.json"
  
  - export_pure_json:
      source: "compiled.json"
      output: "{{target}}.json"
      strip_metadata: true
  
  - validate_structure:
      source: "{{target}}.json"
      schema: "semantic-json.schema"

outputs:
  - compiled_canvas: "compiled.json"
  - pure_data: "{{target}}.json"
```

### Kiro Spec Integration

```yaml
# Canvas-based spec template
spec_type: "canvas-driven"
phases:
  design:
    canvas_group: "design-phase-group"
    compilation: "spatial-semantic"
    output: "design-spec.json"
  
  requirements:
    canvas_group: "requirements-phase-group" 
    compilation: "flow-topology"
    output: "requirements-spec.json"
  
  tasks:
    canvas_group: "tasks-phase-group"
    compilation: "dependency-order"
    output: "tasks-spec.json"
```

### Templater Integration

```javascript
// Templater script for Canvas instantiation
<%*
const canvasTemplate = {
  nodes: [
    {
      id: "{{title-slug}}",
      type: "text",
      x: 0, y: 0, width: 400, height: 200,
      text: `---
id: {{id}}
title: "{{title}}"
type: ["{{type}}"]
status: "{{status}}"
---

# {{title}}

{{description}}`
    }
  ],
  edges: []
};

const canvasPath = `${tp.file.folder(true)}/{{title-slug}}.canvas`;
await app.vault.create(canvasPath, JSON.stringify(canvasTemplate, null, 2));
%>
```

## Validation and Quality Assurance

### Structural Validation

```javascript
// Validate Canvas structure for compilation
const validateCanvas = (canvasData) => {
  const errors = [];
  
  // Node validation
  const nodeIds = new Set();
  canvasData.nodes.forEach(node => {
    if (!node.id || typeof node.id !== 'string') {
      errors.push(`Invalid node ID: ${node.id}`);
    }
    if (nodeIds.has(node.id)) {
      errors.push(`Duplicate node ID: ${node.id}`);
    }
    nodeIds.add(node.id);
    
    if (!['text', 'file', 'link', 'group'].includes(node.type)) {
      errors.push(`Invalid node type: ${node.type}`);
    }
  });
  
  // Edge validation
  const edgeIds = new Set();
  canvasData.edges.forEach(edge => {
    if (!edge.id || edgeIds.has(edge.id)) {
      errors.push(`Invalid/duplicate edge ID: ${edge.id}`);
    }
    edgeIds.add(edge.id);
    
    if (!nodeIds.has(edge.fromNode)) {
      errors.push(`Edge references non-existent fromNode: ${edge.fromNode}`);
    }
    if (!nodeIds.has(edge.toNode)) {
      errors.push(`Edge references non-existent toNode: ${edge.toNode}`);
    }
  });
  
  return errors;
};
```

### Semantic Quality Checks

```javascript
// Validate semantic compilation quality
const validateSemanticCompilation = (originalCanvas, compiledCanvas) => {
  const checks = {
    nodeCount: originalCanvas.nodes.length === compiledCanvas.nodes.length,
    edgeCount: originalCanvas.edges.length === compiledCanvas.edges.length,
    spatialOrder: validateSpatialOrdering(compiledCanvas.nodes),
    hierarchicalStructure: validateHierarchy(compiledCanvas.nodes),
    edgeIntegrity: validateEdgeReferences(compiledCanvas)
  };
  
  return {
    valid: Object.values(checks).every(Boolean),
    checks
  };
};
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Scrambled node order | Obsidian auto-save | Use Semantic-JSON plugin compilation |
| Missing edge references | Invalid node IDs | Validate Canvas structure before compilation |
| Broken hierarchy | Overlapping groups | Adjust group boundaries or use explicit containment |
| Flow topology errors | Circular dependencies | Check edge directions and remove cycles |
| Export validation fails | Schema mismatch | Update schema or fix data structure |

### Debug Workflows

```javascript
// Debug Canvas compilation issues
const debugCompilation = (canvasData) => {
  console.log('=== Canvas Debug Info ===');
  
  // Spatial analysis
  const spatialStats = analyzeSpatialDistribution(canvasData.nodes);
  console.log('Spatial distribution:', spatialStats);
  
  // Hierarchy analysis
  const hierarchyStats = analyzeHierarchy(canvasData.nodes);
  console.log('Hierarchy structure:', hierarchyStats);
  
  // Flow analysis
  const flowStats = analyzeFlowTopology(canvasData.edges);
  console.log('Flow topology:', flowStats);
  
  // Validation results
  const validation = validateCanvas(canvasData);
  console.log('Validation errors:', validation);
};
```

## Performance Optimization

### Large Canvas Handling

```javascript
// Optimize compilation for large canvases
const optimizeCompilation = {
  // Spatial indexing for faster lookups
  spatialIndex: (nodes) => {
    const index = new Map();
    nodes.forEach(node => {
      const key = `${Math.floor(node.y / 100)}-${Math.floor(node.x / 100)}`;
      if (!index.has(key)) index.set(key, []);
      index.get(key).push(node);
    });
    return index;
  },
  
  // Batch processing for hierarchy building
  batchHierarchy: (nodes, batchSize = 100) => {
    const batches = [];
    for (let i = 0; i < nodes.length; i += batchSize) {
      batches.push(nodes.slice(i, i + batchSize));
    }
    return batches.map(batch => buildHierarchyBatch(batch));
  },
  
  // Streaming compilation for memory efficiency
  streamCompilation: async function* (canvasData) {
    yield* compileNodesStream(canvasData.nodes);
    yield* compileEdgesStream(canvasData.edges);
  }
};
```

## Future Enhancements

### Planned Features

- **Real-time collaboration**: Multi-user Canvas editing with semantic preservation
- **Version control integration**: Git-aware Canvas change tracking
- **Advanced templating**: Conditional Canvas generation with complex logic
- **Cross-platform export**: Integration with other visual modeling tools
- **AI-assisted layout**: Automatic spatial optimization for semantic clarity

### Integration Opportunities

- **Exocortex agents**: Canvas analysis and generation through specialized AI
- **Workshop automation**: Canvas-driven deployment pipelines
- **Kiro power packaging**: Canvas-based tool configuration and distribution
- **Multi-modal workflows**: Integration with other cognitive modeling approaches

---

*Visual modeling meets structured data. Design with canvas, process with semantic compilation, deploy with cognitive architecture.* 🎨