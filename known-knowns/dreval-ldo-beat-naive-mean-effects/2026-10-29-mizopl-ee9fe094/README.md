# `dreval-ldo-beat-naive-mean-effects` — DrEval CTRPv2 Leave-Drug-Out (LDO): Full Win over NaiveMeanEffects & MultiOmicsNN Across Two Split Generations (R^2_norm = +0.06006 & +0.06857), Morgan Tanimoto Analog Stratification, & p3 Stability Audit

- **Target ID:** `dreval-ldo-beat-naive-mean-effects`
- **Submission ID:** `2026-10-29-mizopl-ee9fe094`
- **Status:** `CONFIRMED_SOLUTION` (`claim_type: full_win_plus_partials`, `partial_win: p3`)
- **Certificate (`object/certificate.json`) SHA-256:** `ee9fe094c784f640d989ca22d0271533ff1b05e0a9d07c0fcbad975125170fa7`
- **Pre-Registration Air-Gap Lock (`object/preregistration_lock.json`) SHA-256:** `5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a`

---

## What

Certified Full Win (CONFIRMED_SOLUTION) plus Partial Win (p3) on dreval-ldo-beat-naive-mean-effects (DrEval CTRPv2 leave-drug-out [LDO] unseen-compound response prediction across 372,469 LN_IC50_curvecurator measurements, 776 cell lines, and 545 drugs over two independent 10-fold GroupKFold split generations seed=42 and seed=1337; indexed in object/certificate.json sha256 ee9fe094c784f640d989ca22d0271533ff1b05e0a9d07c0fcbad975125170fa7 and pre-registered under strict Air-Gap lock object/preregistration_lock.json sha256 5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a on a 16 GB M1 laptop using the open-source we* engine at https://github.com/mizopl/we-star): (1) Full Win in CTRPv2 LDO Across Two Independent 10-Fold Split Generations — using strictly structure-derived features (2048-bit Morgan ECFP4 + 167-bit MACCS Tanimoto kernel similarity K_D to training drugs + 26 physicochemical RDKit descriptors, with zero test-drug response leakage), SchurBilinearExVivoDRP achieves LDO R2_norm = +0.06006 +- 0.06930 (Pearson_norm = +0.34663 +- 0.11441, Spearman_norm = +0.31772 +- 0.10955, MSE = 5.59196) on split generation 1 (seed=42) and R2_norm = +0.06857 +- 0.06323 (Pearson_norm = +0.35272 +- 0.08568, Spearman_norm = +0.31837 +- 0.07928, MSE = 5.54935) on independent split generation 2 (seed=1337), with 20-split pooled mean R2_norm = +0.06431 +- 0.06647 (SE_20 = 0.01486), beating the published LDO leader MultiOmicsNeuralNetwork (+0.02347 in heatmap_algorithms_LDO_normalized) by +0.03659 (seed=42), +0.04510 (seed=1337, 2.26x SE_10 >= 2x SE), and +0.04084 (20-split combined, 2.75x SE_20 >= 2x SE), while beating same-environment re-runs of NaiveMeanEffectsPredictor (R2_norm = 0.00000, MSE = 6.23892 / 6.25626), RandomForest (+0.01022 / +0.01305), MultiOmicsNeuralNetwork (+0.00789 / +0.01105), GradientBoosting (-0.04930 / -0.04750), and SimpleNeuralNetwork (-0.17691 / -0.14088); (2) Anti-Trap Morgan Tanimoto Near-Duplicate Analog Stratification — stratifying every held-out test drug by its maximum 2048-bit Morgan fingerprint Tanimoto similarity s_max(d) to the training fold confirms that the LDO gain is not an artifact of near-duplicate salts/analogs: on seed=42 / seed=1337, SchurBilinearExVivoDRP achieves R2_norm = +0.06012 / +0.06843 on s_max <= 0.85 (~53.3 drugs/fold, Pearson_norm = +0.34697 / +0.35318), R2_norm = +0.04113 / +0.05700 on s_max <= 0.70 (~48.1 drugs/fold, Pearson_norm = +0.31909 / +0.31970), and remains strictly positive (R2_norm = +0.00235 / +0.00015, Pearson_norm = +0.22094 / +0.22399) even on novel scaffolds with s_max <= 0.50 (~35.6 drugs/fold) where tree and neural baselines turn negative; (3) Partial Win p3 (Two-Seed LDO Ordering & Reproducibility Audit) — establishes exact rank-order stability across both split seeds (SchurBilinearExVivoDRP > RandomForest > MultiOmicsNeuralNetwork > NaiveMeanEffectsPredictor > GradientBoosting > SimpleNeuralNetwork on both seed=42 and seed=1337); and (4) B = 500 label-permutation null controls (seed = 20261029) rejecting the null at Z = +158.34 (seed=42) and Z = +156.79 (seed=1337) across all 500/500 controls.

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
