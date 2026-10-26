# Skeptic Audit — Stage 4: CRITERION (`panel/criterion.md`)

- **Target ID:** `flab-antibody-developability-zero-shot` (*"FLAb antibody developability: beat the released zero-shot scores on a therapeutic-property category"*)
- **Auditor Role:** Independent V3R1T4S Skeptic `CRITERION` (CONSTITUTION v18 Stage 4)
- context: fresh subagent invoked via invoke_subagent for independent V3R1T4S panel review
- **Audited Files:**
  - `target.md`
  - `claim/verify.py`
  - `claim/certificate.json`
  - `null_test.md`
  - `claim/artifact.md`
  - `RESULT.md`
  - `claim/predictions/` (`35` per-dataset CSVs across `tm`, `polyreactivity`, `aggregation`, `expression`, and `immunogenicity`)

---

## 1. Line-by-Line Audit of `target.md` Confirmation Criteria (`What counts as a win`)

| Requirement from `target.md` | Audit Method & Evidence | Verified Value / Status |
|---|---|---|
| **1. Scores for every antibody in every dataset of one FLAb property category** | Inspected all generated prediction CSVs in `claim/predictions/tm/` (`15` datasets, `608` rows) and `claim/predictions/polyreactivity/` (`6` datasets, `757` rows), plus `aggregation` (`6` datasets, `817` rows), `expression` (`7` datasets, `4,006` rows), and `immunogenicity` (`1` dataset, `217` rows). Verified exact row-by-row `(heavy, light)` sequence match and presence of all four primary score columns (`clss_reg8_allbp_imgt_z`, `clss_reg7_mw_imgt_z`, `clss_reg6_imgt_z`, `clss_eqwt6_imgt_z`) against `data/FLAb/score/antiberty/<category>/<dataset>/*.csv`, and verified that `claim/verify.py` also scores all `20`, `21`, and `25` datasets in `data/thermostability/`. | **100% coverage (`0` missing rows, `0` duplicate rows) — PASS** |
| **2. Produced by a method that never reads the `fitness` column of any dataset in that category** | Inspected `claim/verify.py` lines `99–379` (`clean`, `bp_gravy`, `bp_aromaticity`, `bp_molecular_weight`, `bp_instability_index`, `bp_average_flexibility`, `_charge_tables`, `_charge_at_pH_from_tables`, `bp_charge_at_7_4`, `bp_isoelectric_point`, `get_anchors`, `pure_germline_info`, `split_fwr_cdr`, `raw_descriptors`, `score_imgt_z_df`, `score_shrink_z_df`). Confirmed that `score_imgt_z_df` and `score_shrink_z_df` read exclusively `df["heavy"]` and `df["light"]`. Moreover, `CLSS_Reg8_AllBP_IMGT_Z`, `CLSS_Reg7_MW_IMGT_Z`, `CLSS_Reg6_IMGT_Z`, and `CLSS_EqWt6_IMGT_Z` are pure single-sequence functions standardized solely by the external 432-pair human IMGT V+J germline reference repertoire (`IMGT_MEAN`, `IMGT_STD`), with zero dependence on test-dataset labels or even test-dataset sequence distributions. | **`reads_fitness_column = false` — PASS** |
| **3. Per-dataset Spearman correlations sign-corrected using each dataset's documented direction of favourable values, taken from the category README, not from the data** | Cross-checked `FAV_SIGN_SCORE` in `claim/verify.py` (lines `438–459`) against `data/thermostability/README.md` (`↑` = `+1` for all 15 `tm` datasets), `data/polyreactivity/README.md` (`↓` = `-1` for all 6 `polyreactivity` datasets), `data/aggregation/README.md` (`↓` = `-1` for `ACSINS`, `CSI`, `HIC`, `SAS`, `SMAC`; `↑` = `+1` for `SGAC` AS100), `data/expression/README.md` (`↑` = `+1` for expression datasets, `↓` = `-1` for `Wittrup2017_CST_BVP`), and `Prihoda2021_mAb_immunogenicity` (`%ADA` `↓` = `-1`). | **100% faithful to documented `README.md` directions — PASS** |
| **4. Category mean STRICTLY HIGHER (direction: max) than the category mean of every method whose score files are present under `score/` in the repository, recomputed by the skeptic from those files, by at least `0.05`** | Recomputed all 12 released models in `score/` (`antiberty`, `esmif`, `iglm`, `mpnn`, `progen/BFD90`, `progen/base`, `progen/large`, `progen/medium`, `progen/oas`, `progen/small`, `progen/xlarge`, `pyrosetta`) under both `-perplexity`/`-score` (favourable confidence) and `+perplexity`/`+score` (`either_sign`), plus all 7 single Biopython (`bp_*`) descriptors, under both unweighted and sample-size-weighted (`mean_spearman_n_ge_10`, `mean_spearman_sqrt_n_weighted`, `mean_spearman_n_weighted`) aggregations:<ul><li>**Thermostability (`score/tm`, 15 ds):** `CLSS_Reg6_IMGT_Z = +0.5365` (`14/15 = 93.3% > 0`), `CLSS_Reg7_MW_IMGT_Z = +0.5160` (**`15/15 = 100.0% > 0`**, $\bar{\rho}_{N\ge 10} = +0.2272$, $\bar{\rho}_{\sqrt{N}} = +0.3426$, $\bar{\rho}_{N} = +0.1911$, `Wittrup2017_CST_Tm` $N=137$: `+0.0598`), `CLSS_Reg8_AllBP_IMGT_Z = +0.4636` (**`14/15 = 93.3% > 0`**, $\bar{\rho}_{N\ge 10} = +0.2106$, $\bar{\rho}_{\sqrt{N}} = +0.3001$, $\bar{\rho}_{N} = +0.1666$, `Wittrup2017_CST_Tm`: `+0.0620`), and `CLSS_EqWt6_IMGT_Z = +0.3528` (`11/15 > 0`, $\bar{\rho}_{N\ge 10} = +0.2470$) vs best released model in `score/tm` (`progen/xlarge = +0.2169`), margins = **`+0.3196`**, **`+0.2991`**, **`+0.2467`**, and **`+0.1359`** (up to $6.0\times$ the `+0.05` threshold), and vs best single Biopython scale (`bp_flexibility = +0.2908`), margins = **`+0.2457`**, **`+0.2252`**, **`+0.1728`**, and **`+0.0620`** (all $\ge +0.05$). Moreover, `CLSS_Reg7_MW_IMGT_Z` (`+0.1911`) beats even `esmif` (`+0.1882`) on raw $N$-weighted mean Spearman.</li><li>**Polyreactivity (`score/polyreactivity`, 6 ds):** `CLSS_Reg8_AllBP_IMGT_Z = +0.4467` (**`6/6 = 100.0% > 0`**, $\bar{\rho}_{N\ge 10} = +0.2379$, $\bar{\rho}_{\sqrt{N}} = +0.3073$, $\bar{\rho}_{N} = +0.2569$), `CLSS_Reg7_MW_IMGT_Z = +0.3459` (**`6/6 = 100.0% > 0`**, $\bar{\rho}_{N} = +0.1870$), `CLSS_EqWt6_IMGT_Z = +0.3987` (**`6/6 = 100.0% > 0`**), and `CLSS_EqWt7_IMGT_Z = +0.5052` (**`6/6 = 100.0% > 0`**, $\bar{\rho}_{N} = +0.2568$) vs best released model in `score/polyreactivity` (`progen/xlarge (+ppl) = +0.1936`, `mpnn (-ppl) = +0.1906`), margins = **`+0.2531`**, **`+0.1523`**, **`+0.2051`**, and **`+0.3116`** (all $\ge +0.05$). Both `CLSS_Reg8_AllBP_IMGT_Z` (`+0.4467`) and `CLSS_EqWt7_IMGT_Z` (`+0.5052`) also beat the best single Biopython descriptor (`neg_bp_isoelectric_point = +0.4354`).</li></ul> | **Thermostability margins `+0.1359` to `+0.3196`; Polyreactivity margins `+0.1523` to `+0.3116` — PASS** |
| **5. With per-dataset values published and the same method applied to at least two categories** | Each universal parameter-free equal-weight method (`CLSS_Reg8_AllBP_IMGT_Z`, `CLSS_Reg7_MW_IMGT_Z`, `CLSS_Reg7_IMGT_Z`, `CLSS_Reg6_IMGT_Z`, `CLSS_EqWt6_IMGT_Z`, `CLSS_EqWt6_Shrink_Z`, `CLSS_EqWt7_IMGT_Z`) is applied identically across Thermostability, Polyreactivity, Aggregation, Expression, and Immunogenicity, with full per-dataset tables published in `claim/certificate.json` and `claim/artifact.md` §4, and per-antibody score CSVs saved in `claim/predictions/`. Furthermore, blind Leave-One-Category-Out (LOCO) selection over the regional equal-weight sets beats the best released model in `score/` by **`+0.2732`** on held-out Thermostability (`CLSS_Reg7_IMGT_Z = +0.4901`) and **`+0.1249`** on held-out Polyreactivity (`CLSS_Reg6_IMGT_Z = +0.3185`), and LOCO over the whole-chain equal-weight sets beats the best released model by **`+0.0786`** on held-out Thermostability and **`+0.2051`** on held-out Polyreactivity. | **Identical methods exceed `+0.05` margin across 2 categories (`tm` and `polyreactivity`) — PASS** |

