---
name: buffett-sec
description: Evaluate a ticker's business quality using annual SEC facts, deterministic Buffett checks, and a number-audited memo. Use for Lab 18 or a Buffett business screen without stock prices.
---

# Buffett business screen

For **Lab 19's investor panel**, use `Lab 19/panel.py TICKER --snapshot` from the workspace root to compute the shared retained SEC packet, or omit `--snapshot` for a new download. Read `Lab 19/outputs/TICKER-panel.md` and write `TICKER-buffett-memo.md` in that output directory, headed `# TICKER — Warren Buffett — VERDICT`. Apply the same business judgment and numeric constraints below. Audit with `python3 "Lab 19/panel.py" TICKER --audit-memos`. The panel engine retains Buffett's original checks and adds the other investors' checks without asking Buffett to adopt their criteria. For standalone Lab 18, keep the original workflow below.

Run the bundled `scripts/sec_facts.py` for the requested ticker. Supply `--user-agent "Name email"` using the user's real contact details, or `SEC_USER_AGENT`. Never invent contact information. Example from the workspace root:

```sh
python3 "Lab 18/skill/buffett-sec/scripts/sec_facts.py" COST --output-dir "Lab 18/outputs" --source-dir "Lab 18/sources"
```

Read the resulting `TICKER-facts.md` before judging. Code selects the last five annual fiscal periods from 10-K facts, retains latest-filed values, applies the lab's tag priorities, and prints values, tags, and provenance. Missing facts stay `not found`; checks with missing inputs and ratios with nonpositive equity stay `not known`. Never fill gaps, substitute quarterly facts, or force data to match an answer key.

Write `TICKER-memo.md` in the output directory, a short Buffett-inspired educational role-play clearly identified as AI-written, not Buffett's actual opinion. Choose **own the business**, **watch it**, or **pass**. Judge persistent earning power, understandable economics, moat evidence and management uncertainty. Passing numerical checks does not establish a moat. Distinguish inference from evidence. Use only numbers printed in the report, in its exact USD-million or percentage format; do not calculate additional numbers in prose. No prices, price targets, valuations, maintenance-capex estimates, invented scores, or paid sources. If owner earnings are missing, explicitly say they cannot be judged. The lab's operating cash flow minus total capital spending is a simplified proxy, not a maintenance-capex reconstruction.

Add a single line below the memo giving a proposed trust decision and reason; label it an AI-drafted decision for the student to review. Never claim personal participation in a partner discussion or a fresh-chat probe.

Audit and bind the memo to its facts:

```sh
python3 "Lab 18/skill/buffett-sec/scripts/sec_facts.py" COST --output-dir "Lab 18/outputs" --audit-memo "Lab 18/outputs/COST-memo.md"
```

Fix unsupported numbers before finishing. The audit checks literal numeric tokens, not whether a valid number has been assigned to the correct metric, unit, or year; review those manually. The Streamlit app detects changed fact packets and does not present an older memo as current. For another ticker, write a new model judgment from its newly computed packet rather than generating a canned verdict in Python.

Philosophy reference: [FAskills Buffett page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md). Read only; do not install FAskills or use its data services. The assignment's formulas and limited business-only scope govern this skill.
