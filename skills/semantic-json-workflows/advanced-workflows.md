# Advanced Semantic-JSON Workflows

Master sophisticated canvas-to-structured-data patterns for complex visual cognitive modeling and multi-system integration.

## Complex Canvas Architectures

### Multi-Phase Development Canvases

Create comprehensive development specifications using the Kiro 3-phase pattern:

```json
{
  "nodes": [
    {
      "id": "design-phase-group",
      "type": "group",
      "x": 0, "y": 0, "width": 800, "height": 400,
      "label": "1. Design Phase",
      "color": "6"
    },
    {
      "id": "requirements-phase-group", 
      "type": "group",
      "x": 850, "y": 0, "width": 800, "height": 400,
      "label": "2. Requirements Phase",
      "color": "5"
    },
    {
      "id": "tasks-phase-group",
      "type": "group", 
      "x": 0, "y": 450, "width": 1650, "height": 600,
      "label": "3. Tasks Phase",
      "color": "4"
    }
  ],
  "edges": [
    {
      "id": "design-to-requirements",
      "fromNode": "design-phase-group",
      "toNode": "requirements-phase-group",
      "label": "model"
    },
    {
      "id": "requirements-to-tasks",
      "fromNode": "requirements-phase-group", 
      "toNode": "tasks-phase-group",
      "label": "sequence"
    },
    {
      "id": "design-to-tasks-direct",
      "fromNode": "design-phase-group",
      "toNode": "tasks-phase-group", 
      "label": "compile"
    }
  ]
}
```

### Exocortex Agent Coordination

Model distributed cognition through specialized agent workflows:

```json
{
  "nodes": [
    {
      "id": "council-agent",
      "type": "text",
      "x": 400, "y": 0, "width": 300, "height": 150,
      "color": "#cba6f7",
      "text": "## Council Agent\n\n- Coordination\n- Decision synthesis\n- Conflict resolution"
    },
    {
      "id": "gnomon-agent",
      "type": "text", 
      "x": 0, "y": 200, "width": 250, "height": 150,
      "color": "#89b4fa",
      "text": "## Gnomon Agent\n\n- Pattern recognition\n- Trend analysis\n- Temporal reasoning"
    },
    {
      "id": "antibody-agent",
      "type": "text",
      "x": 300, "y": 200, "width": 250, "height": 150, 
      "color": "#a6e3a1",
      "text": "## Antibody Agent\n\n- Error detection\n- Quality assurance\n- Validation"
    },
    {
      "id": "triquetra-agent",
      "type": "text",
      "x": 600, "y": 200, "width": 250, "height": 150,
      "color": "#f9e2af", 
      "text": "## Triquetra Agent\n\n- Creative synthesis\n- Novel combinations\n- Innovation"
    },
    {
      "id": "mutation-agent",
      "type": "text",
      "x": 900, "y": 200, "width": 250, "height": 150,
      "color": "#fab387",
      "text": "## Mutation Agent\n\n- Variation generation\n- Exploration\n- Adaptation"
    }
  ],
  "edges": [
    {
      "id": "council-coordinates-gnomon",
      "fromNode": "council-agent",
      "toNode": "gnomon-agent", 
      "label": "coordinates"
    },
    {
      "id": "gnomon-informs-antibody",
      "fromNode": "gnomon-agent",
      "toNode": "antibody-agent",
      "label": "informs"
    },
    {
      "id": "antibody-validates-triquetra", 
      "fromNode": "antibody-agent",
      "toNode": "triquetra-agent",
      "label": "validates"
    },
    {
      "id": "triquetra-inspires-mutation",
      "fromNode": "triquetra-agent", 
      "toNode": "mutation-agent",
      "label": "inspires"
    },
    {
      "id": "mutation-feeds-council",
      "fromNode": "mutation-agent",
      "toNode": "council-agent",
      "label": "feeds-back"
    }
  ]
}
```

## Advanced Compilation Techniques

### Flow Topology Analysis

Enable sophisticated dependency analysis through flow sorting:

