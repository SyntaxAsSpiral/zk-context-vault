#!/usr/bin/env python3
"""
Portable astrology pulse script for Agent Skills.

Basic mode uses only the Python standard library:
- approximate sunrise/sunset via NOAA-style formula
- planetary hour ruler via Chaldean sequence
- tattwa segment from most recent sunrise
- biorhythm cycles from birth date

Optional: if kerykeion is installed, moon sign is included.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

CHALDEAN_ORDER = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]
DAY_RULERS = {
    0: "Moon",      # Monday
    1: "Mars",      # Tuesday
    2: "Mercury",   # Wednesday
    3: "Jupiter",   # Thursday
    4: "Venus",     # Friday
    5: "Saturn",    # Saturday
    6: "Sun",       # Sunday
}
STANDARD_TATTWA_SEQUENCE = ["Prithvi", "Apas", "Tejas", "Vayu", "Akasha"]
TATTWA_START = {
    0: "Apas",      # Monday
    1: "Tejas",     # Tuesday
    2: "Prithvi",   # Wednesday
    3: "Akasha",    # Thursday
    4: "Apas",      # Friday
    5: "Vayu",      # Saturday
    6: "Tejas",     # Sunday
}
BIORHYTHM_CYCLES = {
    "physical": 23,
    "emotional": 28,
    "intellectual": 33,
    "spiritual": 38,
}
PLANET_GLYPHS = {
    "Saturn": "♄",
    "Jupiter": "♃",
    "Mars": "♂",
    "Sun": "☉",
    "Venus": "♀",
    "Mercury": "☿",
    "Moon": "☽",
}
TATTWA_GLYPHS = {
    "Akasha": "⊙",
    "Vayu": "🜁",
    "Tejas": "🜂",
    "Prithvi": "🜃",
    "Apas": "🜄",
}


def success(query: dict[str, Any], result: dict[str, Any], warnings: list[str]) -> dict[str, Any]:
    return {"ok": True, "backend": "bundled-approximation", "query": query, "result": result, "warnings": warnings}


def failure(error: str, detail: str, warnings: list[str] | None = None) -> dict[str, Any]:
    return {"ok": False, "error": error, "detail": detail, "warnings": warnings or []}


def parse_datetime(value: str | None, tz: ZoneInfo) -> dt.datetime:
    if not value:
        return dt.datetime.now(tz)
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = dt.datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError("datetime must be ISO 8601, e.g. 2026-04-30T08:00:00-07:00") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=tz)
    return parsed.astimezone(tz)


def load_profile(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"profile not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"profile is not valid JSON: {exc}") from exc


def get_location(profile: dict[str, Any]) -> dict[str, Any]:
    loc = profile.get("current_location") or {}
    birth = profile.get("birth") or {}
    merged = {
        "label": loc.get("label") or birth.get("place") or "unspecified",
        "lat": loc.get("lat", birth.get("lat")),
        "lon": loc.get("lon", birth.get("lon")),
        "timezone": loc.get("timezone") or birth.get("timezone") or "UTC",
    }
    missing = [k for k in ("lat", "lon", "timezone") if merged.get(k) is None]
    if missing:
        raise ValueError(f"missing location fields: {', '.join(missing)}")
    merged["lat"] = float(merged["lat"])
    merged["lon"] = float(merged["lon"])
    if not -90 <= merged["lat"] <= 90:
        raise ValueError("latitude must be between -90 and 90")
    if not -180 <= merged["lon"] <= 180:
        raise ValueError("longitude must be between -180 and 180")
    return merged


def normalize_angle(deg: float) -> float:
    return deg % 360.0


def noaa_sun_event(day: dt.date, lat: float, lon: float, tz: ZoneInfo, event: str) -> dt.datetime | None:
    """Approximate sunrise/sunset for a date/location. Returns localized datetime."""
    if event not in {"rise", "set"}:
        raise ValueError("event must be rise or set")
    zenith = 90.833
    n = day.timetuple().tm_yday
    lng_hour = lon / 15.0
    t = n + ((6 - lng_hour) / 24.0 if event == "rise" else (18 - lng_hour) / 24.0)
    mean_anomaly = (0.9856 * t) - 3.289
    true_long = mean_anomaly + (1.916 * math.sin(math.radians(mean_anomaly))) + (0.020 * math.sin(math.radians(2 * mean_anomaly))) + 282.634
    true_long = normalize_angle(true_long)
    right_asc = math.degrees(math.atan(0.91764 * math.tan(math.radians(true_long))))
    right_asc = normalize_angle(right_asc)
    l_quadrant = math.floor(true_long / 90.0) * 90.0
    ra_quadrant = math.floor(right_asc / 90.0) * 90.0
    right_asc = (right_asc + (l_quadrant - ra_quadrant)) / 15.0
    sin_dec = 0.39782 * math.sin(math.radians(true_long))
    cos_dec = math.cos(math.asin(sin_dec))
    cos_h = (math.cos(math.radians(zenith)) - (sin_dec * math.sin(math.radians(lat)))) / (cos_dec * math.cos(math.radians(lat)))
    if cos_h > 1 or cos_h < -1:
        return None
    hour_angle = 360.0 - math.degrees(math.acos(cos_h)) if event == "rise" else math.degrees(math.acos(cos_h))
    hour_angle /= 15.0
    local_mean = hour_angle + right_asc - (0.06571 * t) - 6.622
    utc_hour = (local_mean - lng_hour) % 24.0
    hour = int(utc_hour)
    minute_float = (utc_hour - hour) * 60
    minute = int(minute_float)
    second = int(round((minute_float - minute) * 60))
    if second == 60:
        second = 0
        minute += 1
    if minute == 60:
        minute = 0
        hour = (hour + 1) % 24
    utc_dt = dt.datetime(day.year, day.month, day.day, hour, minute, second, tzinfo=dt.timezone.utc)
    return utc_dt.astimezone(tz)


def sun_bounds_for_day(day: dt.date, lat: float, lon: float, tz: ZoneInfo) -> tuple[dt.datetime, dt.datetime]:
    sunrise = noaa_sun_event(day, lat, lon, tz, "rise")
    sunset = noaa_sun_event(day, lat, lon, tz, "set")
    if sunrise is None or sunset is None:
        raise ValueError("sunrise/sunset unavailable for this date/location, likely polar day/night")
    return sunrise, sunset


def planetary_hour(now: dt.datetime, lat: float, lon: float, tz: ZoneInfo) -> dict[str, Any]:
    today = now.date()
    sunrise, sunset = sun_bounds_for_day(today, lat, lon, tz)
    if sunrise <= now < sunset:
        period = "day"
        planetary_day = today
        start, end = sunrise, sunset
        segment_offset = 0
    elif now >= sunset:
        period = "night"
        planetary_day = today
        tomorrow_sunrise, _ = sun_bounds_for_day(today + dt.timedelta(days=1), lat, lon, tz)
        start, end = sunset, tomorrow_sunrise
        segment_offset = 12
    else:
        period = "night"
        planetary_day = today - dt.timedelta(days=1)
        _, prev_sunset = sun_bounds_for_day(planetary_day, lat, lon, tz)
        start, end = prev_sunset, sunrise
        segment_offset = 12

    duration = (end - start) / 12
    idx_in_period = min(11, max(0, int((now - start) / duration)))
    total_offset = segment_offset + idx_in_period
    day_ruler = DAY_RULERS[planetary_day.weekday()]
    start_idx = CHALDEAN_ORDER.index(day_ruler)
    ruler = CHALDEAN_ORDER[(start_idx + total_offset) % len(CHALDEAN_ORDER)]
    seg_start = start + duration * idx_in_period
    seg_end = start + duration * (idx_in_period + 1)
    return {
        "ruler": ruler,
        "day_ruler": day_ruler,
        "hour_index": idx_in_period + 1,
        "period": period,
        "starts_at": seg_start.isoformat(),
        "ends_at": seg_end.isoformat(),
        "sunrise": sunrise.isoformat(),
        "sunset": sunset.isoformat(),
    }


def tattwa(now: dt.datetime, lat: float, lon: float, tz: ZoneInfo) -> dict[str, Any]:
    sunrise, _ = sun_bounds_for_day(now.date(), lat, lon, tz)
    source_day = now.date()
    if now < sunrise:
        source_day = now.date() - dt.timedelta(days=1)
        sunrise, _ = sun_bounds_for_day(source_day, lat, lon, tz)
    minutes = (now - sunrise).total_seconds() / 60.0
    cycle_pos = minutes % 120.0
    segment_index = int(cycle_pos // 24)
    start_element = TATTWA_START[source_day.weekday()]
    start_index = STANDARD_TATTWA_SEQUENCE.index(start_element)
    element = STANDARD_TATTWA_SEQUENCE[(start_index + segment_index) % len(STANDARD_TATTWA_SEQUENCE)]
    segment_start = now - dt.timedelta(minutes=(cycle_pos % 24))
    return {
        "element": element,
        "start_element": start_element,
        "segment_minutes": 24,
        "minutes_since_segment_start": round(cycle_pos % 24, 2),
        "segment_starts_at": segment_start.isoformat(),
        "source_sunrise": sunrise.isoformat(),
    }


def biorhythms(birth_date: str, target: dt.datetime) -> dict[str, Any]:
    try:
        birth = dt.datetime.strptime(birth_date, "%Y-%m-%d").replace(tzinfo=target.tzinfo)
    except ValueError as exc:
        raise ValueError("birth.date must be YYYY-MM-DD") from exc
    diff_days = (target - birth).total_seconds() / 86400.0
    output: dict[str, Any] = {}
    for name, period in BIORHYTHM_CYCLES.items():
        angle = 2 * math.pi * diff_days / period
        percent = (math.sin(angle) + 1) * 50
        output[name] = {
            "value": round(percent, 2),
            "trend": "Ascending" if math.cos(angle) > 0 else "Descending",
            "critical": 48 <= percent <= 52,
            "period_days": period,
        }
    return output


def optional_moon_sign(now: dt.datetime, loc: dict[str, Any], warnings: list[str]) -> dict[str, Any] | None:
    try:
        from kerykeion import AstrologicalSubject  # type: ignore
    except Exception:
        warnings.append("moon sign unavailable: optional dependency kerykeion is not installed")
        return None
    try:
        subject = AstrologicalSubject(
            "Now",
            now.year,
            now.month,
            now.day,
            now.hour,
            now.minute,
            lat=loc["lat"],
            lng=loc["lon"],
            tz_str=loc["timezone"],
        )
        moon = subject.moon
        sign = moon.get("sign") if isinstance(moon, dict) else getattr(moon, "sign", None)
        return {"sign": sign, "backend": "kerykeion"}
    except Exception as exc:
        warnings.append(f"moon sign unavailable: kerykeion failed: {exc}")
        return None


def synthesize_markdown(payload: dict[str, Any]) -> str:
    if not payload.get("ok"):
        return f"⚡ pulse failed: {payload.get('error')}: {payload.get('detail')}"
    result = payload["result"]
    query = payload.get("query", {})
    ph = result.get("planetary_hour", {})
    tt = result.get("tattwa", {})
    moon = result.get("moon") or {}
    bios = result.get("biorhythms", {})

    ruler = ph.get("ruler", "?")
    element = tt.get("element", "?")
    g_ruler = PLANET_GLYPHS.get(ruler, "")
    g_element = TATTWA_GLYPHS.get(element, "")
    period = ph.get("period", "?")
    hour_idx = ph.get("hour_index", "?")
    loc_label = query.get("location", {}).get("label", "")
    ts = query.get("datetime", "")[:16] if query.get("datetime") else ""

    header = f"# ⟁ Pulse · {ts}" + (f" · {loc_label}" if loc_label else "")
    lines = [header, ""]

    moon_str = f" · ☽ {moon['sign']}" if moon.get("sign") else ""
    lines.append(f"{g_ruler} **{ruler}** · {period} {hour_idx} · {g_element} **{element}**{moon_str}")
    lines.append("")

    lines.append("## ⚡ Biorhythm Wave")
    for name, data in bios.items():
        val = data.get("value", 0)
        trend = data.get("trend", "")
        period_d = data.get("period_days", "?")
        arrow = "↑" if "Ascending" in trend else "↓"
        crit = " ⚠ critical" if data.get("critical") else ""
        lines.append(f"- **{name}** ({period_d}d) · {val:.1f}% {arrow}{crit}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Symbols are terrain, not verdict. Track what actually correlates.*")

    if payload.get("warnings"):
        lines.append("")
        lines.append("**⚠ Warnings**")
        for warning in payload["warnings"]:
            lines.append(f"- {warning}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a portable astrology pulse for agent workflows.")
    parser.add_argument("--profile", default=str(Path(__file__).resolve().parents[1] / "assets" / "profile.example.json"), help="Path to profile JSON")
    parser.add_argument("--datetime", dest="datetime_value", help="ISO 8601 datetime. If omitted, uses now in profile timezone.")
    parser.add_argument("--json", action="store_true", help="Emit JSON (default unless --markdown is used)")
    parser.add_argument("--markdown", action="store_true", help="Emit a simple Markdown reading")
    args = parser.parse_args()

    warnings: list[str] = ["sunrise/sunset and planetary hours use approximate standard-library calculations"]
    try:
        profile_path = Path(args.profile)
        profile = load_profile(profile_path)
        loc = get_location(profile)
        tz = ZoneInfo(str(loc["timezone"]))
        now = parse_datetime(args.datetime_value, tz)
        birth = profile.get("birth") or {}
        if not birth.get("date"):
            raise ValueError("birth.date is required for biorhythms")
        query = {
            "profile": str(profile_path),
            "name": profile.get("name"),
            "datetime": now.isoformat(),
            "location": loc,
        }
        result = {
            "planetary_hour": planetary_hour(now, loc["lat"], loc["lon"], tz),
            "tattwa": tattwa(now, loc["lat"], loc["lon"], tz),
            "biorhythms": biorhythms(str(birth["date"]), now),
        }
        moon = optional_moon_sign(now, loc, warnings)
        if moon:
            result["moon"] = moon
        payload = success(query, result, warnings)
        if args.markdown:
            print(synthesize_markdown(payload))
        else:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    except Exception as exc:
        payload = failure("astro_pulse_error", str(exc), warnings)
        if args.markdown:
            print(synthesize_markdown(payload))
        else:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
