# `dreval-exvivo-beataml2-pdx-transfer` (`p3`): Unlabeled Ex Vivo Transfer-Gap Decomposition Across `BeatAML2` & `PDX_Bruna`

## What

- **Target ID:** `dreval-exvivo-beataml2-pdx-transfer`
- **Package ID:** `2026-11-07-mizopl-d1d47e16`
- **Claimed Partial Ladder Step:** `p3` (*"Decompose the cell-line-to-ex-vivo transfer gap into the contributions of (i) assay and readout differences, (ii) expression-platform shift, and (iii) drug overlap between CTRPv2 and the ex vivo screen"*, using strictly `CTRPv2` training data and unlabeled ex vivo features/metadata)
- **Internal 3-Skeptic Panel Status (our own panel's status):** `CONFIRMED_PARTIAL` (`panel/gate.md`)
- **Confirmed Scope (`panel/gate.md`):** On the 10 official CTRPv2 cross-validation splits of dreval-exvivo-beataml2-pdx-transfer, unadjusted SchurBilinearExVivoDRP achieves 10-split mean R2_norm = -0.09514 +- 0.00706 (Pearson_norm = +0.08461 +- 0.00873, Spearman_norm = +0.12617 +- 0.01275, MSE = 15.2230 +- 0.1055) on all 19,823 BeatAML2 rows and R2_norm = -0.39248 +- 0.02784 (Pearson_norm = +0.10046 +- 0.01842, Spearman_norm = +0.20911 +- 0.00906, MSE = 15.8705 +- 0.3121) on all 1,046 PDX_Bruna rows (with R2_norm = +0.01186 +- 0.00550 across 10/10 splits on the 79 shared BeatAML2 drugs, N = 11,901, vs R2_norm = -0.48996 +- 0.01551 on the 75 unseen BeatAML2 drugs, N = 7,922). Under partial ladder p3, applying each of the three corrections estimated strictly from CTRPv2 training splits and unlabeled ex vivo features/metadata (zero access to held-out y_true) on its own to the same SchurBilinearExVivoDRP predictions shows that (i) assay and readout concentration-window shift dominates both cohorts (closing -1.5013 MSE and lifting R2_norm by +0.10800 to +0.01286 +- 0.00444 [10/10 splits > 0], Pearson_norm = +0.18286 +- 0.00822 on BeatAML2; closing -4.1895 MSE and lifting R2_norm by +0.36758 to -0.02490 +- 0.01705, Pearson_norm = +0.33553 +- 0.01082 on PDX_Bruna, or +0.04462 +- 0.00346 under pooled CTRPv2 OLS), followed on BeatAML2 by (iii) drug overlap (-1.3121 MSE, +0.09439 R2_norm to -0.00075 +- 0.00590, Pearson_norm = +0.16529 +- 0.00898) and (ii) expression-platform shift (-0.1982 MSE, +0.01426 R2_norm to -0.08088 +- 0.00790), and on PDX_Bruna by (ii) expression-platform shift (-1.9630 MSE, +0.17224 R2_norm to -0.22024 +- 0.01500) and (iii) drug overlap (-1.4511 MSE, +0.12732 R2_norm to -0.26516 +- 0.02788); combining all three unlabeled corrections cumulatively lifts 10-split mean R2_norm to +0.05710 +- 0.00305 (10/10 splits > 0, Pearson_norm = +0.24186 +- 0.00739, MSE = 13.1068 +- 0.0422) on all 19,823 BeatAML2 rows and to +0.10159 +- 0.00598 (10/10 splits > 0, Pearson_norm = +0.35691 +- 0.01104, MSE = 10.2395 +- 0.0612) on all 1,046 PDX_Bruna rows.

### Executive Summary of Findings

1. **Out-of-the-Box Unadjusted Evaluation (All Evaluated Rows vs Shared/Unseen Drug Strata):**
   - **`BeatAML2` (`19,823` feature-valid rows/split across `484` primary AML patient samples and `154` unique drugs; upstream `BeatAML2.csv` `sha256: 259d409e33d87be1c63139fd2c38f82d2d94be23442010bc2b5fd71cd5de73d9`):**
     - On **all `19,823` rows** (`154` drugs), unadjusted `SchurBilinearExVivoDRP` achieves 10-split mean `R2_norm = -0.09514 +- 0.00706` (`0/10` splits `> 0`), `Pearson_norm = +0.08461 +- 0.00873`, `Spearman_norm = +0.12617 +- 0.01275`, and `MSE = 15.2230 +- 0.1055`.
     - Paired side-by-side across the drug-overlap boundary: on the **`79` shared clinical oncology drugs** present in `CTRPv2` (`N = 11,901` rows/split), unadjusted `SchurBilinearExVivoDRP` achieves **`R2_norm = +0.01186 +- 0.00550` (`10/10` splits `> 0`), `Pearson_norm = +0.18519 +- 0.01202`, `Spearman_norm = +0.31011 +- 0.02152`, and `MSE = 17.5735 +- 0.1055`**, whereas on the **`75` unseen drugs** absent from `CTRPv2` (`N = 7,922` rows/split), `R2_norm` collapses to **`-0.48996 +- 0.01551` (`Pearson_norm = -0.03940 +- 0.00593`, `Spearman_norm = +0.01078 +- 0.00551`, `MSE = 11.6920 +- 0.1217`)**.
   - **`PDX_Bruna` (`1,046` feature-valid rows/split across `25` breast-cancer PDX models and `100` unique drugs [`49` shared = `555` rows, `51` unseen = `491` rows]; upstream `PDX_Bruna.csv` `sha256: 63ef6dc157bc6bf0dc7a08a18ca86ff84509b8d2ef5e1f4a3c42a3cfbf368ee4`):**
     - On **all `1,046` rows** (`100` drugs), unadjusted `SchurBilinearExVivoDRP` achieves 10-split mean `R2_norm = -0.39248 +- 0.02784` (`0/10` splits `> 0`), `Pearson_norm = +0.10046 +- 0.01842`, `Spearman_norm = +0.20911 +- 0.00906`, and `MSE = 15.8705 +- 0.3121` (`shared drugs` $N=555$: `R2_norm = -0.39285 +- 0.03488`, `MSE = 14.0900 +- 0.3432`; `unseen drugs` $N=491$: `R2_norm = -0.39812 +- 0.02288`, `Pearson_norm = +0.34738 +- 0.00994`, `Spearman_norm = +0.35337 +- 0.00682`, `MSE = 17.8831 +- 0.2926`).

2. **Unlabeled `p3` Transfer-Gap Decomposition — Applying Each Correction ON ITS OWN to the Same `SchurBilinearExVivoDRP` Predictions (`Zero y_true Access`):**
   Every adjustment below is estimated **strictly from `CTRPv2` training splits (`train + validation`) and unlabeled ex vivo features/metadata** (with zero access to held-out `BeatAML2` or `PDX_Bruna` `y_true` values):
   - **Factor (i) — Assay & Readout Concentration-Window Shift ($\Delta^{(i)}_{\text{assay}}(c,d)$):**
     In `CTRPv2`, `314` compounds were screened across multiple plate dilution ranges (`min_dose_M`, `max_dose_M`, median $\max\text{dose} \approx 66\ \mu\text{M}$, $\overline{\ln(\text{max\_dose}_{\mu\text{M}})} = +4.0177$), whereas `BeatAML2` screens up to $10\ \mu\text{M}$ ($\overline{\ln(\text{max\_dose}_{\mu\text{M}})} = +2.2202$) and `PDX_Bruna` screens up to $4\text{--}5\ \mu\text{M}$ ($\overline{\ln(\text{max\_dose}_{\mu\text{M}})} = +1.3145$). Fitting a **within-drug Fixed-Effect (`FE`) linear regression** of `LN_IC50_curvecurator` on $(\ln\text{min\_dose}_{\mu\text{M}}, \ln\text{max\_dose}_{\mu\text{M}})$ strictly on `CTRPv2` training split $k$ (`10-split mean`: $\hat{\beta}_{\text{min}}^{\text{FE}} = +0.000642,\ \hat{\beta}_{\text{max}}^{\text{FE}} = +0.376184$) isolates the pure CurveCurator concentration-window readout dependence without confounding drug potency. Evaluating $\Delta^{(i)}_{\text{assay}}(c,d)$ from each drug's `CTRPv2` reference concentration window to the target screen's unlabeled plate bounds `[min_dose_M, max_dose_M]` (`10-split mean shift = -0.84049 +- 0.01498` on `BeatAML2`; `-1.01552 +- 0.01918` on `PDX_Bruna`) and applying $\hat{y} \mapsto \hat{y} + \Delta^{(i)}_{\text{assay}}$ **on its own** to `SchurBilinearExVivoDRP`:
     - **`BeatAML2` (`all 19,823 rows`):** Lifts `R2_norm` from `-0.09514` to **`+0.01286 +- 0.00444`** (`10/10` splits `> 0`, gain **`+0.10800`**), lifts `Pearson_norm` from `+0.08461` to **`+0.18286 +- 0.00822`** (gain **`+0.09825`**), lifts `Spearman_norm` from `+0.12617` to **`+0.21093 +- 0.00966`**, and cuts `MSE` from `15.2230` to **`13.7217 +- 0.0666`** (gap closed: **`-1.5013` MSE**).
     - **`PDX_Bruna` (`all 1,046 rows`):** Lifts `R2_norm` from `-0.39248` to **`-0.02490 +- 0.01705`** (gain **`+0.36758`**; under pooled `CTRPv2` OLS `only_i_assay_protocol_ols_all`, reaches **`+0.04462 +- 0.00346`** across `10/10` splits with `MSE = 10.8888 +- 0.0352`), lifts `Pearson_norm` from `+0.10046` to **`+0.33553 +- 0.01082`** (gain **`+0.23507`**), lifts `Spearman_norm` from `+0.20911` to **`+0.39008 +- 0.00992`**, and cuts `MSE` from `15.8705` to **`11.6811 +- 0.1893`** (gap closed: **`-4.1895` MSE**).
   - **Factor (ii) — Expression-Platform Shift ($\Delta^{(ii)}_{\text{platform}}$):**
     In `SchurBilinearExVivoDRP`, multi-omic cell representations (`logz, lm, dt, pw, bionic`) are standardized across samples using `CTRPv2` cell-line RNA-seq mean and SD (`std_view` in `how-we-built-it/stage2_inner_ablation.py`), inducing an unlabeled cohort offset relative to single-view KRR (`RawPlatformKRR_Ablation`): $\Delta^{(ii)}_{\text{platform}} = -\mathbb{E}_{(c,d)}[\hat{y}_{\text{schur}}(c,d) - \hat{y}_{\text{raw\_krr}}(c,d)]$ (`10-split mean = -0.14191 +- 0.05285` on `BeatAML2` RNA-seq; `-0.36781 +- 0.08580` on `PDX_Bruna` Illumina HumanHT-12 v4 BeadChip microarray). Applying $\hat{y} \mapsto \hat{y} + \Delta^{(ii)}_{\text{platform}}$ **on its own** to `SchurBilinearExVivoDRP`:
     - **`BeatAML2` (`all 19,823 rows`):** Lifts `R2_norm` from `-0.09514` to **`-0.08088 +- 0.00790`** (gain **`+0.01426`**) and cuts `MSE` from `15.2230` to **`15.0248 +- 0.1113`** (gap closed: **`-0.1982` MSE**), while within-sample van der Waerden (`vdW`) rank-normal expression alignment (`RawPlatformKRR_Ablation -> SchurBilinearExVivoDRP`) lifts `Pearson_norm` from `-0.01006` to **`+0.08461`** (gain **`+0.09467`**) and `R2_norm` from `-0.10512` to `-0.09514` (`+0.00998`).
     - **`PDX_Bruna` (`all 1,046 rows`):** Lifts `R2_norm` from `-0.39248` to **`-0.22024 +- 0.01500`** (gain **`+0.17224`**) and cuts `MSE` from `15.8705` to **`13.9075 +- 0.1677`** (gap closed: **`-1.9630` MSE**).
   - **Factor (iii) — Drug Overlap Between `CTRPv2` and the Ex Vivo Screen ($\Delta^{(iii)}_{\text{overlap}}(c,d)$):**
     In `CTRPv2`, ~400 of the `545` compounds are inactive chemical diversity probes ($\mu_{\text{CTRP}} = +1.8530\ \ln(\mu\text{M})$), whereas both `BeatAML2` and `PDX_Bruna` screen targeted clinical oncology panels. Consequently, unseen drugs ($d \notin D_{\text{CTRPv2}^{(k)}}$) default to `CTRPv2`'s probe-dominated global prior (`mean y_pred_schur = +1.6319` on `BeatAML2` unseen drugs vs `+0.3408` on shared drugs; `+2.6722` on `PDX_Bruna` unseen drugs vs `+1.8774` on shared drugs). Aligning unseen drugs via the strictly unlabeled prediction prior difference $\Delta^{(iii)}_{\text{overlap}}(c,d) = \mathbb{I}(d \notin D_{\text{CTRPv2}^{(k)}})(\overline{\hat{y}_{\text{shared}}}^{(k)} - \overline{\hat{y}_{\text{unseen}}}^{(k)})$ (`10-split mean = -1.29523 +- 0.02490` on `BeatAML2`; `-0.75936 +- 0.03246` on `PDX_Bruna`) **on its own** on all evaluated rows:
     - **`BeatAML2` (`all 19,823 rows`):** Lifts `R2_norm` from `-0.09514` to **`-0.00075 +- 0.00590`** (`5/10` splits `> 0`, gain **`+0.09439`**), lifts `Pearson_norm` from `+0.08461` to **`+0.16529 +- 0.00898`** (gain **`+0.08068`**), lifts `Spearman_norm` from `+0.12617` to **`+0.21161 +- 0.01078`**, and cuts `MSE` from `15.2230` to **`13.9110 +- 0.0881`** (gap closed: **`-1.3121` MSE**). On the `79` shared drugs stratum ($N=11,901$), `R2_norm` is **`+0.01186 +- 0.00550`** (`10/10` splits `> 0`, gain **`+0.10700`** vs all rows).
     - **`PDX_Bruna` (`all 1,046 rows`):** Lifts `R2_norm` from `-0.39248` to **`-0.26516 +- 0.02788`** (gain **`+0.12732`**), lifts `Pearson_norm` from `+0.10046` to **`+0.12168 +- 0.01707`**, and cuts `MSE` from `15.8705` to **`14.4194 +- 0.3132`** (gap closed: **`-1.4511` MSE**).

3. **Which Single Factor Dominates?**
   - **On both `BeatAML2` and `PDX_Bruna`, Factor (i) — Assay & Readout Concentration-Window Shift — is the #1 dominant single factor**, closing **`-1.5013` MSE (`+0.10800` `R2_norm`, `+0.09825` `Pearson_norm`)** on `BeatAML2` and **`-4.1895` MSE (`+0.36758` `R2_norm`, `+0.23507` `Pearson_norm`)** on `PDX_Bruna` on its own.
   - **On `BeatAML2` (RNA-seq $\to$ RNA-seq), Factor (iii) — Drug Overlap (`79` shared vs `75` unseen drugs) — is a close #2 co-dominant factor** (`-1.3121` MSE, `+0.09439` `R2_norm` on all rows; `+0.10700` `R2_norm` on the `79` shared drugs), whereas Factor (ii) cohort platform offset is #3 (`-0.1982` MSE, `+0.01426` `R2_norm`) because both cohorts use RNA-seq and within-sample `vdW` normal-score ranking already aligns their marginal distributions (`+0.09467` `Pearson_norm` over `RawPlatformKRR_Ablation`).
   - **On `PDX_Bruna` (RNA-seq $\to$ Illumina HT-12 v4 BeadChip microarray), Factor (ii) — Expression-Platform Shift — is the #2 factor** (`-1.9630` MSE, `+0.17224` `R2_norm`), ahead of #3 Factor (iii) Drug Overlap (`-1.4511` MSE, `+0.12732` `R2_norm`).
   - **Cumulative Unlabeled Progression (`(i) + (iii) + (ii)` on all evaluated rows, zero `y_true`):** Combining all three unlabeled adjustments lifts 10-split mean `R2_norm` to **`+0.05710 +- 0.00305` (`10/10` splits `> 0`, `Pearson_norm = +0.24186 +- 0.00739`, `Spearman_norm = +0.25798 +- 0.00983`, `MSE = 13.1068 +- 0.0422`, total gap closed `-2.1162` MSE / `+0.15224` `R2_norm`)** on all `19,823` `BeatAML2` rows, and to **`+0.10159 +- 0.00598` (`10/10` splits `> 0`, `Pearson_norm = +0.35691 +- 0.01104`, `Spearman_norm = +0.35221 +- 0.01022`, `MSE = 10.2395 +- 0.0612`, total gap closed `-5.6310` MSE / `+0.49407` `R2_norm`)** on all `1,046` `PDX_Bruna` rows.

---

## Check It Yourself

Run the standalone verification suite from the package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected terminal output (`exit 0`, final line `PASS`):

```text
========================================================================
V3R1T4S Verification — dreval-exvivo-beataml2-pdx-transfer (p3)
========================================================================
[OK] SHA256SUMS manifest verified (53 files).
[OK] Zero ground-truth response (`y`) columns copied into `object/*.csv`.
[OK] BeatAML2 (N=19,823/split, 484 AML patients, 154 drugs [79 shared, 75 unseen]): unadjusted R2_norm=-0.09514+-0.00706, Pearson_norm=+0.08461+-0.00873, MSE=15.2230; shared drugs (N=11,901) R2_norm=+0.01186.
[OK] BeatAML2 p3 single-factor (each on its own, zero y_true): (i) Assay FE R2_norm=+0.01286 (dMSE=-1.5013), (ii) Platform R2_norm=-0.08088 (dMSE=-0.1982), (iii) Overlap R2_norm=-0.00075 (dMSE=-1.3121); cumulative (i)+(ii)+(iii) R2_norm=+0.05710+-0.00305 (10/10 splits > 0).
[OK] PDX_Bruna (N=1,046/split, 25 PDX models, 100 drugs [49 shared, 51 unseen]): unadjusted R2_norm=-0.39248+-0.02784, Pearson_norm=+0.10046+-0.01842, MSE=15.8705.
[OK] PDX_Bruna p3 single-factor (each on its own, zero y_true): (i) Assay FE R2_norm=-0.02490 (dMSE=-4.1895), (ii) Platform R2_norm=-0.22024 (dMSE=-1.9630), (iii) Overlap R2_norm=-0.26516 (dMSE=-1.4511); cumulative (i)+(ii)+(iii) R2_norm=+0.10159+-0.00598 (10/10 splits > 0).
PASS
```

---

## Compared To

### Table 1: Unadjusted Out-of-the-Box Baselines Across All 10 Official `CTRPv2` Splits (`object/certificate.json`)

Comparator links: `https://dilis-lab.github.io/drevalpy-report/index.html`, `https://dilis-lab.github.io/drevalpy-report/LCO.html`, and Zenodo `https://zenodo.org/records/14974099`.

| Cohort & Stratum | Model / Baseline | `R2_norm` (Mean $\pm$ SD) | `Pearson_norm` (Mean $\pm$ SD) | `Spearman_norm` (Mean $\pm$ SD) | `MSE` (Mean $\pm$ SD) | `R2_raw` (Mean $\pm$ SD) | `Pearson_raw` (Mean $\pm$ SD) | Splits `R2_norm > 0` |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`BeatAML2` — All Drugs ($N=19,823$, `154` drugs)** | `SchurBilinearExVivoDRP` | `-0.09514 +- 0.00706` | `+0.08461 +- 0.00873` | `+0.12617 +- 0.01275` | `15.2230 +- 0.1055` | `-0.83232 +- 0.01270` | `+0.21552 +- 0.00707` | `0 / 10` |
| **`BeatAML2` — All Drugs ($N=19,823$, `154` drugs)** | `RawPlatformKRR_Ablation` | `-0.10512 +- 0.00698` | `-0.01006 +- 0.00955` | `-0.00090 +- 0.01568` | `15.3618 +- 0.1024` | `-0.84902 +- 0.01232` | `+0.19818 +- 0.00826` | `0 / 10` |
| **`BeatAML2` — All Drugs ($N=19,823$, `154` drugs)** | `RandomForest_SameEnv` | `-0.11782 +- 0.03878` | `+0.23218 +- 0.00657` | `+0.26537 +- 0.01891` | `15.5381 +- 0.5340` | `-0.87025 +- 0.06427` | `+0.27358 +- 0.01106` | `0 / 10` |
| **`BeatAML2` — All Drugs ($N=19,823$, `154` drugs)** | `GradientBoosting_SameEnv` | `-0.13324 +- 0.02836` | `+0.20922 +- 0.00770` | `+0.23199 +- 0.01827` | `15.7526 +- 0.3933` | `-0.89606 +- 0.04734` | `+0.27756 +- 0.00991` | `0 / 10` |
| **`BeatAML2` — All Drugs ($N=19,823$, `154` drugs)** | `NaiveMeanEffectsPredictor` | `-0.07339 +- 0.00203` | `+0.00000 +- 0.00000` | `+0.00000 +- 0.00000` | `14.9207 +- 0.0330` | `-0.79593 +- 0.00397` | `+0.22866 +- 0.00143` | `0 / 10` |
| **`BeatAML2` — Shared Drugs Only ($N=11,901$, `79` drugs)** | `SchurBilinearExVivoDRP` | **`+0.01186 +- 0.00550`** | **`+0.18519 +- 0.01202`** | **`+0.31011 +- 0.02152`** | `17.5735 +- 0.1055` | `-0.85889 +- 0.01116` | `+0.30541 +- 0.00547` | **`10 / 10`** |
| **`BeatAML2` — Unseen Drugs Only ($N=7,922$, `75` drugs)** | `SchurBilinearExVivoDRP` | `-0.48996 +- 0.01551` | `-0.03940 +- 0.00593` | `+0.01078 +- 0.00551` | `11.6920 +- 0.1217` | `-0.78102 +- 0.01854` | `+0.23510 +- 0.01122` | `0 / 10` |
| **`PDX_Bruna` — All Drugs ($N=1,046$, `100` drugs)** | `SchurBilinearExVivoDRP` | `-0.39248 +- 0.02784` | `+0.10046 +- 0.01842` | `+0.20911 +- 0.00906` | `15.8705 +- 0.3121` | `-0.98541 +- 0.03904` | `+0.23548 +- 0.01083` | `0 / 10` |
| **`PDX_Bruna` — All Drugs ($N=1,046$, `100` drugs)** | `RawPlatformKRR_Ablation` | `-0.18939 +- 0.01549` | `+0.21946 +- 0.01303` | `+0.26100 +- 0.02103` | `13.5558 +- 0.1758` | `-0.69584 +- 0.02199` | `+0.28990 +- 0.01084` | `0 / 10` |
| **`PDX_Bruna` — All Drugs ($N=1,046$, `100` drugs)** | `RandomForest_SameEnv` | `-0.29623 +- 0.02244` | `+0.07715 +- 0.01008` | `+0.18460 +- 0.01987` | `14.7737 +- 0.2625` | `-0.84820 +- 0.03284` | `+0.11491 +- 0.01134` | `0 / 10` |
| **`PDX_Bruna` — All Drugs ($N=1,046$, `100` drugs)** | `GradientBoosting_SameEnv` | `-0.16638 +- 0.02703` | `+0.13012 +- 0.01639` | `+0.20569 +- 0.02034` | `13.2936 +- 0.3074` | `-0.66304 +- 0.03846` | `+0.13270 +- 0.01750` | `0 / 10` |
| **`PDX_Bruna` — All Drugs ($N=1,046$, `100` drugs)** | `NaiveMeanEffectsPredictor` | `-0.21288 +- 0.01246` | `+0.00000 +- 0.00000` | `+0.00000 +- 0.00000` | `13.8237 +- 0.1440` | `-0.72936 +- 0.01802` | `+0.19323 +- 0.00496` | `0 / 10` |
| **`PDX_Bruna` — Shared Drugs Only ($N=555$, `49` drugs)** | `SchurBilinearExVivoDRP` | `-0.39285 +- 0.03488` | `-0.00688 +- 0.01602` | `+0.06556 +- 0.00933` | `14.0900 +- 0.3432` | `-1.19816 +- 0.05355` | `+0.16823 +- 0.01211` | `0 / 10` |
| **`PDX_Bruna` — Unseen Drugs Only ($N=491$, `51` drugs)** | `SchurBilinearExVivoDRP` | `-0.39812 +- 0.02288` | **`+0.34738 +- 0.00994`** | **`+0.35337 +- 0.00682`** | `17.8831 +- 0.2926` | `-0.83882 +- 0.03008` | `+0.34399 +- 0.01012` | `0 / 10` |

### Table 2: Unlabeled `p3` Transfer-Gap Decomposition — Single-Factor (Each on Its Own) & Cumulative Progression (`object/stage3_p3_gap_decomposition.json`)

Every adjustment below is applied to the **exact same `SchurBilinearExVivoDRP` predictions (`y_pred_schur`)** and estimated **strictly from `CTRPv2` training splits and unlabeled ex vivo features/metadata (zero access to `y_true`)**:

| Cohort (`N` / Split) | Decomposition Mode & Slice Key | `R2_norm` (Mean $\pm$ SD) | $\Delta R^2_{\text{norm}}$ vs Unadj | `Pearson_norm` (Mean $\pm$ SD) | `Spearman_norm` (Mean $\pm$ SD) | `MSE` (Mean $\pm$ SD) | $\Delta\text{MSE}$ Closed | Splits `> 0` | Single-Factor Dominance Rank |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`BeatAML2` ($19,823$)** | `unadjusted_all_drugs` (`Step 0`) | `-0.09514 +- 0.00706` | `+0.00000` | `+0.08461 +- 0.00873` | `+0.12617 +- 0.01275` | `15.2230 +- 0.1055` | `+0.0000` | `0 / 10` | Baseline |
| **`BeatAML2` ($19,823$)** | **Only (i) Assay Protocol FE (`only_i_assay_protocol_fe_all`)** | **`+0.01286 +- 0.00444`** | **`+0.10800`** | **`+0.18286 +- 0.00822`** | **`+0.21093 +- 0.00966`** | **`13.7217 +- 0.0666`** | **`-1.5013`** | **`10 / 10`** | **Rank #1 (Dominant)** |
| **`BeatAML2` ($19,823$)** | Only (i-alt) Assay Protocol Pooled OLS (`only_i_assay_protocol_ols_all`) | `-0.00149 +- 0.00309` | `+0.09365` | `+0.10608 +- 0.00700` | `+0.13883 +- 0.01079` | `13.9213 +- 0.0402` | `-1.3018` | `5 / 10` | *(Pooled OLS comparator)* |
| **`BeatAML2` ($19,823$)** | **Only (ii) Expression-Platform Shift (`only_ii_platform_shift_all`)** | `-0.08088 +- 0.00790` | `+0.01426` | `+0.08461 +- 0.00873` | `+0.12617 +- 0.01274` | `15.0248 +- 0.1113` | `-0.1982` | `0 / 10` | **Rank #3** *(RNA-seq $\to$ RNA-seq)* |
| **`BeatAML2` ($19,823$)** | **Only (iii) Drug-Overlap Prior (`only_iii_drug_overlap_prior_all`)** | `-0.00075 +- 0.00590` | **`+0.09439`** | **`+0.16529 +- 0.00898`** | **`+0.21161 +- 0.01078`** | **`13.9110 +- 0.0881`** | **`-1.3121`** | `5 / 10` | **Rank #2 (Co-Dominant)** |
| **`BeatAML2` ($11,901$)** | Only (iii-stratum) Shared Drugs (`only_iii_shared_drugs_stratum`, `79` drugs) | **`+0.01186 +- 0.00550`** | `+0.10700` | `+0.18519 +- 0.01202` | `+0.31011 +- 0.02152` | `17.5735 +- 0.1055` | `+2.3505` | **`10 / 10`** | *(79 shared vs 75 unseen)* |
| **`BeatAML2` ($19,823$)** | **Cumulative Step 1 (`+(i) Assay FE`: `cumulative_step1_plus_assay_fe_all`)** | **`+0.01286 +- 0.00444`** | `+0.10800` | `+0.18286 +- 0.00822` | `+0.21093 +- 0.00966` | `13.7217 +- 0.0666` | `-1.5013` | **`10 / 10`** | Cumulative `+(i)` |
| **`BeatAML2` ($19,823$)** | **Cumulative Step 2 (`+(i)+(iii)`: `cumulative_step2_plus_overlap_prior_all`)** | **`+0.05752 +- 0.00321`** | `+0.15266` | `+0.24186 +- 0.00739` | `+0.25798 +- 0.00983` | `13.1010 +- 0.0456` | `-2.1220` | **`10 / 10`** | Cumulative `+(i)+(iii)` |
| **`BeatAML2` ($19,823$)** | **Cumulative Step 3 (`+(i)+(iii)+(ii)`: `cumulative_step3_plus_platform_shift_all`)** | **`+0.05710 +- 0.00305`** | **`+0.15224`** | **`+0.24186 +- 0.00739`** | **`+0.25798 +- 0.00983`** | **`13.1068 +- 0.0422`** | **`-2.1162`** | **`10 / 10`** | **All 3 Unlabeled Factors** |
| **`BeatAML2` ($11,901$)** | Shared Drugs + Unlabeled `(i)+(ii)` (`shared_drugs_plus_assay_fe_and_platform`) | **`+0.06708 +- 0.00384`** | `+0.16222` | `+0.26559 +- 0.00916` | `+0.36897 +- 0.01635` | `16.5914 +- 0.0669` | `+1.3684` | **`10 / 10`** | Shared stratum `+(i)+(ii)` |
| **`PDX_Bruna` ($1,046$)** | `unadjusted_all_drugs` (`Step 0`) | `-0.39248 +- 0.02784` | `+0.00000` | `+0.10046 +- 0.01842` | `+0.20911 +- 0.00906` | `15.8705 +- 0.3121` | `+0.0000` | `0 / 10` | Baseline |
| **`PDX_Bruna` ($1,046$)** | **Only (i) Assay Protocol FE (`only_i_assay_protocol_fe_all`)** | `-0.02490 +- 0.01705` | **`+0.36758`** | **`+0.33553 +- 0.01082`** | **`+0.39008 +- 0.00992`** | **`11.6811 +- 0.1893`** | **`-4.1895`** | `1 / 10` | **Rank #1 (Dominant)** |
| **`PDX_Bruna` ($1,046$)** | Only (i-alt) Assay Protocol Pooled OLS (`only_i_assay_protocol_ols_all`) | **`+0.04462 +- 0.00346`** | `+0.43710` | `+0.33191 +- 0.00265` | `+0.35432 +- 0.00344` | `10.8888 +- 0.0352` | `-4.9817` | **`10 / 10`** | *(Pooled OLS comparator)* |
| **`PDX_Bruna` ($1,046$)** | **Only (ii) Expression-Platform Shift (`only_ii_platform_shift_all`)** | `-0.22024 +- 0.01500` | **`+0.17224`** | `+0.10046 +- 0.01842` | `+0.20911 +- 0.00906` | **`13.9075 +- 0.1677`** | **`-1.9630`** | `0 / 10` | **Rank #2** *(RNA-seq $\to$ Microarray)* |
| **`PDX_Bruna` ($1,046$)** | **Only (iii) Drug-Overlap Prior (`only_iii_drug_overlap_prior_all`)** | `-0.26516 +- 0.02788` | **`+0.12732`** | `+0.12168 +- 0.01707` | `+0.15984 +- 0.00531` | **`14.4194 +- 0.3132`** | **`-1.4511`** | `0 / 10` | **Rank #3** |
| **`PDX_Bruna` ($555$)** | Only (iii-stratum) Shared Drugs (`only_iii_shared_drugs_stratum`, `49` drugs) | `-0.39285 +- 0.03488` | `-0.00037` | `-0.00688 +- 0.01602` | `+0.06556 +- 0.00933` | `14.0900 +- 0.3432` | `-1.7805` | `0 / 10` | *(49 shared vs 51 unseen)* |
| **`PDX_Bruna` ($1,046$)** | **Cumulative Step 1 (`+(i) Assay FE`: `cumulative_step1_plus_assay_fe_all`)** | `-0.02490 +- 0.01705` | `+0.36758` | `+0.33553 +- 0.01082` | `+0.39008 +- 0.00992` | `11.6811 +- 0.1893` | `-4.1895` | `1 / 10` | Cumulative `+(i)` |
| **`PDX_Bruna` ($1,046$)** | **Cumulative Step 2 (`+(i)+(iii)`: `cumulative_step2_plus_overlap_prior_all`)** | **`+0.04836 +- 0.01488`** | `+0.44084` | `+0.35691 +- 0.01104` | `+0.35221 +- 0.01022` | `10.8461 +- 0.1649` | `-5.0244` | **`10 / 10`** | Cumulative `+(i)+(iii)` |
| **`PDX_Bruna` ($1,046$)** | **Cumulative Step 3 (`+(i)+(iii)+(ii)`: `cumulative_step3_plus_platform_shift_all`)** | **`+0.10159 +- 0.00598`** | **`+0.49407`** | **`+0.35691 +- 0.01104`** | **`+0.35221 +- 0.01022`** | **`10.2395 +- 0.0612`** | **`-5.6310`** | **`10 / 10`** | **All 3 Unlabeled Factors** |
| **`PDX_Bruna` ($555$)** | Shared Drugs + Unlabeled `(i)+(ii)` (`shared_drugs_plus_assay_fe_and_platform`) | `-0.00413 +- 0.00834` | `+0.38835` | `+0.12065 +- 0.01875` | `+0.23704 +- 0.02133` | `10.1578 +- 0.0698` | `-5.7128` | `2 / 10` | Shared stratum `+(i)+(ii)` |

---

## Not Claimed

1. **Primary Criterion (`R2_norm >= 0.02` on unadjusted full-cohort `BeatAML2`) Not Claimed:** On unadjusted out-of-the-box predictions across all `19,823` `BeatAML2` rows, `SchurBilinearExVivoDRP` achieves `R2_norm = -0.09514 +- 0.00706` (`+0.01186 +- 0.00550` on the `79` shared drugs, $N=11,901$, which is a subset and below `0.02`).
2. **Partial Steps `p1` and `p2` Not Claimed:** On unadjusted `BeatAML2` (`N = 19,823`), `SchurBilinearExVivoDRP` `Pearson_norm = +0.08461 +- 0.00873` is below same-environment `RandomForest_SameEnv` (`+0.23218 +- 0.00657`); on unadjusted `PDX_Bruna` (`N = 1,046`), `Pearson_norm = +0.10046 +- 0.01842` is below same-environment `GradientBoosting_SameEnv` (`+0.13012 +- 0.01639`).
3. **Zero Held-Out Ex Vivo Label Calibration:** No `BeatAML2` or `PDX_Bruna` `y_true` (`LN_IC50_curvecurator`) values are used anywhere in `p3` for training, fine-tuning, hyperparameter selection, response-scale calibration, or row filtering.
4. **Prospective Clinical Utility Not Claimed:** `BeatAML2` and `PDX_Bruna` are retrospective ex vivo pharmacogenomic screens; clinical treatment selection requires prospective clinical trials.

---

## Credits

- **Benchmark & Upstream Data:** `dilis-lab/drevalpy` (Judith Bernett, Pascal Iversen, Markus List, Katharina Baum et al., *Briefings in Bioinformatics* 2026; Zenodo record `14974099`).
- **Contributor:** `@mizopl` (`we*`).
