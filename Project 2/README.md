# Project 2 — Investment Management Application

I used **OpenAI GPT-6 Luna through Codex** to help develop, modify, and produce this financial application. I reviewed and agree with the analysis and recommendation; the analysis and decision are mine. **For education, not investment advice.**

**Model version 0.2.1.** This is an unnamed educational portfolio research tool. It compares two simple baselines, a 60/40 benchmark, and the lowest-volatility allocation that meets the proposed return and risk rules. It does not place trades.

## Start the app

From this folder, install the dependencies once:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Run the app:

```sh
.venv/bin/python -m streamlit run app.py
```

Open the local address Streamlit prints. In the existing course workspace, the installed environment can launch it with:

```sh
"Lab 15/.venv/bin/python" -m streamlit run "Project 2/app.py" --server.port 8522
```

The app uses retained data and does not fetch live prices. The controls change the risk premium, estimation window, cost, risk ceiling, and stress assumptions. The reset control restores the configured base case.

## Current research result

The proposed policy uses a seven-year horizon, no scheduled withdrawals, BIL/IEF/LQD/VTI, a 60% VTI / 20% IEF / 20% LQD benchmark, a 4-percentage-point premium over the dated 3-month Treasury reference, and a 12% annualized-volatility ceiling. These are proposed educational assumptions, not approved client instructions.

For the proposed November 23, 2026 decision, the reference is 4.34%, making the net annual estimate hurdle 8.34%. With a 12% ceiling, the 60-month screen finds a 35% BIL / 65% VTI portfolio at 8.61% estimated net return and 10.28% estimated volatility. This is a historical estimate, not a forecast or validated strategy; the app authorizes no capital. The 36-month sensitivity finds a different feasible portfolio and is not independent validation.

## Intended user, repository map, and sources

The intended user is a portfolio analyst presenting a research decision to an investment committee. The app supports a decision to pilot or reject a proposed portfolio process; it does not authorize trades.

- `app.py` builds the interactive interface.
- `model.py` calculates estimates, compares portfolios, applies the mandate rules, and runs sensitivities.
- `market_data.py` checks the retained price files, Treasury vintage, dates, and source hashes.
- `config.json` contains the proposed mandate inputs; `run.py` produces the saved text and JSON reports.
- `sources/market/manifest.json` identifies the retained Yahoo Finance monthly adjusted-price responses and the ALFRED DGS3MO Treasury snapshot, with dates, URLs, units, and hashes.
- `outputs/visible-output.md` and `outputs/results.json` contain the executed base case and stress results.
- `docs/` contains the decision memo, mandate, data card, validation record, and submission checklist.

## Known limits

The annual return figures are historical arithmetic estimates, not a seven-year forecast or a validated investment strategy. The app uses one retrieved price history, a proposed additional cost, and a 5-percentage-point allocation grid. It does not establish realized performance, drawdowns, liquidity, turnover, taxes, or actual implementation costs. The Treasury rate is short term and may change. Check data-provider terms before redistributing raw source files publicly.

## Reproduce and check

From this folder:

```sh
python3 run.py
```

The command updates [`outputs/visible-output.md`](outputs/visible-output.md) and [`outputs/results.json`](outputs/results.json). Run automated checks with the course environment:

```sh
"../Lab 15/.venv/bin/python" support/check_results.py
```

The checks compare calculations against independent numerical calculations, verify source integrity and date gates, exercise app controls, and reproduce the run in an isolated copy. They do not fulfill the human AI-off prediction requirement.

## Assignment records

- [Decision memo](docs/decision-memo.md)
- [Mandate](docs/mandate.md)
- [Data card](docs/data-card.md)
- [Validation and AI-use record](docs/validation-and-ai-use.md)
- [Rubric review](docs/rubric-review.md)
- [Submission manifest](docs/submission-manifest.md)
- [Prediction draft](docs/AI-off-prediction.md) and [reported result](docs/AI-off-result.md)
- [Student review guide](docs/student-review.md)
- [Video checklist](docs/video-checklist.md)

The student's stated deadline is November 23, 2026 at 11:59 p.m. A student-supplied prediction and result are recorded; verify the pre-run GitHub commit chronology and supporting output before describing it as a locked record. Final transcript corrections, video links, and Brightspace upload remain outstanding.
