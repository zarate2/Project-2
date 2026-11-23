# Data card and decision-time rules

## Portfolio prices

The app uses monthly adjusted USD price levels for BIL, IEF, LQD, and VTI from Yahoo Finance. Raw responses, the derived CSV, retrieval metadata, and SHA-256 hashes are retained in [`sources/market/`](../sources/market/). The 121 levels run from October 2016 through October 2026 and yield 120 monthly returns. The first day labels a completed monthly bar; it is not the publication date. The last complete month is October 2026, before the proposed November 23 decision.

Returns are price relatives minus one. Expected return is monthly arithmetic mean times 12; covariance uses sample monthly covariance times 12. The default uses 60 returns. Adjusted historical values retrieved in November 2026 are one information set; they do not recreate the prices known at every historical rebalance. No point-in-time strategy backtest is claimed. Before public redistribution, confirm the data provider's permitted use and redistribution terms.

## Treasury reference

The return hurdle uses FRED series DGS3MO, retrieved as the exact November 22, 2026 ALFRED vintage. The latest available observation is November 19 at 4.34% per annum (investment basis). The source CSV, URL, retrieval timestamp, units, and hash are recorded in [`manifest.json`](../sources/market/manifest.json). The rate is converted from percent to a decimal before calculations. It is a short-term reference and not a locked seven-year yield.

The hurdle equals the Treasury reference plus a 4-percentage-point proposed premium. A 5-point premium is tested as a stress. Neither premium is a forecast or guarantee. The 4.34% observation plus 4 points produces an 8.34% annual net estimate hurdle. The model subtracts a separate 0.25% annual cost estimate from gross returns; this cost has not been calibrated to a real implementation.

## Assumptions and limits

The 7-year horizon, no-withdrawal policy, 60/40 benchmark, 12% annualized-volatility ceiling, return premium, and selection rule are proposed policy inputs, not sourced market facts. The 60-month estimation window and 5-point portfolio grid are design choices. The benchmark is 60% VTI, 20% IEF, and 20% LQD. The eligible proxies are U.S. Treasury bills (BIL), Treasury notes (IEF), investment-grade corporate bonds (LQD), and U.S. equities (VTI).

Annualized arithmetic estimates are screening statistics. Volatility is not a loss limit. The model does not establish compounded seven-year returns, rolling strategy results, drawdowns, liquidity, turnover, taxes, or realized implementation costs. No withdrawals are required in the assignment, so the revised app does not model payouts or reserves.

## Preserved historical material

Earlier CPI, VT, and NVDA research files belong to the pre-revision baseline. They remain for traceability but do not feed the version 0.2.1 portfolio decision. The earlier version is archived in [`history/before-mandate-v0.2.zip`](../history/before-mandate-v0.2.zip).

AI disclosure: OpenAI Codex assisted with this documentation and model implementation. Student review remains required.
