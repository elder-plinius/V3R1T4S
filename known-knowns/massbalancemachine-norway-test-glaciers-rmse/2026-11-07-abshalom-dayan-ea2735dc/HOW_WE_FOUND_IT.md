# How we found it

(contributor text, unverified)

The brief was a small model (at most 20 fitted parameters) with winter RMSE at most 0.59 m w.e. on the 14 withheld
Norwegian glaciers of Sjursen et al. 2025. Winter balance is mostly accumulated snow, so the candidates were monthly
predictors built from the shipped ERA5-Land fields: precipitation, solid precipitation (precipitation in months whose
stake-level temperature, by a fixed 0.0065 K/m lapse rate, is under 1.0 C), positive degree days, and their products
with the climate-cell-minus-stake altitude difference. A glacier-grouped 6-fold CV over all 1471 subsets of up to 4 of
14 predictors (plus an intercept) picked solid precipitation and its altitude product. The model was frozen and then
scored once on the test set. Larger linear sets overfit across glaciers.