```javascript
// Advanced flow compilation with cycle detection
class FlowTopologyCompiler {
  constructor(canvas) {
    this.nodes = new Map(canvas.nodes.map(n => [n.id, n]));
    this.edges = canvas.edges;
    this.flowGroups = new Map();
  }
  
  analyzeFlowTopology() {
    // Build adjacency graph
    const graph = this.buildDirectedGraph();
    
    // Detect cycles
    const cycles = this.detectCycles(graph);
    if (cycles.length > 0) {
      throw new Error(`Circular dependencies detected: ${cycles.join(', ')}`);
    }
    
    // Compute topological ordering
    const topologicalOrder = this.topologicalSort(graph);
    
    // Assign flow depths
    return this.assignFlowDepths(topologicalOrder);
  }
  
  buildDirectedGraph() {
    const graph = new Map();
    
    // Initialize nodes
    for (const node of this.nodes.values()) {
      graph.set(node.id, { outgoing: [], incoming: [] });
    }
    
    // Add edges
    for (const edge of this.edges) {
      if (this.isDirectionalEdge(edge)) {
        graph.get(edge.fromNode).outgoing.push(edge.toNode);
        graph.get(edge.toNode).incoming.push(edge.fromNode);
      }
    }
    
    return graph;
  }
  
  isDirectionalEdge(edge) {
    // Check edge direction semantics
    const hasForwardArrow = edge.toEnd === 'arrow' && edge.fromEnd !== 'arrow';
    const hasReverseArrow = edge.fromEnd === 'arrow' && edge.toEnd !== 'arrow';
    const isBidirectional = edge.fromEnd === 'arrow' && edge.toEnd === 'arrow';
    
    return hasForwardArrow || hasReverseArrow || isBidirectional;
  }
  
  detectCycles(graph) {
    const visited = new Set();
    const recursionStack = new Set();
    const cycles = [];
    
    const dfs = (nodeId, path) => {
      if (recursionStack.has(nodeId)) {
        const cycleStart = path.indexOf(nodeId);
        cycles.push(path.slice(cycleStart).join(' → '));
        return;
      }
      
      if (visited.has(nodeId)) return;
      
      visited.add(nodeId);
      recursionStack.add(nodeId);
      path.push(nodeId);
      
      for (const neighbor of graph.get(nodeId).outgoing) {
        dfs(neighbor, [...path]);
      }
      
      recursionStack.delete(nodeId);
    };
    
    for (const nodeId of graph.keys()) {
      if (!visited.has(nodeId)) {
        dfs(nodeId, []);
      }
    }
    
    return cycles;
  }
  
  topologicalSort(graph) {
    const inDegree = new Map();
    const queue = [];
    const result = [];
    
    // Calculate in-degrees
    for (const [nodeId, connections] of graph) {
      inDegree.set(nodeId, connections.incoming.length);
      if (connections.incoming.length === 0) {
        queue.push(nodeId);
      }
    }
    
    // Kahn's algorithm
    while (queue.length > 0) {
      const current = queue.shift();
      result.push(current);
      
      for (const neighbor of graph.get(current).outgoing) {
        inDegree.set(neighbor, inDegree.get(neighbor) - 1);
        if (inDegree.get(neighbor) === 0) {
          queue.push(neighbor);
        }
      }
    }
    
    return result;
  }
  
  assignFlowDepths(topologicalOrder) {
    const depths = new Map();
    
    for (const nodeId of topologicalOrder) {
      const incoming = this.getIncomingNodes(nodeId);
      if (incoming.length === 0) {
        depths.set(nodeId, 0); // Source node
      } else {
        const maxIncomingDepth = Math.max(...incoming.map(id => depths.get(id)));
        depths.set(nodeId, maxIncomingDepth + 1);
      }
    }
    
    return depths;
  }
}
```

### Labeled Edge Embedding

Transform edge relationships into self-contained node properties:

