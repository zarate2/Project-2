# How Labs 13–19 support this project

| Lab | Contribution | Where it appears |
|---|---|---|
| 13 — Mandate | Sample objective, payouts/reserves and constraints; historical named proposal excluded from active app | [Mandate](mandate.md), [original excerpt](../sources/lab-reference/Lab13-mandate.md), `config.json` |
| 14 — Baselines | Equal weighting, inverse volatility and benchmark comparison | `portfolio.py`, baseline table in app; [reference results](../sources/lab-reference/Lab14-results.json) |
| 15 — Stability | Monthly return estimation, covariance, grid search and window/estimate sensitivity | Original `portfolio.py` retained; `model.py` adds net cost, risk and equity constraints; [saved lab results](../sources/lab-reference/Lab15-results.json) |
| 16 — Provenance | Availability is distinct from observation date; reject ineligible inputs | `signal_data.py`; [original gate example](../sources/lab-reference/Lab16-asof.py) |
| 17 — Point in time | CPI vintage snapshots, revision awareness, data card and no-current-fallback rule | `signal_data.py`, [data card](data-card.md), [snapshot manifest](../sources/cpi-manifest.json) |
| 18 — Buffett skill | Annual SEC fact selection, business checks and literal numeric auditing | `sec_facts.py`, saved Buffett memo, preserved skill source |
| 19 — Legend panel | Shared financial packet, three perspectives, policy binding and NVDA as a VT holding | `panel.py`, `research.py`, investor tab and [memos](../research/memos/) |

The [import manifest](../sources/import-manifest.json) records original paths and hashes for copied files. Lab 15's engine, Lab 19's SEC/panel code and saved source data are preserved. New glue code is limited to the portfolio policy layer, vintage gate, project interface and reproducible report.

Copied skill instructions are retained as provenance; their original lab-specific Codex invocation paths are not a standalone skill installation for this project. The web app uses the local Python modules and policy file directly and needs no skill installation, model call or API token. Reusable skill packaging can be revisited if needed.

The copied lab sources are historical evidence, not proof that the new combined application is validated. This project has its own verification log and open requirements.
