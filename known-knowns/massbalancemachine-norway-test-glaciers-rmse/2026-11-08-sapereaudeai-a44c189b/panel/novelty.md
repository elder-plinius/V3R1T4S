# NOVELTY skeptic report: massbalancemachine-norway-test-glaciers-rmse, partial win p3

context: subagent (Claude Code Agent tool, fresh context)

Claim judged: `claim/CLAIM.md`. An independent re-implementation (own record building from the shipped wide CSV, own split by the 14 test BREIDs, own aggregated objective, own training call, own scorer; shared: xgboost 3.2.0, MBM's selected hyperparameters, base_score 0.5, feature names, shipped data) gives test RMSEs Ba 0.9962 (n 1065), Bw 0.5881 (n 999), Bs 0.7001 (n 1028). The claim is p3 only.

## 1. Status source (one plain fetch, no retry)

- URL: https://github.com/khsjursen/ML_MB_Norway
- Fetched: Sun Nov 8 17:38:59 UTC 2026 (request start, from `date -u`; finished 17:39:00 UTC). Command: `timeout 40 curl -sS -A "V3R1T4S panel"`.
- HTTP 200, 218591 bytes, sha256 1ed70449494abbce7997621ff3798f6228a789ee22bcadce0011de11130e6b9a.
- Value read: head commit `32d8175adab27963c6ca2766f2420f24cdb72a6b` ("currentOid" in the page), 403 commits, `"releaseCount":1`. This is the same head commit the claim recorded at 17:30:39 UTC, so nothing new has been posted. The front page prints no RMSE. The published values are notebook `src/3.1.1_ML_model_performance_test.ipynb`, cell 36, at that commit. The claim's copy (`claim/data/3.1.1_ML_model_performance_test.ipynb`, sha256 b6226ca7ba52e5c42d3aad2d6bde514bce62c56c545c5f833b2d54d2010599ad) gives, read locally:
  - "Mass Balance Machine - Ba: RMSE=1.00, MSE=0.99, MAE=0.77, Bias=-0.01, R²=0.64, Count=1065"
  - "Mass Balance Machine - Bw: RMSE=0.59, MSE=0.35, MAE=0.46, Bias=-0.01, R²=0.66, Count=999"
  - "Mass Balance Machine - Bs: RMSE=0.70, MSE=0.49, MAE=0.54, Bias=0.04, R²=0.72, Count=1028"

  PR #1022's record gives the same sha256 for its own raw fetch of that notebook from main at 2026-11-08T16:46:59Z, so the copy matches the published file.
- Release check (the tree can lag its releases): `gh api repos/khsjursen/ML_MB_Norway/releases` lists one release, tag `v.1.0.0`, published 2025-03-13T20:11:44Z, with no assets and an empty body, so it holds nothing beyond the tree. There are two forks (whigg, lsetiawan), and neither has been pushed since it was created (pushed_at 2025-06-10, before both creation dates).

## 2. V3R1T4S repository (github.com/elder-plinius/V3R1T4S), read-only via `gh`

Pull requests, all states. Searches run: "massbalancemachine", "ML_MB_Norway", "MassBalanceMachine", "mass balance", "glacier", "Norway", "Sjursen", "MBM", "xgboost", "norway-test-glaciers", "stake", "Sjursen 2025", plus "in:body" versions of the first two. They return only two PRs:
- **#1022** (open, another contributor, created 2026-11-08T17:04:00Z): "[claim] massbalancemachine-norway-test-glaciers-rmse: 3-parameter linear winter model, Bw RMSE 0.5239 on the 14 test glaciers (partial win p2, bar 0.59)". https://github.com/elder-plinius/V3R1T4S/pull/1022
- **#1023** (open draft, the workspace owner's own PR, created 2026-11-08T17:24:20Z): "bank: ... three pitfalls". It changes only `bank/targets.json`. https://github.com/elder-plinius/V3R1T4S/pull/1023

The 40 most recent PRs (#981 to #1023) contain no other PR on this target. Issues, all states, searched for "massbalancemachine", "ML_MB_Norway", "glacier", "mass balance", "MBM", "Norway", "xgboost" and "in:body ML_MB_Norway": no issue on this target. #1021 is a kit issue about concurrent runs and mentions no glacier work.

On main (head 850aa9c47bdff40c45ec29daeda96967c6f3a179, 2026-11-08T14:04:40Z):
- `TROPHY_CASE.md` (31306 bytes) has no match for massbalance, ML_MB, glacier, Norway or Sjursen.
- `known-knowns/` has 31 entries and none for this target.
- `sealed-envelopes/` has no entry for this target.
- `known-unknowns/earth-and-sky/massbalancemachine-norway-test-glaciers-rmse.md` is the open hunt page. It lists p3 as open: "**p3:** Reproduce MBM's three test RMSEs within 0.01 m w.e. from the shipped CSVs with an independent re-implementation (validates the split and scorer)."
- In `bank/targets.json`, the target card reads "As of 2026-10-30 no lower RMSE on this split by a model without test-glacier observations has been found". Its verification method (verbatim) is: "Skeptic clones ML_MB_Norway, checks that the training code reads only rows whose RGIID is not among the 14 test glaciers (code read plus a run with test rows deleted from the training input), recomputes the test RMSEs with a 10-line script on the same measurement counts and compares with the notebook 3.1.1 output."
- The pinned local repo copy (commit cf68067, 2026-11-03) predates the target and has nothing on it.

### Ruling on #1022 (its files read from `refs/pull/1022/head`)

- **#1022 does not claim p3.** Its `how-we-built-it/CLAIM.md` says: "Claimed: partial win **p2** only. Not claimed: the main criterion and p1 (this model predicts winter balances only)." Its `INDEX.csv` has one row, for cell "p2 test RMSE Bw". Its PR body's "Not claimed" section also lists only the main criterion and p1. No #1022 file contains the string "p3".
- **#1022 reproduces MBM only by scoring the shipped model.** Its `how-we-built-it/baseline/command.txt` is `python3 -I -B xgb_json_walk.py ../data/src_Training_cluster_2024-10-24_10-30-28_custom_loss_best_model.json ...`. Its `how-we-built-it/code/xgb_json_walk.py` is described as "Reproduce MBM's test RMSEs (PREREG baseline) from its shipped XGBoost JSON with an own numpy tree walker". Its `baseline/output.txt` reads "MBM shipped model on test: {'Ba': 0.9962, 'n_Ba': 1065, 'Bw': 0.5881, 'n_Bw': 999, 'Bs': 0.7001, 'n_Bs': 1028}". The PR's record table lists the row "MBM reproduced from its shipped model (`how-we-built-it/baseline/`) | same | 0.9962 / 0.5881 / 0.7001".
- **#1022 has no retraining of MBM's configuration.** Its only gradient-boosting model, GBM1 (`how-we-built-it/code/gbm.py`, an own numpy GBM with MBM's aggregated objective), used a different configuration: "depth": 3, "lam": 20, n_max 500, feature set F2 (`how-we-built-it/table/run1/test_ledger_run1.tsv`). It scored 0.9305 / 0.5931 / 0.6749, which is not within 0.01 of 1.00 / 0.70 (`test_ledger_run1.tsv`). The later models MB1, BL1, BL2 and HY1 are blends or other models, not MBM's configuration.
- **A shipped-model reproduction does not pre-empt an independent re-implementation as CLAIM.md defines it.** CLAIM.md defines the re-implementation as "own record building ..., own split by the 14 test BREIDs, own aggregated-MSE objective, own training call and own scorer". Scoring the authors' trained booster re-implements inference and scoring only. It cannot show which rows the model was trained on, so it does not validate the split that p3's own words name ("validates the split and scorer"). It also cannot carry the bank's verification step "a run with test rows deleted from the training input", which needs a training run. Of the "trivial edits" listed in the kit, re-scoring the published booster is the nearest one (a re-evaluation of a published object). It gives the same three numbers, but it is not an object that satisfies p3. The claim's object, a booster retrained from the wide CSV with own code, is not obtainable from the shipped booster by deletion, restriction, relabelling or polish. `claim/supporting/lens2_output.txt` line 3 shows the retrained trees are not a copy: "trees with identical text dump: 1 of 300 (ours 300)". In `claim/code/reimpl_p3.py`, the shipped booster is loaded (line 200) only after the primary score is printed, for secondary check (b).
- **Ruling: #1022 does not cover p3, and its shipped-model baseline does not pre-empt this claim.**

### Ruling on #1023 and the owner's own prior run

#1023 is the claimant's own draft and makes no claim. Its body says: "The run reproduced MBM's numbers (0.9962 / 0.5881 / 0.7001, n = 1065 / 999 / 1028) with the shipped booster, and again with its own retraining of MBM's configuration. That meets p3's wording, but the result is single-context and unpanelled, and we make no claim on it here." This is the same identity's earlier disclosure, which PREREG.md also states: "Run 2026-11-08-1646 already saw 0.9962 / 0.5881 / 0.7001 from a retrain with the same configuration". It is not prior coverage by a third party, so it does not pre-empt the claim.

## 3. Literature and public code, last 24 months (Nov 2024 to Nov 2026)

Web searches (WebSearch, 4 queries): reproductions or re-implementations of MBM on the Norway test glaciers, MassBalanceMachine Norway 14 test glaciers 2026, Sjursen 2025 benchmark follow-ups, the published values 1.00 / 0.59 / 0.70 together with "reproduced", and EGU26 transfer learning with MBM in Norway or Scandinavia. Found:
- Sjursen et al. 2025, TC 19:5801 (https://tc.copernicus.org/articles/19/5801/2025/) and its EGUsphere discussion (https://egusphere.copernicus.org/preprints/2025/egusphere-2025-1206/). This is the original, not a reproduction.
- van der Meer et al. 2026, "Glacier Mass Balance Modeling Using a Long Short-Term Memory Network", JGR MLC (https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2026JH001250). It is a Swiss LSTM study. Its only Norway figures are Sjursen et al.'s 1980-2019 subset values (0.55 winter, 0.97 annual), quoted, not reproduced. #1022's novelty file records the same reading of its full text.
- Maslov et al. 2026, GlaUnTI, TC 20:6045 (https://tc.copernicus.org/articles/20/6045/2026/). It uses a different 13-glacier European test set and restates Sjursen et al.'s annual 1.00 as a citation.

None of these re-implements MBM's training and reports its own test RMSEs on the 14 Norway glaciers.

GitHub code search (`gh search code`) for the shipped CSV name `stake_mb_norway_cleaned_ids_latlon_wattributes_climate`, for `custom_loss_best_model.json`, for `ML_MB_Norway` and for the test-list literal "54, 703, 941, 1135" finds only:
- khsjursen/ML_MB_Norway itself (the original training code, `src/2.1.2_model_training_cluster.py`);
- the V3R1T4S hunt page;
- ODINN-SciML/MassBalanceMachine (https://github.com/ODINN-SciML/MassBalanceMachine), the authors' successor framework. Its `massbalancemachine/dataloader/SourceManager.py` (`SourceManagerNorway`, last changed 2026-04-13) downloads the two shipped ML_MB_Norway monthly CSVs and hard-codes the same 14 test RGI ids. `regions/RGI_08_Norway/3.2. Train-ML-model.ipynb` trains XGBoost by random search (`n_iter=45`) on `norway_kamilla_glacierlist`.
  - All 56 cells of that notebook have no outputs (0 outputs in total), as do the Norway preprocessing notebook's 40 cells.
  - The repository has no Norway test (only `tests/models/test_iceland_train.py` and `test_swiss_train.py`) and no Norway results file.
  - Its releases v0.1.0 (2025-11-10) and v0.2.0 (2026-01-26) have no assets.
  - So it publishes no reproduced Norway test RMSEs. It is also the original authors' own framework, not an independent re-implementation.

  It does not cover p3.

## 4. Comparison with the published object and neighbouring cells, and the tie clause

- p3's success condition is a match with the published values within 0.01. By construction it is a tie with MBM's numbers, not a record against them. The kit's "strictly beats everything known; a tie is not a record" therefore cannot be read for this cell as "beat 1.00 / 0.59 / 0.70". For a reproduction partial win, the novelty test is whether a published object already satisfies p3: a public, independent re-implementation, including training on the training glaciers only, that reproduces the three RMSEs within 0.01. None exists (sections 2 and 3).
- **Neighbouring cells.**
  - p2 is claimed by #1022 (Bw only) and is not touched here.
  - p1 and the main criterion are not claimed.
  - The 1980-2019 subset values (notebook 3.3, n 517) are a different cell.
- **Seeds named.** The claim names what it is seeded from: MBM's hyperparameters ("notebook 2.1.1 cell 52 output"), base_score 0.5 "from the shipped booster JSON", MBM's 11 feature names, and the shipped data. It credits Sjursen et al. 2025, the ML_MB_Norway repository, NVE and xgboost.
- **What the seeds alone give.** Re-scoring the published booster gives the same three numbers but is not a p3 object. The claim's retrain is the only public object that is.
- **Note for the other skeptics, not a novelty defect.** The retrain matches the shipped booster's RMSEs at all four printed decimals (`claim/result/primary_output.txt`, check (b)). Lens 2 reports that MBM's notebook grid and some variants do not land within 0.01 (for example tree_method exact: 1.0476 / 0.6075 / 0.7021). Whether this tolerance tells MBM's configuration apart from the others is for the criterion skeptic.

## 5. Verdict

- No V3R1T4S PR, issue, TROPHY_CASE entry, known-knowns or sealed-envelopes entry claims or covers p3. The only other claim on this target, open PR #1022, claims p2 only, and its MBM numbers come from scoring the shipped booster, which is not an independent re-implementation of training as CLAIM.md defines it and as the bank's verification method requires.
- No paper or public code from the last 24 months independently re-implements MBM and reproduces these three Norway test RMSEs.
- The status source is unchanged (head 32d8175, HTTP 200).
- p3 is new.
- Fetch log: the status page was fetched once (HTTP 200). There were no refusals, blocks or retries. Every other read was through the authenticated read-only `gh` API or the WebSearch tool.

pass: true
