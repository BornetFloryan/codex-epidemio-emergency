---
name: trend-analysis
description: Trigger when user asks to analyze a time series, epidemic trend, increasing or decreasing cases, compare last values, detect hausse, baisse, stabilité, tendance épidémique, incidence trend, or weekly health indicators.
allowed-tools: Bash(python3 *), Read
---

# Trend Analysis

Use this skill to analyze a simple epidemiological time series and qualify the trend.

## When to use

Use this skill when the user asks whether an indicator is:

- increasing;
- decreasing;
- stable;
- unknown.

## Command

With sample data:

```bash
python3 .codex/skills/trend-analysis/main.py --sample
```

With manual values:

```bash
python3 .codex/skills/trend-analysis/main.py --values 12 15 18 22
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
