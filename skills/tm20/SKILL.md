---
name: tm20
description: >-
  Print 80 mm thermal slips and receipts on the mesh Epson TM-T20III via tm20/tm20-set
  or the tm20 print receiver. Use when designing or printing tape, item listings,
  logos, QR, ESC/POS, 1-bit art, or when the user mentions tm20, TM-T20III, thermal
  printer, 80 mm receipts, or the mesh print receiver. Slash: /tm20
metadata:
  author: zk
  version: "0.5.0"
  category: print
  compatibility: USB and tm20 binaries are the tm20 Pi only; other hosts POST the receiver. No CUPS. Paper must be loaded.
---

# tm20 — 80 mm tape

Host, USB id, udev, binaries, paper size, receiver URL: mesh **Services → tm20 thermal** and **Mesh print receiver**. This skill is how to *compose* and *which door to knock*. Do not install tm20 on every box. Do not CUPS. Do not router-USB.

## The cottage and the sealed pattern

There is only one loom, in a cottage at the edge of the wood (`tm20`, the Pi). The loom will burn if two weavers grab the shuttle at once, and it will reprint the same numbered cloth if a forgetful messenger knocks twice.

**Sitting at the loom** is `tm20` / `tm20-set` on the `tm20` host. You see the cloth as it forms. You can stop, trim a stitch, ask if the loom is awake (`hello`, `status`, `list`), or throw away a spoiled preview (`--dry --png`) before any wool is spent. Use this when you are *in the cottage*, designing, debugging, or laying a hand on the machine.

**Sending a sealed pattern** is POST `http://tm20:8766/print`. You do not touch the shuttle. A keeper (the receiver) takes one pattern at a time, will not weave the same job id twice, and cuts the cloth only after the pattern is already finished. Use this when you are *in another house* (adeck, a phone, a long-running service) or when two projects might arrive at once — Holliday Table, holliday-estate, sideriod.

If you are standing in the cottage and only trying a stitch, sit at the loom. If you are sending work from afar, or a script must print without you watching, seal the pattern.

Do not do both for the same job.

## Direct USB (on `tm20`)

Live group `plugdev` is required (new login after `usermod`). This session may still need `-g plugdev`.

```bash
# preview (no USB) — inspect the 2× PNG before burning paper
tm20-set --dry --png /tmp/tm20-preview print md /path/to/slip.md

# print
sudo -u zk -g plugdev tm20-set print md /path/to/slip.md

# smoke
sudo -u zk -g plugdev tm20 list     # must show * 04b8:0e28
sudo -u zk -g plugdev tm20 hello    # SYSTEM ONLINE + cut
sudo -u zk -g plugdev tm20 status   # cover closed, paper present
```

From another host, SSH those same commands only for design/debug/smoke — not for app-driven copies. USB execution is the `tm20` Pi only. `tm20` / `tm20-set` and the receiver are a later layer on that appliance (udev is already in the sdImage). If `id` already shows `plugdev`, `tm20-set print md` is enough.

`tm20` = protocol (hello, list, text, qr, status). `tm20-set` = typeset markdown/sheets → `GS ( L)` raster. Jobs that need type, figures, or QR-as-image go through `tm20-set print md`.

Do not print if the cover is open or the roll is out — the head will cook the platen.

## Receiver (scripted, any mesh host)

Token: `PRINT_TOKEN` (alias `HOLIDAY_PRINT_TOKEN`). Unique `job_id` (alias `slip_id`). Send a 576px PNG *or* markdown, not both. Optional `source`: `holliday-table`, `holliday-estate`, `sideriod`.

```bash
# health
curl -fsS -H "Authorization: Bearer $PRINT_TOKEN" http://tm20:8766/health

# PNG job (already-inspected raster, e.g. Le Festin)
# POST /print  {"job_id","source","sha256","image": "<base64 png>"}

# markdown job (tm20-set print md on tm20)
# POST /print  {"job_id","source","sha256","markdown": "# HLD-0028\n\n..."}
```

