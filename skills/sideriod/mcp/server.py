#!/usr/bin/env python3
"""
sideriod MCP server — chronographic oracle.

Requires sideriod installed at ~/sideriod with gnomon.py daemon.
No API key. No cloud. No fallback.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# ── Sideriod ──────────────────────────────────────────────────────────────────

SIDERIOD_DIR = Path.home() / "sideriod"
PULSE_PATH = SIDERIOD_DIR / "pulse.json"

NOT_INSTALLED = (
    '{"ok": false, "error": "sideriod not found", '
    '"detail": "Install sideriod at ~/sideriod — see SKILL.md for setup guide."}'
)


def _available() -> bool:
    return SIDERIOD_DIR.exists() and (SIDERIOD_DIR / "daemon" / "gnomon.py").exists()


def _refresh() -> dict:
    result = subprocess.run(
        ["nix", "develop", "--command", "python3", "daemon/gnomon.py"],
        cwd=SIDERIOD_DIR,
        capture_output=True,
        text=True,
        timeout=90,
    )
    if result.returncode != 0:
        raise RuntimeError(f"gnomon failed: {result.stderr.strip()}")
    return json.loads(PULSE_PATH.read_text())


def _read() -> dict:
    return json.loads(PULSE_PATH.read_text())


# ── Server ────────────────────────────────────────────────────────────────────

mcp = FastMCP(
    "sideriod_mcp",
    host=os.environ.get("SIDERIOD_MCP_HOST", "127.0.0.1"),
    port=int(os.environ.get("SIDERIOD_MCP_PORT", "8000")),
)

PLANET_GLYPHS = {
    "Saturn": "♄", "Jupiter": "♃", "Mars": "♂", "Sun": "☉",
    "Venus": "♀", "Mercury": "☿", "Moon": "☽",
}
TATTWA_GLYPHS = {
    "Akasha": "⊙", "Vayu": "🜁", "Tejas": "🜂", "Prithvi": "🜃", "Apas": "🜄",
}


# ── Input models ──────────────────────────────────────────────────────────────

class PulseInput(BaseModel):
    refresh: bool = Field(True, description="Run gnomon.py to freshen pulse before reading.")


# ── Tools ─────────────────────────────────────────────────────────────────────

@mcp.tool(name="sideriod_get_pulse", annotations={"readOnlyHint": True})
def sideriod_get_pulse(params: PulseInput) -> str:
    """
    Compute the full symbolic pulse for the current moment.

    Returns kerykeion + flatlib data: planetary hour, tattwa, moon sign,
    congruence, resonance_hz, mood, secretion_window, 99 Names affinities,
    and biorhythm waves. Primary tool — call this first for an oracle reading.
    """
    if not _available():
        return NOT_INSTALLED
    try:
        pulse = _refresh() if params.refresh else _read()
        return json.dumps({"ok": True, "result": pulse}, indent=2, ensure_ascii=False)
    except Exception as exc:
        return json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False)


@mcp.tool(name="sideriod_get_planetary_hour", annotations={"readOnlyHint": True})
def sideriod_get_planetary_hour() -> str:
    """Current planetary hour ruler, day ruler, hour index, and tattwa from pulse.json."""
    if not _available():
        return NOT_INSTALLED
    try:
        pulse = _read()
        ruler = pulse.get("hour_ruler", "?")
        return json.dumps({
            "ok": True,
            "result": {
                "ruler": ruler,
                "glyph": PLANET_GLYPHS.get(ruler, ""),
                "day_ruler": pulse.get("planetary_day"),
                "hour_index": pulse.get("hour_index"),
                "tattwa": pulse.get("tattwa"),
                "timestamp": pulse.get("timestamp"),
            },
        }, indent=2, ensure_ascii=False)
    except Exception as exc:
        return json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False)


@mcp.tool(name="sideriod_get_tattwa", annotations={"readOnlyHint": True})
def sideriod_get_tattwa() -> str:
    """Current tattwa (elemental tide) from pulse.json."""
    if not _available():
        return NOT_INSTALLED
    try:
        pulse = _read()
        element = pulse.get("tattwa", "?")
        return json.dumps({
            "ok": True,
            "result": {
                "element": element,
                "glyph": TATTWA_GLYPHS.get(element, ""),
                "timestamp": pulse.get("timestamp"),
            },
        }, indent=2, ensure_ascii=False)
    except Exception as exc:
        return json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False)


@mcp.tool(name="sideriod_get_biorhythms", annotations={"readOnlyHint": True})
def sideriod_get_biorhythms() -> str:
    """
    Biorhythm wave state from pulse.json: physical (23d), emotional (28d),
    intellectual (33d), spiritual (38d) — value, trend, critical flag.
    Birth date sourced from sideriod profile.
    """
    if not _available():
        return NOT_INSTALLED
    try:
        pulse = _read()
        bios = pulse.get("biorhythms")
        if not bios:
            return json.dumps({"ok": False, "error": "no biorhythms in pulse — check sideriod profile has birth date"}, ensure_ascii=False)
        return json.dumps({"ok": True, "result": bios}, indent=2, ensure_ascii=False)
    except Exception as exc:
        return json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False)


@mcp.tool(name="sideriod_server_info", annotations={"readOnlyHint": True})
def sideriod_server_info() -> str:
    """Sideriod installation status and pulse freshness."""
    return json.dumps({
        "sideriod_dir": str(SIDERIOD_DIR),
        "sideriod_available": _available(),
        "pulse_path": str(PULSE_PATH),
        "pulse_exists": PULSE_PATH.exists(),
        "pulse_timestamp": _read().get("timestamp") if PULSE_PATH.exists() else None,
    }, indent=2)


# ── Resources ─────────────────────────────────────────────────────────────────

@mcp.resource("sideriod://glyph_keys")
def glyph_keys() -> str:
    """Seed phrases for planetary hour rulers and tattwas. Load for oracle synthesis."""
    return """\
