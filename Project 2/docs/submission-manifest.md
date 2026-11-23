# Project 2 requirement and submission manifest

Model version 0.2.1; documents revised November 22, 2026. Relative links below identify local files, not publication. GitHub publication, final freeze and Brightspace submission are pending. This folder currently has no Git repository.

Working assessment: [rubric review](rubric-review.md), based on the retained [Brightspace rubric](../sources/Project2-rubric.pdf). These are review references, not additional required student deliverables. The review distinguishes completed code from missing personal and publication evidence.

| Base requirement | Evidence | Baseline status |
|---|---|---|
| 1. Runnable Python web app | [README](../README.md), [app.py](../app.py), [requirements](../requirements.txt) | Implemented; automated app and isolated-run checks saved |
| 2. Mandate | [Mandate](mandate.md), [config.json](../config.json) | No named client; revised choices are proposals requiring the student's review |
| 3. Two baselines and constrained portfolio with verdicts | [Model](../model.py), [output](../outputs/visible-output.md) | Implemented; 60-month base case infeasible; modeled verdicts and separate deployment gate |
| 4. Point-in-time signal and card | [Market data gate](../market_data.py), [data card](data-card.md) | Dated Treasury signal implemented; full strategy validation pending |
| 5. Estimate/window/cost/constraint stresses and stop | [Results](../outputs/results.json), [visible report](../outputs/visible-output.md) | Implemented; 36-month sensitivity passes but is not validation; no automatic relaxation |
| 6. Locked Changed-Input Record | [After-run comparison](AI%20off%20prediction%20and%20result.md) | Supplied prediction was uploaded after the run; does not meet the required pre-run commit sequence |
| 7. Recommendation, range and monitors | [Memo](decision-memo.md) | Reject base allocation as infeasible; zero capital authorization; personal decision review pending |
| 8. Opening AI/ownership and education statements | [README](../README.md), [memo](decision-memo.md) | AI and education disclosures included; personal ownership statement and videos pending |

| Submission item | Location/status |
|---|---|
| Repository URL and frozen evidence commit | PENDING — not supplied or published; record full commit SHA and commit-specific links |
| Decision memo | [docs/decision-memo.md](decision-memo.md); final GitHub link pending |
| Validation/AI-use record | [docs/validation-and-ai-use.md](validation-and-ai-use.md); final GitHub link pending |
| Human locked record and before/after evidence | Current comparison was uploaded after the run and does not meet the required sequence; ask instructor about a fresh test |
| Visible output | [outputs/visible-output.md](../outputs/visible-output.md) |
| Full settings/results and source provenance | [config.json](../config.json), [results.json](../outputs/results.json), [data card](data-card.md); final GitHub links pending |
| Verification and startup evidence | [Verification.txt](../outputs/Verification.txt), [cold-run record](cold-run.md); recorded automated baseline checks only |
| Video 1 — evolution and checked AI output; ≤3:00 | YouTube URL, title, measured duration, timestamp index and face visibility check pending |
| Video 2 — code walkthrough; ≤5:00 | YouTube URL, title, measured duration, timestamp index and face visibility check pending |
| Video 3 — committee case opening with live app; ≤5:00 | YouTube URL, title, measured duration, timestamp index and face visibility check pending |
| Transcript draft 1 | `docs/transcript-video-1.txt` — present; correct against final video, especially figures that differ from current app; GitHub URL pending |
| Transcript draft 2 | `docs/transcript-video-2.txt` — present; verify wording against final video; GitHub URL pending |
| Transcript draft 3 | `docs/transcript-video-3.txt` — present; verify wording against final video; GitHub URL pending |
| Video access and transcript checks | Not performed; no scripts or placeholders counted as recorded videos |
| This manifest | `docs/submission-manifest.md`; final GitHub URL and Brightspace attachment pending |
| Brightspace due date | November 23, 2026, 11:59 p.m., reported by the student; timezone not specified |
| Brightspace submission time and receipt | PENDING — no upload claimed |

Once published, replace pending locations with actual stable GitHub links, except videos which use YouTube URLs. Preserve a commit-specific link to each final evidence file. A later manifest commit can point to the frozen evidence commit; do not try to embed a commit's own hash inside itself.

## Final checks

- [x] Student confirmed the Project 2 assignment Markdown controls requirements and supplied the deadline; use Brightspace's displayed timezone.
- [ ] Complete student review and the required ownership statements in the README, memo and each video.
- [ ] Include the genuine locked prediction, before/after outputs and dated commits in the validation attachment; retain the original prediction unchanged.
- [ ] Confirm the app starts from the published README and record the final repository commit.
- [ ] Confirm memo, visible output, validation and recordings agree on dates, assumptions, numbers and recommendation.
- [ ] Check all three video lengths, visible face, required openings, corrected captions and timestamped transcripts using the [video checklist](video-checklist.md).
- [ ] Verify instructional-team repository access and logged-out access to every YouTube video; record checker and check time below.
- [ ] Inspect the final package for credentials/private data, then commit and push it. Record the frozen evidence SHA and final links.
- [ ] Attach the same final `decision-memo.md` and `validation-and-ai-use.md` files to Brightspace, with this manifest. Attach the three corrected transcripts or provide their repository links. Include all required supporting evidence through the manifest.
- [ ] Reopen the uploaded files/links, verify the selected versions and save the submission receipt.

Access checker/date/time: PENDING. Frozen evidence SHA: PENDING. Manifest commit/link: PENDING. Brightspace receipt location: PENDING.

The [course checklist](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/projects/major-project-student-checklist.md), checked November 22, says Project 2 does not submit Edition A/B or Research-Evolution. The [provided assignment](../sources/Assignment.md) remains the scope reference. The baseline archive is for comparison and cannot substitute for the human locked record.
