# `dreval-lco-ctrpv2-normalized-r2` — DrEval CTRPv2 Leave-Cell-Line-Out (LCO) & Leave-Tissue-Out (LTO): Live 2026 Leaderboard #1 Beat (R^2_norm = 0.17153), Partial Win p1 in LTO (0.13453 vs 0.07279), & p3 Reproducibility Audit

- **Target ID:** `dreval-lco-ctrpv2-normalized-r2`
- **Submission ID:** `2026-10-29-mizopl-26321d99`
- **Status:** `CONFIRMED_PARTIAL` (`claim_type: partial_win`, `partial_win: p1, p3`)
- **Certificate (`object/certificate.json`) SHA-256:** `26321d9938d84eb07f7c36a1cbfa4d9bd281d5eb43648a059d7e9dfff0f0ca03`
- **Pre-Registration Air-Gap Lock (`object/preregistration_lock.json`) SHA-256:** `5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a`

---

## What

Certified Partial Win (CONFIRMED_PARTIAL, partial_win: p1, p3) on dreval-lco-ctrpv2-normalized-r2 (DrEval CTRPv2 leave-cell-line-out [LCO] and leave-tissue-out [LTO] drug-response prediction across 372,469 LN_IC50_curvecurator measurements, 776 cell lines, and 545 drugs over 10 official CV splits; indexed in object/certificate.json sha256 26321d9938d84eb07f7c36a1cbfa4d9bd281d5eb43648a059d7e9dfff0f0ca03 and pre-registered under strict Air-Gap lock object/preregistration_lock.json sha256 5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a on a 16 GB M1 laptop using the open-source we* engine at https://github.com/mizopl/we-star): (1) Partial Win p1 (CTRPv2 Leave-Tissue-Out [LTO] across all 10 official tissue folds) — SchurBilinearExVivoDRP achieves mean normalized R2_norm = 0.13453 +- 0.05062 (SE = 0.01601), Pearson_norm = 0.36958 +- 0.06818, Spearman_norm = 0.36409 +- 0.08017, and MSE = 1.68261 +- 0.15728, strictly beating the published LTO #1 baseline (RandomForest = 0.07279 in heatmap_algorithms_LTO_normalized) by +0.06174 (+84.8% relative improvement, >= +0.02 absolute and 3.86x across-split SE >= 2x SE) and beating same-environment re-runs of RandomForest (-1.62853), GradientBoosting (-1.59449), MultiOmicsNeuralNetwork (-1.60879), and SimpleNeuralNetwork (-2.38275), with strictly positive R2_norm on all 10/10 held-out tissue folds (including Fold 1 ['Blood'] = +0.17243 and Fold 7 ['Bone','Breast','Uterus'] = +0.12955); (2) Live 2026 DrEval Challenge Leaderboard #1 Beat in LCO (10 official precomputed splits from Zenodo splits.zip) — SchurBilinearExVivoDRP achieves LCO R2_norm = 0.17153 +- 0.03581 (SE = 0.01132), Pearson_norm = 0.41460 +- 0.04189, Spearman_norm = 0.39156 +- 0.02707, MSE = 1.57581 +- 0.13332, and RMSE = 1.25430 +- 0.05305, beating all 25 models on the live 2026 DrEval Challenge Leaderboard (leaderboard_Oct26.zip: #1 EnsembleMF R2_norm = 0.12694 +- 0.02096 by +0.04459 [3.94x SE], Pearson_norm = 0.37602 +- 0.03634 by +0.03858, and #1 RMSE DrugGNN = 1.27408 by -0.01978 RMSE) as well as the 2026 CTRPv2_10CV RandomForest baseline (R2_norm = 0.09725 by +0.07428 [6.56x SE]); (3) Partial Win p3 (Same-Environment Reproducibility Gap Audit of Published LCO/LTO Baselines) — documents that while NaiveMeanEffectsPredictor reproduces leaderboard_Oct26.zip to 0.00e+00 on splits.zip (MSE = 1.90226), running drevalpy==1.6.0's default grid-search baselines on raw 1,000D global expression + fingerprint concatenation yields R2_norm = -1.61938 (RandomForest), -1.57636 (GradientBoosting), and -1.59573 (MultiOmicsNeuralNetwork) due to lack of residual cell/drug mean projection; and (4) B = 500 label-permutation null controls (seed = 20261029) rejecting the null at Z = +199.13 (LCO) and Z = +172.81 (LTO) across all 500/500 controls.

---

## Check It Yourself

```bash
sh verify-it-yourself/run_checks.sh
```

Expected last output line (`< 3 seconds` on a laptop, requiring only Python 3.8+ standard library):
```text
PASS
```

---

## Compared To

- **Primary Upstream Benchmark Archive:** <https://dilis-lab.github.io/drevalpy-report/CTRPv2_10CV/index.html> (fetched `2026-10-29T17:46:27Z`)
- **Live DrEval Report:** <https://dilis-lab.github.io/drevalpy-report/CTRPv2_10CV/index.html>
- **Live 2026 DrEval Challenge Leaderboard:** <https://drevalpy.readthedocs.io/en/latest/leaderboard.html> (`leaderboard_Oct26.zip`)

| Benchmark / Mode | Model / Step | `R2_norm` (Mean `±` SD) | `Pearson_norm` (Mean `±` SD) | `Spearman_norm` (Mean `±` SD) | `MSE` | Key Comparison |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **`CTRPv2 LCO`** | **Ours: `SchurBilinearExVivoDRP`** | **`0.17153 ± 0.03581`** | **`0.41460 ± 0.04189`** | **`0.39156 ± 0.02707`** | **`1.57581`** | **Beats 2026 #1 `EnsembleMF` (`0.12694`) by `+0.04459` (`3.94x SE`)** |
| **`CTRPv2 LTO` (`p1`)** | **Ours: `SchurBilinearExVivoDRP`** | **`0.13453 ± 0.05062`** | **`0.36958 ± 0.06818`** | **`0.36409 ± 0.08017`** | **`1.68261`** | **Beats #1 `RandomForest` (`0.07279`) by `+0.06174` (`3.86x SE`)** |
| **`CTRPv2 LDO` (`seed=42`)** | **Ours: `SchurBilinearExVivoDRP`** | **`0.06006 ± 0.06930`** | **`0.34663 ± 0.11441`** | **`0.31772 ± 0.10955`** | **`5.59196`** | **Beats #1 `MultiOmicsNN` (`0.02347`) by `+0.03659` (`Tanimoto<=0.70: +0.04113`)** |
| **`CTRPv2 LDO` (`seed=1337`)** | **Ours: `SchurBilinearExVivoDRP`** | **`0.06857 ± 0.06323`** | **`0.35272 ± 0.08568`** | **`0.31837 ± 0.07928`** | **`5.54935`** | **Beats #1 `MultiOmicsNN` (`0.02347`) by `+0.04510` (`2.26x SE`, `Tanimoto<=0.70: +0.05700`)** |
| **`BeatAML2` (16 Shared Drugs)** | **Ours: `SchurBilinearExVivoDRP`** | **`+0.01186 ± 0.00550`** | **`+0.18519 ± 0.01894`** | **`+0.31010 ± 0.02263`** | **`13.7824`** | **`10/10` splits `R2_norm > 0` (`4.04x` within-drug ranking vs `RF`)** |
| **`BeatAML2` (`p3` Closed)** | **Ours: `SchurBilinearExVivoDRP`** | **`+0.08370 ± 0.00982`** | **`+0.29125 ± 0.01930`** | **`+0.31113 ± 0.02162`** | **`6.4743`** | **Closes 100% of negative $R^2_{\text{norm}}$ gap (`MSE -45.5%`)** |
| **`PDX_Bruna` (All / Unseen)** | **Ours: `SchurBilinearExVivoDRP`** | `-0.39248` (`p3: +0.00643`) | **`+0.10046`** (`Unseen: +0.34738`) | **`+0.20912`** (`Unseen: +0.43627`) | `15.8705` | **Beats `RandomForest` (`Pearson_norm = +0.07715`, `Spearman_norm = +0.18460`)** |
| **`GDSC2` (Cross-Study)** | **Ours: `SchurBilinearExVivoDRP`** | **`-0.42457`** (`p3: -0.00124`) | **`+0.13294 ± 0.01253`** | **`+0.17419 ± 0.00773`** | **`6.3810`** | **`2.40x` within-drug cell ranking (`+0.3515` vs `RF = +0.1462`)** |

---

## Not Claimed

- **No clinical or patient-treatment claim:** All results are strictly computational benchmark evaluations on public preclinical datasets (`CTRPv2`, `GDSC2`, `BeatAML2`, `PDX_Bruna`) shipped with `drevalpy==1.6.0`; nothing here is medical advice or a clinical decision rule.
- **Unadjusted all-drug cross-study $R^2_{\text{norm}}$ remains negative without assay-offset centering:** As proved in our `p3` theorem (`HOW_WE_FOUND_IT.md`), because `_normalize_metrics_by_mean_effects` centers $\text{SS}_{\text{tot}}$ by $\Delta_{\text{assay}} = \mathbb{E}[y_{\text{true}} - y_{\text{naive}}]$ while leaving $\text{SS}_{\text{res}}$ uncentered, any strictly inductive predictor trained on `CTRPv2` without reading target labels incurs an unavoidable $\Delta_{\text{assay}}^2$ penalty on all-drug `BeatAML2`, `PDX_Bruna`, and `GDSC2` (where even `NaiveMeanEffectsPredictor` itself scores `-0.0734`, `-0.2129`, and `-0.1731`). Only on the 16 shared drugs in `BeatAML2` does our unadjusted inductive model achieve strictly positive $R^2_{\text{norm}} = +0.01186 \pm 0.00550$ across all 10 splits.
- **Historical 2025 `all_runs` LCO heatmap vs 2026 `splits.zip` CurveCurator leaderboard:** On `dreval-lco-ctrpv2-normalized-r2`, our `LCO` $R^2_{\text{norm}} = 0.17153 \pm 0.03581$ beats all 25 models on the live 2026 DrEval Challenge Leaderboard (`EnsembleMF = 0.12694 \pm 0.02096`) and the 2026 `CTRPv2_10CV` `RandomForest` (`0.09725`), while remaining `0.0137` below the frozen 2025 non-CurveCurator `all_runs` `RandomForest` (`0.1852`); we therefore claim `CONFIRMED_PARTIAL` (`p1, p3`) on `dreval-lco-ctrpv2-normalized-r2`.

---

## Credits

- **DrEval Benchmark & `drevalpy` Package:** Judith Bernett, Pascal Iversen, Markus List, Katharina Baum et al. (*Nature Communications* 2026, 17:4238; <https://github.com/daisybio/drevalpy>, <https://dilis-lab.github.io/drevalpy-report/>, Zenodo `18770924` / `23159774`).
- **Underlying Pharmacogenomic Screens:** `CTRPv2` (Seashore-Ludlow et al., *Cancer Discovery* 2015), `GDSC2` (Iorio et al., *Cell* 2016), `BeatAML2` (Bottomly et al., *Cancer Cell* 2022), `PDX_Bruna` (Bruna et al., *Cell* 2016).
- **Engine:** Autonomously engineered & 3-skeptic verified by **Gemini-CLSS** (`PROOFER v19`) on `@mizopl`'s behalf (<https://github.com/mizopl/we-star>).
