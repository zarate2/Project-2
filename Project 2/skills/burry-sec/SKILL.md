---
name: burry-sec
description: Write a skeptical business memo from annual SEC cash-versus-income and liabilities-to-equity checks. Use for Michael Burry's Lab 19 panel without prices or invented accounting allegations.
---

# Michael Burry business lens

Use the shared engine at `../../panel.py` relative to this file. From the workspace root run `python3 "Lab 19/panel.py" COST --snapshot`; for new data omit `--snapshot` and supply the user's real contact User-Agent. Read `Lab 19/outputs/TICKER-panel.md`. All investors must use the same annual fact packet and Lab 18 selection rules.

The engine computes operating cash flow at least net income in every annual row, and latest liabilities no more than twice year-end equity. The first check needs all annual input pairs; the second needs latest liabilities and strictly positive equity. Any missing required input means `not known`, never an inferred zero or a failed check. Liabilities are broader than debt. A cash-versus-income failure is a reason to investigate, not proof of accounting fraud.

Write `Lab 19/outputs/TICKER-burry-memo.md` headed `# TICKER — Michael Burry — VERDICT`, choosing `Own the business`, `Watch it`, or `Pass`. Identify AI-written educational role-play, not his actual opinion. Use the skeptical accounting and downside lens from [FAskills](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md), without installing that project or using its data services. Distinguish observed gaps/divergences from hypotheses requiring footnotes or further research.

Use only numbers printed by the shared engine, with matching units and periods. Do not add price targets, fabricated accounting accusations, short recommendations, financial estimates or invented confidence scores. Explain the business conclusion and its limits. Audit with `python3 "Lab 19/panel.py" TICKER --audit-memos`. Fix unsupported numbers; manually review year/metric attribution because literal number matching does not establish meaning. Judge independently rather than treating the panel as a majority vote.
