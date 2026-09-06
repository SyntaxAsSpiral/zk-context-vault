---
name: tm20-motifs
---

# Motif library

Do not vendor 2 MB color PNGs into this skill. Fetch from the source repo, reduce to 1-bit next to the slip, print.

## Sources

| Source | What it is | License |
|---|---|---|
| [SyntaxAsSpiral/esotericons](https://github.com/SyntaxAsSpiral/esotericons) | Operator’s icon set — geometric seals with an eye. PNG + ICO + fake-SVG (raster wrapped). | CC BY 4.0 · Zach Battin |
| Estate lockup | `holliday-estate/brand/render_logo.py` — house, shou roundel, leiwen | project |
| Object | Leiwen, yoke, hoof, roundel photographed on the piece | the thing itself |

Bjorn’s tape ([thread](https://x.com/bjornpagen/status/2091212203839926334)) is a **layout** study, not an image dump: title + centered emblem + field note + 2-col kv + `DO NOT REPLY` closer. Engraving/hatch survives dither. Do not copy his figures into the library.

## Esotericons on tape

Masters are **RGBA**. Transparent pixels are paper. `Image.convert("L")` drops alpha and paints the hidden RGB (usually black) — that was the boxed background on the first test strip. Always flatten onto white first. Soft glow in the alpha becomes dither grain; that is fine.

Geometry still helps (`triquetra`, `yantra`, `l-pentagram`, `hermetic`, `numogram`, `celtic*`). Painterly ones (`cottagecore`, `lotus`, `alch*`) just dither heavier — preview, don’t ban.

Fetch one:

```bash
curl -fsSL -o triquetra.png \
  https://raw.githubusercontent.com/SyntaxAsSpiral/esotericons/main/triquetra.png
```

Prep (~480 px). Keep gray for Floyd–Steinberg:

```python
from PIL import Image, ImageEnhance
im = Image.open("triquetra.png").convert("RGBA")
bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
im = Image.alpha_composite(bg, im).convert("L")
im = ImageEnhance.Contrast(im).enhance(1.4)
im.resize((480, 480)).save("triquetra-tape.png")
```

Put `triquetra-tape.png` in the markdown figure. `tm20-set` dithers it.

Attribution on public slips: “Esotericon by Zach Battin, CC BY 4.0.”

## Adding a fav

1. Prefer a mark you already own (esotericon, estate renderer, object motif).
2. Check it at 1-bit ~200–480 px. If it dies, it is not a tape motif yet.
3. Note the stem name and one-line “when to use” here. Do not commit the color master into `skills/tm20/`.
4. Slip markdown: `![triquetra](triquetra-1bit.png)` as its own paragraph.

## Slip skeleton (Bjorn layout, our marks)

```markdown
![mark](triquetra-1bit.png)

# Title

Two or three short lines.

| field | value |
| :--- | ---: |
| a | b |

DO NOT REPLY. One closer.
```
