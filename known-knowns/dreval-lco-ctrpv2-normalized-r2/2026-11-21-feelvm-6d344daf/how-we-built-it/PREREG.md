# PREREG — dreval-lco-ctrpv2-normalized-r2

Frozen 2026-11-21T01:50Z (date -u) BEFORE any attack output exists. No attack code has been scored yet.

## Criterion (verbatim from bank/targets.json)

[Success means a new model, implemented as a drevalpy model class, run through drevalpy's own pipeline on the same dataset and test mode as the public report (CTRPv2, test_mode=LCO, the same number of CV splits as the report's run, lnIC50 response, the package's own split generation with the report's seed/configuration), whose mean normalized R^2 across the CV splits, computed by drevalpy's own evaluation code, is STRICTLY HIGHER (direction: max) than the maximum normalized R^2 over ALL models in https://dilis-lab.github.io/drevalpy-report/heatmaps/heatmap_algorithms_LCO_normalized.html, re-fetched and re-decoded live immediately before claiming, by at least 0.02 absolute AND by at least 2x the across-split standard error of the attacker's own result, while not being worse than the live best normalized Pearson by more than 0.01. ... same-splits RandomForest re-run requirement ... both must be beaten ... hyperparameters only on inner validation partitions ... leaderboard Pearson constraint ...]

(Full text in target.md; copied verbatim there and in claim/ at claim time.)

## Frozen statistic and thresholds

1. Run protocol: drevalpy==1.6.0 (pip), dataset CTRPv2 (Zenodo record 23159774 file CTRPv2.zip, the dataset the package loader fetches), test_mode=LCO, n_cv_splits=10, response lnIC50, drevalpy's own split generation with the package default seed/config of that version. Attacker and RandomForest baseline run in the SAME venv on the SAME generated splits.
2. Primary statistic: mean over the 10 CV splits of normalized R^2 as written by drevalpy's own evaluation code (evaluation_results.csv rows of the model, test_mode LCO), cross-validated by an independent recomputation from true_vs_pred.csv minus the pipeline's NaiveMeanEffectsPredictor predictions. The two must agree to <1e-6 or the claim dies.
3. R2 win: attacker_mean_normR2 >= LIVE_MAX_normR2 + 0.02 AND >= 2x SE, where SE = sample std (ddof=1) of the attacker's 10 per-split normalized R^2 values / sqrt(10). LIVE_MAX_normR2 = max over all models in the live heatmap re-decoded at claim time (today: 0.185180).
4. RandomForest re-run rule: reproduce RF on the same env+splits. If |ourRF_mean_normR2 - 0.1852| <= 0.02, the live-bar comparison stands alone; if the difference exceeds 0.02, the attacker must ALSO satisfy the same margins (0.02 absolute AND 2x SE) against ourRF_mean_normR2.
5. Pearson constraint: attacker mean normalized Pearson (same protocol) >= 0.4247 (= 0.4347 - 0.01, bank-recorded report best; live report tables 404 as of 2026-11-21, corroborated by paper "0.43") AND >= live leaderboard max normalized Pearson re-read at claim time (today: 0.376 EnsembleMF, from leaderboard_light.png re-fetched at claim time).
6. p2 partial (named): attacker mean normalized Pearson >= 0.4447 AND mean normalized Spearman >= 0.4383 AND mean normalized R^2 >= 0.175180 (live best - 0.01), all under the same protocol.
7. p1 partial (named): same criterion in LTO: attacker mean normalized R^2 >= 0.092794 (live LTO max 0.072794 + 0.02) AND >= 2x SE, with same-splits LTO RF re-run.
8. Leakage audit (mandatory before any claim): test-fold cell lines never in that split's training data; no scaler/PCA/gene-filter/variance-selection fitted on data including test-fold cell lines; hyperparameters selected only via drevalpy's inner validation partitions (early stopping or validation split provided by the package); no test-fold prediction touched before final evaluation.
9. Honesty guardrails: no touching of drevalpy evaluation code; the attacker model class may use only training-fold data at fit time (package API enforces fit(train; validation)); all model classes saved as source in claim/.

null_test: not needed because the claim is an explicit benchmark score checked by a deterministic checker (drevalpy's own evaluation plus an independent recomputation from written CSVs) against a live table value re-read at claim time — not a search, key, period, language or "beats chance" claim. (Optional non-frozen audit: permutation of attacker predictions vs truth within split, reported if run.)

## Re-verification cadence

Re-decode the live heatmap + leaderboard image immediately before any claim (rule 8 of LESSONS; criterion says "re-fetched ... immediately before claiming").