Inspect a preview before the POST. Duplicate job ids return the prior status and do not print again. Uncertain means check the tape before minting a new id.

## Design Markdown for thermal tape

Craft a `.md` document for a 576-dot-wide (~203 dpi), monochrome thermal tape. Length can grow; width cannot. tm20 is a strict printable subset of CommonMark/GFM, not a browser: unsupported constructs, missing glyphs, and clipped content fail.

### Design language

- Prefer one short `#` masthead, then a clear reading order: context, substance, conclusion. Use `##` for sections; H3–H6 do not create smaller visual levels.
- Be economical, not cryptic. Use short paragraphs and concrete labels. Keep necessary detail; move supporting sources into notes rather than deleting it.
- Let typography do the work: bold for key facts, italic for secondary emphasis, monospace for literal identifiers. Avoid walls of bold, all-caps paragraphs, decorative emoji, ASCII boxes, and space-padded pseudo-columns.
- Use two-column tables for label/value pairs and prices. Reserve three columns for genuinely compact data. Prefer stacked labeled paragraphs for wide records.
- Use a rule before a total or major transition, not between every paragraph. One blank line separates blocks; extra blank lines are not layout controls.
- Receipts: masthead → context → items → total. Reading tapes: short sections and prose. Checklists: one concrete action per task. Adapt the structure to the content; do not force every document into a receipt.

### Supported Markdown

| Construct | Rendering | Authoring constraints |
| --- | --- | --- |
| Paragraphs | 11 pt sans; word wrapping, no hyphenation | Avoid long unbroken strings. Source soft breaks become spaces; use a trailing backslash or two spaces for a hard break. |
| Headings | H1: 18 pt; H2–H6: 11 pt bold | Nonempty plain text only: no emphasis, code, links, images, or math. Prefer ATX `#` syntax. |
| Inline styles | `*italic*`, `**bold**`, combinations, `~~strike~~` | Styles can nest; strikethrough spans wrapped lines. Keep them out of headings. |
| Code spans | Monospace; whitespace normalized | For short literals, not manual alignment. Fitting spans stay unbroken. |
| Code blocks | Fenced or indented monospace | No highlighting or wrapping. Split long lines explicitly; indentation consumes width. |
| Lists | Dash bullets; ordered starts and `.` / `)` delimiters preserved | At most three list levels. Blank lines distinguish loose from tight lists. |
| Tasks | `- [ ]` and `- [x]` boxes | Use list-item syntax, not free-standing bracket decorations. |
| Quotes | Indented blocks | At most three quote levels, counted separately from list levels. Nesting reduces usable width. |
| Rules | Full-tape two-dot line | Put blank lines around `---`; immediately beneath text it can become a Setext heading. |
| Tables | Two or three columns; bold header; left/right alignment | Use `---` or `---:`; never centered `:---:`. Every row needs exactly the header's cell count. Cells contain inline content, not nested blocks. |
| Links | Italic labels; numbered destination endnotes when needed | Inline, reference, angle, and recognized bare links work. Define references; use consistent titles for repeated destinations. Long URLs can overflow even in notes. A link is not a QR. |
| Footnotes | First-use numbering shared with link notes; multiblock definitions | Define every `[^name]`. Unused definitions disappear. Indent continuation blocks. |
| Images | Standalone PNG/JPEG, shrunk to fit and dithered; never upscaled | Image alone in its paragraph, not inside a link or table. Alt text is not printed: put meaningful captions in a separate paragraph. |
| Math | LaTeX via RaTeX: `\(inline\)` and `\[display\]` | Dollars are currency, not delimiters. No heading math; display math belongs in a separate paragraph, outside styles, links, and tables. Unsupported formulas/glyphs fail. |
| Text conventions | Escapes/entities decoded; smart quotes, dashes, ellipses in prose | Use code for literal punctuation. Glyph coverage is finite; do not assume emoji or arbitrary scripts are available. |

