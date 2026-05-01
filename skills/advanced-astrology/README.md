# advanced-astrology

**Chronographic oracle for agents.** Computes the present moment as symbolic tessellation — planetary hours, tattwas, biorhythms, moon sign — and guides agents to emit it in the oracular register.

Not a horoscope generator. Not a birth-chart reader. **Right now as cosmogram.**

## What makes this different

- **Computed, not confected.** Real planetary hours (Chaldean sequence timed from sunrise), tattwa cycles, biorhythm waves from birth date. No hallucinated positions.
- **Present-tense.** Not natal fate or next-week forecast. *This moment*, precisely calculated.
- **Oracular voice.** The skill teaches synthesis — reading multiple symbolic systems as a single composite and emitting the whole. Dense. Laconic. Pyroglossia.
- **Agent-native.** Standard-library Python, JSON output, graceful backend cascade. Runs anywhere Python does.

## Quick Start

```bash
python scripts/astro_pulse.py --profile assets/profile.example.json --markdown
```

See [`SKILL.md`](SKILL.md) for the full oracle arc and glyph keys.

## Install

```bash
npx skills add <owner/repo>@advanced-astrology
```

## Backends

1. `sideriod` or configured astrology CLI — highest precision
2. Bundled `scripts/astro_pulse.py` — standard-library approximations + optional `kerykeion` moon sign
3. Partial mode — computes available signals, names gaps

## License

MIT
