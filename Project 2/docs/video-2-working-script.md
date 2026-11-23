# Video 2 — Working Script

**Practice script, not a transcript.** Keep the final video at or under 5:00 and keep your face visible while sharing readable code or app output. The changed-input example below is from the earlier 3.5%-to-4.5% premium test. Identify it as an earlier test; the current saved premium is 4% and the current allocation is different.

## 0:00–0:25 — Opening

I used GPT-6 Luna through Codex to help develop, modify, and produce this financial application. I reviewed and agree with the analysis and recommendation. The analysis and decision are mine. This is for education, not investment advice. I’ll show how the code turns the mandate into a portfolio decision and what checks can stop that decision.

## 0:25–1:05 — Inputs and dated data

In `config.json`, the four funds are BIL, IEF, LQD, and VTI. The saved settings use a seven-year horizon, a 60-month estimation window, a 12% volatility limit, a 4-percentage-point premium, and a 0.25% added annual cost. The three-month Treasury observation is dated November 19, 2026, and is 4.34%. Adding the four-point premium gives an 8.34% return hurdle. The Treasury rate is a short-term reference; it is not locked in for seven years.

In `market_data.py`, the app reads the retained prices and dated Treasury source. It checks that the requested information is available for the chosen date and window. The model uses completed monthly data through October 2026, rather than a live price feed.

## 1:05–2:20 — How the model makes a decision

In `model.py`, `calculate` loads and validates the settings, reads the data, estimates annual returns, volatility, and correlations, and builds a covariance matrix. It compares equal-weight, inverse-volatility, and 60/40 benchmark portfolios.

Then it searches long-only allocations in five-percentage-point steps. In `evaluate`, each candidate is checked against four rules: weights must total 100%; its net return estimate must meet the Treasury-plus-premium hurdle; volatility must stay at or below 12%; and U.S. equity must stay within its configured cap. Among candidates passing every rule, the model selects the one with the lowest estimated volatility. If none passes, it stops and reports no feasible allocation rather than quietly relaxing a rule.

## 2:20–3:10 — Current output and limits

For the current saved assumptions, the app reports 35% BIL and 65% VTI, an 8.61% estimated net return, and 10.28% estimated volatility. That passes the model’s return and risk screens. The separate deployment check still fails: independent performance, real costs, liquidity, implementation, and review evidence are incomplete. So the recommendation is paper research only, with zero new capital authorized. A modeled pass is not proof of future performance.

## 3:10–4:15 — Input checks and stresses

The code also rejects malformed settings, missing or inconsistent monthly data, invalid weights, and invalid correlation inputs. The stress suite changes one assumption at a time, including the return estimate, estimation window, cost, equity cap, and return premium. These are visible sensitivity results; they are not predictions I made before seeing the output.

## 4:15–4:40 — Changed-input experiment

In my earlier changed-input test, the baseline premium was 3.5 percentage points, with a 60-month window, zero VTI return shift, 0.25% added annual cost, a 12% volatility limit, and a 100% U.S. equity cap. The model showed 40% BIL and 60% VTI. I recorded a prediction to raise only the premium from 3.5 to 4.5 points. I expected BIL to fall and VTI to rise because the optimizer would need more return under the same limits. The recorded result was 30% BIL and 70% VTI, so the allocation moved in the direction I predicted. This is an observed model response, not evidence of future performance. It was an earlier model setup; the current saved premium is 4%, and the current portfolio is 35% BIL and 65% VTI.

Before recording, verify that the GitHub history shows the prediction was committed before this test. If it does not, describe this as a recorded comparison, not a locked experiment.

## 4:40–4:55 — Close

The code makes the assumptions and constraints visible, but it does not establish that this is a validated investment strategy. My decision remains zero capital until the missing evidence and independent review are complete.
