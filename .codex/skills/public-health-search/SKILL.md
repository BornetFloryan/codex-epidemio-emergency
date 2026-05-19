---
name: public-health-search
description: Trigger when user asks to find public health datasets, epidemiological data sources, Santé publique France, Sentinelles, Géodes, data.gouv.fr, open data, health surveillance, veille sanitaire, or sources for emergency epidemiology.
allowed-tools: Bash(python3 *), Read
---

# Public Health Search

Use this skill to search or describe public data sources useful for epidemiological emergency monitoring.

## When to use

Use this skill when the user asks for:

- public health datasets;
- epidemiological data sources;
- Santé publique France, Géodes, Sentinelles or data.gouv.fr resources;
- sources useful for sanitary crisis monitoring.

## Command

```bash
python3 .codex/skills/public-health-search/main.py "$ARGUMENTS"
```

## Expected output

Return:

- trend;
- last value;
- previous value;
- delta;
- interpretation;
- limits.

Do not overinterpret the result.