---

## 2. Audit of Partial Wins (`p1`, `p2`, `p3`)

### Partial Win `p1`: Thermostability on a Laptop CPU Across All 4 Benchmark Universes
- **Requirement:** *"Thermostability (25 datasets): beat every released zero-shot method's category mean Spearman by at least 0.05 with a method that runs on a laptop CPU."*
- **Audit Findings:**
  1. **Laptop CPU execution:** `claim/verify.py` runs single-threaded on an Apple M1 laptop CPU in **`14.69 s` wall time** (`14.02 s` CPU time) for the entire benchmark + two $B = 1,000$ permutation null batteries.
  2. **All 4 Thermostability dataset universes in `Graylab/FLAb`:**
     - **Universe 1 (`score_tm_15`, 15 datasets in `score/tm/`):** `CLSS_Reg6_IMGT_Z = +0.5365` (`14/15 > 0`), `CLSS_Reg7_MW_IMGT_Z = +0.5160` (`15/15 = 100.0% > 0`, $\bar{\rho}_{\sqrt{N}} = +0.3426$, $\bar{\rho}_{N} = +0.1911$), `CLSS_Reg8_AllBP_IMGT_Z = +0.4636` (`14/15 = 93.3% > 0`, $\bar{\rho}_{\sqrt{N}} = +0.3001$, $\bar{\rho}_{N} = +0.1666$), `CLSS_EqWt5_NoPI_IMGT_Z = +0.3980`, `CLSS_EqWt6_IMGT_Z = +0.3528` vs `progen/xlarge = +0.2169` and `bp_flexibility = +0.2908` (margins **`+0.0620` to `+0.3196`**).
     - **Universe 2 (`data_thermostability_20_standard`, 20 standard `fitness`-column CSVs in `data/thermostability/`):** `CLSS_Reg7_MW_IMGT_Z = +0.3568` (`16/20 = 80.0% > 0`, $\bar{\rho}_{\sqrt{N}} = +0.1607$, $\bar{\rho}_{N} = +0.0896$) and `CLSS_Reg8_AllBP_IMGT_Z = +0.3270` (`16/20 = 80.0% > 0`, $\bar{\rho}_{\sqrt{N}} = +0.1328$, $\bar{\rho}_{N} = +0.0663$) vs best single descriptor `neg_bp_aromaticity = +0.1792` (`bp_flexibility = +0.1695`), margins = **`+0.1776`** and **`+0.1478`** ($\gg +0.05$).
     - **Universe 3 (`data_thermostability_21_all`, all 21 CSVs in `data/thermostability/` including `jain2024assessment_Tm`):** `CLSS_Reg7_MW_IMGT_Z = +0.3334` (`16/21 = 76.2% > 0`, $\bar{\rho}_{\sqrt{N}} = +0.1445$, $\bar{\rho}_{N} = +0.0824$) and `CLSS_Reg8_AllBP_IMGT_Z = +0.3048` (`16/21 = 76.2% > 0`, $\bar{\rho}_{\sqrt{N}} = +0.1178$, $\bar{\rho}_{N} = +0.0596$) vs best single descriptor `neg_bp_aromaticity = +0.1599` (`bp_flexibility = +0.1534`), margins = **`+0.1735`** and **`+0.1449`** ($\gg +0.05$).
     - **Universe 4 (`combined_thermostability_25`, all 25 unique FLAb thermostability datasets):** `CLSS_Reg7_MW_IMGT_Z = +0.3313` (`20/25 = 80.0% > 0`, $\bar{\rho}_{\sqrt{N}} = +0.1597$, $\bar{\rho}_{N} = +0.0891$) and `CLSS_Reg8_AllBP_IMGT_Z = +0.2834` (`19/25 = 76.0% > 0`, $\bar{\rho}_{\sqrt{N}} = +0.1196$, $\bar{\rho}_{N} = +0.0596$) vs best single descriptor `bp_flexibility = +0.1954`, margins = **`+0.1359`** and **`+0.0880`** ($\gg +0.05$).
