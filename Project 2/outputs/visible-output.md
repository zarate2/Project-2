AI disclosure: OpenAI Codex assisted with implementation, testing and drafting. Student ownership confirmation is pending.

For education, not investment advice.

# Project 2 — version 0.2.1

PILOT in paper research only, with 0% new capital authorized. Consider adoption only after the assumptions are reviewed and independent performance, costs, liquidity and implementation evidence support it.

Calculated 2026-11-22 for the proposed decision date 2026-11-23. Prices retrieved 2026-11-22, through completed month 2026-10. No live feed is used.

## Mandate and information set

Seven-year planning horizon; no scheduled withdrawals or payout reserve. Universe BIL / IEF / LQD / VTI. Benchmark: 60% VTI, 20% IEF, 20% LQD. Fully invested, long-only. Annualized volatility ceiling 12.00%; equity cap 100% (100% means no separate equity restriction beyond long-only and the volatility ceiling).

Three-month Treasury reference: 4.34%, observation 2026-11-19, ALFRED vintage 2026-11-22, downloaded 2026-11-22T20:54:07.481087+00:00. Return premium 4.00 percentage points gives a 8.34% annual net screen. Additional annual cost 0.25%; estimation uses 60 monthly returns.

The Treasury rate is a short-term reference, not a rate locked in for seven years. Returns are annualized arithmetic estimates, not a seven-year compound forecast. The return premium and risk ceiling are policy choices, not guaranteed outcomes. The cost estimate remains provisional.

## Comparisons

| Portfolio | Weights BIL / IEF / LQD / VTI | Gross | Net proxy | Volatility | Modeled verdict | Deployment |
| --- | --- | --- | --- | --- | --- | --- |
| Equal weight | 25.00% / 25.00% / 25.00% / 25.00% | 3.46% | 3.21% | 7.54% | FAIL: Net return proxy >= Treasury rate + premium | FAIL — validation and review incomplete |
| Inverse volatility | 87.49% / 5.47% / 4.33% / 2.71% | 3.45% | 3.20% | 1.34% | FAIL: Net return proxy >= Treasury rate + premium | FAIL — validation and review incomplete |
| 60/40 benchmark | 0.00% / 20.00% / 20.00% / 60.00% | 6.69% | 6.44% | 11.98% | FAIL: Net return proxy >= Treasury rate + premium | FAIL — validation and review incomplete |
| Constrained portfolio | 35.00% / 0.00% / 0.00% / 65.00% | 8.86% | 8.61% | 10.28% | PASS | FAIL — validation and review incomplete |

## Sensitivities

| Scenario | BIL / IEF / LQD / VTI | Net proxy | Volatility | Status |
| --- | --- | --- | --- | --- |
| Base | 35% / 0% / 0% / 65% | 8.61% | 10.28% | FEASIBLE |
| Estimate: VTI minus 1 percentage point | 25% / 0% / 0% / 75% | 8.66% | 11.84% | FEASIBLE |
| Window: 36 months | 75% / 0% / 0% / 25% | 8.44% | 3.21% | FEASIBLE |
| Cost: plus 1 percentage point | 25% / 0% / 0% / 75% | 8.41% | 11.84% | FEASIBLE |
| Constraint: U.S. equity cap at most 25% | No feasible allocation | — | — | STOP — no feasible 5-point allocation |
| Target: premium plus 1 percentage point | 25% / 0% / 0% / 75% | 9.41% | 11.84% | FEASIBLE |

**Research range across feasible scenarios:** BIL: 25%–75%; IEF: 0%–0%; LQD: 0%–0%; VTI: 25%–75%. The range is not a menu of independently combinable weights and grants no capital authorization.

## Decision conditions

Stop if no allocation is feasible, a required source or vintage is unavailable, integrity fails, or inputs are invalid. Do not substitute another date or relax the risk limit. Monitor estimated net return versus the Treasury-relative target, volatility, allocation drift, costs and source eligibility at each review. Annual rebalancing is a proposed convention, not an implemented trading simulation.

These estimates use one information set and are not an out-of-sample strategy evaluation. Ten years of retained prices allow additional outcome checks, but this screen has not validated a seven-year realized return, actual transaction costs, liquidity or turnover. Adoption requires that evidence and review; otherwise retain paper research only or reject an infeasible scenario.

The previous inflation/global-equity/payout version is archived in history/before-mandate-v0.2.zip. The old NVDA persona research is retained as historical material and does not drive this screen.

Human AI-off prediction, prior GitHub commit, independent user run, ownership confirmation, videos/transcripts and submission remain pending.

Sources: sources/market/manifest.json. Full results: outputs/results.json. Reproduce with python3 run.py.
