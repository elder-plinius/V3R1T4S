context: subagent
# CRITERION verdict — srbench-2025-blackbox-dominate-leader, dataset 522_pm10

Method: I worked only from the claim package. I independently re-scored all 30
expressions in expressions.txt with code/check_srbench.py, recomputed the leader
and Pareto front from data/results.feather, re-ran the fixed procedure in
code/gam_sr.py on seeds 769 and 32157, and computed the constant-mean null on
all 30 splits. sha256 of data/results.feather matches table_record.txt
(5b428264a346f6bbbeabded219f87454b9206afa70c19c012075c672533f342e).

## Clause-by-clause literal check

(a) 30 splits are the listed ones: PASS. expressions.txt has exactly 30
expressions; their seeds equal the 30 distinct random_state values for
522_pm10 in data/results.feather (769..32157). code/check_srbench.py splits
with sklearn train_test_split(train_size=0.75, test_size=0.25,
random_state=seed) on the 500 rows in file order, matching
data/evaluate_model.py. Training subsampling rule: data/evaluate_model.py
subsamples only when max_train_samples > 0 (default 0); with 500 rows / 375
train rows there is no indication it applied, and the claim uses the full
375-row train, consistent with the rule as coded. (Caveat: per-algorithm run
configs are not in this package, so this is the rule as coded, not a
re-verification of SRBench's run configs.)

(b) One closed-form expression per split: PASS. Each expression is a finite
sum of 19–21 terms, each term an elementary univariate function (linear,
square, Abs, sqrt(Abs(.)), log(1+Abs(.)), hinge Max(0, x-q) / Max(0, q-x),
sin/cos of hour_of_day and day only) with a fitted scalar coefficient plus
one intercept. No lookup tables, no numeric array literals, no hundreds of
piecewise branches; at most 3 terms per feature shape as preregistered.

(c) Median test R2 STRICTLY GREATER than the live leader: PASS. Recomputed
median test R2 over the 30 splits = 0.331263 (range 0.167275–0.407556; every
saved per-split R2 and complexity in expressions.txt reproduced exactly).
Recomputed leader from data/results.feather: PS-Tree, median r2_test =
0.300852 over its 30 rows, median model_size = 4996.5 (0 rows with
model_size -1). 0.331263 > 0.300852, strict, margin +0.030411. Next best
algorithm QLattice is 0.276510, so no other algorithm's median exceeds the
claim either.

(d) Median complexity <= leader's median model size: PASS. Recomputed median
complexity via SRBench's own symbolic_utils.complexity = 145.5, and 145.5 <=
4996.5 (2.9% of the leader's size). On the "median" reading: the 30
complexities are integers sorted [134, 135, 137, 137, 137, 138, 142, 142, 143,
143, 143, 144, 144, 145, 145, 146, 147, 147, 148, 148, 149, 149, 150, 150, 151,
152, 152, 152, 154, 155]; the 15th is 145 and the 16th is 146, so the standard
median is their average, 145.5. This is the right reading: the leader's own
median model size 4996.5 is computed under the identical even-sample
convention, so the comparison is like-for-like.

(e) Procedure fixed before scoring, no per-split hand edits: PASS on the
evidence in the package. code/gam_sr.py is a single deterministic procedure
(module-level constants: 8 backfitting rounds, 20 quantile bins, 3 smoothing
passes, 60-point grid, <=3 terms per shape, joint OLS refit); it contains no
seed-conditional branches and no per-split edits. Re-running it reproduced
the saved expressions character-for-character on both seeds tested (769:
R2 0.313793, cx 147; 32157: R2 0.364998, cx 137). Fitting uses train only
(backfitting, compression grid, quartiles, OLS refit); test data is touched
only to build the design matrix for an internal R2 consistency warning and
for the checker's scoring — it never enters term selection or coefficients.
PREREG.md is timestamped 2026-11-13 06:05 UTC, before scoring; within-package
evidence only, but the code determinism corroborates it.

(f) Partial win p1 (fallback): ALSO MET. Recomputed Pareto front for
522_pm10: (0.3009, 4996.5), (0.2765, 35), (0.2342, 30), (0.1932, 20.5),
(0.1758, 9.5), (0.1204, 3), (-0.0040, 1). Claim point (0.3313, 145.5) is
dominated by no algorithm's point (no algorithm has both R2 > 0.3313 and
size < 145.5) and strictly dominates the front point PS-Tree (0.3009, 4996.5).

(g) Null model: PASS with a wide margin. Constant-mean predictor (train mean)
scored on the same 30 splits gives median test R2 = -0.004441 (range
-0.041148 to -0.000166), i.e. chance level is ~0 as preregistered; the claim
beats it by 0.335704. No search-over-chance concern applies: the claim is 30
explicit expressions checked deterministically, not a selected statistic.

## Hunted stretches — none found
- "closed-form expression": not stretched; the expressions are closed-form
  sums of elementary functions, and the hinge terms are single Max(0, .)
  atoms, not a binned lookup.
- "fixed procedure": not stretched; one code path for all splits, no
  test-R2-driven selection anywhere (selection uses train-only inner
  quantities; the PREREG lens-1 beam search is not the procedure used here).
- "median": not stretched; standard even-sample median, applied identically
  to both sides of clause (d).
- Minor non-issue: algorithm E2E has 29 rows in the table instead of 30;
  it is not the leader and does not affect the bar.

confirmed_scope: The fixed GAM-shape-compression procedure in code/gam_sr.py returns one closed-form expression per listed seed for dataset 522_pm10 with median test R2 0.331263, strictly above PS-Tree's live-table median 0.300852, at median complexity 145.5, at or below PS-Tree's median model size 4996.5.
pass: true