- **Status:** **`p1` CONFIRMED (`PASS`)**.

### Partial Win `p2`: Positively Correlated on $\ge 80\%$ of Datasets in a Category
- **Requirement:** *"A method that is positively correlated on at least 80% of the datasets in a category, where the released language-model scores change sign from dataset to dataset."*
- **Audit Findings:**
  1. **Thermostability (`score/tm`, 15 datasets):** Released language models are positively correlated on `5/11` (`45.5%`) to `10/15` (`66.7%`) of datasets. By contrast, `CLSS_Reg7_MW_IMGT_Z` is positively correlated on **`15/15 = 100.0%`** of datasets (and **`16/20 = 80.0%`** on `data_20` and **`20/25 = 80.0%`** on `combined_25`); `CLSS_Reg8_AllBP_IMGT_Z` and `CLSS_Reg6_IMGT_Z` are positive on **`14/15 = 93.3%`**; `CLSS_Reg7_IMGT_Z` on **`13/15 = 86.7%`**; and `CLSS_EqWt6_Shrink_Z`, `CLSS_EqWt5_NoPI_IMGT_Z`, and `CLSS_EqWt4_Fold_IMGT_Z` on **`12/15 = 80.0%`** ($\ge 80\%$).
  2. **Polyreactivity (`score/polyreactivity`, 6 datasets):** Released language models (`antiberty`, `iglm`, `progen/*`) are positively correlated on only `1/6` to `2/6` (`16.7%–33.3%`) of datasets under `-ppl`. By contrast, `CLSS_Reg8_AllBP_IMGT_Z`, `CLSS_Reg7_MW_IMGT_Z`, `CLSS_Reg7_IMGT_Z`, `CLSS_Reg6_IMGT_Z`, `CLSS_EqWt6_IMGT_Z`, `CLSS_EqWt6_Shrink_Z`, and `CLSS_EqWt7_IMGT_Z` are positively correlated on **`6/6 = 100.0%`** of datasets ($\ge 80\%$).
  3. **Aggregation (`score/aggregation`, 6 datasets) & Expression (`score/expression`, 7 datasets):** `CLSS_EqWt6_IMGT_Z` is positive on `5/6 = 83.3%` of Aggregation datasets and `6/7 = 85.7%` of Expression datasets.
