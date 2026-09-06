---
name: tm20
description: 'Print 80 mm thermal slips and receipts on the mesh Epson TM-T20III via
  tm20/tm20-set. Use when designing or printing tape, item listings, logos, QR, ESC/POS,
  1-bit art, or when the user mentions tm20, TM-T20III, thermal printer, or 80 mm
  receipts. Slash: /tm20'
compatibility: Print host is quita (USB). Other hosts SSH in. No CUPS. Paper must
  be loaded.
metadata:
  author: zk
  version: 0.3.0
  category: print
---

# tm20 — 80 mm tape

Host, USB id, udev, binaries, paper size: mesh **Services → tm20 thermal**. This skill is how to *compose and print*. Do not install tm20 on every box. Do not CUPS. Do not router-USB.

## Print

Always on **quita**. Live group `plugdev` is required (new login after `usermod`). This session may still need `-g plugdev`.

```bash
# preview (no USB) — inspect the 2× PNG before burning paper
ssh quita 'tm20-set --dry --png /tmp/tm20-preview print md /path/to/slip.md'

# print
ssh quita 'sudo -u zk -g plugdev tm20-set print md /path/to/slip.md'

# smoke
ssh quita 'sudo -u zk -g plugdev tm20 list'     # must show * 04b8:0e28
ssh quita 'sudo -u zk -g plugdev tm20 hello'    # SYSTEM ONLINE + cut
```

On quita itself: same commands without `ssh quita`. Binaries: `/usr/local/bin/tm20`, `tm20-set`. Clone: `~/src/tm20`. If `id` already shows `plugdev`, `tm20-set print md` is enough.

`tm20` = protocol (hello, list, text, qr, status). `tm20-set` = typeset markdown/sheets → `GS ( L)` raster. Jobs that need type, figures, or QR-as-image go through `tm20-set print md`.

Do not print if the cover is open or the roll is out — the head will cook the platen.

## Markdown contract

Tape is **576 dots** wide (~203 dpi). `tm20-set` Floyd–Steinbergs images to 1-bit, **never scales up**.

| Markdown | Tape |
|---|---|
| `#` | Display mark, 18 pt |
| `##`+ | Body head, 11 pt |
| paragraph | 11 pt Helvetica-family |
| `![alt](file.png)` | Figure, **own paragraph** (no mixed text+image) |
| pipe table | 2–3 columns only; **first row is the header** |
| `[text](url)` | Italic + footnote, not a QR |
| `$` | Currency, not math |

Image dests are local paths or `file:` relative to the `.md`. HTTP dests fail.

Preview with `--dry --png DIR` and **read the PNG** before USB. Empty table headers (`| \| |`) waste a band of white. Empty *body* cells in a tick column collapse — put `[ ]` in the cell. A figure wider than 576 shrinks; a 111 px QR stays 111 px — render QR ~200 px, 1-bit, quiet zone included.

Linux `tm20-set` faces are Liberation Sans/Mono. Serif, tracked display, or a feast title belongs **in the raster** (PIL), not in markdown `#`.

```markdown
![mark](logo-thermal.png)

# HLD-0028

## Rosewood coffee table

One or two sentences. Facts, not atmosphere.

| qty | 1 |
| :--- | ---: |
| condition | good |
| stored | garage |

![catalog](qr-catalog.png)
```

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

Rebuild a lockup with the project’s renderer if one exists (estate: `brand/render_logo.py`; feast: `family-cookbook/slips/sample/compose_feast.py`). Change geometry in the renderer.

Motif library: `references/motifs.md`.

## Checklist

1. Paper in, cover closed, `tm20 list` sees the Epson.
2. Markdown + local assets next to it. Gray plates stay gray; type stays black.
3. `--dry --png` — heading hierarchy, no giant white gap, QR large enough to scan, gilding still reads as curves.
4. `tm20-set print md`.
5. If blank tape: heat side of the roll faces the head (paper over the top).
