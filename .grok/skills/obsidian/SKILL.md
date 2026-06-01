---
name: obsidian
description: Use when working with Obsidian vaults — creating or editing .md notes,
  wikilinks, callouts, frontmatter, embeds, tags, or Obsidian-specific syntax; or
  when interacting with a vault via the obsidian CLI to read, create, search, manage
  notes/tasks/properties, or develop and debug plugins and themes.
metadata:
  author: zk
  version: '1.0'
  category: obsidian
---

# Obsidian

## Obsidian Flavored Markdown

Create and edit valid Obsidian Flavored Markdown. Covers Obsidian-specific extensions only — standard Markdown is assumed knowledge.

### Workflow: Creating a Note

1. **Add frontmatter** with properties (title, tags, aliases) at the top. See [PROPERTIES.md](references/PROPERTIES.md) for all property types.
2. **Write content** with standard Markdown plus Obsidian-specific syntax below.
3. **Link related notes** using `[[wikilinks]]` for vault notes; standard `[text](url)` for external URLs only.
4. **Embed content** with `![[embed]]` syntax. See [EMBEDS.md](references/EMBEDS.md) for all embed types.
5. **Add callouts** with `> [!type]` syntax. See [CALLOUTS.md](references/CALLOUTS.md) for all callout types.
6. **Verify** the note renders correctly in reading view.

### Internal Links (Wikilinks)

```markdown
[[Note Name]]                          Link to note
[[Note Name|Display Text]]             Custom display text
[[Note Name#Heading]]                  Link to heading
[[Note Name#^block-id]]                Link to block
[[#Heading in same note]]              Same-note heading link
```

Define a block ID by appending `^block-id` to any paragraph. For lists/quotes, place it on a separate line after the block.

### Embeds

```markdown
![[Note Name]]                         Embed full note
![[Note Name#Heading]]                 Embed section
![[image.png|300]]                     Embed image with width
![[document.pdf#page=3]]               Embed PDF page
```

### Callouts

```markdown
> [!note]
> Basic callout.

> [!warning] Custom Title
> Callout with a custom title.

> [!faq]- Collapsed by default
> Foldable callout (- collapsed, + expanded).
```

Common types: `note`, `tip`, `warning`, `info`, `example`, `quote`, `bug`, `danger`, `success`, `failure`, `question`, `abstract`, `todo`. See [CALLOUTS.md](references/CALLOUTS.md) for full list.

### Properties (Frontmatter)

```yaml
---
title: My Note
date: 2024-01-15
tags:
  - project
  - active
aliases:
  - Alternative Name
cssclasses:
  - custom-class
---
```

See [PROPERTIES.md](references/PROPERTIES.md) for all property types and tag syntax rules.

### Tags

```markdown
#tag                    Inline tag
#nested/tag             Nested tag with hierarchy
```

Tags can also be defined in frontmatter under the `tags` property.

### Other Obsidian-Specific Syntax

```markdown
%%hidden comment%%                     Comment (hidden in reading view)
==Highlighted text==                   Highlight
$e^{i\pi} + 1 = 0$                    Inline math (LaTeX)
```

Mermaid diagrams: use ` ```mermaid ` blocks. To link nodes to vault notes, add `class NodeName internal-link;`.

---

## Obsidian CLI

Use the `obsidian` CLI to interact with a running Obsidian instance. **Requires Obsidian to be open.**

Run `obsidian help` for all available commands. Full docs: https://help.obsidian.md/cli

### Syntax

**Parameters** take a value with `=`. Quote values with spaces:

```bash
obsidian create name="My Note" content="Hello world"
```

**Flags** are boolean switches with no value:

```bash
obsidian create name="My Note" silent overwrite
```

For multiline content use `\n` for newlines, `\t` for tabs.

### File & Vault Targeting

- `file=<name>` — resolves like a wikilink (name only, no path or extension)
- `path=<path>` — exact path from vault root, e.g. `folder/note.md`
- Without either, the active file is used.
- Prefix any command with `vault=<name>` to target a specific vault:

```bash
obsidian vault="My Vault" search query="test"
```

### Common Patterns

```bash
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" template="Template" silent
obsidian append file="My Note" content="New line"
obsidian search query="search term" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
obsidian tasks daily todo
obsidian tags sort=count counts
obsidian backlinks file="My Note"
```

Use `--copy` on any command to copy output to clipboard. Use `silent` to suppress file opening. Use `total` on list commands for a count.

### Plugin Development Cycle

After code changes to a plugin or theme:

1. **Reload** the plugin:
   ```bash
   obsidian plugin:reload id=my-plugin
   ```
2. **Check for errors** — fix and repeat if any:
   ```bash
   obsidian dev:errors
   ```
3. **Verify visually:**
   ```bash
   obsidian dev:screenshot path=screenshot.png
   obsidian dev:dom selector=".workspace-leaf" text
   ```
4. **Check console:**
   ```bash
   obsidian dev:console level=error
   ```

Additional developer commands:

```bash
obsidian eval code="app.vault.getFiles().length"     # Run JS in app context
obsidian dev:css selector=".workspace-leaf" prop=background-color
obsidian dev:mobile on                               # Toggle mobile emulation
```
