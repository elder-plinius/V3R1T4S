# HOW_WE_FOUND_IT (contributor text, unverified)

The brief: beat the public best normalized R^2 / Pearson for cancer drug-response prediction
on CTRPv2 leave-cell-line-out in the drevalpy benchmark.

What failed first:
- The published RandomForest (0.1852 normalized R^2) did NOT reproduce under the pinned
  drevalpy 1.6.0's own metric (0.1060). Diagnosis (the run's main finding): the package
  changed its normalization ruler after the report - v1.3.1's NaiveMeanEffectsPredictor
  (overall + cell-line + drug effects, no tissue fallback) vs v1.6.0's (adds a tissue
  fallback for unseen cell lines) - and its split RNG (legacy np.random.seed vs
  default_rng). Under the report's ruler the RF re-run reproduces the published values to
  0.0005. The report's exact CV partition is not publicly recoverable (25-33% membership
  overlap); the partition choice turned out to be immaterial.
- A drug-mean-only residual model (ResidualOmics131) scored 0.1254 - dead: the report's
  ruler leaves tissue variance in the target, and a drug-mean base forfeits it.

What worked:
- Model the residual against the naive ruler directly, from gene expression, with all
  preprocessing fitted on training folds only (LCO-safe).
- Two complementary members averaged: (a) the package's own naive-predictor base + multi-output
  ridge (PCA / reduced-rank options tuned on validation); (b) a tissue-x-drug train-fold mean
  base + ridge (the tissue structure the report's ruler keeps in the target).
- Validation-Pearson model selection (disclosed, PREREG.v5) after RMSE selection proved
  misaligned with the normalized metrics.
- Final run att_v1ens_v2: Pearson 0.459961 / Spearman 0.443224 / R^2 0.208691 under the
  report's ruler; same-splits RF gate 0.1857 vs published 0.1852 (PASS).

Marked "contributor text, unverified" per kit/SUBMIT.md; the claim, checker and panel files
carry the verifiable content.
