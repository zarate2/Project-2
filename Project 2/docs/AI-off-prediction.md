# AI-Off Changed-Input Prediction

Baseline inputs: target above the Treasury rate 3.5%; estimation window 60 months; VTI expected return shift 0 percentage points; additional annual cost 0.25%; annual volatility limit 12%; maximum U.S. equity allocation 100%.

With these inputs, the model shows an allocation of 40% BIL and 60% VTI. I will test the target above the Treasury rate. I will keep all other inputs the same and increase the target from 3.5% to 4.5%.

My prediction is that a higher target return will lead the optimizer to take more modeled risk in an attempt to reach that target. I expect the BIL allocation to decrease and the VTI allocation to increase.