Linux `tm20-set` faces are Liberation Sans/Mono. Serif, tracked display, or a feast title belongs **in the raster** (PIL), not in markdown `#`.

`tm20-set` Floyd–Steinbergs images to 1-bit. A figure wider than 576 dots shrinks; it never scales up. A 111 px QR stays 111 px, so render QR around 200 px, 1-bit, with its quiet zone included.

Use local image paths or `file:` paths relative to the `.md`. Remote image URLs require external access and are unsuitable for deterministic jobs. A markdown POST to the receiver cannot see files on the caller; send self-contained markdown whose assets exist on `tm20`, or render and send a PNG.

### Footguns to avoid

- No raw HTML, including comments or `<br>`. No CSS, YAML front matter, definition-list extension, image-size attributes, or browser layout tricks.
- Escape literal table pipes as `\|`, even inside code spans. Backticks alone do not protect a pipe from splitting a cell.
- Escape literal square brackets (`\[` and `\]`) when they are not links, footnotes, or tasks; apparent references without definitions reject.
- Keep amount columns right-aligned with consistent decimal precision. Their digits are tabular, but there is no spreadsheet-style number formatting.
- Narrow a table by shortening labels or moving detail into prose, not by dropping data. Missing glyphs or overflow are not invitations to invent substitutes or silently omit content.
- Empty table headers waste a band of white. Empty body cells in a tick column collapse; use a task list, or put `[ ]` in the cell when a table is required.

### Receipt idiom

A header-only table after a rule gives the total the same alignment as the items, with automatic header emphasis. Keep the separator row even without body rows:

```markdown
# Corner shop

Order 42\
5 September 2026

| Item | Amount |
| --- | ---: |
| Coffee | 6.00 |
| Bread | 4.50 |

---

| Total | 10.50 |
| --- | ---: |

Thank you.
```

Preview with `--dry --png DIR` and **read the PNG** before USB or receiver submission.

## Tape design

Thermal is a **stamp**, not a screen.

**Two inks:**

| Job | How |
|---|---|
| Mark, lockup, QR, type | Solid black (`fill=0` / mode `1`). Stamps want filled shapes and punched counters. |
| Engraving, hatch, gilding, still-life | Keep **gray `L`**. `tm20-set` Floyd–Steinbergs. That is how Bjorn’s plates hold shade. |

Do not threshold a hatch plate “to be safe.” Do not bake lettering in an image model — OpenType via tm20-set or PIL.

- **Stroke ≥ 4 px** at the size that will hit the tape, for solid marks. Hatch can go finer because dither carries it.
- **Motifs from the object** (estate leiwen from the furniture) or from the meal (vegetables on a feast card).
- **Lockup vs header.** Full lockup (~400 dots) is a masthead. Short item slips need a smaller mark.
- **Gilding / cartouche height.** A Celtic knot or vine band needs **~160–180 dots** of height or Floyd–Steinberg collapses it to a rule. Lighten *after* it has height; crushing then bleaching is how a border becomes a line.
- **One frame for a menu.** A week bill of fare is one cartouche (double line + corner knots + head/foot vine), not lace on every day.
- Photos as thumbnails only if they survive dither. Busy garage shots become static.

Rebuild a lockup with the project’s renderer if one exists (estate: `brand/render_logo.py`; feast: `family-cookbook/slips/template/render.py`). Change geometry in the renderer.

Motif library: `references/motifs.md`.

## Checklist

1. Paper in, cover closed, `tm20 list` sees the Epson (direct) or `/health` is ok (receiver).
2. Markdown + local assets next to it, or an inspected 576px PNG. Gray plates stay gray; type stays black.
3. `--dry --png` — heading hierarchy, no giant white gap, QR large enough to scan, gilding still reads as curves.
4. On `tm20`, designing: `tm20-set print md`. From a service or another host: POST the receiver with a new `job_id`.
5. If blank tape: heat side of the roll faces the head (paper over the top).
