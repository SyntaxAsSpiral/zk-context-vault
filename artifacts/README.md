---
id: artifacts-readme
title: "Artifacts Directory"
type: 
  - "documentation"
  - "readme"
category: "artifacts"
tags:
  - "canvas"
  - "semantic-json"
  - "obsidian"
  - "visual-modeling"
  - "kiro-specs"
created: 2026-01-11
modified: 2026-01-11
status: "active"
glyph: "🎨"
lens: "visual-cognitive-modeling"
---

# Artifacts Directory

*Visual cognitive modeling through canvas-to-semantic-JSON workflows.*

## What This Is

This directory contains visual artifacts that bridge the gap between conceptual modeling and structured data. Using Obsidian Canvas for visual design and the [Semantic-JSON plugin](https://github.com/SyntaxAsSpiral/Semantic-JSON) for advanced JSON IDE features, these artifacts enable sophisticated visual-to-structured-data workflows.

Think of it as "visual programming for cognitive architecture" - where complex systems can be designed visually and then converted to structured formats for processing.

## The Canvas-to-Semantic-JSON Workflow

### The Anticompiler Philosophy

Semantic-JSON operates as an **anticompiler** - inverting the classical compilation process to restore human-legible structure from machine-dense formats. Where traditional compilers collapse alternatives and erase provenance, the anticompiler **decompresses intent** and makes implicit relations explicit.

**The Problem**: Obsidian scrambles Canvas JSON on every save, discarding semantic order and randomizing node positions. A canvas with logical flow (Title → Overview → Details) becomes an incoherent jumble where the title appears last in the array despite being visually first.

**The Solution**: Semantic compilation preserves spatial semantics as stable, deterministic structure - transforming visual language into linear reading order while maintaining full JSON Canvas spec compliance.

### Visual Design Phase
1. **Canvas Creation**: Design complex systems visually in Obsidian Canvas
2. **Spatial Semantics**: Position, containment, color, and directionality carry meaning
3. **Node Structure**: Use structured text nodes with YAML frontmatter and templater syntax
4. **Edge Semantics**: Define meaningful relationships through labeled edges with flow topology
5. **Group Organization**: Use canvas groups to represent system boundaries and hierarchical containment

### Semantic Compilation Phase
1. **Spatial Analysis**: Plugin reads canvas as visual language, extracting meaning from coordinates, colors, and topology
2. **Hierarchical Ordering**: Nodes compiled into reading sequence (top-to-bottom, left-to-right, depth-first through containment)
3. **Flow Topology**: Optional directional flow sorting transforms spatial diagrams into sequential narratives
4. **Edge Processing**: Labeled relationships embedded directly into nodes; unlabeled edges preserved or stripped based on flow context
5. **Deterministic Output**: Stable JSON with consistent field ordering, optimized for Git diffs and LLM ingestion

### Advanced Processing Features
1. **Pure JSON Export**: Strips Canvas metadata while preserving compiled semantic structure
2. **Labeled Edge Embedding**: Relationships become self-contained node properties with directional `from`/`to` arrays  
3. **Content Identity Extraction**: Surfaces semantic keys from YAML frontmatter, Markdown headers, and structured content
4. **Import Scaffolding**: Reverse process creates visual Canvas from pure JSON data structures

## Current Artifacts

### Implementation Spec Template
- **File**: [impl-spec-example.canvas](impl-spec-example.canvas)
- **Purpose**: Template for Kiro 3-phase specification process
- **Structure**: Design → Requirements → Tasks with preserved edge semantics
- **Features**: Templater integration, mermaid diagrams, task dependency modeling

**Edge Semantics**:
| Type | Purpose | Usage | Flow Context |
|------|---------|-------|--------------|
| `model` | SPEC → REQUIREMENTS refinement | Sequential design flow | Architectural modeling |
| `sequence` | REQUIREMENTS → TASKS derivation | Implementation flow | Process sequencing |
| `compile` | SPEC → TASKS shortcut | Direct compilation | Bypass intermediate steps |
| `blocks` | Hard dependency/order | Task scheduling | Execution constraints |
| `relates` | Soft association | Conceptual links | Semantic relationships |

### Canvas Compilation Features

**Spatial Semantic Compilation**: The plugin reads canvas as visual language where position, containment, color, and directionality encode meaning:
- **Position** (x, y coordinates) → Linear reading sequence (top-to-bottom, left-to-right)
- **Containment** (bounding boxes) → Hierarchical structure (depth-first traversal)
- **Color** (node/edge colors) → Semantic taxonomy and visual grouping
- **Directionality** (arrow endpoints) → Information flow topology and execution order

**Hierarchical Node Ordering**: Nodes compile into deterministic sequence preserving visual semantics:
1. **Root orphan nodes** (not contained by groups) - sorted spatially or semantically
2. **Root groups** (not nested) - followed immediately by all contents
3. **Nested groups** - recursive depth-first traversal with consistent sorting rules
4. **Flow topology** (optional) - directional edges define execution/dependency order

**Edge Processing Intelligence**:
- **Labeled edges** embedded as directional `from`/`to` arrays in connected nodes
- **Flow sorting** compiles edge topology into node sequence order
- **Spatial sorting** preserves visual relationships through coordinate-based ordering
- **Pure JSON export** strips Canvas metadata while preserving semantic structure

### Catppuccin Theme Canvas
- **File**: [🩷Catppuccin.canvas](golden/🩷Catppuccin.canvas)
- **Purpose**: Visual theme and color palette modeling
- **Integration**: Referenced in [bedtime prompt](../prompts/bedtime.md) for character design

## Semantic-JSON Plugin Integration

The [Semantic-JSON plugin](https://github.com/SyntaxAsSpiral/Semantic-JSON) transforms Obsidian into a sophisticated JSON IDE with **anticompiler** capabilities - inverting traditional compilation to restore human-legible structure from machine-dense formats.

### Core Anticompiler Features

**Semantic Decompression**: Where traditional compilers collapse alternatives and erase provenance, Semantic-JSON **decompresses intent** and makes implicit relations explicit:
- **Spatial semantics** → Linear reading order (preserves visual flow as sequential structure)
- **Hierarchical containment** → Depth-first traversal (bounding boxes become nested organization)  
- **Flow topology** → Sequential narratives (directional edges become execution order)
- **Color taxonomy** → Semantic grouping (visual categories become logical clusters)

**Stable Determinism**: Solves Obsidian's JSON scrambling problem:
- **Before**: Random node ordering, chaotic field sequences, impossible Git diffs
- **After**: Deterministic compilation preserving spatial intent as stable structure
- **Benefits**: Clean diffs, LLM-friendly structure, human-readable JSON

### Advanced JSON IDE Capabilities
- **Syntax highlighting** for complex JSON structures with Canvas-aware validation
- **Schema validation** ensuring proper node/edge structure and unique ID constraints
- **Intelligent autocomplete** for Canvas properties and templater syntax
- **Real-time compilation** with visual feedback and error detection
- **Smart recompilation** preserving semantic structure across saves

### Canvas-Specific Intelligence
- **Hierarchical ordering** with depth-first traversal through spatial containment
- **Flow analysis** transforming directional topology into sequential reading order
- **Edge embedding** converting labeled relationships into self-contained node properties
- **Content extraction** surfacing identity keys from YAML, Markdown, and structured text
- **Pure JSON export** stripping Canvas metadata while preserving compiled semantics

### Compilation Layers

**Layer 1: Spatial Semantic Compilation** *(active)*
- Coordinates → Reading sequence
- Bounding boxes → Hierarchical nesting  
- Edge directionality → Flow topology
- Color values → Semantic taxonomy

**Layer 2: Content Identity Extraction** *(planned)*
- YAML frontmatter → Identity keys (`title`, `name`, `id`)
- Markdown headers → Semantic labels (`# Title` → `"Title"`)
- Structured content → Meaningful node names

**Layer 3: Fallback Determinism** *(always active)*
- Alphabetical sorting for plain text
- Stable truncation for long content
- ID-based fallback for edge cases

## Integration with Cognitive Architecture

### Workshop System
Canvas artifacts integrate with the [workshop system](../workshop/README.md) through:
- **Slice extraction** from canvas node content
- **Recipe compilation** using canvas-defined structures
- **Template generation** from canvas patterns
- **Automated assembly** of visual designs into deployable formats

### Structured Development
Canvas files align with Kiro's 3-phase spec process:
- **Design phase** represented as visual canvas layout
- **Requirements phase** structured as detailed node content
- **Tasks phase** organized as dependency-linked task nodes

### Templater Integration
Canvas nodes support full templater functionality:
- **Dynamic content** generation through `{{variable}}` syntax
- **Interactive prompts** for canvas instantiation
- **Conditional logic** within node structures
- **Template inheritance** across canvas artifacts

## Usage Patterns

### Creating New Canvas Artifacts
1. **Start with template**: Copy existing canvas structure or use import scaffolding
2. **Design spatial semantics**: Position nodes to encode reading flow and hierarchical relationships
3. **Define edge topology**: Choose appropriate relationship types (`blocks`, `relates`, `model`, `sequence`, `compile`)
4. **Structure node content**: Use consistent YAML frontmatter and templater syntax `{{variable}}`
5. **Validate with compilation**: Use Semantic-JSON plugin to ensure structural integrity and stable ordering

### Converting Canvas to Structured Data
1. **Compile canvas**: Plugin automatically orders nodes/edges by spatial semantics and flow topology
2. **Export pure JSON**: Strip Canvas metadata while preserving compiled semantic structure
3. **Process relationships**: Labeled edges embedded as directional `from`/`to` arrays in nodes
4. **Extract structured content**: Parse YAML frontmatter, Markdown headers, and templater variables
5. **Deploy via workshop**: Use recipe system for target deployment with slice integration

### Visual System Modeling
1. **Map system boundaries**: Use canvas groups for component separation and hierarchical containment
2. **Define information flows**: Use labeled edges for process relationships and directional topology
3. **Model dependencies**: Use `blocks` edges for execution constraints and ordering requirements
4. **Document interfaces**: Use structured node content for API specifications and integration points
5. **Validate completeness**: Ensure all edge references exist and flow topology is coherent

### Advanced Anticompiler Workflows
1. **Spatial → Sequential**: Transform visual diagrams into linear narratives through flow compilation
2. **Hierarchical → Flat**: Extract nested group structures as sequential organization
3. **Relational → Embedded**: Convert edge networks into self-contained node relationships
4. **Visual → Semantic**: Compile color taxonomy and spatial positioning into logical structure
5. **Canvas → Data**: Generate clean JSON artifacts optimized for programmatic processing

## Advanced Patterns

### Multi-Phase Workflows
Canvas artifacts can represent complex multi-phase processes:
- **Phase separation** through visual grouping
- **Sequential flow** through edge semantics
- **Parallel processing** through independent node chains
- **Conditional branching** through edge labels and node content

### Template Hierarchies
Canvas templates can inherit and extend:
- **Base templates** defining common structure
- **Specialized templates** for specific domains
- **Composite templates** combining multiple patterns
- **Dynamic templates** with templater-driven variation

### Semantic Validation
The Semantic-JSON plugin enables sophisticated validation:
- **Schema enforcement** for node and edge structures
- **Reference integrity** checking for edge connections
- **Content validation** for embedded YAML and markdown
- **Template syntax** verification for templater expressions

## Future Enhancements

### Planned Features
- **Automated mermaid generation** from canvas structures
- **Real-time collaboration** on canvas artifacts
- **Version control integration** for canvas change tracking
- **Advanced templating** with conditional canvas generation

### Integration Opportunities
- **Exocortex agents** for canvas analysis and generation
- **Workshop automation** for canvas-driven deployments
- **Kiro power packaging** of canvas-based tools
- **Cross-platform export** to other visual modeling tools

---

*Visual modeling meets structured data. Design with canvas, process with semantic JSON, deploy with cognitive architecture.* 🎨

## Links

- **[Semantic-JSON Plugin](https://github.com/SyntaxAsSpiral/Semantic-JSON)** - Advanced JSON IDE for Obsidian
- **[Semantic-JSON Workflows Skill](../skills/semantic-json-workflows/README.md)** - Complete canvas-to-structured-data workflow mastery
- **[Workshop System](../workshop/README.md)** - Recipe-based assembly and deployment
- **[Agent System Architecture](../agents/README.md)** - Structured development processes
- **[Prompts](../prompts/README.md)** - Epistemic rendering stack integration