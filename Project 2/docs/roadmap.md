# Next changes — working list

Revised November 22, 2026 after Project 1 feedback. The student confirmed that the [Project 2 assignment](../sources/Assignment.md) controls the requirements and requested no named client. Keep its investment-management objectives and label the numerical mandate as sample assumptions. Due November 23, 2026 at 11:59 p.m., as reported by the student; deadline timezone was not specified.

The student-supplied [rubric review](rubric-review.md) now guides the step-by-step work. Validation carries 75/300 points and financial soundness 60/300; completing artifacts must accompany evidence that tests the material claims. A working app and disclosed limitations alone do not establish the highest rubric level.

1. **Review the current 12% volatility ceiling and 4-point return premium.** The app implements the student's current mandate in version 0.2.1. The revised risk ceiling makes the 60-month base screen feasible, but independent validation, cost support, liquidity, and implementation evidence remain incomplete; the app authorizes no capital.
2. **Validate outcomes relevant to the revised mandate.** Test the Treasury-relative return and risk claims; distinguish initial allocation from rebalancing. Remove payout validation once withdrawals and their reserve rule are removed from the implementation. Retain dated inputs and avoid estimating and evaluating a strategy on the same sample without disclosure. A seven-year horizon cannot be presented as a demonstrated seven-year result from five years of prices.
3. **Model implementation.** Supply initial holdings, turnover accounting, cost estimates, liquidity evidence, rebalance timing and breach responses. Do not relabel a static weight difference as annual turnover.
4. **Challenge the process.** Stress the Treasury-relative return premium, plausible costs/constraints and estimation windows; consider an honest reject if conditions cannot be met. Retain information available at each evaluation date before claiming a historical signal backtest.
5. **Review the investor exhibit.** Decide whether it adds useful committee context. It currently raises questions about a VT holding and does not justify stock selection or ETF trading.
6. **Complete human and delivery records.** Independently review the analysis, verify that the AI-off prediction was committed before the run, record the result, record three face-visible videos within their caps, correct timestamped transcripts, and fill actual GitHub/YouTube links. Freeze the evidence and upload the required Markdown files and manifest to Brightspace. Use the [video checklist](video-checklist.md) and [submission manifest](submission-manifest.md).

For each revision, save the scenario JSON, explain the decision effect in `CHANGELOG.md`, regenerate visible output, update the memo, and run the relevant checks. The 0.1.0 ZIP remains the reference. No baseline, test output or template should be represented as the student's unassisted prediction.

Do not run a new locked-experiment scenario while its human prediction is pending. Existing stress results can support development but cannot retrospectively become an unseen prediction.
