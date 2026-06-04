---
name: geo-zone-context
description: Trigger when user asks for geographic context, commune lookup, zone context, city location, INSEE code, postal code, department, region, population, latitude, longitude, or emergency geographic framing for a French place.
allowed-tools: Bash(python .codex/skills/geo-zone-context/main.py *), Read
---

# Geo Zone Context

Use this skill to identify a French commune and return a short geographic context useful in an emergency briefing.

## Command

```bash
python .codex/skills/geo-zone-context/main.py "$ARGUMENTS"
```

## Expected output

Return JSON with:

- queried place;
- source API;
- best matching commune;
- INSEE code;
- postal codes;
- department;
- region;
- population;
- approximate coordinates;
- operational summary;
- limits;
- sources.

Always include the sources and limits in the final answer.
For source details, see `references/sources.md`.
