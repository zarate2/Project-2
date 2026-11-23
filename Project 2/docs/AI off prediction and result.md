## Prediction — preserve as provided
11/22 at 10:50PM
> Baseline inputs: target above the Treasury rate 3.5%; estimation window 60 months; VTI expected return shift 0 percentage points; additional annual cost 0.25%; annual volatility limit 12%; maximum U.S. equity allocation 100%.
>
> With these inputs, the model shows an allocation of 40% BIL and 60% VTI. I will test the target above the Treasury rate. I will keep all other inputs the same and increase the target from 3.5% to 4.5%.
>
> My prediction is that a higher target return will lead the optimizer to take more modeled risk in an attempt to reach that target. I expect the BIL allocation to decrease and the VTI allocation to increase.

The student initially wrote “60 days”; this is recorded as **60 months**, matching the app's estimation-window control. Please correct this record if the actual setting was different.

## Reported observation — provided by the student
Observation at 11/22 at 10:56pm
> After entering the new target, I found my prediction to be correct. VTI increased from 60% to 70%, and BIL decreased from 40% to 30%.

These are reported model allocations, not realized investment returns. Exact run time, saved settings, before/after output files, and the result's rule verdict have not been supplied.

## Evidence needed to complete the assignment record

- Date/time and timezone when the prediction was written.
- Confirmation that the student wrote the prediction with AI assistance off.
- GitHub repository URL and immutable commit link/hash showing the prediction, baseline configuration, and before output were pushed before the changed case was run.
- Before and after configuration/output files showing only the return premium changed from 3.5% to 4.5%.
- Changed-case run time and immutable result link/hash.
- Whether the model passed the return/risk rules or remained infeasible, and the student's interpretation of that decision.

The local Project 2 folder is not currently a Git repository, so no commit or push chronology can be verified here. If the prediction was not committed and pushed before the test, do not backdate it or claim the required sequence was met; ask the instructor whether a fresh experiment is needed.
