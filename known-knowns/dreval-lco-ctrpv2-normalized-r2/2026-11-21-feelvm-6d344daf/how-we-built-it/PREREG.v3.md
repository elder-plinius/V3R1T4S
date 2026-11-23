# PREREG v3 — dreval-lco-ctrpv2-normalized-r2

Timestamp: 2026-11-21T04:49Z (date -u) BEFORE any Track B attacker score exists (Track B RF
splits 0-1 already evaluated, recorded below as gate evidence). All win thresholds unchanged
from PREREG.md/PREREG.v2.md.

## Protocol fix (definist lens, from command output)

PREREG.v2 assumed the report's exact CV partition could be reconstructed from v1.3.1 code +
seed. Verified FALSE: memberships extracted from the report's own true_vs_pred.csv
(streamed from all_results.zip; per-split test cell-line sets saved to
dreval_run/report_lco_memberships.pkl) overlap the legacy-RNG reconstruction by only
25-33% per split — the report's partition is not recoverable from public artifacts.

What IS recovered and verified:
1. RULER: the report's normalized metrics used drevalpy v1.3.1's NaiveMeanEffectsPredictor
   (overall + cell_line_effect + drug_effect; NO tissue fallback). Evidence: recomputing our
   RF predictions against the v1.3.1-ruler lands on the report's per-split values
   (split 0: ours 0.2584 vs report 0.2750; split 1: ours 0.1678 vs report 0.1696), while the
   v1.6.0 ruler gives 0.1453/0.0907 for the same predictions. RF Pearson split 1: ours 0.4110
   vs report 0.4213.
2. DATA: response table identical across report (15481989), era (17343165) and current
   (23159774) records (sha256 7f73133d... for report vs era CTRPv2.csv; response stats equal;
   gene_expression.csv sha256 identical in all three).
3. VERSION: report eval files dated 2025-05-26 -> drevalpy ~v1.3.1 (released 2025-05-09).

## Frozen Track B protocol (primary, criterion-faithful)

- Splits: drevalpy v1.3.1's own documented split algorithm (remove NaN -> legacy
  np.random.seed(42) permutation -> GroupKFold(10) over cell lines -> group-level validation
  split, train_test_split(random_state=42)), run on the pinned data. These are "the package's
  own split generation with the report's seed/configuration" under the report's package
  version. The report's exact partition being unrecoverable is disclosed; the RF baseline
  (re-run on these splits) landing at the published level validates protocol-level equivalence.
- Ruler: v1.3.1 semantics (implemented in code/compute_naive_preds_v131.py, fitted on the same
  train+validation rows the pipeline uses). Primary normalized metrics = recomputed per split
  under this ruler. The v1.6.0-ruler values (drevalpy's own report output) are co-reported.
- Baseline gate (from PREREG.v2, unchanged): Track B RF mean normalized R^2 (10 splits,
  v1.3.1 ruler) must be within +-0.02 of 0.1852; else no win claim may rest on Track B.
- Win thresholds UNCHANGED: mean normR2 >= live_max + 0.02 (live max 0.185180 today) AND >= 2x
  SE; Pearson >= 0.4247 AND >= live leaderboard max; p2/p1 as in PREREG.md. All Track B
  attacker numbers compared under the v1.3.1 ruler; the RF rule compares against the Track B
  RF re-run AND the published 0.1852 (both must be beaten, per the bank criterion).
- Track A (v1.6.0 splits + v1.6.0 ruler) continues as the current-package track; it feeds the
  reproducibility finding and the same-splits attacker-vs-RF comparison under the pinned
  package's own metric.

null_test: not needed because (unchanged) explicit benchmark score vs live table value.
