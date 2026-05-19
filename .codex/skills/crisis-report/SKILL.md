---
name: crisis-report
description: Trigger when user asks for an emergency report, situation note, crisis summary, epidemiological briefing, note sanitaire, cellule de crise, synthèse opérationnelle, niveau d’attention, signaux à surveiller, or public health emergency summary.
allowed-tools: Bash(python3 *), Read
---

# Crisis Report

Use this skill to produce a short operational epidemiological situation note.

## When to use

Use this skill when the user asks for:

- a crisis report;
- a public health situation note;
- an epidemiological summary for decision makers;
- a short operational briefing.

## Command

```bash
python3 .codex/skills/crisis-report/main.py "$ARGUMENTS"
```

## Expected output

Return a structured note with:

- title;
- operational summary;
- attention level;
- signals to monitor;
- limits;
- sources;
- medical caution.

Do not provide individual medical diagnosis.
