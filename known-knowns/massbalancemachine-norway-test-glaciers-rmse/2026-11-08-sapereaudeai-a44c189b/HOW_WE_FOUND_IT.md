# How we found it (contributor text, unverified)

The goal was the bank's partial win p3: reproduce the Mass Balance Machine's three test RMSEs from the shipped CSVs
with an independent re-implementation, to validate the split and the scorer before anyone trusts a claimed gain.

A first run (2026-11-08, 16:46 UTC) scored the shipped booster with its own scorer and also retrained MBM's selected
configuration with its own pipeline; both gave 0.9962 / 0.5881 / 0.7001. That retrain was scored on the shipped
monthly test CSV and was never panelled.

This run froze a PREREG first (how-we-built-it/PREREG.md). It states which parts are our own code (record building
from the wide CSV, the split, the one test cleaning rule, the aggregated objective, the training call, the scorer)
and which are shared (the xgboost library, MBM's hyperparameters). The pass rule is each RMSE within 0.01 of the
notebook's printed value with the exact counts. We then rebuilt everything in one file and also rebuilt the test set
from the wide CSV.

What mattered:
- The repository drops one test winter record with balance 9.99 (notebook 2.1.1, "Remove strange value"). Without
  that rule the winter count is 1000 and Bw is 0.6529.
- The reproduction depends on xgboost's histogram method: with tree_method exact the RMSEs are 1.0476 / 0.6075 /
  0.7021, which misses.
- Our retrain differs from the shipped booster by at most 3.6e-7 per monthly prediction. It is a real retrain that
  converges to the same model (only 1 of 300 tree dumps is textually identical).
- None of the 24 configurations of MBM's own notebook grid lands within 0.01 of all three values, so the tolerance
  picks out MBM's configuration.
- Training with every test-glacier row deleted from the input gives bit-identical test predictions.

What did not count: several grid configurations score lower than MBM on Ba or Bw. We saw those scores on the test
glaciers, and none is lower on all three, so they are not claimed.
