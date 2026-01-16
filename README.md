# Context Vault

*A comprehensive cognitive infrastructure for AI-augmented development and knowledge work.*

**Status**: ✓ Working baseline established with unified sync workflow

> **Note**: This is ZK's personal context vault with ZK-specific content. The **workshop system** (assembly scripts, templates, recipe patterns in `workshop/`) is designed to be reusable with any content library. See [AGENTS.md](AGENTS.md) for adaptation guidance.

## What This Is

This is not just documentation. It's a **cognitive infrastructure**—a systematic approach to context engineering, agent systems, and knowledge management that transforms how you work with AI. The vault provides the foundational patterns, tools, and frameworks needed to build sophisticated AI-augmented workflows while maintaining epistemic hygiene and assumption-hostile design.

Think of it as "the missing manual for working with AI systems at scale."

## The Architecture

The vault operates through 7 core systems that form a complete cognitive stack:

```
Principles → Skills → Agents → Prompts → Artifacts → Workshop → Exocortex
     ↓         ↓        ↓        ↓         ↓          ↓         ↓
Foundation → Capabilities → Identity → Cognition → Modeling → Assembly → Memory
```

### Core Systems

| System | Purpose | Key Insight | Integration |
|--------|---------|-------------|-------------|
| **[Principles](agents/steering-global-principles.md)** | Anti-assumption framework | Every yama guards against a presumption | Foundation for all other systems |
| **[Skills](skills/README.md)** | Custom skill development examples | Agent Skills standard (flat structure, SKILL.md) | Workshop compilation sources |
| **[Agents](agents/README.md)** | Single-agent steering patterns | `.kiro/` modular context system (Kiro canonical) | Hierarchical context management |
| **[Prompts](prompts/README.md)** | Epistemic rendering stack | Same content through different cognitive lenses | Cognitive transformation toolkit |
| **[Artifacts](artifacts/README.md)** | Visual cognitive modeling | Canvas-to-semantic-JSON anticompiler workflow | Bridge visual design and structured data |
| **[Workshop](workshop/README.md)** | Recipe-based assembly system | Write once, deploy everywhere via slice architecture | Context compilation and deployment |
| **[Exocortex](exocortex/README.md)** | Pentadyadic multi-agent architecture | Distributed cognition through specialized AI agents | Advanced multi-agent coordination |

## The Cognitive Stack

### Layer 1: Foundational Principles

The [Covenant Principles](agents/steering-global-principles.md) provide the philosophical foundation—an anti-assumption framework that prevents the cardinal sin of presumption. Every principle guards against a specific assumption that leads to cognitive failure.

**Key Insight**: Assumptions are the root cause of AI system failures. Explicit principles create assumption-hostile design.

### Layer 2: Technical Capabilities

The [Skills Library](skills/README.md) provides custom skill development examples following the Agent Skills standard (agentskills.io). These demonstrate skill creation patterns while the vault also integrates production-ready skills from community repositories (Anthropic, Vercel, muratcankoylan).

**Key Insight**: Skills follow flat structure with SKILL.md at root. Optional Kiro Power packaging via workshop recipes.

### Layer 3: Single-Agent Steering

The [Agent System](agents/README.md) documents universal patterns for single-agent configuration across AI coding platforms (Kiro, Claude Code, Codex, Charm). Focus is on explicit context management through hierarchical steering (Global → Workspace → Project) with `.kiro/` as the canonical modular context system for Kiro users.

**Key Insight**: Single-agent steering through explicit, modular context. Multi-agent coordination moved to Exocortex. Platform-agnostic patterns with platform-specific features.

### Layer 4: Visual Cognitive Modeling

The [Artifacts System](artifacts/README.md) bridges visual design and structured data through canvas-to-semantic-JSON workflows. Using Obsidian Canvas for visual modeling and the Semantic-JSON anticompiler, complex systems can be designed visually and converted to structured formats for processing.

**Key Insight**: Visual modeling preserves spatial semantics that linear text cannot capture. The anticompiler decompresses visual intent into stable, deterministic structure.

### Layer 5: Cognitive Transformation

The [Epistemic Rendering Stack](prompts/README.md) provides different cognitive lenses for exploring the same concepts—from gentle bedtime stories to heated philosophical dialectics. Each lens reveals different aspects of truth.

**Key Insight**: No single cognitive approach captures complete truth. Multiple lenses preserve meaning through multiplicity.

### Layer 6: Assembly & Deployment

The [Workshop System](workshop/README.md) uses recipe-based compilation to assemble context from distributed sources. The slice architecture enables modular composition with target-specific formatting.

**Key Insight**: Context assembly should be explicit and reproducible. Recipes enable version control for cognitive artifacts.

### Layer 7: Advanced Coordination

The [Exocortex Architecture](exocortex/README.md) implements sophisticated multi-agent coordination through the pentadyadic pattern—five specialized agents working in coordinated evaluation and synthesis.

**Key Insight**: Distributed cognition requires explicit coordination protocols. Specialization enables capabilities beyond single-agent limits.

## Integration Patterns

### Cross-System Coherence

The systems maintain coherence through several mechanisms:

