---
name: cathie-wood-sec
description: Write an innovation-focused business memo using annual SEC revenue growth and R&D checks. Use for Cathie Wood's Lab 19 panel, without price forecasts.
---

# Cathie Wood business lens

Use the shared engine at `../../panel.py` relative to this file, so every persona reads the same facts. From the workspace root run:

```sh
python3 "Lab 19/panel.py" COST --snapshot
```

For a new ticker omit `--snapshot` and supply `--user-agent "Name real-email"` or `SEC_USER_AGENT`. The engine prints the annual financial table, XBRL provenance, endpoint revenue CAGR, R&D/revenue and all investor checks. Read `Lab 19/outputs/TICKER-panel.md` before writing. No FAskills installation or paid data sources.

The executable settings in [policy.json](policy.json) are the source of truth: growth threshold 15%, R&D threshold 5%. Code computes revenue CAGR as `(last / first) ** (1 / 4) - 1`, requiring a full five-year window and valid endpoints; R&D uses the latest annual ResearchAndDevelopmentExpense divided by revenue. Missing inputs give `not known` checks. Missing R&D remains `not found`, never zero. To run the assigned threshold probe change growth_threshold to 0.05, rerun code, record the result, then explicitly retain or restore the chosen setting. Do not edit only prose or hardcode the resulting verdict.

Write `Lab 19/outputs/TICKER-cathie-wood-memo.md`, headed `# TICKER — Cathie Wood — VERDICT`, choosing `Own the business`, `Watch it`, or `Pass`. Clearly identify this as AI-written educational role-play, not her actual opinion. Apply the innovation lens from [FAskills](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/cathie_wood.md): growth, reinvestment and the possibility of durable adoption. Historical growth and R&D do not prove technological advantage, profitable innovation or future expansion. Make that uncertainty explicit.

Use only printed numbers, matching their units and dates. No invented market sizes, cost curves, holdings, scores, forecasts or price targets. Finish with a line stating the growth threshold retained and why. Audit with `python3 "Lab 19/panel.py" TICKER --audit-memos`; resolve flags before finishing. The audit is literal numeric support, not a semantic truth check. Preserve independent judgment; do not automatically equate a check result with an ownership verdict.
