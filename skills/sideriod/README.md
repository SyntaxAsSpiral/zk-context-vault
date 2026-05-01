# sideriod

**Chronographic oracle for agents.** Computes the present moment as symbolic tessellation — planetary hours, tattwas, biorhythms, moon sign, congruence, 99 Names affinities — and emits it in the oracular register.

Not a horoscope generator. Not a birth-chart reader. **Right now as cosmogram.**

## Install

```bash
npx skills add <owner/repo>@sideriod
```

## Quick Start

```bash
# Set up sideriod locally (one-time)
git clone https://github.com/zk-phi/sideriod ~/sideriod
cd ~/sideriod && nix develop
cp assets/profile.example.json assets/profile.json
# edit profile.json with your location + birth date
python3 daemon/gnomon.py

# Run the MCP server
python3 mcp/server.py
```

Or ask an agent to run the setup — the SKILL.md has the full guide.

## License

MIT (MCP server + skill). Sideriod engine: GPL (pyswisseph/Swiss Ephemeris).