- **Slice Architecture**: Consistent `<!-- slice:type=identifier -->` markers enable modular composition
- **Workshop Recipes**: Automated assembly from distributed sources with target-specific formatting
- **Steering Hierarchy**: Global → Workspace → Project context inheritance
- **Principle Enforcement**: Covenant principles guide design decisions across all systems

### Deployment Targets

The vault supports multiple deployment scenarios:

| Target | Source Systems | Assembly Method | Use Case |
|--------|----------------|-----------------|----------|
| **Claude Code** | Skills + Agents | Workshop recipes | Technical skill deployment |
| **Kiro Powers** | Skills + Prompts | Power packaging | User-friendly capabilities |
| **Canvas Workflows** | Artifacts + Workshop | Semantic-JSON compilation | Visual system modeling and structured data export |
| **Exocortex Agents** | All systems | Slice extraction | Advanced multi-agent coordination |
| **Documentation** | All systems | Cross-linking | Knowledge management and discovery |

## Operational Philosophy

### Bespoke-First Design

Following the [Bespoke Principle](agents/steering-global-principles.md#✨-bespokedness), the vault optimizes for operator workflow over enterprise patterns. When rewrite takes an hour, optimize for beauty and razor-sharp function over long-term maintainability.

### Assumption-Hostile Architecture

Every component explicitly guards against assumptions. The [Data Fidelity Principle](agents/steering-global-principles.md#🗣️-data-fidelity) ensures UNKNOWN > INVENTED. Missing information triggers queries rather than presumptive behavior.

### Context Hygiene

The [Context Hygiene Principle](agents/steering-global-principles.md#🧬-context-hygiene) prevents context-stuffing and wholesale transmission. Context is compiled per-recipient and per-turn, maintaining clean cognitive boundaries.

### Work Preservation

The [Work Preservation Principle](agents/steering-global-principles.md#⛔-work-preservation) ensures nothing gets lost. Changes are explicit and reversible. "Out of scope" triggers questions, not automatic cleanup.

## Getting Started

### For Context Engineering
1. Start with [Covenant Patterns](skills/covenant-patterns/SKILL.md) for foundational principles
2. Study [Agent Steering](skills/agent-steering/SKILL.md) for context compilation techniques
3. Implement progressive disclosure patterns through agent context assembly

### For Agent Development
1. Review [Agent System Architecture](agents/README.md) for single-agent steering patterns
2. Understand `.kiro/` modular context system (Kiro users) or equivalent platform patterns
3. Explore hierarchical steering (Global → Workspace → Project)
4. See [Exocortex](exocortex/README.md) for multi-agent coordination (separate concern)

### For Cognitive Work
1. Explore [Epistemic Rendering](prompts/README.md) approaches
2. Use [Workshop Recipes](workshop/README.md) for context assembly
3. Consider [Exocortex Multi-Agent Coordination](exocortex/README.md) for complex tasks

### For Visual Modeling
1. Explore [Canvas-to-Semantic-JSON](artifacts/README.md) workflows
2. Use [Implementation Spec Templates](artifacts/golden/impl-spec-example.canvas) for structured development
3. Apply [Anticompiler Principles](artifacts/README.md#anticompiler-philosophy) for visual-to-data transformation

### For Advanced Coordination
1. Study [Exocortex Architecture](exocortex/README.md) for pentadyadic multi-agent patterns
2. Review [Multi-Agent Coordination Skill](skills/multi-agent-coordination/SKILL.md) for coordination frameworks
3. Implement [Triquetra Evaluation](skills/multi-agent-coordination/SKILL.md#the-triquetra-pattern) for quality assessment

## The Vault Advantage

This cognitive infrastructure solves fundamental problems in AI-augmented work:

- **No Black Boxes**: Every behavior is explicitly configured and documented
- **Assumption Resistance**: Principles prevent presumptive failures
- **Modular Composition**: Slice architecture enables flexible assembly
- **Multiple Deployment**: Write once, deploy to multiple targets
- **Cognitive Flexibility**: Multiple lenses reveal different aspects of truth
- **Workflow Integration**: Systems work together rather than in isolation

The result is AI assistance that enhances rather than replaces human cognition, maintaining transparency and control while providing sophisticated capabilities.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The cognitive infrastructure patterns, documentation approaches, and architectural frameworks are freely available for adaptation and use. Build upon them, modify them, make them your own.

**Reusable Components:**
- Workshop system (`workshop/src/`, templates, recipe patterns)
- Specifications (`skills/spec-agent-skill.md`, `skills/spec-kiro-power.md`)
- Assembly patterns and slice architecture
- Covenant Principles framework
- `.kiro/` modular context system pattern

**Personal Content:**
- ZK's specific agent configurations, custom skills, prompts, and artifacts
- These serve as examples but contain ZK-specific implementations

**Community Skills:**
- Production-ready skills available from [Anthropic](https://github.com/anthropics/skills), [Vercel](https://github.com/vercel-labs/agent-skills), and [muratcankoylan](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)
- This vault's skills/ directory demonstrates custom skill development patterns

A template repository (workshop system without personal content) may be created in the future for easier bootstrapping.

---

*The vault is not a destination but a foundation. Build upon it.* ⧉
