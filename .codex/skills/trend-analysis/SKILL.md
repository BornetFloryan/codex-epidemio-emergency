---
name: trend-analysis
description: Trigger when user asks to analyze a time series, epidemic trend, increasing or decreasing cases, compare last values, detect hausse, baisse, stabilite, tendance epidemique, incidence trend, or weekly health indicators.
allowed-tools: Bash(python *), Read
---

# Trend Analysis

Use this skill to analyze a simple epidemiological time series and qualify the trend.

## Command

With sample data:

```bash
python .codex/skills/trend-analysis/main.py --sample
```

With manual values:

```bash
python .codex/skills/trend-analysis/main.py --values 12 15 18 22
```

## Expected output

Return JSON with:

- trend;
- last value;
- previous value;
- delta;
- interpretation;
- limits.

Do not overinterpret the result.

For method details, see `references/method.md`.
