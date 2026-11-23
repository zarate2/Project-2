# Project 2 in plain language

Build a small portfolio app and use evidence to decide whether its selection process should be used, tested further, or rejected. The assignment requires an app, portfolio rules, two simple baselines, a constrained portfolio, one dated signal, stress tests, a recommendation, and your own prediction written before one changed-input run. There is no named client in the assignment. No corporate valuation is part of this project.

Your deadline is November 23, 2026 at 11:59 p.m., as reported by you. Use Brightspace's timezone.

## What the current app says

The proposed mandate seeks a net estimate four percentage points above the dated 3-month Treasury rate. It uses a seven-year planning horizon, no scheduled withdrawals, U.S. stocks and Treasury/corporate bonds, a 60/40 comparison, and a 12% annualized-volatility ceiling. It chooses the lowest estimated volatility among allocations that meet the target and ceiling.

The current reference is 4.34%, so the target is 8.34%. With a 60-month estimation window and 12% risk limit, the model finds 35% BIL / 65% VTI, with an estimated 8.61% net return and 10.28% volatility. This is a model-selected research mix, not an approved investment. A 36-month window also passes but uses different historical estimates; it is not proof that the process works.

## Walk through the app

The app is open in Chrome at **http://127.0.0.1:8522**. Work through it in this order:

1. Leave the sidebar defaults as they are and note the 4-point premium, 60-month window, 0.25% additional cost, and 12% risk limit.
2. In **Portfolio & mandate**, read the decision banner. Check the Treasury reference, net target, volatility limit, and best net estimate. The short Treasury rate may change; it is not locked in for seven years.
3. Scroll within the page to **Same assumptions, four portfolios**. Compare equal weight, inverse volatility, the 60/40 benchmark, and the constrained result. Read each modeled pass/fail reason.
4. Open **Treasury signal**. Confirm the observed date, ALFRED vintage, and the formula adding the premium. The data card explains units and source timing.
5. Open **Stress tests**. The default scenario table already shows a shorter-window case passing and the other stresses stopping. This is useful for understanding sensitivity; it is not your unseen prediction.
6. Open **How to use & limits**. Review what the model leaves unvalidated.
7. Use **Reset to saved assumptions** if you change any control. Controls recalculate immediately, so do not run your required new experiment before its AI-off prediction is committed and pushed to GitHub.

This walkthrough is practice. You can inspect the built-in stress results without entering a new value. Tell the assistant which label or calculation you want explained before making a new change.

## Your personal prediction and test

After development is complete and you create the repository, choose one new input change yourself. With AI off, record the old and new values with units, what you expect to happen to the return/risk result and decision, and why. Commit and push that prediction before entering the changed value. Save the resulting output separately and write whether your prediction matched. Preserve your original prediction unchanged. Do not use a known stress case as if it were unseen.

## What remains for submission

Create and push the repository; verify the human prediction-before-run record; review and own the analysis; rerun the checks; correct the transcripts against the three videos and confirm their time caps and face visibility; then upload the required documents and manifest to Brightspace. The [submission manifest](submission-manifest.md) tracks the artifacts. Do not claim an upload, prediction, or personal review until it happens.

AI disclosure: OpenAI Codex helped develop and explain the app. The student must review the final decision and take responsibility for it.