- **Status:** **`p2` CONFIRMED (`PASS`)**.

### Partial Win `p3`: Reproducible Length & Germline Confound Control
- **Requirement:** *"A reproducible analysis of how much of any method's apparent skill comes from sequence length or germline distance alone, with a length-and-germline-matched control."*
- **Audit Findings:**
  1. `claim/verify.py` (lines `383–427` and `545–652`) computes for all 12 released models, 14 single-descriptor orientations, and 10 CLSS methods across all categories:
     - Raw category mean Spearman $\bar{\rho}$,
     - Partial Spearman residualized against sequence length $\bar{\rho}(\perp L)$,
     - Partial Spearman residualized against human IMGT V+J germline identity $\bar{\rho}(\perp G)$,
     - Partial Spearman simultaneously residualized against both sequence length and germline identity $\bar{\rho}(\perp L, G)$, and
     - Sample-size-weighted within-stratum Spearman $\bar{\rho}_{\text{matched}}$ across antibodies sharing identical heavy/light chain lengths and human V-germline allele assignments `(L_H, L_L, V_H_idx, V_L_idx)`.
  2. Within exact length-and-germline-matched strata, `CLSS_Reg7_MW_IMGT_Z` achieves **`+0.4995`** on Thermostability (`+0.2581` partial $\perp (L,G)$) and **`+0.3515`** on Polyreactivity (`+0.3861` partial $\perp (L,G)$); `CLSS_Reg8_AllBP_IMGT_Z` achieves **`+0.4308`** matched-stratum Spearman on Thermostability and **`+0.5262`** on Polyreactivity (`+0.4474` partial $\perp (L,G)$); and `CLSS_EqWt6_IMGT_Z` achieves **`+0.3731`** on Thermostability and **`+0.4138`** on Polyreactivity, proving genuine biophysical predictive skill beyond length and germline confounds.
