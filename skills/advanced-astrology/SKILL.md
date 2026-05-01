---
name: advanced-astrology
description: Use when the user asks for astrology readings, celestial timing, planetary hours, tattwa cycles, moon sign, biorhythms, or symbolic timing weather for planning, reflection, or ritual. Also when an agent needs chronographic context or natal-timing synthesis.
license: MIT
compatibility: Requires Python 3.10+ for bundled scripts. Basic mode uses the Python standard library; optional high-precision moon/ephemeris support can use kerykeion, flatlib, or pyswisseph when installed.
metadata:
  author: zk
  version: "0.2.0"
---

# Chronographic Oracle

Computes the present moment as symbolic tessellation — planetary hour, tattwa, moon sign, biorhythms — and emits it in the oracular register. Not fate, not forecast. The texture of *right now*, precisely calculated.

## Golden Rule

**Compute first. Emit second.**

The oracle speaks from the data, not around it.

## Capability Layers

Prefer the highest-fidelity available backend, degrade gracefully:

1. **Installed backend:** if `sideriod`, `astro-agent`, or another configured astrology CLI is available, use its `--json` output.
2. **Bundled script:** run `scripts/astro_pulse.py` — standard-library astronomy approximations plus optional `kerykeion` moon sign.
3. **Partial mode:** if location, timezone, or birth date is missing, compute available signals only and name the gaps.

See `references/backends.md`.

## Quick Start

```bash
python scripts/astro_pulse.py --profile assets/profile.example.json --json
python scripts/astro_pulse.py --profile assets/profile.example.json --markdown
```

Custom datetime: `--datetime 2026-04-30T08:00:00-07:00`

## Profile

Required: `current_location.lat/lon/timezone` (planetary hours + tattwa) and `birth.date` (biorhythms). Optional richer fields for backend use. See `assets/profile.example.json`.

## Oracle Arc

1. **Compute.** Run backend or `scripts/astro_pulse.py --json`. Name any missing signals — don't fill gaps.
2. **Hold the lattice.** Before writing, read all signals at once. Planetary hour + tattwa + biorhythm phase + moon sign form a single composite tile. What is the character at this intersection — not part by part, but whole?
3. **Emit.** One to three sentences, present tense, concrete image. State what the composite reveals. No hedging — the oracle speaks or stays silent.
4. **Ground the posture.** Two suggestions framed as invitation: "A useful posture: ..." not "You should..."
5. **Acknowledge the edge.** One sentence on what this reading cannot see. Invite tracking.

The register is **pyroglossia** — fire-tongue above the fissure. The Pythia didn't explain her vision; she emitted it. Synthesize the whole; don't recite the parts.

## Glyph Keys

Seeds for synthesis — the oracle combines and transforms, doesn't recite.

### Planetary Hour Rulers

| Ruler | Seed |
|-------|------|
| Saturn ♄ | *The crystallizer holds the hour. Heavy, patient, geometric.* |
| Jupiter ♃ | *The field opens. Wisdom moves outward.* |
| Mars ♂ | *The edge leads. The cut is clean.* |
| Sun ☉ | *The light is direct. Everything visible.* |
| Venus ♀ | *The field draws near. Beauty as intelligence.* |
| Mercury ☿ | *The nerve fires. Signal faster than the hand.* |
| Moon ☽ | *The tide pulls inward. Interior weather rising.* |

### Tattwas

| Tattwa | Seed |
|--------|------|
| Akasha ⊙ | *Before the first sound.* |
| Vayu 🜁 | *The idea moves.* |
| Tejas 🜂 | *The cut clarifies.* |
| Prithvi 🜃 | *The ground holds.* |
| Apas 🜄 | *The feeling flows.* |

For guardrails: `references/interpretation-boundaries.md`.

## Common Mistakes

- **Computing after speaking.** Never invent positions or moon signs. Run the script; if unavailable, say so.
- **Listing instead of emitting.** "Saturn hour = structure, Prithvi = earth" is a report. Synthesize the composite — speak the whole.
- **Hedging into silence.** "This might possibly suggest..." defeats the register. Speak or stay silent.
- **Isolating biorhythms.** Read the phase shape: aligned, diverging, at a critical crossing? The wave-terrain is the signal.

JSON contract: `references/output-schema.md`
