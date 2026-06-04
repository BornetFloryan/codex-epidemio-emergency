---
name: health-dataset-search
description: Trigger when user asks to find public health datasets, epidemiological data sources, data.gouv.fr resources, Sante publique France, Sentinelles, Geodes, open data, veille sanitaire, veille epidemiologique, grippe, gastro-enterite, or emergency health monitoring sources.
allowed-tools: Bash(python .codex/skills/health-dataset-search/main.py *), Read
---

# Health Dataset Search

Use this skill to search public health and epidemiology datasets through the data.gouv.fr API.

## Command

```bash
python .codex/skills/health-dataset-search/main.py "$ARGUMENTS"
```

## Expected output

Read the JSON output and summarize:

- query;
- source API;
- relevant datasets;
- organizations;
- relevance score;
- available resources;
- sources;
- limits.

Always include the sources and limits in the final answer.
Do not provide individual medical diagnosis.

For API details, see `references/api.md`.