# Glyph Keys

## Planetary Hour Rulers
♄ Saturn   — The crystallizer holds the hour. Heavy, patient, geometric.
♃ Jupiter  — The field opens. Wisdom moves outward.
♂ Mars     — The edge leads. The cut is clean.
☉ Sun      — The light is direct. Everything visible.
♀ Venus    — The field draws near. Beauty as intelligence.
☿ Mercury  — The nerve fires. Signal faster than the hand.
☽ Moon     — The tide pulls inward. Interior weather rising.

## Tattwas
⊙ Akasha  — Before the first sound.
🜁 Vayu   — The idea moves.
🜂 Tejas  — The cut clarifies.
🜃 Prithvi — The ground holds.
🜄 Apas   — The feeling flows.

Seeds for synthesis. Combine and transform — don't recite."""


# ── Prompts ───────────────────────────────────────────────────────────────────

@mcp.prompt(name="oracle_reading")
def oracle_reading(pulse_json: str, context: str = "") -> str:
    """
    Guide oracle synthesis from sideriod pulse data.
    Pass the JSON output of sideriod_get_pulse as pulse_json.
    Optionally include operator context (current task, question, mood).
    """
    context_block = f"\nOperator context: {context}\n" if context.strip() else ""
    return f"""\
You have the following sideriod pulse:

{pulse_json}
{context_block}
Read this as a chronographic oracle. Follow the Oracle Arc:

1. Hold the lattice. Read all signals at once — planetary hour, tattwa,
   biorhythm phase, moon sign, congruence/mood, secretion window, and
   99 Names affinities. What is the composite character at this intersection?
   Not signal by signal — whole.

2. Emit. One to three sentences, present tense, concrete image. State
   what the composite reveals. No hedging — speak or stay silent.

3. Ground the posture. Two suggestions framed as invitation:
   "A useful posture: ..." not "You should..."

4. Acknowledge the edge. One sentence on what this reading cannot see.
   Invite tracking — does this correlate with your experience?

The register is pyroglossia — fire-tongue above the fissure. Dense.
Laconic. Synthesize the whole; don't recite the parts.

Load sideriod://glyph_keys for seed phrases if needed."""


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    transport = os.environ.get("SIDERIOD_MCP_TRANSPORT", "stdio")
    if transport in ("http", "streamable-http"):
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
