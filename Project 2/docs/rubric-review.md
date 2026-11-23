# Project 2 rubric review

Reviewed November 22, 2026 against all six pages of the student-supplied [Brightspace rubric](../sources/Project2-rubric.pdf), the [Project 2 assignment](../sources/Assignment.md), current code, saved results and supporting documents. This is an evidence audit, not a predicted grade or a claim of instructor approval.

**Conclusion:** the app implements the main portfolio comparison, dated signal and stress-test requirements. The submission is incomplete. The largest unresolved issues are the financial evidence behind the mandate, the student's before-run experiment, independent reproduction and final communication artifacts.

## How the requirements fit together

- The rubric allocates 300 points across the six criteria below. Validation is the largest category, followed by financial soundness.
- Page 1 contains Edition A/B language. The Project 2 assignment explicitly says neither is submitted; its specific submission instructions govern this review. Keep the historical baseline for comparison without adding an Edition A/B deliverable. Record any later instructor clarification rather than silently treating the conflict as resolved by the rubric alone.
- A named client is not required. An explicit intended user still is: the portfolio analyst operates the app and an investment committee decides whether to pilot or adopt the process under the stated sample mandate.
- The PDF does not add WACC, FCFF or EV/EBITDA requirements. The financial review stays focused on investment management.
- The rubric values reproducibility of the app. The assignment's submission list does not request an additional challenge record.
- Video caps and face visibility come from the course checklist and Project 1 feedback, not from this six-page PDF. They remain in the delivery checklist.

## Criterion-by-criterion findings

| Criterion | Points | Evidence already present | What still needs work |
|---|---:|---|---|
| Problem definition and decision usefulness | 45 | Sample mandate, analyst/committee roles, seven-year horizon, constraints, paper-only recommendation and reversal conditions | Student must understand and justify the goal and limits. Explain why the proposed process is useful for the intended decision; a client name is unnecessary. |
| Data integrity and traceability | 45 | Saved raw sources, URLs, dates, hashes, transformations, CPI vintage rule and separation of later NVDA research | Support material judgments such as costs and risk limits; document the basis for source redistribution before publishing retained data. A correct hash does not establish licensing rights or validate an economic assumption. |
| Financial soundness and judgment | 60 | Arithmetic return/covariance calculations, equal-weight and inverse-volatility comparisons, constrained search, stress ranges and explicit stop/reversal conditions | The annual screen does not establish rolling-five-year net performance or payout funding. Explain the CPI-plus-3-percentage-point convention, benchmark choice, provisional IEF reserve eligibility and why adverse estimates can increase equity. Liquidity, turnover and costs remain unverified. |
| Technical execution and usability | 45 | Working Streamlit app, pinned main dependency, offline report, source/failure checks, scenario downloads and automated isolated execution | Repository is unpublished. The isolated check uses an existing Python environment; it is not a fresh dependency installation or independent user test. Student must be able to explain the decision code. |
| Validation, sensitivity and reproducibility | 75 | Independent NumPy comparison, legacy reference result, four stress dimensions, invalid-input/missing-vintage tests, saved automated cold run | Human AI-off prediction and before/after decision effects are absent. Personal check of an AI output is not documented. Highest-risk financial claims need targeted evidence; no holdout or historical strategy evaluation is established. |
| Professional communication | 30 | README, memo, validation draft, data card, manifest and video checklist | Ownership remains pending; three videos, corrected transcripts, actual artifact URLs, access checks and Brightspace submission are absent. Final documents need one consistency pass after the substantive revisions. |

## What was independently checked in this review

[Audit evidence](../outputs/rubric-review-checks.json) records the rubric hash and these checks:

- All 61 monthly adjusted closes for each of four funds match the saved raw responses: 244 values, with matching months and source hashes.
- The price CSV agrees with the source metadata; all four CPI snapshots match their recorded hashes.
- The most recent automated cold-run hashes match the saved report and JSON results.
- The existing [verification log](../outputs/Verification.txt) records 11 passing tests. Its code covers numerical estimates/search, failure behavior, source integrity, app controls and isolated execution. This rubric audit does not represent that run as a fresh dependency installation or user study.
- The price sample contains 60 monthly returns. That supplies only one complete five-year window, insufficient to demonstrate robustness across rolling five-year periods. A 36-month sensitivity is a different estimation window, not out-of-sample validation.

No source data was refreshed, no new student experiment was run and no financial policy was changed. Rendering used PyMuPDF because Poppler was unavailable; all six pages were visually inspected. Existing tests cannot establish future returns, economic suitability or the student's understanding.

## Revision order

1. **Define and defend the mandate.** Review the intended decision, goal, benchmark, payout assumptions, reserve treatment and risk/cost limits. Keep the portfolio unnamed. Record the student's reasons in ordinary language.
2. **Match the financial evidence to the claim.** Decide which historical outcome/payout checks can be supported by available data and how limitations affect the recommendation. Do not describe an in-sample replay as a validated investment strategy. A justified pilot or reject is permitted, but disclosure alone does not guarantee a high rubric level.
3. **Document personal review and an AI-output check.** Identify the exact claim or calculation, the independent evidence used, the result and any correction. Review the decision code and recommendation.
4. **Publish the development repository, then complete the human experiment.** The AI-off prediction must be committed and pushed before the changed case runs. Preserve the prediction and both outputs; record predicted and actual effects on the decision, including no change.
5. **Confirm reproducibility.** Preserve the automated isolated run and verify that the published README and repository reproduce the saved result.
6. **Finish communication and delivery.** Add truthful ownership statements, reconcile documents/results, record the three videos with corrected timestamped transcripts, freeze evidence, verify access and submit the required files by November 23 at 11:59 p.m. in Brightspace's timezone.

Use this review as the standard for later revisions: identify the criterion affected, add real evidence, update the recommendation when warranted, and close a pending item only when the activity has occurred.
