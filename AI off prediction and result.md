# AI-Off Changed-Input Prediction

## Baseline inputs

- Target above the Treasury rate: 3.5 percentage points
- Estimation window: 60 months
- VTI expected return shift: 0 percentage points
- Additional annual cost: 0.25%
- Annual volatility limit: 12%
- Maximum U.S. equity allocation: 100%

With these inputs, the model showed an allocation of 40% BIL and 60% VTI.

## Prediction

I will increase the target above the Treasury rate from 3.5 to 4.5 percentage points and keep all other inputs the same. I predict that the higher target will lead the optimizer to take more modeled risk in an attempt to reach that return. I expect the BIL allocation to decrease and the VTI allocation to increase.

## After-run result

After entering the new target, I found my prediction to be correct. VTI increased from 60% to 70%, and BIL decreased from 40% to 30%.