```javascript
// Advanced edge embedding with relationship analysis
class LabeledEdgeEmbedder {
  constructor(canvas) {
    this.nodes = new Map(canvas.nodes.map(n => [n.id, n]));
    this.edges = canvas.edges;
  }
  
  embedRelationships() {
    const labeledEdges = this.edges.filter(edge => edge.label);
    const relationshipMap = this.buildRelationshipMap(labeledEdges);
    
    // Embed relationships into nodes
    for (const [nodeId, relationships] of relationshipMap) {
      const node = this.nodes.get(nodeId);
      if (relationships.outgoing.length > 0) {
        node.to = relationships.outgoing;
      }
      if (relationships.incoming.length > 0) {
        node.from = relationships.incoming;
      }
    }
    
    // Remove embedded edges from main array
    const unlabeledEdges = this.edges.filter(edge => !edge.label);
    
    return {
      nodes: Array.from(this.nodes.values()),
      edges: unlabeledEdges,
      relationshipStats: this.analyzeRelationships(relationshipMap)
    };
  }
  
  buildRelationshipMap(labeledEdges) {
    const map = new Map();
    
    // Initialize all nodes
    for (const nodeId of this.nodes.keys()) {
      map.set(nodeId, { outgoing: [], incoming: [] });
    }
    
    // Process labeled edges
    for (const edge of labeledEdges) {
      const relationship = {
        node: edge.toNode,
        label: edge.label,
        edgeId: edge.id
      };
      
      const reverseRelationship = {
        node: edge.fromNode,
        label: edge.label,
        edgeId: edge.id
      };
      
      map.get(edge.fromNode).outgoing.push(relationship);
      map.get(edge.toNode).incoming.push(reverseRelationship);
    }
    
    return map;
  }
  
  analyzeRelationships(relationshipMap) {
    const stats = {
      totalRelationships: 0,
      relationshipTypes: new Map(),
      nodeConnectivity: new Map(),
      hubNodes: [],
      isolatedNodes: []
    };
    
    for (const [nodeId, relationships] of relationshipMap) {
      const totalConnections = relationships.outgoing.length + relationships.incoming.length;
      stats.nodeConnectivity.set(nodeId, totalConnections);
      
      if (totalConnections === 0) {
        stats.isolatedNodes.push(nodeId);
      } else if (totalConnections >= 5) {
        stats.hubNodes.push(nodeId);
      }
      
      // Count relationship types
      for (const rel of [...relationships.outgoing, ...relationships.incoming]) {
        const count = stats.relationshipTypes.get(rel.label) || 0;
        stats.relationshipTypes.set(rel.label, count + 1);
        stats.totalRelationships++;
      }
    }
    
    return stats;
  }
}
```

### Content Identity Extraction

Advanced semantic key extraction from structured content:

```javascript
// Sophisticated content analysis and identity extraction
class ContentIdentityExtractor {
  constructor() {
    this.yamlParser = require('js-yaml');
    this.markdownParser = require('markdown-it')();
  }
  
  extractIdentity(node) {
    switch (node.type) {
      case 'text':
        return this.extractFromText(node.text);
      case 'file':
        return this.extractFromFile(node.file, node.subpath);
      case 'link':
        return this.extractFromURL(node.url);
      case 'group':
        return this.extractFromGroup(node.label);
      default:
        return { id: node.id, type: 'unknown' };
    }
  }
  
  extractFromText(text) {
    // Try YAML frontmatter first
    const yamlMatch = text.match(/^---\n(.*?)\n---/s);
    if (yamlMatch) {
      try {
        const yaml = this.yamlParser.load(yamlMatch[1]);
        return {
          id: yaml.id || yaml.name || yaml.title,
          title: yaml.title,
          type: yaml.type,
          category: yaml.category,
          tags: yaml.tags,
          status: yaml.status,
          metadata: yaml
        };
      } catch (e) {
        // Fall through to other extraction methods
      }
    }
    
    // Try Markdown headers
    const headerMatch = text.match(/^(#{1,6})\s+(.+)$/m);
    if (headerMatch) {
      const level = headerMatch[1].length;
      const title = headerMatch[2].trim();
      return {
        id: this.slugify(title),
        title: title,
        type: 'markdown-section',
        level: level,
        content: text
      };
    }
    
    // Try structured lists
    const listMatch = text.match(/^[-*+]\s+(.+)/m);
    if (listMatch) {
      return {
        id: this.slugify(listMatch[1]),
        title: listMatch[1],
        type: 'list-item',
        content: text
      };
    }
    
    // Fallback to first line
    const firstLine = text.split('\n')[0].trim();
    return {
      id: this.slugify(firstLine),
      title: firstLine,
      type: 'text-content',
      content: text
    };
  }
  
  extractFromFile(filePath, subpath) {
    const fileName = filePath.split('/').pop();
    const baseName = fileName.replace(/\.[^/.]+$/, "");
    
    let identity = {
      id: this.slugify(baseName),
      title: baseName,
      type: 'file-reference',
      filePath: filePath,
      fileName: fileName
    };
    
    if (subpath) {
      // Handle heading/block references
      const cleanSubpath = subpath.replace(/^#/, '');
      identity.subpath = cleanSubpath;
      identity.id += `-${this.slugify(cleanSubpath)}`;
      identity.title += ` (${cleanSubpath})`;
    }
    
    return identity;
  }
  
  extractFromURL(url) {
    try {
      const urlObj = new URL(url);
      const domain = urlObj.hostname;
      const path = urlObj.pathname;
      
      // Try to extract meaningful title from URL
      let title = domain;
      if (path && path !== '/') {
        const pathSegments = path.split('/').filter(Boolean);
        title = pathSegments[pathSegments.length - 1] || domain;
      }
      
      return {
        id: this.slugify(`${domain}-${title}`),
        title: title,
        type: 'url-reference',
        url: url,
        domain: domain,
        path: path
      };
    } catch (e) {
      return {
        id: this.slugify(url),
        title: url,
        type: 'url-reference',
        url: url
      };
    }
  }
  
  extractFromGroup(label) {
    if (!label) {
      return {
        id: 'unnamed-group',
        title: 'Unnamed Group',
        type: 'group-container'
      };
    }
    
    return {
      id: this.slugify(label),
      title: label,
      type: 'group-container',
      label: label
    };
  }
  
  slugify(text) {
    return text
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .replace(/[\s_-]+/g, '-')
      .replace(/^-+|-+$/g, '');
  }
}
```

