# The .kiro/ Modular Context System

**Purpose**: Project-specific context management through modular, composable documentation that Kiro loads automatically.

## What .kiro/ Is

The `.kiro/` directory is Kiro's **project-level context system**—a structured way to provide project-specific guidance, specifications, hooks, and steering rules that augment Kiro's global configuration.

Think of it as "project DNA" that Kiro reads to understand your specific codebase, workflows, and constraints.

## Directory Structure

```
.kiro/
├── steering/          # Modular context documents (auto-loaded)
│   ├── product.md     # What this project is and why it exists
│   ├── structure.md   # Directory organization and file conventions
│   ├── tech.md        # Technology stack and tooling
│   └── custom-*.md    # Additional project-specific context
├── hooks/             # Automated workflow triggers (.kiro.hook JSON)
└── specs/             # 3-phase structured development
    └── {feature}/
        ├── requirements.md
        ├── design.md
        └── tasks.md
```

## The Three Components

### 1. Steering Files (`.kiro/steering/*.md`)

**Purpose**: Modular context documents that Kiro loads automatically as workspace-level steering rules.

**Kiro default modules:**
- **product.md** - Project overview, core purpose, philosophy
- **structure.md** - Directory organization, file naming, cross-references
- **tech.md** - Technology stack, tooling, development workflows

**Custom modules:**
- Add any `.md` file to `.kiro/steering/` for additional context
- Examples: `api-patterns.md`, `security.md`, `deployment.md`, `testing.md`
- Name files descriptively—filename appears in Kiro UI

**Automatic inclusions:**
- **AGENTS.md** at workspace root is automatically pulled into project steering
- Appears in Kiro UI under "Workspace" steering section
- Provides project-specific agent guidance without needing to be in `.kiro/steering/`

**How to create:**
- Navigate to the appropriate UI screen (Hooks, Specs, or Steering)
- Describe what you want in the structured prompt
- Kiro generates an agent chat that creates the files
- Make any follow-up edits through the agent chat
- Files appear in `.kiro/` and can be edited directly afterward

**How it works:**
- Kiro automatically loads all `.md` files in `.kiro/steering/`
- Kiro also loads `AGENTS.md` from workspace root (if present)
- Each file becomes a workspace-level steering rule
- Content appears in Kiro's context as "Included Rules"
- Modular design = add/remove context by adding/removing files

**When to use:**
- Project has specific conventions or constraints
- Team needs shared understanding of architecture
- Onboarding new developers (human or AI)
- Documenting technology decisions and patterns

**Example use cases:**
- API design patterns specific to this project
- Database schema conventions
- Testing strategies and requirements
- Deployment procedures
- Code review guidelines

### 2. Hooks (`.kiro/hooks/*.kiro.hook`)

**Purpose**: Automated workflow triggers that execute based on IDE events.

**Hook types:**
- `fileEdited` - Trigger when files are saved
- `fileCreated` - Trigger when files are created
- `fileDeleted` - Trigger when files are deleted
- `userTriggered` - Manual trigger via UI button
- `promptSubmit` - Trigger when message sent to agent
- `agentStop` - Trigger when agent execution completes

**Hook actions:**
- `askAgent` - Send prompt to Kiro (for file events, user triggers)
- `runCommand` - Execute shell command (for prompt/agent events only)

**How to create:**
- Navigate to the Hooks screen in Kiro UI
- Describe what you want the hook to do
- Kiro generates an agent chat that creates the `.kiro.hook` file
- Make any follow-up edits through the agent chat
- Optionally create markdown prompts in `prompts/hook-prompts/` first

**File format:**
```json
{
  "name": "Hook Name",
  "description": "What this hook does",
  "version": "1",
  "when": {
    "type": "fileEdited",
    "patterns": ["*.ts", "*.tsx"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Review changes and suggest improvements"
  }
}
```

**Canonical source pattern:**
This vault (zk-context-vault) serves as the **canonical source** for reusable hooks. Workshop recipes can deploy hooks from here to project-specific `.kiro/hooks/` directories.

**Hook development workflow:**
1. Create markdown prompt in `prompts/hook-prompts/`
2. Use Kiro UI to create `.kiro.hook` JSON config
3. Test in this vault's `.kiro/hooks/`
4. Deploy to other projects via workshop recipes

### 3. Specs (`.kiro/specs/{feature}/`)

**Purpose**: 3-phase structured development process for features.

**Phase structure:**
1. **requirements.md** - User stories, acceptance criteria, glossary
2. **design.md** - Architecture, approach, data models, correctness properties
3. **tasks.md** - Implementation breakdown with checkboxes

**How to create:**
- Navigate to the Specs screen in Kiro UI
- Describe the feature you want to spec
- Kiro generates an agent chat that creates all 3 phase files
- Make any follow-up edits through the agent chat
- Follow the 3-phase workflow: Design → Requirements → Tasks → Implementation

