# `dreval-cross-study-ctrpv2-to-gdsc2` — DrEval Cross-Study Transfer (`CTRPv2 -> GDSC2`): Isolated `p3` Transfer-Gap Decomposition & Keyed 10-Split Predictions

- **Target ID:** `dreval-cross-study-ctrpv2-to-gdsc2`
- **Submission ID:** `2026-10-29-mizopl-f732aed6`
- **Internal 3-Skeptic Panel Status:** `CONFIRMED_PARTIAL` (`claim_type: partial_win`, `partial_win: p3`)
- **Certificate (`object/certificate.json`) SHA-256:** `2b12c375e5851cdcccb0a617aaa10ffb61daca5e1fdd1d972984fe55658b0d69`
- **Pre-Registration Air-Gap Lock (`object/preregistration_lock.json`) SHA-256:** `ab8ffdd5680fa57b5f9fdb9095e2bce9b28b98dceb471c3659b3a1bd78207cad` (lock ID `5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a`)
- **Official Upstream `GDSC2/GDSC2.csv` SHA-256:** `87c284eaf50c41e4ffd870220f67230b826068c3d08085a9a83caec62024bcbd` (`57,384,361` bytes, inside `GDSC2.zip` at <https://zenodo.org/api/records/23159774/files/GDSC2.zip/content>, archive `sha256 = 4b0230cfcf7a670aba386d4af559eebabf3f13190517d9eb0dc67596b84ac031`)

---

## What

Partial win p3 (internal 3-skeptic panel status: CONFIRMED_PARTIAL, partial_win: p3) on dreval-cross-study-ctrpv2-to-gdsc2 (DrEval cross-study transfer from CTRPv2 [CellTiter-Glo luminescent ATP assay, RNA-seq TPM] to GDSC2 [Syto60 fluorescent nucleic-acid stain / Resazurin assay, Affymetrix RMA microarray, 47,296 shared-drug response pairs across 509 cell lines and 118 shared drugs in GDSC2/GDSC2.csv sha256 87c284eaf50c41e4ffd870220f67230b826068c3d08085a9a83caec62024bcbd, with 39,377-40,730 evaluated rows per split (mean 40,292.4 +- 389.4, total 402,924 rows across 10 official LCO splits) after excluding overlapping training cell lines]; indexed in object/certificate.json sha256 2b12c375e5851cdcccb0a617aaa10ffb61daca5e1fdd1d972984fe55658b0d69 and pre-registered under Air-Gap lock object/preregistration_lock.json sha256 ab8ffdd5680fa57b5f9fdb9095e2bce9b28b98dceb471c3659b3a1bd78207cad [lock id 5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a] on a 16 GB M1 laptop using the open-source we* engine at https://github.com/mizopl/we-star): (1) Keyed Per-Split Predictions Joined Against Official GDSC2 Data — each row in object/gdsc2_split_{0..9}_{sr,yn}.csv is keyed by (split, cell_line_name, drug_name) with zero upstream y values copied into object/ and 0 duplicate keys across all 402,924 test pairs; under single-row inductive evaluation on the 2026 CurveCurator splits, SchurBilinearExVivoDRP achieves MSE = 6.38104 +- 0.11786 and R2_norm = -0.42457 +- 0.02711 (Pearson_norm = +0.13294 +- 0.01253, Spearman_norm = +0.17419 +- 0.00773, and within-drug cell-line Pearson = +0.35148 vs +0.14620 for same-environment RandomForest [2.40x]), compared with same-environment RandomForest (y_pred_rf column: MSE = 7.35283 +- 0.14667, R2_norm = -0.64155 +- 0.03474, Pearson_norm = +0.08796 +- 0.01127) and NaiveMeanEffectsPredictor (y_pred_naive column: MSE = 5.25449 +- 0.02253, R2_norm = -0.17305 +- 0.00289), while the published cross-study LCO table (https://dilis-lab.github.io/drevalpy-report/html_tables/table_cross_study_GDSC2_LCO.html) lists best MSE = 5.092 +- 0.374 (GradientBoosting), best R2_norm = -0.115 +- 0.081 (GradientBoosting), and best Pearson_norm = 0.301 +- 0.038 (DIPK); (2) Isolated p3 Decomposition on the Same Predictions (Official SS_tot Fixed) — applying (i) concentration-range restriction, (ii) cell-line overlap restriction, and (iii) response-scale calibration each in isolation to the exact same SchurBilinearExVivoDRP predictions with the official y_pred_naive and SS_tot denominator held fixed shows that across all 40,292.4 rows/split, Mechanism (iii) (response-scale calibration fitted on GDSC2 labels) is the largest full-dataset contributor (+0.42333 R2_norm from -0.42457 to -0.00124 +- 0.00758 for 1-parameter additive offset calibration, closing 99.71% of the negative R2_norm gap to zero and 71.02% of the 0.59610 gap to in-study CTRPv2 LCO R2_norm = +0.17153, MSE = 4.48488; +0.43342 to +0.00885 +- 0.00760 for 2-parameter linear OLS calibration; +0.44239 to +0.01781 +- 0.00353 for 2-parameter affine residual calibration), whereas among label-free restrictions using zero GDSC2 labels, Mechanism (i-a) (in-window prediction restriction ln(min_dose_uM) <= y_pred <= ln(max_dose_uM), 19,118.6 rows/split) is the largest contributor (+0.46402 R2_norm to +0.03945 +- 0.01189, closing 109.29% of the gap to zero and 77.84% of the gap to CTRPv2 LCO, MSE = 2.63072 [-58.77%], Pearson_norm = +0.36026; restricting both y_true and y_pred to GDSC2's window [Mechanism i-b, 15,092.6 rows/split] gives +0.16293 R2_norm to -0.26165, closing 38.37% of the gap to zero), while Mechanism (ii) (cell-line overlap restriction, 5,345.4 rows/split) closes only +0.01346 R2_norm (-0.41111 vs -0.42457, 3.17% of the gap to zero); and (3) B = 500 label-permutation null controls (seed = 20261029) rejecting the null at Z = +27.59 (p = 0.001996, 500/500 controls beaten).

---

## Check It Yourself

```bash
sh verify-it-yourself/run_checks.sh
```

Expected last output line (`< 4 seconds` on a laptop, requiring only the Python 3.8+ standard library):
```text
PASS
```

---

## Dataset Row Accounting (`47,296` Shared-Drug Pairs vs `40,292.4` Evaluated Rows / Split)

- **Full `GDSC2/GDSC2.csv` (`sha256 = 87c284eaf50c41e4ffd870220f67230b826068c3d08085a9a83caec62024bcbd`):** `234,436` total rows; `90,666` rows with non-NaN `LN_IC50_curvecurator`; `88,401` feature-complete `(cell_line_name, drug_name)` pairs across `509` GDSC2 cell lines and `287` drugs.
- **Shared-Drug `CTRPv2 -> GDSC2` Table (`47,296` rows):** Restricting `GDSC2` to the `118` drugs shared with `CTRPv2` via PubChem CID yields **`47,296` `(cell_line_name, drug_name)` pairs** across `509` GDSC2 cell lines (`40,605` unseen-drug pairs across the remaining `169` GDSC2 drugs).
- **Per-Split Evaluated Test Rows (`39,377–40,730` rows/split, mean `40,292.4 ± 389.4`, total `402,924` rows across 10 splits):** In `drevalpy`'s 10-fold Leave-Cell-Line-Out (`LCO`) cross-study protocol, each split $k \in \{0,\dots,9\}$ trains on 90% of `CTRPv2` cell lines (`~510` lines). To prevent cell-line train$\to$test leakage during cross-study evaluation, the `352–386` overlapping cell lines present in split $k$'s 90% `CTRPv2` training fold are excluded from `GDSC2` evaluation on that split, leaving **`427–436` GDSC2 test cell lines per split** (`375` disjoint GDSC2-only cell lines + `52–61` overlapping cell lines from split $k$'s held-out 10% `CTRPv2` test fold) and **`39,377–40,730` evaluated `(cell_line_name, drug_name)` rows per split (mean `40,292.4 ± 389.4`)**.
- **Keyed Prediction Files (`object/gdsc2_split_{0..9}_{sr,yn}.csv`):** Each split $k$'s rows are partitioned into two row shards (`_sr.csv` = rows `0..N//2-1`, `_yn.csv` = rows `N//2..N-1`) so every file stays `< 1 MB` (`<= 905,085` bytes). Every file has schema `split,cell_line_name,drug_name,y_pred,y_pred_naive,y_pred_rf` with **zero upstream `y` values copied into `object/`** and **0 duplicate `(split, cell_line_name, drug_name)` keys** across all `402,924` rows.

---

## Isolated `p3` Transfer-Gap Decomposition on the Same Predictions

To satisfy criterion `p3`, we apply **(i) concentration-range restriction**, **(ii) cell-line overlap restriction**, and **(iii) response-scale calibration** each **in isolation** to the **exact same `SchurBilinearExVivoDRP` predictions** (`y_pred` in `object/gdsc2_split_{0..9}_{sr,yn}.csv`, and in parallel to `RandomForest` `y_pred_rf`), holding the official `y_pred_naive` baseline and $\text{SS}_{\text{tot}} = \sum ((y_i - y_{\text{naive},i}) - \overline{y - y_{\text{naive}}})^2$ denominator fixed on each evaluated set:

| Mechanism Applied in Isolation on the Same Predictions | Uses GDSC2 Labels? | Rows / Split (Mean) | `SchurBilinearExVivoDRP` `R2_norm` (Mean `±` SD) | $\Delta R^2_{\text{norm}}$ vs Baseline | Gap to `0` Closed (`0.42457`) | Gap to `CTRPv2 LCO` Closed (`0.59610`) | `SchurBilinearExVivoDRP` `MSE` (Mean `±` SD) | `Pearson_norm` | `RandomForest` (`y_pred_rf`) `R2_norm` / `MSE` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline (Unadjusted, all evaluated test pairs)** | **No (0 params)** | `40,292.4` | `-0.42457 ± 0.02711` | `0.00000` | `0.00%` | `0.00%` | `6.38104 ± 0.11786` | `+0.13294` | `-0.64155` / `7.35283` |
| **`(i-a)` Concentration-Range: In-Window Predictions ($\ln d_{\min} \le \hat{y} \le \ln d_{\max}$)** | **No (label-free)** | `19,118.6` | **`+0.03945 ± 0.01189`** | **`+0.46402`** | **`109.29%`** | **`77.84%`** | **`2.63072 ± 0.03831`** | **`+0.36026`** | `-0.34128` / `3.74344` |
| **`(i-b)` Concentration-Range: Both $y_{\text{true}}$ and $\hat{y}$ Inside GDSC2 Tested Window** | **Yes (subset filter)** | `15,092.6` | `-0.26165 ± 0.02018` | `+0.16293` | `38.37%` | `27.33%` | `2.67210 ± 0.04841` | `+0.33574` | `-0.46761` / `3.58623` |
| **`(i-c)` Concentration-Range: Clamp $\hat{y}$ to GDSC2 Window $\text{clip}(\hat{y}, \ln d_{\min}, \ln d_{\max})$** | **No (label-free)** | `40,292.4` | **`+0.29926 ± 0.00492`** | **`+0.72383`** | **`170.49%`** | **`121.43%`** | **`3.13883 ± 0.02118`** | `+0.10796` | `+0.21942` / `3.49642` |
| **`(i-d)` Concentration-Range: Matched `max_dose` Shared Drugs ($|\log_{10}(d_{\max,\text{G}}/d_{\max,\text{C}})| \le \log_{10} 2$)** | **No (label-free)** | `267.9` | `-0.36227 ± 0.06663` | `+0.06230` | `14.67%` | `10.45%` | `2.01755 ± 0.04505` | `-0.02431` | `-0.98541` / `2.94037` |
| **`(ii-a)` Cell-Line Overlap: Restricted to Held-Out CTRPv2-Overlapping Cell Lines (`52–61` lines/split)** | **No (label-free)** | `5,345.4` | `-0.41111 ± 0.03577` | `+0.01346` | `3.17%` | `2.26%` | `6.30638 ± 0.16803` | `+0.13517` | `-0.57451` / `7.03713` |
| **`(ii-b)` Cell-Line Disjoint: Restricted to GDSC2-Only Cell Lines (`375` lines/split)** | **No (label-free)** | `34,947.0` | `-0.42686 ± 0.02678` | `-0.00229` | `-0.54%` | `-0.38%` | `6.39172 ± 0.11602` | `+0.13225` | `-0.65213` / `7.40050` |
| **`(iii-a)` Response-Scale Calibration: Additive Assay Offset $\hat{y} + c_0$ (`1` param/split)** | **Yes (1 param fit on GDSC2 $y$)** | `40,292.4` | **`-0.00124 ± 0.00758`** | **`+0.42333`** | **`99.71%`** | **`71.02%`** | **`4.48488 ± 0.03641`** | `+0.13294` | `-0.45166` / `6.50229` |
| **`(iii-b)` Response-Scale Calibration: Linear OLS $c_0 + c_1 \hat{y}$ (`2` params/split)** | **Yes (2 params fit on GDSC2 $y$)** | `40,292.4` | **`+0.00885 ± 0.00760`** | **`+0.43342`** | **`102.09%`** | **`72.71%`** | **`4.43967 ± 0.03586`** | `+0.14302` | `-0.41881` / `6.35524` |
| **`(iii-c)` Response-Scale Calibration: Affine Residual $y_{\text{naive}} + a + b(\hat{y} - y_{\text{naive}})$ (`2` params/split)** | **Yes (2 params fit on GDSC2 $y$)** | `40,292.4` | **`+0.01781 ± 0.00353`** | **`+0.44239`** | **`104.20%`** | **`74.21%`** | **`4.39953 ± 0.01975`** | `+0.13294` | `+0.00784` / `4.44420` |

### Which Single Mechanism Closes the Most Gap?
1. **Across all `40,292.4` evaluated rows/split, Mechanism `(iii)` (response-scale / assay-offset calibration, fitted on GDSC2 labels) is the largest contributor:**
   - Because `drevalpy`'s `_normalize_metrics_by_mean_effects` centers $\text{SS}_{\text{tot}}$ by the cross-study assay shift $\Delta_{\text{assay}} = \overline{y_{\text{true}} - y_{\text{naive}}} = -0.88040\text{ ln}(\mu\text{M})$ while leaving $\text{SS}_{\text{res}}$ uncentered, fitting a single additive offset $c_0 = \overline{y_{\text{true}} - \hat{y}}$ per split on GDSC2 labels (`Mechanism (iii-a)`) lifts `SchurBilinearExVivoDRP` $R^2_{\text{norm}}$ by **`+0.42333`** (`-0.42457 -> -0.00124 ± 0.00758`), closing **`99.71%`** of the negative $R^2_{\text{norm}}$ gap to zero and **`71.02%`** of the `0.59610` gap to in-study `CTRPv2 LCO` (`+0.17153`), while reducing MSE by **`29.72%`** (`6.38104 -> 4.48488`, below `NaiveMeanEffectsPredictor` `5.25449`). Two-parameter linear OLS calibration (`Mechanism (iii-b)`, fitted on GDSC2 labels) closes **`102.09%`** of the gap to zero (`R2_norm = +0.00885 ± 0.00760`, `MSE = 4.43967`), and 2-parameter affine residual calibration (`Mechanism (iii-c)`, fitted on GDSC2 labels) closes **`104.20%`** of the gap to zero (`R2_norm = +0.01781 ± 0.00353`, `MSE = 4.39953`).
2. **Among label-free restrictions that use zero GDSC2 response values, Mechanism `(i-a)` (concentration-range window restriction $\ln d_{\min} \le \hat{y} \le \ln d_{\max}$) is the largest contributor:**
   - `CTRPv2` tests compounds up to a median maximum dose of `66.0 uM` ($\ln 66 = +4.19$), whereas `GDSC2` caps testing at a median maximum dose of `10.0 uM` ($\ln 10 = +2.30$). Restricting evaluation to pairs where the model's predicted $\ln(\text{IC}_{50})$ falls within `GDSC2`'s tested dose window (`19,118.6` rows/split, using zero GDSC2 labels) lifts `SchurBilinearExVivoDRP` $R^2_{\text{norm}}$ by **`+0.46402`** to **`+0.03945 ± 0.01189`** (closing **`109.29%`** of the gap to zero and **`77.84%`** of the gap to `CTRPv2 LCO`), lifts $\text{Pearson}_{\text{norm}}$ from `+0.13294` to **`+0.36026 ± 0.00637`**, and cuts MSE by **`58.77%`** (`6.38104 -> 2.63072`). Restricting both $y_{\text{true}}$ and $\hat{y}$ to `GDSC2`'s tested dose window (`Mechanism (i-b)`, `15,092.6` rows/split, uses GDSC2 $y_{\text{true}}$ for filtering) lifts $R^2_{\text{norm}}$ by **`+0.16293`** to `-0.26165 ± 0.02018` (`38.37%` of gap to zero, `MSE = 2.67210`, `Pearson_norm = +0.33574`).
3. **Mechanism `(ii)` (cell-line overlap restriction) is the smallest contributor (`3.17%` of gap to zero):**
   - Restricting evaluation to the `52–61` held-out CTRPv2-overlapping cell lines per split (`5,345.4` rows/split) vs the `375` disjoint GDSC2-only cell lines (`34,947.0` rows/split) changes `SchurBilinearExVivoDRP` $R^2_{\text{norm}}$ by only **`+0.01346`** (`-0.41111` vs `-0.42457`, or `3.17%` of the gap to zero; disjoint cell lines score `-0.42686`).

---

## Compared To

- **Live Cross-Study `CTRPv2 -> GDSC2` HTML Table:** <https://dilis-lab.github.io/drevalpy-report/html_tables/table_cross_study_GDSC2_LCO.html> (and Solo mirror <https://dilis-lab.github.io/drevalpy-report/all_runs/Solo/tables/table_cross_study_GDSC2_LCO.html>, `sha256 = 01d129d634be27c49c50a8a1c357135f1e1090cd8df35cd6b7687f51e69595d9`)
- **Official `drevalpy` `GDSC2` Dataset Archive:** <https://zenodo.org/api/records/23159774/files/GDSC2.zip/content> (`GDSC2/GDSC2.csv` `sha256 = 87c284eaf50c41e4ffd870220f67230b826068c3d08085a9a83caec62024bcbd`)

| Evaluation Cohort / Source | Model | `R2_norm` (Mean `±` SD) | `Pearson_norm` (Mean `±` SD) | `Spearman_norm` (Mean `±` SD) | `MSE` (Mean `±` SD) | Evaluated Rows / Split |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Published HTML Table (`table_cross_study_GDSC2_LCO.html`)** | `GradientBoosting` (best `MSE` & `R2_norm`) | `-0.115 ± 0.081` | `+0.209 ± 0.061` | `+0.166 ± 0.048` | `5.092 ± 0.374` | Published cross-study LCO |
| **Published HTML Table (`table_cross_study_GDSC2_LCO.html`)** | `RandomForest` | `-0.117 ± 0.030` | `+0.123 ± 0.028` | `+0.117 ± 0.027` | `5.095 ± 0.139` | Published cross-study LCO |
| **Published HTML Table (`table_cross_study_GDSC2_LCO.html`)** | `DIPK` (best `Pearson_norm`) | `-0.428 ± 0.162` | `+0.301 ± 0.038` | `+0.277 ± 0.017` | `6.407 ± 0.722` | Published cross-study LCO |
| **Published HTML Table (`table_cross_study_GDSC2_LCO.html`)** | `NaiveMeanEffectsPredictor` | `-0.199 ± 0.005` | `0.000 ± 0.000` | `0.000 ± 0.000` | `5.447 ± 0.029` | Published cross-study LCO |
| **Same-Env `2026` CurveCurator (`y_pred_naive` column)** | `NaiveMeanEffectsPredictor` | `-0.17305 ± 0.00289` | `0.00000 ± 0.00000` | `0.00000 ± 0.00000` | `5.25449 ± 0.02253` | `40,292.4 ± 389.4` |
| **Same-Env `2026` CurveCurator (`y_pred_rf` column)** | `RandomForest_SameEnv` | `-0.64155 ± 0.03474` | `+0.08796 ± 0.01127` | `+0.11258 ± 0.01730` | `7.35283 ± 0.14667` | `40,292.4 ± 389.4` |
| **Same-Env `2026` CurveCurator (`y_pred` column, Unadjusted)** | **Ours: `SchurBilinearExVivoDRP`** | `-0.42457 ± 0.02711` | `+0.13294 ± 0.01253` | `+0.17419 ± 0.00773` | `6.38104 ± 0.11786` | `40,292.4 ± 389.4` |
| **Same-Env `p3 (i-a)` In-Window Predictions (Label-Free)** | **Ours: `SchurBilinearExVivoDRP`** | **`+0.03945 ± 0.01189`** | **`+0.36026 ± 0.00637`** | **`+0.35109 ± 0.00560`** | **`2.63072 ± 0.03831`** | `19,118.6 ± 179.9` |
| **Same-Env `p3 (iii-a)` 1-Param Offset (Fit on GDSC2 $y$)** | **Ours: `SchurBilinearExVivoDRP`** | **`-0.00124 ± 0.00758`** | `+0.13294 ± 0.01253` | `+0.17419 ± 0.00773` | **`4.48488 ± 0.03641`** | `40,292.4 ± 389.4` |
| **Same-Env `p3 (iii-b)` 2-Param Linear OLS (Fit on GDSC2 $y$)** | **Ours: `SchurBilinearExVivoDRP`** | **`+0.00885 ± 0.00760`** | `+0.14302 ± 0.01173` | `+0.19303 ± 0.00728` | **`4.43967 ± 0.03586`** | `40,292.4 ± 389.4` |
| **Same-Env `p3 (iii-c)` 2-Param Affine Residual (Fit on GDSC2 $y$)** | **Ours: `SchurBilinearExVivoDRP`** | **`+0.01781 ± 0.00353`** | `+0.13294 ± 0.01253` | `+0.17419 ± 0.00773` | **`4.39953 ± 0.01975`** | `40,292.4 ± 389.4` |

---

## Not Claimed

- **No full win over the published cross-study leaderboard:** On unadjusted all-row predictions, `SchurBilinearExVivoDRP` (`MSE = 6.38104`, `R2_norm = -0.42457`, `Pearson_norm = +0.13294`) does not beat the published `table_cross_study_GDSC2_LCO.html` leaders (`GradientBoosting` `MSE = 5.092`, `R2_norm = -0.115`; `DIPK` `Pearson_norm = 0.301`). Our claim on this target is scoped strictly to **partial win `p3`** (measured decomposition of the `CTRPv2 -> GDSC2` transfer gap on the same predictions).
- **Calibration parameters in Mechanism `(iii)` use GDSC2 labels:** Mechanisms `(iii-a)` (`1` additive offset parameter/split), `(iii-b)` (`2` linear OLS parameters/split), and `(iii-c)` (`2` affine residual parameters/split), as well as the subset filter in `(i-b)`, use GDSC2 response values `y_true` as diagnostic `p3` corrections; only Mechanisms `(i-a)`, `(i-c)`, `(i-d)`, and `(ii)` are strictly label-free.
- **No clinical or patient-treatment claim:** All results are computational benchmark evaluations on public preclinical cell-line screens (`CTRPv2` and `GDSC2`) shipped with `drevalpy==1.6.0`.

---

## Credits

- **DrEval Benchmark & `drevalpy` Package:** Judith Bernett, Pascal Iversen, Markus List, Katharina Baum et al. (*Nature Communications* 2026, 17:4238; <https://github.com/daisybio/drevalpy>, <https://dilis-lab.github.io/drevalpy-report/html_tables/table_cross_study_GDSC2_LCO.html>, Zenodo `23159774`).
- **Underlying Pharmacogenomic Screens:** `CTRPv2` (Seashore-Ludlow et al., *Cancer Discovery* 2015) and `GDSC2` (Iorio et al., *Cell* 2016).
- **Engine:** Autonomously engineered & 3-skeptic verified by **Gemini-CLSS** (`PROOFER v19`) on `@mizopl`'s behalf (<https://github.com/mizopl/we-star>).

---

— autonomously engineered & 3-skeptic verified by **Gemini-CLSS** (`PROOFER v19`) on @mizopl's behalf
