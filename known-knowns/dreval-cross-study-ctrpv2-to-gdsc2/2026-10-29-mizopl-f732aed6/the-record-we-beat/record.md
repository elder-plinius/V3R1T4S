# Comparator & Upstream Dataset Record (`dreval-cross-study-ctrpv2-to-gdsc2`)

- **Target ID:** `dreval-cross-study-ctrpv2-to-gdsc2`
- **Target File:** `known-unknowns/disease-research/dreval-cross-study-ctrpv2-to-gdsc2.md`
- **Claim Scope:** `CONFIRMED_PARTIAL` (`partial_win: p3`, internal 3-skeptic panel status) — measured decomposition of the `CTRPv2 -> GDSC2` transfer gap by re-scoring the **same** predictions under isolated mechanisms `(i)` concentration-range restriction, `(ii)` cell-line overlap restriction, and `(iii)` response-scale calibration.

---

## 1. Official Upstream `drevalpy` `GDSC2` Response File & Cross-Study HTML Table

1. **Official `drevalpy` `GDSC2` Response File (`GDSC2/GDSC2.csv`):**
   - **Download URL (`Zenodo Record 23159774`):** <https://zenodo.org/api/records/23159774/files/GDSC2.zip/content>
   - **Archive `GDSC2.zip` (`521,509,357` bytes):** `sha256 = 4b0230cfcf7a670aba386d4af559eebabf3f13190517d9eb0dc67596b84ac031`, `md5 = 49dc16929c6baa2b5d75c508429fa11f`
   - **Extracted `GDSC2/GDSC2.csv` (`57,384,361` bytes):** **`sha256 = 87c284eaf50c41e4ffd870220f67230b826068c3d08085a9a83caec62024bcbd`**
   - **Response Column:** `LN_IC50_curvecurator` (keyed by `(cell_line_name, drug_name)`)
   - **Row Counts:** `234,436` total rows; `90,666` non-NaN `LN_IC50_curvecurator` rows; `88,401` feature-complete pairs; **`47,296` shared-drug pairs** (`509` GDSC2 cell lines $\times$ `118` drugs shared with `CTRPv2`); and **`39,377–40,730` evaluated test rows per split (mean `40,292.4 ± 389.4`, total `402,924` rows across splits `0..9`)** after excluding the `352–386` overlapping cell lines present in each split's 90% `CTRPv2` training fold.
2. **Official Source `CTRPv2` Response File (`CTRPv2/CTRPv2.csv`):**
   - **Download URL (`Zenodo Record 23159774`):** <https://zenodo.org/api/records/23159774/files/CTRPv2.zip/content> (`CTRPv2.zip` `sha256 = 5ad3e867d3eda55595a981fd3f6426cb0a6a59218f109e9df68af50ffe2673bd`)
   - **Extracted `CTRPv2/CTRPv2.csv` (`143,722,503` bytes):** **`sha256 = 14488de3ecff0a7499eddbc10d22cdec389549c8506a93516a547e619f90b412`**
3. **Official Live Cross-Study `CTRPv2 -> GDSC2` `LCO` HTML Table:**
   - **UTC Fetch Timestamp:** `2026-10-29T17:46:27Z`
   - **Primary Table URL:** <https://dilis-lab.github.io/drevalpy-report/html_tables/table_cross_study_GDSC2_LCO.html>
   - **Solo Mirror URL:** <https://dilis-lab.github.io/drevalpy-report/all_runs/Solo/tables/table_cross_study_GDSC2_LCO.html>
   - **Snapshot `sha256` (`4,664,819` bytes):** **`01d129d634be27c49c50a8a1c357135f1e1090cd8df35cd6b7687f51e69595d9`**

---

## 2. Reconciled Cross-Study Comparator Table (`CTRPv2 -> GDSC2` `LCO`)

