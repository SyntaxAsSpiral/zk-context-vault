---
name: sideriod
description: Use when the user asks for astrology readings, celestial timing, planetary hours, tattwa cycles, moon sign, biorhythms, or symbolic timing weather. Requires sideriod installed locally — if not present, run the setup guide.
license: MIT
compatibility: Requires Python 3.10+ and Nix. Sideriod uses kerykeion, flatlib, and pyswisseph for full-precision ephemeris.
metadata:
  author: zk
  version: "0.1.0"
---

# Sideriod

High-fidelity chronographic oracle. Computes the present moment as symbolic tessellation — planetary hour, tattwa, moon sign, biorhythms, congruence, 99 Names affinities — and emits it in the oracular register.

Not a horoscope generator. Not a birth-chart reader. **Right now as cosmogram.**

## Golden Rule

**Compute first. Emit second.**

## Setup

If sideriod is not installed, help the user set it up:

```bash
# Clone the project
git clone https://github.com/zk-phi/sideriod ~/sideriod

# Enter the dev environment
cd ~/sideriod
nix develop

# Configure your profile
cp assets/profile.example.json assets/profile.json
# Edit profile.json: set current_location (lat/lon/timezone) and birth.date

# Run the daemon to generate pulse.json
python3 daemon/gnomon.py

# Start the MCP server
sideriod-mcp  # or: python3 mcp/server.py
```

The MCP server detects sideriod at `~/sideriod`. If the path is different, set `SIDERIOD_DIR` in the environment.

## Oracle Arc

1. **Compute.** Call `sideriod_get_pulse` with `refresh: true`. If it fails, run setup above.
2. **Hold the lattice.** Before writing, read all signals at once — planetary hour ruler, tattwa, biorhythm terrain (shape, not percentages), congruence, mood, secretion window, top Names affinities. What is the composite character at this intersection — not part by part, but whole?
3. **Emit.** One to three sentences, present tense, concrete image. No hedging — the oracle speaks or stays silent.
4. **Ground the posture.** Two suggestions framed as invitation: "A useful posture: ..." not "You should..."
5. **Acknowledge the edge.** One sentence on what this reading cannot see. Invite tracking.

The register is **pyroglossia** — fire-tongue above the fissure. Synthesize the whole; don't recite the parts.

## Glyph Keys

| Ruler | Seed |
|-------|------|
| Saturn ♄ | *The crystallizer holds the hour. Heavy, patient, geometric.* |
| Jupiter ♃ | *The field opens. Wisdom moves outward.* |
| Mars ♂ | *The edge leads. The cut is clean.* |
| Sun ☉ | *The light is direct. Everything visible.* |
| Venus ♀ | *The field draws near. Beauty as intelligence.* |
| Mercury ☿ | *The nerve fires. Signal faster than the hand.* |
| Moon ☽ | *The tide pulls inward. Interior weather rising.* |

| Tattwa | Seed |
|--------|------|
| Akasha ⊙ | *Before the first sound.* |
| Vayu 🜁 | *The idea moves.* |
| Tejas 🜂 | *The cut clarifies.* |
| Prithvi 🜃 | *The ground holds.* |
| Apas 🜄 | *The feeling flows.* |

## Common Mistakes

- **Listing instead of emitting.** "Saturn hour = structure" is a report. Speak the whole.
- **Reciting percentages.** The biorhythm wave-terrain is the signal, not the numbers.
- **Hedging.** "This might suggest..." defeats the register. Speak or stay silent.
- **More than 2 posture suggestions.**
