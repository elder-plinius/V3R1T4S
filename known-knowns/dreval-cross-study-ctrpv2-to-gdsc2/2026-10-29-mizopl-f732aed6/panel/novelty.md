# Skeptic 2 — Novelty & Comparator Audit (`dreval-cross-study-ctrpv2-to-gdsc2`)

- reviewer: Novelty & Comparator Skeptic (`novelty`)
- context: fresh independent skeptic review session (zero shared context)
- target_id: `dreval-cross-study-ctrpv2-to-gdsc2`
- submission_id: `2026-10-29-mizopl-f732aed6`
- internal_panel_verdict: `CONFIRMED_PARTIAL` (`partial_win: p3`)

## 1. Audit Against the Live Cross-Study Comparator Table

Checked the official cross-study HTML comparator table at <https://dilis-lab.github.io/drevalpy-report/html_tables/table_cross_study_GDSC2_LCO.html> (and Solo mirror <https://dilis-lab.github.io/drevalpy-report/all_runs/Solo/tables/table_cross_study_GDSC2_LCO.html>, `sha256 = 01d129d634be27c49c50a8a1c357135f1e1090cd8df35cd6b7687f51e69595d9`):
- Best published `MSE`: `GradientBoosting = 5.092 ± 0.374` (`RandomForest = 5.095 ± 0.139`, `NaiveMeanEffectsPredictor = 5.447 ± 0.029`).
- Best published `R^2_norm`: `GradientBoosting = -0.115 ± 0.081` (`RandomForest = -0.117 ± 0.030`, `NaiveMeanEffectsPredictor = -0.199 ± 0.005`).
- Best published `Pearson_norm`: `DIPK = 0.301 ± 0.038` (`GradientBoosting = 0.209 ± 0.061`, `SimpleNeuralNetwork = 0.178 ± 0.054`, `RandomForest = 0.123 ± 0.028`).

Because our unadjusted single-row inductive model `SchurBilinearExVivoDRP` scores `MSE = 6.38104 ± 0.11786`, `R2_norm = -0.42457 ± 0.02711`, and `Pearson_norm = +0.13294 ± 0.01253` on the 2026 CurveCurator `GDSC2.csv` splits, it does not beat the published cross-study leaderboard on unadjusted `R2_norm`, `MSE`, or `Pearson_norm`. Scoping the submission strictly to **partial win `p3`** (measured decomposition of the `CTRPv2 -> GDSC2` transfer gap by re-scoring the same predictions) is therefore honest and appropriate.

## 2. Internal Number Reconciliation

Verified that all prose files (`README.md`, `HOW_WE_FOUND_IT.md`, `the-record-we-beat/record.md`, `verify-it-yourself/RECEIPTS.md`) and `object/certificate.json` report the exact same 10-split numbers computed from the `y_pred`, `y_pred_rf`, and `y_pred_naive` columns of `object/gdsc2_split_{0..9}_{sr,yn}.csv`:
- `SchurBilinearExVivoDRP` (`y_pred`): `MSE = 6.38104 ± 0.11786`, `R2_norm = -0.42457 ± 0.02711`, `Pearson_norm = +0.13294 ± 0.01253`, `Spearman_norm = +0.17419 ± 0.00773`.
- Same-environment `RandomForest` (`y_pred_rf`): `MSE = 7.35283 ± 0.14667`, `R2_norm = -0.64155 ± 0.03474`, `Pearson_norm = +0.08796 ± 0.01127`, `Spearman_norm = +0.11258 ± 0.01730`.
- Same-environment `NaiveMeanEffectsPredictor` (`y_pred_naive`): `MSE = 5.25449 ± 0.02253`, `R2_norm = -0.17305 ± 0.00289`.

pass: true
