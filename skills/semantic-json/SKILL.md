---
name: semantic-json
description: Use when working with Obsidian Canvas files as cognitive modeling tools — compiling spatial/visual structure into deterministic JSON, designing canvas layouts with semantic color and edge conventions, exporting structured data from canvas, or importing JSON into canvas form.
---

# Semantic-JSON

*Canvas-to-structured-data anticompiler workflows for visual cognitive modeling.*

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

---

## Semantic-JSON Plugin

> The plugin is generally present in ZK's vaults. If absent, the compilation workflows below can be done manually by editing the `.canvas` JSON directly.

**Author:** Zach Battin — [github.com/SyntaxAsSpiral/Semantic-JSON](https://github.com/SyntaxAsSpiral/Semantic-JSON)  
**Version:** 0.3.0 · Desktop only · Requires Obsidian ≥ 1.5.0

### Commands

| Full command ID (for `executeCommandById`) | Name | Effect |
|---------------------------------------------|------|--------|
| `semantic-json:compile-active-canvas` | Compile active canvas | Reorders nodes/edges by spatial semantics and flow topology |
| `semantic-json:export-as-pure-json` | Export as pure JSON | Strips Canvas metadata, embeds labeled edges, outputs clean JSON |
| `semantic-json:import-json-to-canvas` | Import JSON to canvas | Scaffolds a `.canvas` from a pure JSON data structure |

Run via Obsidian command palette or bind to a hotkey.

### Settings (`data.json`)

| Setting | Default | Effect |
|---------|---------|--------|
| `autoCompile` | `true` | Compiles on every canvas save |
| `colorSortNodes` | `true` | Groups nodes by color value during compilation |
| `colorSortEdges` | `true` | Groups edges by color value |
| `flowSortNodes` | `true` | Applies flow topology ordering (depth-first from source nodes) |
| `semanticSortOrphans` | `false` | Semantically sorts nodes not contained by any group |
| `stripEdgesWhenFlowSorted` | `true` | Removes unlabeled edges from output when flow sort is active |

With `autoCompile: true` the canvas is recompiled on every save — manual invocation of `compile-active-canvas` is only needed to force a recompile without saving.

### Agent Workflow: Reading Complex Canvases

Raw Obsidian canvas JSON is scrambled on every save — node order is random, spatial metadata adds noise, and edge relationships are unembedded. For large or complex canvases, always export clean JSON before attempting to read or analyze.

```bash
# Open the canvas and export clean JSON via obsidian CLI
obsidian open path="path/to/canvas.canvas" silent
obsidian eval code="app.commands.executeCommandById('semantic-json:export-as-pure-json')"
```

The export writes a `.json` file alongside the canvas (same name, `.json` extension). Read that file instead of the raw `.canvas`.

**What you get:**
- Nodes in deterministic spatial order (top-to-bottom, left-to-right, depth-first through groups)
- Labeled edges embedded as `from`/`to` arrays on nodes — no need to cross-reference edge list
- Canvas metadata (coordinates, dimensions) stripped — just content and structure
- Flow topology resolved into sequential order when `flowSortNodes` is active

**When to use:** Any canvas with more than ~10 nodes, nested groups, or labeled edge relationships. For small flat canvases the raw JSON is readable; for anything complex the compiled export is significantly lower noise.

---

## Canvas JSON Spec

A `.canvas` file is JSON with two top-level arrays:

```json
{ "nodes": [], "edges": [] }
```

### Node Types

All nodes require: `id` (16-char hex), `type`, `x`, `y`, `width`, `height`.

| Type | Extra required field | Notes |
|------|----------------------|-------|
| `text` | `text` (string, Markdown) | Use `\n` for newlines — never `\\n` |
| `file` | `file` (vault-relative path) | Optional: `subpath` (`#heading` or `#^block`) |
| `link` | `url` | External URL |
| `group` | — | Optional: `label`, `background`, `backgroundStyle` |

Array order = z-index: first node is bottom layer.

### Edge Attributes

| Attribute | Required | Default | Values |
|-----------|----------|---------|--------|
| `id` | Yes | — | unique string |
| `fromNode` | Yes | — | node id |
| `toNode` | Yes | — | node id |
| `fromSide` | No | — | `top` `right` `bottom` `left` |
| `toSide` | No | — | `top` `right` `bottom` `left` |
| `fromEnd` | No | `none` | `none` `arrow` |
| `toEnd` | No | `arrow` | `none` `arrow` |
| `color` | No | — | preset or hex |
| `label` | No | — | string |

### IDs

Generate 16-character lowercase hex strings: `"6f0ad84f44ce9c17"`. IDs must be unique across both nodes and edges.

### Layout

- `x` increases right, `y` increases down; position is top-left corner
- Coordinates can be negative (infinite canvas)
- Space nodes 50–100px apart; 20–50px padding inside groups
- Align to grid multiples of 10 or 20

### Validation Checklist

After creating or editing a canvas:
1. All `id` values unique across nodes and edges
2. Every `fromNode`/`toNode` references an existing node ID
3. Required fields present per node type
4. `type` is one of: `text`, `file`, `link`, `group`
5. `fromSide`/`toSide` one of: `top`, `right`, `bottom`, `left`
6. `fromEnd`/`toEnd` one of: `none`, `arrow`
7. Color presets are `"1"`–`"6"` or valid hex
8. JSON is valid and parseable (watch for unescaped newlines in `text` fields)

---

## Visual Design Patterns

### Canvas Structure Design

```yaml
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

| Preset | Color | Semantic meaning |
|--------|-------|-----------------|
| `"1"` | Red | Urgent / error / critical path |
| `"2"` | Orange | Warning / alternative path |
| `"3"` | Yellow | In-progress / horizontal flow |
| `"4"` | Green | Success / complete / horizontal connections |
| `"5"` | Cyan | Info / reference / vertical connections |
| `"6"` | Purple | Special / custom / unique relationships |

---

## Compilation Workflows

### Basic Canvas Compilation

```javascript
const compileCanvas = (canvasData) => {
  const spatialOrder = analyzeSpatialSemantics(canvasData.nodes);
  const hierarchicalNodes = buildHierarchy(spatialOrder);
  const processedEdges = compileEdgeTopology(canvasData.edges);
  return { nodes: hierarchicalNodes, edges: processedEdges };
};
```

### Flow Topology Compilation

```yaml
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
  if (options.embedLabeledEdges) embedRelationships(stripped.nodes, compiledCanvas.edges);
  if (!options.stripEdges) stripped.edges = compiledCanvas.edges.filter(e => !e.label);
  return stripped;
};
```

---

## Advanced Patterns

### Labeled Edge Embedding

```javascript
const embedRelationships = (nodes, edges) => {
  edges.filter(e => e.label).forEach(edge => {
    const from = nodes.find(n => n.id === edge.fromNode);
    if (!from.to) from.to = [];
    from.to.push({ node: edge.toNode, label: edge.label });

    const to = nodes.find(n => n.id === edge.toNode);
    if (!to.from) to.from = [];
    to.from.push({ node: edge.fromNode, label: edge.label });
  });
};
```

### Content Identity Extraction

```javascript
const extractContentIdentity = (node) => {
  switch (node.type) {
    case 'text': {
      const yaml = node.text.match(/^---\n(.*?)\n---/s);
      if (yaml) { const p = parseYAML(yaml[1]); return p.title || p.name || p.id; }
      const header = node.text.match(/^#+\s+(.+)$/m);
      if (header) return header[1];
      return node.text.substring(0, 50).trim();
    }
    case 'file':  return path.basename(node.file);
    case 'link':  return node.url;
    case 'group': return node.label || 'Group';
    default:      return node.id;
  }
};
```

### Import Scaffolding

```javascript
const importJSONToCanvas = (jsonData, options = {}) => {
  const canvas = { nodes: [], edges: [] };
  let nodeId = 0, x = 0, y = 0;

  const processValue = (value, key = null, depth = 0) => {
    const id = `node-${nodeId++}`;
    const baseX = x + (depth * 300);

    if (Array.isArray(value)) {
      canvas.nodes.push({ id, type: 'group', x: baseX, y, width: 250,
        height: value.length * 100 + 50, label: key ? `[${key}]` : '[Array]',
        color: options.arrayColor || '4' });
      value.forEach((item, i) => { y += 100; processValue(item, i, depth + 1); });

    } else if (typeof value === 'object' && value !== null) {
      canvas.nodes.push({ id, type: 'group', x: baseX, y, width: 250,
        height: Object.keys(value).length * 80 + 50, label: key || '{Object}',
        color: options.objectColor || '6' });
      Object.entries(value).forEach(([k, v]) => { y += 80; processValue(v, k, depth + 1); });

    } else {
      canvas.nodes.push({ id, type: 'text', x: baseX, y, width: 200, height: 60,
        text: `**${key || 'Value'}**: ${value}`, color: options.primitiveColor || '2' });
      y += 80;
    }
  };

  processValue(jsonData);
  return canvas;
};
```

---

## Integration Patterns

### Artifacts System Integration

Canvas workflows integrate with the [artifacts system](../../artifacts/README.md) through:
- **Visual modeling infrastructure**: Canvas-to-semantic-JSON anticompiler workflows
- **Template repositories**: Reusable canvas patterns for common design scenarios
- **Reference implementations**: Example canvases demonstrating best practices

### Workshop Recipe Integration

```yaml
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

### Templater Integration

```javascript
<%*
const canvasTemplate = {
  nodes: [{
    id: "{{title-slug}}",
    type: "text",
    x: 0, y: 0, width: 400, height: 200,
    text: `---\nid: {{id}}\ntitle: "{{title}}"\ntype: ["{{type}}"]\nstatus: "{{status}}"\n---\n\n# {{title}}\n\n{{description}}`
  }],
  edges: []
};
const canvasPath = `${tp.file.folder(true)}/{{title-slug}}.canvas`;
await app.vault.create(canvasPath, JSON.stringify(canvasTemplate, null, 2));
%>
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Scrambled node order | Obsidian auto-save | Use Semantic-JSON plugin compilation |
| Missing edge references | Invalid node IDs | Validate canvas structure before compilation |
| Broken hierarchy | Overlapping groups | Adjust group boundaries or use explicit containment |
| Flow topology errors | Circular dependencies | Check edge directions and remove cycles |
| Export validation fails | Schema mismatch | Update schema or fix data structure |

### Debug

```javascript
const debugCompilation = (canvasData) => {
  console.log('Spatial:', analyzeSpatialDistribution(canvasData.nodes));
  console.log('Hierarchy:', analyzeHierarchy(canvasData.nodes));
  console.log('Flow:', analyzeFlowTopology(canvasData.edges));
  console.log('Errors:', validateCanvas(canvasData));
};
```
