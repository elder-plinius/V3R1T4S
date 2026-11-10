# CRITERION verdict

context: subagent

## Success criterion (verbatim from claim.md)

"For a named dataset D among the 12 SRBench 2025 black-box datasets: a symbolic
regression procedure run on each of the 30 splits used in results.feather
(train_test_split with train_size 0.75 and random_state equal to each listed
seed, as in experiment/evaluate_model.py on the srbench_2025 branch, including
its training subsampling rule) that returns one closed-form expression per
split, such that (a) the median test R^2 over the 30 splits is STRICTLY GREATER
(direction: max) than the highest median r2_test of any algorithm for D in
https://github.com/cavalab/srbench/tree/srbench_2025/results/black-box-tuning
(results.feather, re-fetched live immediately before claiming), and (b) the
median complexity of the 30 expressions, computed with SRBench's own
symbolic_utils.complexity, is less than or equal to that leading algorithm's
median model_size. The procedure must be fixed before scoring (no per-split
hand edits)."

Dataset: 1028_SWD. Bar per table_record.txt: median test R^2 > 0.3800
(PS-Tree) and median complexity <= 3270.

## What I checked (independent checker written from the criterion, before reading check_srbench.py)

- **Bar recomputed from data/results.feather (all 28 algorithms):** PS-Tree is
  the leader, median r2_test = 0.3800, median model_size = 3270 (n = 30).
  Runner-up EQL 0.3736 / size 59. No algorithm exceeds 0.3800. The bar in
  table_record.txt matches exactly. (One wrinkle: E2E has only 24 rows, not 30,
  but its median r2_test is -0.0012, so it cannot affect the leader.)
- **File integrity:** sha256 of data/results.feather and data/1028_SWD.tsv.gz
  both match table_record.txt. Dataset is 1,000 rows, 10 features (In1..In10),
  target in {2, 3, 4, 5}.
- **Seeds:** the 30 seeds in expressions.json are exactly the 30 random_state
  values in the table for 1028_SWD (769..32157), all unique.
- **Split convention validated against the table itself:** re-scoring recorded
  EQL expressions on train_test_split(train_size=0.75, random_state=seed) with
  train-standardized X and y reproduces their recorded r2_test to <= 0.0001
  (seeds 769, 860, 1685). The split definition is therefore the table's own.
  (The 1,000-row dataset means the training subsampling rule never triggers:
  750 train rows.)
- **Independent re-score of all 30 claimed expressions** (own parser, SRBench's
  symbolic_utils.complexity from data/symbolic_utils.py, test split only):
  every per-split R^2 and complexity reproduced to < 1e-3 of the values in
  expressions.json. Median test R^2 = 0.3911, median complexity = 75.5.
  (claim.md states 0.3910; the 0.0001 gap is the coefficient-rounding artifact
  already disclosed in REPRODUCE.md. Either value clears the bar.)
- **(a) 0.3911 > 0.3800, strictly: PASS. (b) 75.5 <= 3270: PASS.**
- **Closed forms:** all 30 expressions are genuine closed forms — exactly 12
  terms each, built only from +, -, *, /, powers, log, sqrt, Max(0, 2-x)
  hinges and a constant. No lookup tables, no array literals, no Piecewise,
  no hundreds of branches. Complexities 66–86. Read in full; the structure is
  uniform across splits.
- **Null model:** constant train-mean predictor scores median test R^2 =
  -0.0027 (chance level ~0). The claimed 0.3911 is far above null, so the null
  comparison is meaningful as a sanity check — but the binding comparison is
  against PS-Tree, where the margin is narrow: +0.0111 on the median, with
  18/30 splits above 0.3800 and per-split R^2 ranging 0.229–0.466. The win is
  real under the literal criterion but not a wide one.
- **No subsumption:** no table algorithm reaches median R^2 0.3911; EQL is
  smaller (median size 59) but lower on R^2 (0.3736). The criterion requires
  beating the leader on R^2 at no more than the leader's size, which holds.
- **No stretched definitions found:** "complexity" is SRBench's own
  symbolic_utils.complexity as the criterion requires; the median is over
  exactly the 30 listed seeds; R^2 is on the test split (verified by
  re-scoring test indices only); the leader is the highest median r2_test over
  all algorithms in the table.

## Limitation (stated, not a failure)

The "procedure fixed before scoring / no per-split hand edits" limb cannot be
directly audited from claim/ alone — the folder contains no procedure code,
and I read nothing outside it. The supporting evidence is the structural
uniformity of the 30 expressions (identical 12-term dictionary form, varying
only as a refit would vary) with no sign of hand editing. This verdict
confirms the scored outcome; it does not independently re-run the procedure.

confirmed_scope: A fixed-form symbolic regression procedure on PMLB dataset 1028_SWD returns one 12-term closed-form expression per split for the 30 listed splits, with median test R^2 0.3911 (strictly above the PS-Tree table leader's 0.3800) and median SRBench complexity 75.5 (at or below the leader's median model_size 3270).

pass: true
