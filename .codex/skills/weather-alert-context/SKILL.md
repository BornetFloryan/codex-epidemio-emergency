---
name: weather-alert-context
description: Trigger when user asks for weather context, meteorological situation, local weather, precipitation, wind, temperature, humidity, weather alert context, vigilance context, or emergency weather framing for a French place.
allowed-tools: Bash(python *), Read
---

# Weather Alert Context

Use this skill to provide local weather context for a French commune in an emergency situation.

## Command

```bash
python .codex/skills/weather-alert-context/main.py "$ARGUMENTS"
```

## Expected output

Return JSON with:

- queried place;
- matched commune;
- coordinates used;
- current temperature;
- humidity;
- precipitation;
- wind speed;
- operational interpretation;
- limits;
- sources.

This skill gives weather context only. It does not replace official vigilance bulletins.

For source details, see `references/sources.md`.