## Integration Architectures

### Workshop Recipe Orchestration

Complex multi-step canvas processing pipelines:

```yaml
# advanced-canvas-pipeline.yml
recipe_id: advanced-canvas-pipeline
description: "Comprehensive canvas processing with validation and deployment"

inputs:
  - canvas_directory: "canvases/"
  - output_directory: "compiled/"
  - validation_schema: "schemas/canvas-schema.json"
  - deployment_targets: ["web", "api", "docs"]

variables:
  timestamp: "{{date:YYYY-MM-DD-HH-mm-ss}}"
  version: "{{git:short-hash}}"

steps:
  - discover_canvases:
      source: "{{canvas_directory}}"
      pattern: "*.canvas"
      output: "canvas_list.json"
  
  - validate_structure:
      source: "{{canvas_list}}"
      schema: "{{validation_schema}}"
      output: "validation_report.json"
      fail_on_error: true
  
  - compile_spatial_semantics:
      source: "{{canvas_list}}"
      output: "{{output_directory}}/compiled/"
      options:
        flow_sort: true
        color_sort: true
        embed_labeled_edges: true
        extract_content_identity: true
  
  - generate_documentation:
      source: "{{output_directory}}/compiled/"
      template: "templates/canvas-docs.md"
      output: "{{output_directory}}/docs/"
  
  - export_api_schemas:
      source: "{{output_directory}}/compiled/"
      format: "openapi"
      output: "{{output_directory}}/api/"
  
  - deploy_artifacts:
      source: "{{output_directory}}/"
      targets: "{{deployment_targets}}"
      version: "{{version}}"
      timestamp: "{{timestamp}}"

outputs:
  - validation_report: "validation_report.json"
  - compiled_canvases: "{{output_directory}}/compiled/"
  - documentation: "{{output_directory}}/docs/"
  - api_schemas: "{{output_directory}}/api/"
  - deployment_manifest: "deployment-{{version}}.json"

error_handling:
  - validation_failure: "halt_pipeline"
  - compilation_error: "log_and_continue"
  - deployment_failure: "rollback_and_notify"
```

### Exocortex Agent Workflows

Canvas-driven multi-agent coordination:

```yaml
# exocortex-canvas-workflow.yml
agent_coordination:
  canvas_source: "agent-workflows.canvas"
  
  agents:
    council:
      role: "coordination"
      canvas_nodes: ["council-agent"]
      responsibilities:
        - "Orchestrate agent interactions"
        - "Resolve conflicts between agents"
        - "Synthesize final decisions"
    
    gnomon:
      role: "analysis"
      canvas_nodes: ["gnomon-agent", "pattern-analysis"]
      responsibilities:
        - "Identify patterns in canvas structure"
        - "Analyze temporal relationships"
        - "Provide trend insights"
    
    antibody:
      role: "validation"
      canvas_nodes: ["antibody-agent", "quality-checks"]
      responsibilities:
        - "Validate canvas structure"
        - "Check semantic consistency"
        - "Ensure quality standards"
    
    triquetra:
      role: "synthesis"
      canvas_nodes: ["triquetra-agent", "creative-combinations"]
      responsibilities:
        - "Generate novel canvas patterns"
        - "Combine existing structures"
        - "Propose innovations"
    
    mutation:
      role: "exploration"
      canvas_nodes: ["mutation-agent", "variations"]
      responsibilities:
        - "Explore canvas variations"
        - "Generate alternative structures"
        - "Test new approaches"

  workflow:
    - phase: "analysis"
      agents: ["gnomon"]
      canvas_input: "raw-canvas.canvas"
      output: "analysis-report.json"
    
    - phase: "validation"
      agents: ["antibody"]
      canvas_input: "raw-canvas.canvas"
      dependencies: ["analysis"]
      output: "validation-report.json"
    
    - phase: "synthesis"
      agents: ["triquetra", "mutation"]
      canvas_input: "raw-canvas.canvas"
      dependencies: ["analysis", "validation"]
      output: "synthesis-options.json"
    
    - phase: "coordination"
      agents: ["council"]
      canvas_input: "synthesis-options.json"
      dependencies: ["synthesis"]
      output: "final-canvas.canvas"
```

