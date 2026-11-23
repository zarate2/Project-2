# Validation and AI-use record

This record distinguishes automated development checks from the personal validation required by the assignment. Automated checks do not count as the student's human AI-off prediction.

## Automated checks

On November 22, 2026, version 0.2.0 used retained monthly adjusted prices for BIL, IEF, LQD, and VTI through October 2026 and the November 22 ALFRED vintage for DGS3MO. Under its 10% ceiling, the 60-month case was infeasible; the best estimate within the ceiling was 8.21% net at 9.50% volatility. This is retained as the earlier baseline. After the student revised the ceiling to 12%, version 0.2.1 found a feasible 60-month result: 35% BIL / 65% VTI, 8.61% estimated net return, and 10.28% estimated volatility. The 36-month sensitivity is also feasible, but neither result is independent validation.

Automated checks cover independent return/risk/grid calculations, the Treasury rate and units, source hashes and date gates, invalid configurations, stress constraints, app interactions/reset, saved-output consistency, and an isolated README run. After changing the ceiling and refreshing the current memo and outputs, `Lab 15/.venv/bin/python Project 2/support/check_results.py` ran all 8 checks successfully on November 22. The saved [`Verification.txt`](../outputs/Verification.txt) contains that latest run.

## Personal requirements — not yet complete

**AI-output check — completed by student, reported November 22, 2026.** The student checked the 4.34% three-month Treasury reference against `sources/market/DGS3MO.csv` and the 0.04 (4-percentage-point) premium against `config.json`. The calculation is `0.0434 + 0.04 = 0.0834`, or an 8.34% target. The inputs and arithmetic agree with the saved source and configuration. This validates the calculation and units; it does not establish that the target is achievable or that the rate will persist.

**Changed-input record: after-run comparison; required pre-run sequence not met.** The student confirmed that the prediction was uploaded to GitHub after the test. The prediction and reported result are preserved below as supplied, but this run does not meet the required prediction-before-run sequence.

Baseline inputs: target above Treasury rate 3.5%; estimation window 60 months; VTI expected return shift 0 percentage points; additional annual cost 0.25%; annual volatility limit 12%; maximum U.S. equity allocation 100%. The model showed 40% BIL / 60% VTI.

The student wrote: “I will test the target above the Treasury rate. I will keep all other inputs the same and increase the target from 3.5% to 4.5%. My prediction is that a higher target return will lead the optimizer to take more modeled risk in an attempt to reach that target. I expect the BIL allocation to decrease and the VTI allocation to increase.”

Reported after-run result: “After entering the new target, I found my prediction to be correct. VTI increased from 60% to 70%, and BIL decreased from 40% to 30%.”

This after-run comparison is not represented as the required locked record. Do not backdate it. The student should ask the instructor whether a fresh, student-chosen experiment can satisfy the requirement.

**Personal review and ownership: incomplete.** The student must read the mandate, output, and limitations; correct anything they do not agree with; and supply the assignment's required ownership statement in their own words.

## AI use

OpenAI GPT-6 Luna through Codex assisted with code, source processing, calculation checks, document drafting, and rubric mapping. The project does not call a model or paid-data API at runtime. AI assistance did not replace the student's responsibility to make and defend the investment decision. The older CPI/NVDA panel materials are retained as historical files and excluded from the current portfolio calculation.

## Remaining evidence

Before submission, verify the prediction's pre-run commit and attach commit-specific evidence; review and own the materials; publish the project files to GitHub; add the final video and transcript links; check the recordings against their time caps and face-visibility requirement; and upload the required artifacts and manifest to Brightspace.
