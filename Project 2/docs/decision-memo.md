# Portfolio process decision

I used **OpenAI GPT-6 Luna through Codex** to help develop, modify, and produce this financial application. I reviewed and agree with the analysis and recommendation; the analysis and decision are mine. **For education, not investment advice.**

**Decision: continue in paper research only; authorize 0% new capital.** With the student's revised 12% annualized-volatility ceiling, the 60-month screen finds a feasible portfolio on the tested 5-percentage-point grid. The model-selected mix is 35% BIL / 65% VTI, with an estimated 8.61% net annual return and 10.28% annualized volatility. It clears the proposed 8.34% return hurdle and 12% ceiling in this historical estimate, but the evidence is not sufficient to authorize investment.

Engine decision: “PILOT in paper research only, with 0% new capital authorized. Consider adoption only after the assumptions are reviewed and independent performance, costs, liquidity and implementation evidence support it.”

The 12% ceiling replaces the earlier 10% ceiling. The student is allowing somewhat more modeled volatility while keeping a defined risk boundary. A higher risk limit does not guarantee a higher return, and volatility does not cap losses. The selection rule still chooses the lowest estimated volatility among allocations that meet the return target within the limit.

The proposed decision date is November 23, 2026. Model version 0.2.1 uses monthly adjusted prices through October 2026, retrieved November 22, and a 60-month estimation window. The universe is BIL, IEF, LQD, and VTI. The comparison is 60% VTI / 20% IEF / 20% LQD. The proposed planning horizon is seven years, with no scheduled withdrawals.

The 3-month Treasury reference is 4.34% (DGS3MO observation November 19, from the November 22 ALFRED vintage). Adding the proposed 4-percentage-point premium sets an 8.34% net screening hurdle. A proposed 0.25% annual cost is subtracted from gross estimates. The short Treasury rate may change and is not a seven-year locked return. Arithmetic estimates are not compounded forecasts.

Equal weight and inverse-volatility portfolios estimate 3.21% and 3.20% net, respectively, and miss the return hurdle. The 60/40 comparison estimates 6.44% net and 11.98% volatility; it is within the revised volatility ceiling but misses the return hurdle. The constrained result is 35% BIL / 65% VTI at 8.61% net and 10.28% volatility.

The 36-month sensitivity produces 75% BIL / 25% VTI at 8.44% net and 3.21% volatility. Other displayed feasible stresses produce different allocations. These are sensitivities using the same historical price set, not independent or out-of-sample validation. They do not prove that a strategy will meet the target over seven years.

The search is limited to four ETF proxies and a 5-point allocation grid. The evidence does not establish realized seven-year performance, reliable risk compensation, liquidity, turnover, taxes, or calibrated implementation cost. Further validation, independent review, and implementation evidence are required before adoption.

**Committee ask:** retain the 35% BIL / 65% VTI result as a paper research candidate only; authorize no capital. Reconsider adoption after independent validation and review of costs, liquidity, and implementation limits.

Figures: [executed output](../outputs/visible-output.md), [full-precision results](../outputs/results.json). Policy and provenance: [mandate](mandate.md), [data card](data-card.md). Validation status: [validation and AI-use record](validation-and-ai-use.md).
