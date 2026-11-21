# PREREG v2 — dreval-lco-ctrpv2-normalized-r2

Timestamp: 2026-11-21T03:54:46Z (date -u), BEFORE any Track B (reconstructed-splits) result exists.
Supersedes PREREG.md's run-protocol section ONLY; all win thresholds, statistics and margins are
UNCHANGED from PREREG.md (mean normalized R^2 >= live_max + 0.02 AND >= 2x across-split SE;
Pearson >= 0.4247 and >= live leaderboard max; p2/p1 thresholds unchanged).

## Why v2 (definist-lens findings, all from command output before any Track B score)

1. The public report's evaluation tables (all_results.zip in Zenodo record 17343165,
   evaluation_results.csv, file dates 2025-05-26) decode to RandomForest mean normalized R^2
   0.185180 = the live heatmap value exactly (nanmean over 10 per-split values; per-split RF
   values [0.275, 0.170, 0.202, 0.210, 0.192, 0.112, 0.110, 0.205, 0.189, 0.186], std 0.048).
   RF Pearson: normalized mean 0.434693 (bank's 0.4347) and Spearman: normalized 0.428291
   (bank's 0.4283) confirmed from the same file.
2. The report's runs used drevalpy ~v1.3.1 (release 2025-05-09; eval files 2025-05-26) and the
   CTRPv2 response CSV that is byte-identical to the pinned v1.6.0 data's response table
   (record 15481989 CTRPv2.csv sha256 7f73133d... == record 17343165 CTRPv2.csv; response
   stats identical to current: 395,024 rows, 159,050 NaN, mean 1.8633, std 2.534;
   gene_expression.csv sha256 identical across all three records).
3. v1.3.1's _leave_group_out_cv shuffles with the LEGACY global RNG (np.random.seed(42);
   np.random.permutation) and carves validation by GROUP (train_test_split over unique training
   cell lines, random_state=42). drevalpy v1.6.0 switched to np.random.default_rng(42) and
   row-level validation. Same nominal seed, DIFFERENT partitions. This is the mechanism behind
   the Track A reproduction gap (RF on v1.6.0 splits: 0.120 after 3 splits vs published 0.1852).
4. Therefore "the package's own split generation with the report's seed/configuration" (the
   bank criterion's own words) is implemented by reconstructing the v1.3.1 split sequence, which
   this track does with the package's own data and documented code (code/recreate_report_splits.py).

## Track B run protocol (the criterion-faithful comparison)

- Data: the pinned package's own CTRPv2 (Zenodo record 23159774 CTRPv2.zip), response column
  LN_IC50_curvecurator — byte-identical response content to the report's record 15481989 file.
- Splits: results/rf_v131repro/CTRPv2/LCO/splits written by code/recreate_report_splits.py
  (v1.3.1 semantics: remove NaN -> legacy np.random.seed(42) permutation -> GroupKFold(10) over
  cell lines -> per-fold group-level validation split via train_test_split(random_state=42)).
  The v1.6.0 pipeline LOADS these splits (prepare_response_splits loads existing split dirs).
- Models: RandomForest (published baseline) and the attacker classes, same venv, same splits.
- Reproduction gate (baseline reproduction, not a tuning knob): our RF re-run on these splits
  must land within +-0.02 of the published 0.1852. If it misses, the split reconstruction is
  unvalidated: no win claim may rest on Track B; the reproducibility finding (p3 shape) is
  reported instead and Track A remains the same-splits evidence.
- Evaluation: drevalpy's own per-split predictions CSVs + independent recomputation
  (code/recompute_normalized.py against code/compute_naive_preds.py's NaiveMeanEffectsPredictor
  predictions, same class and train+validation fold as the pipeline). The report's own
  per-split values (all_results/evaluation_results.csv) are the authoritative per-split record
  of the published run; the live heatmap z-decode remains the live table for the win bar.
- Leakage audit unchanged (PREREG.md item 8).

## Unchanged frozen thresholds (restated from PREREG.md; no edits)

- R2 win: attacker mean normR2 >= LIVE_MAX_normR2 + 0.02 AND >= 2x SE(10 splits). Today's live
  max 0.185180 (re-decode at claim time).
- RF re-run rule: if |ourRF_mean - 0.1852| > 0.02, attacker must ALSO beat ourRF_mean by the
  same margins. On Track B the gate is the same rule with ourRF = the Track B RF re-run.
- Pearson: attacker mean normPearson >= 0.4247 AND >= live leaderboard max (re-read at claim).
- p2: normPearson >= 0.4447 AND normSpearman >= 0.4383 AND normR2 >= 0.175180.
- p1 (LTO): separate run; bar = live LTO max + 0.02 (0.072794 + 0.02 = 0.092794 today).
- p3: same-env same-splits re-run of RF, MultiOmicsRandomForest, DIPK with > 0.02 gap + logs
  (Track A is the current-data version of this; Track B gives the v1.3.1-semantics version).

null_test: not needed because (unchanged) the claim is an explicit benchmark score checked by a
deterministic checker against a live table value re-read at claim time.