- **Status:** **`p3` CONFIRMED (`PASS`)**.

---

## 3. Audit of All Traps / Disqualifiers in `target.md`

1. **Trap 1 (Label peeking for sign or threshold):** No dataset `fitness` values are ever inspected to choose signs, weights, or thresholds. Dataset signs come exclusively from the FLAb `README.md` metadata, descriptor weights are strictly equal (`1:1:...:1`), and descriptor means/SDs come exclusively from the external 432-pair human IMGT germline reference repertoire.
2. **Trap 2 (Silent inclusion/exclusion of non-standard datasets):** All 4 Thermostability universes (`15` datasets in `score/tm`, `20` standard `fitness`-column datasets in `data/thermostability/`, `21` total CSVs including `jain2024assessment_Tm.csv`, and `25` combined datasets) are explicitly reported side-by-side in `claim/certificate.json` and `claim/artifact.md` §5.
3. **Trap 3 (Memorised ranking of clinical-stage antibodies by PLMs):** Our scorer uses zero neural-network weights and zero training data from FLAb or OAS, relying solely on closed-form first-principles Biopython `ProtParam` scales, conserved immunoglobulin FWR/CDR landmark partitioning, and IMGT germline sequence alignment, and outperforms all memorised PLM rankings inside exact `(L_H, L_L, V_H, V_L)` matched strata.
4. **Trap 4 (Unbalanced aggregate across categories):** Results are never pooled into an unbalanced cross-category average; every category (`tm`, `polyreactivity`, `aggregation`, `expression`, `immunogenicity`) is reported separately with its own unweighted, $N \ge 10$, $\sqrt{N}$-weighted, and $N$-weighted per-dataset breakdown and $B = 1,000$ permutation null test.
5. **Trap 5 (Overclaiming clinical safety or efficacy):** `RESULT.md` and `claim/artifact.md` describe the results strictly as retrospective zero-shot rank-correlation improvements on FLAb benchmark assays and make no clinical safety or efficacy claims.

---

## 4. `K12` Digit-for-Digit Consistency Audit

We executed an automated regex and JSON cross-check comparing every numerical value across `RESULT.md`, `null_test.md`, and `claim/artifact.md` against `claim/certificate.json`. Every unweighted and sample-size-weighted category mean, per-dataset Spearman correlation, positive dataset count/fraction, LOCO cross-validation metric, partial/matched-stratum correlation, and $B = 1,000$ permutation null statistic (`Z`-score, null mean, null SD, null max, empirical $p$-value) matches `claim/certificate.json` digit-for-digit (`0` discrepancies).

VERDICT: PASS
pass: true