## Performance and Scalability

### Large Canvas Optimization

Handle complex canvases with thousands of nodes:

```javascript
// Optimized compilation for large canvases
class LargeCanvasCompiler {
  constructor(options = {}) {
    this.batchSize = options.batchSize || 1000;
    this.useWorkers = options.useWorkers || false;
    this.cacheEnabled = options.cacheEnabled || true;
    this.spatialIndex = new SpatialIndex();
  }
  
  async compileCanvas(canvas) {
    // Build spatial index for fast lookups
    this.spatialIndex.buildIndex(canvas.nodes);
    
    // Process in batches to avoid memory issues
    const nodeBatches = this.createBatches(canvas.nodes, this.batchSize);
    const compiledBatches = [];
    
    for (const batch of nodeBatches) {
      if (this.useWorkers) {
        compiledBatches.push(await this.compileWithWorker(batch));
      } else {
        compiledBatches.push(this.compileBatch(batch));
      }
    }
    
    // Merge batches maintaining semantic order
    const compiledNodes = this.mergeBatches(compiledBatches);
    
    // Process edges with optimized algorithms
    const compiledEdges = await this.compileEdgesOptimized(canvas.edges);
    
    return {
      nodes: compiledNodes,
      edges: compiledEdges,
      metadata: {
        originalNodeCount: canvas.nodes.length,
        compiledNodeCount: compiledNodes.length,
        processingTime: Date.now() - this.startTime,
        batchCount: nodeBatches.length
      }
    };
  }
  
  createBatches(nodes, batchSize) {
    const batches = [];
    for (let i = 0; i < nodes.length; i += batchSize) {
      batches.push(nodes.slice(i, i + batchSize));
    }
    return batches;
  }
  
  async compileWithWorker(batch) {
    return new Promise((resolve, reject) => {
      const worker = new Worker('canvas-compiler-worker.js');
      worker.postMessage({ batch, options: this.options });
      
      worker.onmessage = (e) => {
        resolve(e.data);
        worker.terminate();
      };
      
      worker.onerror = (error) => {
        reject(error);
        worker.terminate();
      };
    });
  }
}

// Spatial indexing for fast containment queries
class SpatialIndex {
  constructor() {
    this.grid = new Map();
    this.cellSize = 100; // pixels
  }
  
  buildIndex(nodes) {
    this.grid.clear();
    
    for (const node of nodes) {
      const cells = this.getCellsForNode(node);
      for (const cell of cells) {
        if (!this.grid.has(cell)) {
          this.grid.set(cell, []);
        }
        this.grid.get(cell).push(node);
      }
    }
  }
  
  getCellsForNode(node) {
    const cells = [];
    const startX = Math.floor(node.x / this.cellSize);
    const endX = Math.floor((node.x + node.width) / this.cellSize);
    const startY = Math.floor(node.y / this.cellSize);
    const endY = Math.floor((node.y + node.height) / this.cellSize);
    
    for (let x = startX; x <= endX; x++) {
      for (let y = startY; y <= endY; y++) {
        cells.push(`${x},${y}`);
      }
    }
    
    return cells;
  }
  
  findContainedNodes(containerNode) {
    const candidateCells = this.getCellsForNode(containerNode);
    const candidates = new Set();
    
    for (const cell of candidateCells) {
      const cellNodes = this.grid.get(cell) || [];
      for (const node of cellNodes) {
        candidates.add(node);
      }
    }
    
    // Filter to actually contained nodes
    return Array.from(candidates).filter(node => 
      this.isContained(node, containerNode)
    );
  }
  
  isContained(node, container) {
    return node.x >= container.x &&
           node.y >= container.y &&
           node.x + node.width <= container.x + container.width &&
           node.y + node.height <= container.y + container.height;
  }
}
```

Transform complex visual models into sophisticated structured systems. Master the anticompiler, harness spatial semantics, deploy with precision! 🎨⚡