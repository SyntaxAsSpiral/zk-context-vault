---
name: tm20
description: >-
  Print 80 mm thermal slips and receipts on the mesh Epson TM-T20III via tm20/tm20-set.
  Use when designing or printing tape, item listings, logos, QR, ESC/POS, 1-bit art,
  or when the user mentions tm20, TM-T20III, thermal printer, or 80 mm receipts.
  Slash: /tm20
compatibility: Print host is quita (USB). Other hosts SSH in. No CUPS. Paper must be loaded.
metadata:
  author: zk
  version: "0.1.0"
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

On quita itself: same commands without `ssh quita`. Binaries: `/usr/local/bin/tm20`, `tm20-set`. Clone: `~/src/tm20`.

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

Preview with `--dry --png DIR` and **read the PNG** before USB. Empty table headers (`| \| |`) waste a band of white. A figure wider than 576 shrinks; a 111 px QR stays 111 px — render QR ~200 px, 1-bit, quiet zone included.

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

Thermal is a **stamp**, not a screen. Design at native 1-bit (mode `1` / threshold), not gray that dithers to mud.

- **Filled shapes, punched counters.** A black house with a white roundel beats an outline gable.
- **Stroke ≥ 4 px** at the size that will hit the tape. Hairlines vanish or become noise.
- **Motifs from the object.** Leiwen / Greek key, yoke, shou roundel — from the photographed piece, not clipart.
- **Exact lettering in type or code** (OpenType via tm20-set, or PIL). Do not bake “HOLLIDAY ESTATE” in an image model.
- **Lockup vs header.** Full lockup (~400 dots) is a masthead. Item slips that must stay short need a smaller mark, not the whole crest.
- **Wordmark:** tracked grotesque, two lines if needed (`HOLLIDAY` / `ESTATE`), then a meander or rule — not a hairline.
- Photos as thumbnails only if they survive dither (one object, hard contrast). Busy garage shots become static.

Rebuild a 1-bit lockup with the project’s renderer if one exists (estate: `brand/render_logo.py`). Change geometry in the renderer, don’t Photoshop the PNG.

## Checklist

1. Paper in, cover closed, `tm20 list` sees the Epson.
2. Markdown + local 1-bit assets next to it.
3. `--dry --png` — heading hierarchy, no giant white gap, QR large enough to scan.
4. `tm20-set print md`.
5. If blank tape: heat side of the roll faces the head (paper over the top).
