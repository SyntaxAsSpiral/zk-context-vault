#!/usr/bin/env python3
"""
advanced-astrology MCP server — chronographic oracle.

Backend cascade:
  1. Sideriod (adeck) — kerykeion + flatlib + pyswisseph, full pulse
  2. Bundled astro_pulse.py — standard-library approximations, portable fallback

No API key. No cloud.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from zoneinfo import ZoneInfo

# ── Backend detection ─────────────────────────────────────────────────────────

SIDERIOD_DIR = Path.home() / "sideriod"
PULSE_PATH = SIDERIOD_DIR / "pulse.json"


def _sideriod_available() -> bool:
    return SIDERIOD_DIR.exists() and (SIDERIOD_DIR / "daemon" / "gnomon.py").exists()


def _refresh_pulse() -> dict:
    """Run gnomon.py via nix develop and return fresh pulse.json contents."""
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


def _read_pulse() -> dict:
    """Read pulse.json without refreshing."""
    return json.loads(PULSE_PATH.read_text())


# ── Bundled fallback ──────────────────────────────────────────────────────────

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from astro_pulse import (
    PLANET_GLYPHS,
    TATTWA_GLYPHS,
    biorhythms,
    failure,
    optional_moon_sign,
    parse_datetime,
    planetary_hour,
    success,
    tattwa,
)

# ── Server ────────────────────────────────────────────────────────────────────

mcp = FastMCP("advanced_astrology_mcp")

BACKEND = "sideriod" if _sideriod_available() else "bundled-approximation"


# ── Input models ──────────────────────────────────────────────────────────────

class PulseInput(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude (-90 to 90). Ignored in sideriod mode (uses profile).")
    lon: float = Field(..., ge=-180, le=180, description="Longitude (-180 to 180). Ignored in sideriod mode.")
    timezone: str = Field(..., description="IANA timezone, e.g. 'America/Denver'. Ignored in sideriod mode.")
    datetime: Optional[str] = Field(None, description="ISO 8601 datetime. Omit for now. Bundled fallback only.")
    birth_date: Optional[str] = Field(None, description="YYYY-MM-DD for biorhythms. Bundled fallback only.")
    refresh: bool = Field(True, description="If true and sideriod is available, runs gnomon.py to freshen pulse.")


class LocationTime(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    timezone: str
    datetime: Optional[str] = Field(None)


class BiorhythmInput(BaseModel):
    birth_date: str = Field(..., description="Birth date YYYY-MM-DD")
    timezone: str = Field(..., description="IANA timezone string")
    datetime: Optional[str] = Field(None, description="Target ISO 8601 datetime. Omit for now.")


# ── Tools ─────────────────────────────────────────────────────────────────────

@mcp.tool(name="astro_get_pulse", annotations={"readOnlyHint": True})
def astro_get_pulse(params: PulseInput) -> str:
    """
    Compute the full symbolic pulse for the current moment.

    Sideriod mode (adeck): runs gnomon.py — returns kerykeion + flatlib data including
    congruence, resonance_hz, mood, secretion_window, and 99 Names affinities.

    Portable mode: returns bundled standard-library approximations.

    Primary tool — call this first for an oracle reading.
    """
    if BACKEND == "sideriod":
        try:
            pulse = _refresh_pulse() if params.refresh else _read_pulse()
            return json.dumps({"ok": True, "backend": "sideriod", "result": pulse}, indent=2, ensure_ascii=False)
        except Exception as exc:
            return json.dumps({"ok": False, "error": str(exc), "backend": "sideriod"}, ensure_ascii=False)

    # Bundled fallback
    warnings = ["sunrise/sunset uses approximate standard-library calculations"]
    try:
        tz = ZoneInfo(params.timezone)
        now = parse_datetime(params.datetime, tz)
        loc = {"lat": params.lat, "lon": params.lon, "timezone": params.timezone, "label": ""}
        result: dict = {
            "planetary_hour": planetary_hour(now, params.lat, params.lon, tz),
            "tattwa": tattwa(now, params.lat, params.lon, tz),
        }
        if params.birth_date:
            result["biorhythms"] = biorhythms(params.birth_date, now)
        moon = optional_moon_sign(now, loc, warnings)
        if moon:
            result["moon"] = moon
        payload = success(
            {"datetime": now.isoformat(), "lat": params.lat, "lon": params.lon, "timezone": params.timezone},
            result, warnings,
        )
        return json.dumps(payload, indent=2, ensure_ascii=False)
    except Exception as exc:
        return json.dumps(failure("astro_get_pulse_error", str(exc), warnings), ensure_ascii=False)


@mcp.tool(name="astro_get_planetary_hour", annotations={"readOnlyHint": True})
def astro_get_planetary_hour(params: LocationTime) -> str:
    """
    Compute the current planetary hour ruler, period (day/night), index, and segment bounds.
    In sideriod mode reads from pulse.json. Lighter than astro_get_pulse.
    """
    if BACKEND == "sideriod":
        try:
            pulse = _read_pulse()
            ruler = pulse.get("hour_ruler", "?")
            return json.dumps({
                "ok": True, "backend": "sideriod",
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
    try:
        tz = ZoneInfo(params.timezone)
        now = parse_datetime(params.datetime, tz)
        result = planetary_hour(now, params.lat, params.lon, tz)
        result["glyph"] = PLANET_GLYPHS.get(result["ruler"], "")
        return json.dumps({"ok": True, "backend": "bundled", "result": result}, indent=2, ensure_ascii=False)
    except Exception as exc:
        return json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False)


@mcp.tool(name="astro_get_tattwa", annotations={"readOnlyHint": True})
def astro_get_tattwa(params: LocationTime) -> str:
    """
    Compute the current tattwa (elemental tide) timed from sunrise.
    In sideriod mode reads from pulse.json.
    """
    if BACKEND == "sideriod":
        try:
            pulse = _read_pulse()
            element = pulse.get("tattwa", "?")
            return json.dumps({
                "ok": True, "backend": "sideriod",
                "result": {
                    "element": element,
                    "glyph": TATTWA_GLYPHS.get(element, ""),
                    "timestamp": pulse.get("timestamp"),
                },
            }, indent=2, ensure_ascii=False)
        except Exception as exc:
            return json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False)
    try:
        tz = ZoneInfo(params.timezone)
        now = parse_datetime(params.datetime, tz)
        result = tattwa(now, params.lat, params.lon, tz)
        result["glyph"] = TATTWA_GLYPHS.get(result["element"], "")
        return json.dumps({"ok": True, "backend": "bundled", "result": result}, indent=2, ensure_ascii=False)
    except Exception as exc:
        return json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False)


@mcp.tool(name="astro_get_biorhythms", annotations={"readOnlyHint": True})
def astro_get_biorhythms(params: BiorhythmInput) -> str:
    """
    Compute biorhythm wave state: physical (23d), emotional (28d),
    intellectual (33d), spiritual (38d) — value, trend, critical flag.
    In sideriod mode reads from pulse.json (profile birth date used).
    """
    if BACKEND == "sideriod":
        try:
            pulse = _read_pulse()
            bios = pulse.get("biorhythms")
            if bios:
                return json.dumps({"ok": True, "backend": "sideriod", "result": bios}, indent=2, ensure_ascii=False)
        except Exception:
            pass
    try:
        tz = ZoneInfo(params.timezone)
        now = parse_datetime(params.datetime, tz)
        result = biorhythms(params.birth_date, now)
        return json.dumps({"ok": True, "backend": "bundled", "result": result}, indent=2, ensure_ascii=False)
    except Exception as exc:
        return json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False)


@mcp.tool(name="astro_server_info", annotations={"readOnlyHint": True})
def astro_server_info() -> str:
    """Return backend mode and sideriod availability."""
    return json.dumps({
        "backend": BACKEND,
        "sideriod_dir": str(SIDERIOD_DIR),
        "sideriod_available": _sideriod_available(),
        "pulse_path": str(PULSE_PATH),
        "pulse_exists": PULSE_PATH.exists(),
    }, indent=2)


# ── Resources ─────────────────────────────────────────────────────────────────

@mcp.resource("astro://glyph_keys")
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
    Guide oracle synthesis from computed pulse data.
    Pass the JSON output of astro_get_pulse as pulse_json.
    Optionally include operator context (current task, question, mood).
    Sideriod pulse includes congruence, resonance_hz, mood, secretion_window,
    and 99 Names affinities — weave these into the synthesis when present.
    """
    context_block = f"\nOperator context: {context}\n" if context.strip() else ""
    return f"""\
You have the following computed astrology pulse:

{pulse_json}
{context_block}
Read this as a chronographic oracle. Follow the Oracle Arc:

1. Hold the lattice. Read all signals at once — planetary hour, tattwa,
   biorhythm phase, moon sign, congruence/mood, secretion window, and
   any 99 Names affinities present. What is the composite character at
   this intersection? Not signal by signal — whole.

2. Emit. One to three sentences, present tense, concrete image. State
   what the composite reveals. No hedging — speak or stay silent.

3. Ground the posture. Two suggestions framed as invitation:
   "A useful posture: ..." not "You should..."

4. Acknowledge the edge. One sentence on what this reading cannot see.
   Invite tracking — does this correlate with your experience?

The register is pyroglossia — fire-tongue above the fissure. Dense.
Laconic. Synthesize the whole; don't recite the parts.

Load astro://glyph_keys for seed phrases if needed."""


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
