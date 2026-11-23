# Video 1 — Working Script

**Practice script, not the final transcript.** After recording, correct the transcript to match what you actually said. Keep the final video at or under 3:00, with your face visible.

## Opening

I used GPT-6 Luna through Codex to help develop, modify, and produce this financial application. I reviewed and agree with the analysis and recommendation. The analysis and decision are mine. This is for education, not investment advice.

## How the system and my thinking changed

The earlier version used an inflation-based return target, global equities, and scheduled withdrawals. I changed the objective to a return target four percentage points above a dated three-month Treasury rate. I chose that premium because investors taking equity and corporate-bond risk should have a higher return target than a short-term Treasury reference, although that target is not guaranteed.

I changed the equity exposure to domestic stocks and kept Treasury and investment-grade corporate bonds in the investment universe. I used a 60/40 stock-and-bond benchmark. The assignment does not require withdrawals, so I removed the payout schedule and reserve. I set a seven-year planning horizon and a 12% annualized-volatility limit. The model looks for the lowest estimated volatility among portfolios that meet the return target and risk limit.

## AI output I checked

The app reported an 8.34% annual net return target. I checked the three-month Treasury observation in the retained DGS3MO source file: it is 4.34%. I also checked the configuration: the required premium is 0.04, or four percentage points. In decimal form, 0.0434 plus 0.04 equals 0.0834, which is 8.34%. I accept the arithmetic and units. This check confirms how the target was calculated; it does not show that the portfolio can achieve it.

## Current decision

With the 60-month estimation window, no tested portfolio meets both the 8.34% return target and the 10% volatility limit. The best return estimate within the risk limit is 8.21%, so the base case is rejected and no allocation is selected. A 36-month sensitivity produces a feasible result, but that is a different estimation window, not proof that the process works. I agree with rejecting the base case and authorizing no capital.