**Workflow:**
```
Design → Requirements → Tasks → Implementation
   ↓          ↓           ↓            ↓
 "How?"    "What?"    "Steps?"    "Execute"
```

**When to use:**
- Building new features
- Refactoring complex systems
- Need structured approach to prevent scope creep
- Want clear acceptance criteria before coding

**Canonical source pattern:**
This vault contains **spec templates** that can be deployed to other projects. The archived `context-management` spec serves as a reference implementation.

## How Kiro Uses .kiro/

### Automatic Loading

When you open a workspace in Kiro:
1. **Global steering** loads first (`~/.kiro/steering/`)
2. **Workspace steering** loads next (`.kiro/steering/`)
3. **Hooks** register automatically (`.kiro/hooks/`)
4. **Specs** available for structured development (`.kiro/specs/`)

**Hierarchy**: Global → Workspace → Project (later overrides earlier)

### Context Compilation

Kiro compiles context per-turn:
- Global principles (operator profile, covenant principles)
- Workspace steering (product, structure, tech)
- Project steering (custom context)
- Active spec (if working on a feature)
- Relevant hooks (if triggered)

This creates **progressive disclosure**—Kiro gets exactly the context needed for the current task without overwhelming token limits.

### Modular Composition

The `.kiro/steering/` pattern enables:
- **Add context** by creating new `.md` files
- **Remove context** by deleting files
- **Update context** by editing files
- **Share context** across projects via workshop recipes

No monolithic configuration files. No context stuffing. Just modular, composable documentation.

## Deployment Pattern

This vault (zk-context-vault) serves as the **canonical source** for reusable `.kiro/` content:

**Canonical sources:**
- `.kiro/hooks/*.kiro.hook` - Reusable hook configurations
- `.kiro/specs/*/` - Spec templates and reference implementations
- `.kiro/steering/*.md` - Example steering modules

**Workshop deployment:**
Workshop recipes can deploy from this vault's `.kiro/` to project-specific `.kiro/` directories:

```yaml
# Example: Deploy hooks to project
name: deploy-hooks-to-project
target_locations:
  - path: ~/projects/my-app/.kiro/hooks/
sources:
  - file: .kiro/hooks/doc-consistency-check.kiro.hook
  - file: .kiro/hooks/murder.kiro.hook
```

This enables:
- **Write once, deploy everywhere** for hooks and specs
- **Version control** for project context
- **Consistent patterns** across multiple projects
- **Easy updates** via workshop sync

## Best Practices

### Steering Files

**Do:**
- Keep each file focused on one aspect (product, structure, tech)
- Use clear headings and consistent formatting
- Include concrete examples and patterns
- Update when project evolves

**Don't:**
- Create monolithic steering files
- Include sensitive information (credentials, keys)
- Duplicate content across files
- Let steering drift from reality

### Hooks

**Do:**
- Test hooks thoroughly before deploying
- Use descriptive names and clear prompts
- Document hook purpose in description field
- Start with `userTriggered` for safety

**Don't:**
- Create hooks that run on every file save (performance)
- Use `runCommand` with destructive operations
- Forget to specify file patterns for file events
- Create hooks without clear purpose

### Specs

**Do:**
- Complete requirements before design
- Complete design before tasks
- Update tasks as you implement
- Mark tasks complete as you go

**Don't:**
- Skip phases (leads to scope creep)
- Write code before requirements clear
- Leave tasks unmarked (loses progress tracking)
- Create specs for trivial changes

## Integration with Workshop

The `.kiro/` system integrates with the workshop for deployment:

**Recipe types that target .kiro/:**
- `recipe-command-*.md` - Deploys hooks to `.kiro/hooks/`
- Custom recipes - Deploy steering files to `.kiro/steering/`
- Spec recipes - Deploy spec templates to `.kiro/specs/`

**Example workflow:**
1. Develop hook in this vault's `.kiro/hooks/`
2. Create workshop recipe to deploy to projects
3. Run `python workshop/src/assemble.py`
4. Run `python workshop/src/sync.py`
5. Hook now available in target project

## Why This Matters

The `.kiro/` modular context system solves fundamental problems:

**No black boxes**: Every behavior explicitly configured and documented
**Assumption resistance**: Project-specific context prevents presumptive failures
**Modular composition**: Add/remove context without editing monolithic files
**Progressive disclosure**: Kiro gets exactly the context needed per-turn
**Workflow integration**: Hooks, specs, and steering work together seamlessly

The result is AI assistance that enhances rather than replaces human cognition, maintaining transparency and control while providing sophisticated project-specific capabilities.

---

*Modular context. Explicit behavior. Assumption-hostile design.* 🧭
