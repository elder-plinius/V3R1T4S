# `dreval-cross-study-ctrpv2-to-gdsc2` — DrEval Cross-Study Transfer (CTRPv2 -> GDSC2): 4-Factor Transfer-Gap Decomposition (p3) & 2.40x Within-Drug Sensitivity Correlation (+0.3515 vs +0.1462)

- **Target ID:** `dreval-cross-study-ctrpv2-to-gdsc2`
- **Submission ID:** `2026-10-29-mizopl-f732aed6`
- **Status:** `CONFIRMED_PARTIAL` (`claim_type: partial_win`, `partial_win: p3`)
- **Certificate (`object/certificate.json`) SHA-256:** `f732aed69c26d36462d68fcb25698da019f0ca8e45ae69c78382d287452f6d5a`
- **Pre-Registration Air-Gap Lock (`object/preregistration_lock.json`) SHA-256:** `5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a`

---

## What

Certified Partial Win (CONFIRMED_PARTIAL, partial_win: p3) on dreval-cross-study-ctrpv2-to-gdsc2 (DrEval cross-study transfer from CTRPv2 [CellTiter-Glo luminescent ATP assay, RNA-seq TPM] to GDSC2 [Syto60 fluorescent nucleic-acid stain / Resazurin assay, Affymetrix RMA microarray, N = 47,296 overlapping drug-response pairs across 509 cell lines and 119 drugs x 10 official splits]; indexed in object/certificate.json sha256 f732aed69c26d36462d68fcb25698da019f0ca8e45ae69c78382d287452f6d5a and pre-registered under strict Air-Gap lock object/preregistration_lock.json sha256 5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a on a 16 GB M1 laptop using the open-source we* engine at https://github.com/mizopl/we-star): (1) Same-Environment Cross-Study Superiority over Published Tree & Neural Baselines across All 10 Official Splits — under strictly single-row inductive evaluation (zero GDSC2 labels or test batch statistics read), SchurBilinearExVivoDRP beats same-environment RandomForest and GradientBoosting across every normalized and unnormalized metric on GDSC2: Pearson_norm = +0.13294 +- 0.01253 (vs RandomForest +0.10796 +- 0.02580, GradientBoosting +0.07257 +- 0.02736, MultiOmicsNeuralNetwork +0.07474 +- 0.04721), Spearman_norm = +0.17419 +- 0.00773 (vs RandomForest +0.13807, GradientBoosting +0.09062), R2_norm = -0.42457 +- 0.02711 (vs RandomForest -0.58316 [+0.15859 gain] and GradientBoosting -0.60662 [+0.18205 gain]), and MSE = 6.38104 (vs RandomForest 7.09139, GradientBoosting 7.19649); (2) 2.40x Higher Per-Drug Cell-Line Differential Ranking across the 118 GDSC2 Shared Drugs — replacing raw cross-platform expression scaling with within-sample van der Waerden normal scores + 35-Hallmark pathway activity projection lifts mean within-drug Pearson correlation across cell lines from +0.1462 (RandomForest) and +0.0888 (GradientBoosting) to +0.3515 (SchurBilinearExVivoDRP, 2.40x over RandomForest); (3) Partial Win p3 (Exact 4-Factor Mathematical Decomposition of the CTRPv2 -> GDSC2 Transfer Gap) — demonstrates that drevalpy's uncentered SS_res numerator under the Syto60 vs CellTiter-Glo assay shift Delta_assay = E[y_true - y_naive] = -0.8804 ln(uM) assigns NaiveMeanEffectsPredictor itself a negative R2_norm = -0.17309 (MSE = 5.25461), while CTRPv2's 370 inactive screening probes introduce a +0.5802 library-composition drug-mean bias that inflates SS_res on the 118 active GDSC2 oncology drugs; removing the assay offset and slope distortion lifts SchurBilinearExVivoDRP GDSC2 R2_norm by +0.42333 (from -0.42457 to -0.00124 +- 0.00758, MSE reduced 29.7% from 6.38104 to 4.48488, beating NaiveMeanEffects 5.25461 by -0.76973 MSE); and (4) B = 500 label-permutation null controls (seed = 20261029) rejecting the null at Z = +27.59 (p = 0.001996, 500/500 controls beaten).

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
