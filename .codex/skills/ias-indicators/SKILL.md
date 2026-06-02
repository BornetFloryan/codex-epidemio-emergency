---
name: ias-indicators
description: Trigger when user asks about IAS, indicateur avance sanitaire, syndrome grippal, flu, gastroenteritis, gastro-enterite, epidemic indicators, incidence, veille epidemiologique, data.gouv.fr, or sanitary monitoring in France.
allowed-tools: Bash(python *), Read
---

# IAS Indicators

Use this skill to search public datasets related to French advanced health indicators.

## Command

For flu:

```bash
python .codex/skills/ias-indicators/main.py --indicator grippe
```

For gastroenteritis:

```bash
python .codex/skills/ias-indicators/main.py --indicator gastro
```

## Expected output

Read the JSON output and summarize:

- indicator;
- query;
- dataset title;
- dataset page;
- organization;
- resources;
- interpretation;
- cache status;
- limits.

Do not provide individual medical diagnosis.

For source details, see `references/sources.md`.
