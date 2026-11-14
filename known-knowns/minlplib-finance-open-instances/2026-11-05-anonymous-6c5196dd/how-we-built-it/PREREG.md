# PREREG (frozen 2026-11-03T19:47:14Z, from date -u, before any attack output was scored)

## Criterion (verbatim; full text in target.md)
Success criterion: "A point file in MINLPLib's text .sol format ... for saa_2 or pricing050 such that an evaluator written
independently ... reports: (a) every variable within its bounds and every binary exactly 0 or 1; (b) maximum absolute
violation over all algebraic constraints <= 1e-8 in double precision, confirmed with 50-digit mpmath; (c) an objective
... strictly better than the '=best=' value ... by more than 1e-6 * max(1, |best|). As of 2026-10-25 the bars are saa_2 <
12.1613089 (min) and pricing050 > -1813.829078 (max)."
Partial win p1: "A machine-checkable certificate that the optimum of pricing050 is at most the best known primal value
plus 1e-6 * |value|. ..."
Partial win p2: "A certified lower bound on the optimal value of saa_2 strictly above 6.02323546 ..."

## Statistics and thresholds
- S1 (pricing050, partial win p1): U = rigorous upper bound on max objvar, computed as U = -LB with
  LB = sum_k lambda_k d_k + sum_i m_i, where lambda in R^5_+ is a fixed vector of decimal numbers written to a file,
  and m_i is a rigorous lower bound (arb ball arithmetic via python-flint, interval branch-and-bound on [0,10]) of
  min_{x in [0,10]} c_i x - sum_k lambda_k a_ki x exp(-b_ki x^p_ki), with all model decimals read as exact decimals.
  PASS iff U <= -1813.829078 + 1e-6 * 1813.829078 = -1813.827264171 (bar computed with |value| = 1813.829078).
  Independent cross-check required: the same bound recomputed with mpmath.iv must also satisfy the threshold.
  Concavity part (i) is reported separately (interval proof of g'' < 0 on [0,10] for each of the 3 term types) but the
  bound in S1 does not depend on it.
- S2 (pricing050, full criterion): a point with evaluator (checker/pricing_eval.py) double and mpmath50 max violation
  <= 1e-8, bounds satisfied, and objective > -1813.829078 + 1e-6 * 1813.829078 = -1813.827264. Expected NOT to happen
  if S1 passes (S1 would forbid it beyond 1e-6 relative).
- S3 (saa_2, full criterion): a point passing an independent saa_2 evaluator (that first reproduces p4 = 12.1613089
  within 1e-7 and rejects a perturbed copy) with objective < 12.1613089 - 1e-6 * 12.1613089.
- S4 (saa_2, p2): any certified lower bound > 6.02323546 with a rerunnable certificate.

## Null design
null_test: not needed because every claim here is an explicit object (a point or a multiplier vector plus interval
enclosures) checked by a deterministic checker against the table value; no search-vs-chance statistic is claimed.

## Baseline (step 3c)
Not an empirical benchmark score. The deterministic evaluator must reproduce posted points first: pricing050 p1
(done before this file: checker/pricing_eval.py gives -1813.82907844984, max violation 7.27e-10, perturbed copies
rejected with violations 0.046 and 0.106); saa_2 p4 must be reproduced before any saa_2 claim.