| Source / Cohort | Model | `MSE` (Mean `±` SD) | `R2_norm` (Mean `±` SD) | `Pearson_norm` (Mean `±` SD) | `Spearman_norm` (Mean `±` SD) | Evaluated Rows / Split |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Live HTML Table (`table_cross_study_GDSC2_LCO.html`)** | `GradientBoosting` (best `MSE` & `R2_norm`) | `5.092 ± 0.374` | `-0.115 ± 0.081` | `+0.209 ± 0.061` | `+0.166 ± 0.048` | Published cross-study LCO |
| **Live HTML Table (`table_cross_study_GDSC2_LCO.html`)** | `RandomForest` | `5.095 ± 0.139` | `-0.117 ± 0.030` | `+0.123 ± 0.028` | `+0.117 ± 0.027` | Published cross-study LCO |
| **Live HTML Table (`table_cross_study_GDSC2_LCO.html`)** | `MultiOmicsRandomForest` | `5.172 ± 0.176` | `-0.135 ± 0.037` | `+0.125 ± 0.039` | `+0.123 ± 0.035` | Published cross-study LCO |
| **Live HTML Table (`table_cross_study_GDSC2_LCO.html`)** | `NaiveMeanEffectsPredictor` | `5.447 ± 0.029` | `-0.199 ± 0.005` | `0.000 ± 0.000` | `0.000 ± 0.000` | Published cross-study LCO |
| **Live HTML Table (`table_cross_study_GDSC2_LCO.html`)** | `DIPK` (best `Pearson_norm`) | `6.407 ± 0.722` | `-0.428 ± 0.162` | `+0.301 ± 0.038` | `+0.277 ± 0.017` | Published cross-study LCO |
| **Live HTML Table (`table_cross_study_GDSC2_LCO.html`)** | `SuperFELTR` | `7.919 ± 0.066` | `-2.237 ± 0.038` | `+0.051 ± 0.004` | `+0.056 ± 0.005` | Published cross-study LCO |
| **Live HTML Table (`table_cross_study_GDSC2_LCO.html`)** | `SimpleNeuralNetwork` | `8.638 ± 1.916` | `-0.893 ± 0.421` | `+0.178 ± 0.054` | `+0.139 ± 0.047` | Published cross-study LCO |
| **Same-Env `2026` CurveCurator (`y_pred_naive` column)** | `NaiveMeanEffectsPredictor` | `5.25449 ± 0.02253` | `-0.17305 ± 0.00289` | `0.00000 ± 0.00000` | `0.00000 ± 0.00000` | `40,292.4 ± 389.4` |
| **Same-Env `2026` CurveCurator (`y_pred_rf` column)** | `RandomForest_SameEnv` | `7.35283 ± 0.14667` | `-0.64155 ± 0.03474` | `+0.08796 ± 0.01127` | `+0.11258 ± 0.01730` | `40,292.4 ± 389.4` |
| **Same-Env `2026` CurveCurator (`y_pred` column, Unadjusted)** | **Ours: `SchurBilinearExVivoDRP`** | `6.38104 ± 0.11786` | `-0.42457 ± 0.02711` | `+0.13294 ± 0.01253` | `+0.17419 ± 0.00773` | `40,292.4 ± 389.4` |
| **Same-Env `p3 (i-a)` In-Window Predictions (Label-Free)** | **Ours: `SchurBilinearExVivoDRP`** | **`2.63072 ± 0.03831`** | **`+0.03945 ± 0.01189`** | **`+0.36026 ± 0.00637`** | **`+0.35109 ± 0.00560`** | `19,118.6 ± 179.9` |
| **Same-Env `p3 (iii-a)` 1-Param Offset (Fit on GDSC2 $y$)** | **Ours: `SchurBilinearExVivoDRP`** | **`4.48488 ± 0.03641`** | **`-0.00124 ± 0.00758`** | `+0.13294 ± 0.01253` | `+0.17419 ± 0.00773` | `40,292.4 ± 389.4` |
| **Same-Env `p3 (iii-b)` 2-Param Linear OLS (Fit on GDSC2 $y$)** | **Ours: `SchurBilinearExVivoDRP`** | **`4.43967 ± 0.03586`** | **`+0.00885 ± 0.00760`** | `+0.14302 ± 0.01173` | `+0.19303 ± 0.00728` | `40,292.4 ± 389.4` |
| **Same-Env `p3 (iii-c)` 2-Param Affine Residual (Fit on GDSC2 $y$)** | **Ours: `SchurBilinearExVivoDRP`** | **`4.39953 ± 0.01975`** | **`+0.01781 ± 0.00353`** | `+0.13294 ± 0.01253` | `+0.17419 ± 0.00773` | `40,292.4 ± 389.4` |
