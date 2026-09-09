---
name: tm20
description: 'Print 80 mm thermal slips and receipts on the mesh Epson TM-T20III via
  tm20/tm20-set or the quita print receiver. Use when designing or printing tape,
  item listings, logos, QR, ESC/POS, 1-bit art, or when the user mentions tm20, TM-T20III,
  thermal printer, 80 mm receipts, or the mesh print receiver. Slash: /tm20'
compatibility: USB and tm20 binaries are quita only. Scripted jobs from other hosts
  POST the print receiver. No CUPS. Paper must be loaded.
metadata:
  author: zk
  version: 0.4.0
  category: print
---

# tm20 — 80 mm tape

Host, USB id, udev, binaries, paper size, receiver URL: mesh **Services → tm20 thermal** and **Mesh print receiver**. This skill is how to *compose* and *which door to knock*. Do not install tm20 on every box. Do not CUPS. Do not router-USB.

## The cottage and the sealed pattern

There is only one loom, in a cottage at the edge of the wood (quita). The loom will burn if two weavers grab the shuttle at once, and it will reprint the same numbered cloth if a forgetful messenger knocks twice.

**Sitting at the loom** is `tm20` / `tm20-set` on quita. You see the cloth as it forms. You can stop, trim a stitch, ask if the loom is awake (`hello`, `status`, `list`), or throw away a spoiled preview (`--dry --png`) before any wool is spent. Use this when you are *in the cottage*, designing, debugging, or laying a hand on the machine.

**Sending a sealed pattern** is POST `http://quita:8766/print`. You do not touch the shuttle. A keeper (the receiver) takes one pattern at a time, will not weave the same job id twice, and cuts the cloth only after the pattern is already finished. Use this when you are *in another house* (adeck, a phone, a long-running service) or when two projects might arrive at once — Holliday Table, holliday-estate, sideriod.

If you are standing in the cottage and only trying a stitch, sit at the loom. If you are sending work from afar, or a script must print without you watching, seal the pattern.

Do not do both for the same job.

## Direct USB (on quita)

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

From another host, SSH those same commands only for design/debug/smoke — not for app-driven copies. Binaries: `/usr/local/bin/tm20`, `tm20-set`. Clone: `~/src/tm20`. If `id` already shows `plugdev`, `tm20-set print md` is enough.

`tm20` = protocol (hello, list, text, qr, status). `tm20-set` = typeset markdown/sheets → `GS ( L)` raster. Jobs that need type, figures, or QR-as-image go through `tm20-set print md`.

Do not print if the cover is open or the roll is out — the head will cook the platen.

## Receiver (scripted, any mesh host)

Token: `PRINT_TOKEN` (alias `HOLIDAY_PRINT_TOKEN`). Unique `job_id` (alias `slip_id`). Send a 576px PNG *or* markdown, not both. Optional `source`: `holliday-table`, `holliday-estate`, `sideriod`.

```bash
# health
curl -fsS -H "Authorization: Bearer $PRINT_TOKEN" http://quita:8766/health

# PNG job (already-inspected raster, e.g. Le Festin)
# POST /print  {"job_id","source","sha256","image": "<base64 png>"}

# markdown job (tm20-set print md on quita)
# POST /print  {"job_id","source","sha256","markdown": "# HLD-0028\n\n..."}
```

Inspect a preview before the POST. Duplicate job ids return the prior status and do not print again. Uncertain means check the tape before minting a new id.

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

Image dests are local paths or `file:` relative to the `.md`. HTTP dests fail. A markdown POST to the receiver cannot see files on the caller — embed what the typesetter needs, or send a PNG.

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

Rebuild a lockup with the project’s renderer if one exists (estate: `brand/render_logo.py`; feast: `family-cookbook/slips/template/render.py`). Change geometry in the renderer.

Motif library: `references/motifs.md`.

## Checklist

1. Paper in, cover closed, `tm20 list` sees the Epson (direct) or `/health` is ok (receiver).
2. Markdown + local assets next to it, or an inspected 576px PNG. Gray plates stay gray; type stays black.
3. `--dry --png` — heading hierarchy, no giant white gap, QR large enough to scan, gilding still reads as curves.
4. On quita, designing: `tm20-set print md`. From a service or another host: POST the receiver with a new `job_id`.
5. If blank tape: heat side of the roll faces the head (paper over the top).
