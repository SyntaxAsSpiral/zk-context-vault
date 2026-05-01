# Output Schema

All executable scripts in this skill should support `--json` and emit a single JSON document to stdout.

## Success

```json
{
  "ok": true,
  "backend": "bundled-approximation",
  "query": {
    "profile": "assets/profile.example.json",
    "datetime": "2026-04-30T08:00:00-07:00",
    "location": {
      "label": "Clovis, NM",
      "lat": 34.4048,
      "lon": -103.2052,
      "timezone": "America/Denver"
    }
  },
  "result": {
    "planetary_hour": {
      "ruler": "Venus",
      "hour_index": 3,
      "period": "day",
      "starts_at": "...",
      "ends_at": "..."
    },
    "tattwa": {
      "element": "Apas",
      "minutes_since_segment_start": 10.5,
      "segment_minutes": 24
    },
    "moon": {
      "sign": "Cancer",
      "backend": "kerykeion"
    },
    "biorhythms": {
      "physical": {"value": 52.1, "trend": "Ascending", "critical": false}
    }
  },
  "warnings": []
}
```

## Failure

```json
{
  "ok": false,
  "error": "invalid_profile",
  "detail": "birth.date is required in YYYY-MM-DD format",
  "warnings": []
}
```

## Requirements

- JSON mode prints no Markdown, ANSI escapes, emoji, or extra logging.
- Use stable key names.
- Include warnings for approximations and unavailable optional signals.
- Use nonzero exit codes for failure.
- Include enough `query` context for an agent to narrate the result without relying on memory.
