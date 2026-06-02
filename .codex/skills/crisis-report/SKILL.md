---
name: crisis-report
description: Trigger when user asks for an emergency report, situation note, crisis summary, epidemiological briefing, note sanitaire, cellule de crise, synthese operationnelle, niveau d'attention, signaux a surveiller, or public health emergency summary.
allowed-tools: Bash(python *), Read
---

# Crisis Report

Use this skill to produce a short operational epidemiological situation note.

## Command

```bash
python .codex/skills/crisis-report/main.py "$ARGUMENTS"
```

## Expected output

Return JSON with:

- title;
- operational summary;
- attention level;
- signals to monitor;
- recommended actions;
- limits;
- sources;
- medical caution.

Do not provide individual medical diagnosis.

For interpretation details, see `references/format.md`.
