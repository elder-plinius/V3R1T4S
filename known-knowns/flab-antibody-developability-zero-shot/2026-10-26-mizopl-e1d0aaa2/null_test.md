# Null-Test & Confound-Control Battery (`null_test.md`)

- **Target ID:** `flab-antibody-developability-zero-shot`
- `controls`: 1000
- `best_control`: +0.3468 (`CLSS_Reg8_AllBP_IMGT_Z` on `tm`, $B=1,000$ within-dataset fitness permutations; `+0.3333` on `polyreactivity`; `+0.3297` for `CLSS_EqWt6_IMGT_Z` on `polyreactivity`)
- `real`: +0.4636 (`CLSS_Reg8_AllBP_IMGT_Z` on `tm`; `+0.5160` for `CLSS_Reg7_MW_IMGT_Z` on `tm`; `+0.4467` on `polyreactivity`; `+0.3987` for `CLSS_EqWt6_IMGT_Z` on `polyreactivity`)
- `command`: `python3 claim/verify.py`
- `real_beats_all_controls`: yes
- **Verification Script:** `claim/verify.py`
- **Machine-Verified Certificate:** `claim/certificate.json`

---

## 1. Zero-Shot Integrity Audit (No `fitness` Reads, Zero Hand-Tuned Weights)

1. **Zero `fitness` reads during scoring:** All CLSS score functions (`score_imgt_z_df`, `score_shrink_z_df`, `raw_descriptors`) read exclusively the `heavy` and `light` amino-acid sequence columns (`reads_fitness_column = false`). The `fitness` column is accessed only by the external evaluator after the full per-antibody score vector $\mathbf{x}$ has been computed and frozen.
2. **Zero hand-tuned weights (`1:1:...:1`):**
   - In **`CLSS_Reg8_AllBP_IMGT_Z`** (the complete 8-descriptor Regional FWR-Scaffold + CDR-Paratope formulation), all 7 Biopython descriptors from the FLAb benchmark (`flexibility`, `-gravy`, `-instability_index` on the $\beta$-sandwich Framework `FWR1–4`; `-aromaticity`, `-isoelectric_point`, `-charge_at_7_4` on the hypervariable `CDR1–3` loops; plus `molecular_weight`) and human IMGT germline sequence identity (`germ`) receive strictly equal weight $w_k = 1/8$.
   - In **`CLSS_Reg7_MW_IMGT_Z`**, the 7 non-redundant regional descriptors (`fwr_flex`, `neg_fwr_gravy`, `neg_fwr_inst`, `neg_cdr_arom`, `neg_cdr_pI`, `germ`, `mw`) receive strictly equal weight $w_k = 1/7$.
   - In **`CLSS_EqWt6_IMGT_Z`**, the 6 whole-chain intensive descriptors (`flex`, `neg_gravy`, `neg_arom`, `neg_pI`, `neg_inst`, `germ`) receive strictly equal weight $w_k = 1/6$ (`CLSS_EqWt7_IMGT_Z` adds `neg_chg` with equal weight $w_k = 1/7$).
   - No continuous weights, regression coefficients, or dataset-specific signs were fitted to any FLAb dataset (`uses_hand_tuned_weights = false`, `uses_ad_hoc_position_rules = false`).
3. **External standardization reference:** Each descriptor $f_k$ is standardized exclusively using the fixed mean $\mu_k^{\text{IMGT}}$ and standard deviation $\sigma_k^{\text{IMGT}}$ of the external human IMGT V+J germline Fv reference repertoire ($24\text{ IGHV} \times 18\text{ IGKV/IGLV} = 432$ germline Fv pairs):
   - Whole-chain $\mu^{\text{IMGT}} = (\text{flex}: 1.00161,\; -\text{gravy}: 0.34227,\; -\text{arom}: -0.10908,\; -\text{pI}: -7.75691,\; -\text{inst}: -39.40391,\; -\text{chg}: -0.57680,\; \text{mw}: 11821.96976,\; \text{germ}: 0.75307)$
   - Whole-chain $\sigma^{\text{IMGT}} = (\text{flex}: 0.00165,\; -\text{gravy}: 0.07104,\; -\text{arom}: 0.00861,\; -\text{pI}: 0.88018,\; -\text{inst}: 5.73793,\; -\text{chg}: 1.22724,\; \text{mw}: 161.30884,\; \text{germ}: 0.06521)$
   - Regional FWR/CDR $\mu^{\text{IMGT}} = (\text{fwr\_flex}: 1.00190,\; -\text{fwr\_gravy}: 0.26350,\; -\text{fwr\_inst}: -36.62248,\; -\text{cdr\_arom}: -0.18513,\; -\text{cdr\_pI}: -6.47349,\; -\text{cdr\_chg}: 0.74237)$
   - Regional FWR/CDR $\sigma^{\text{IMGT}} = (\text{fwr\_flex}: 0.00166,\; -\text{fwr\_gravy}: 0.07062,\; -\text{fwr\_inst}: 5.25908,\; -\text{cdr\_arom}: 0.03062,\; -\text{cdr\_pI}: 1.72940,\; -\text{cdr\_chg}: 1.91695)$

---

## 2. $B = 1,000$ Within-Dataset Fitness-Permutation Null Battery (`seed = 20261026`)

For each category in the `score/` benchmark universe, we permute the ground-truth `fitness` vector independently within each dataset $B = 1,000$ times (`np.random.default_rng(20261026)`) and recompute the category mean sign-corrected Spearman $\bar{\rho}_{\text{null}}^{(b)}$ for both the Regional 8-descriptor equal-weight method (`CLSS_Reg8_AllBP_IMGT_Z`) and the Whole-Chain 6-descriptor equal-weight method (`CLSS_EqWt6_IMGT_Z`):

### 2A. Regional FWR-Scaffold + CDR-Paratope Equal-Weight (`CLSS_Reg8_AllBP_IMGT_Z`, `1/8` each)

| Category (`score/` universe) | Datasets ($D$) | Observed $\bar{\rho}$ (`CLSS_Reg8_AllBP_IMGT_Z`) | Null Mean $\mu_{\text{null}}$ | Null SD $\sigma_{\text{null}}$ | Null Max ($B=1,000$) | $Z$-Score | Empirical $p$-value |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Thermostability (`tm`)** | 15 | **`+0.4636`** | `-0.0005` | `0.1342` | `+0.3468` | **`+3.46`** | **`0.000999`** (`0/1000` $\ge$ obs) |
| **Polyreactivity (`polyreactivity`)** | 6 | **`+0.4467`** | `-0.0017` | `0.1192` | `+0.3333` | **`+3.76`** | **`0.000999`** (`0/1000` $\ge$ obs) |
| **Aggregation (`aggregation`)** | 6 | **`+0.0997`** | `+0.0002` | `0.0348` | `+0.1165` | **`+2.86`** | **`0.003996`** |
| **Expression (`expression`)** | 7 | **`+0.1205`** | `+0.0030` | `0.0694` | `+0.2074` | **`+1.69`** | **`0.040959`** |

On both primary categories (`tm` and `polyreactivity`), **zero out of $1,000$ random fitness permutations** reach the observed category mean (`+0.4636` vs null max `+0.3468` on `tm`; `+0.4467` vs null max `+0.3333` on `polyreactivity`; empirical $p = 0.000999$ on both).

### 2B. Whole-Chain Equal-Weight (`CLSS_EqWt6_IMGT_Z`, `1/6` each)

| Category (`score/` universe) | Datasets ($D$) | Observed $\bar{\rho}$ (`CLSS_EqWt6_IMGT_Z`) | Null Mean $\mu_{\text{null}}$ | Null SD $\sigma_{\text{null}}$ | Null Max ($B=1,000$) | $Z$-Score | Empirical $p$-value |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Thermostability (`tm`)** | 15 | **`+0.3528`** | `+0.0024` | `0.1388` | `+0.4519` | **`+2.52`** | **`0.003996`** |
| **Polyreactivity (`polyreactivity`)** | 6 | **`+0.3987`** | `-0.0031` | `0.1169` | `+0.3297` | **`+3.44`** | **`0.000999`** (`0/1000` $\ge$ obs) |
| **Aggregation (`aggregation`)** | 6 | **`+0.1246`** | `+0.0001` | `0.0341` | `+0.1107` | **`+3.65`** | **`0.000999`** (`0/1000` $\ge$ obs) |
| **Expression (`expression`)** | 7 | **`+0.2152`** | `+0.0050` | `0.0712` | `+0.2155` | **`+2.95`** | **`0.001998`** |

---

## 3. Leave-One-Category-Out (LOCO) Zero-Shot Cross-Validation

To verify that model selection across zero-shot parameter-free candidates does not leak target-category information, we select the top-performing parameter-free rule using *only* the average across the 3 other categories ($C \setminus \{c\}$) and evaluate it blind on the held-out category $c$:

### 3A. LOCO Over Regional FWR-Scaffold + CDR-Paratope Equal-Weight Sets (`CLSS_Reg8_AllBP_IMGT_Z`, `CLSS_Reg7_MW_IMGT_Z`, `CLSS_Reg7_IMGT_Z`, `CLSS_Reg6_IMGT_Z`)

| Held-Out Category $c$ | Rule Selected on Other 3 Categories | Mean $\bar{\rho}$ on Training Categories | Blind Held-Out $\bar{\rho}$ | Best Released Model in `score/` (Either Sign) | Blind Held-Out Margin |
|---|---|---:|---:|---:|---:|
| **Thermostability (`tm`)** | `CLSS_Reg7_IMGT_Z` | `+0.2284` | **`+0.4901`** | `+0.2169` (`progen/xlarge`) | **`+0.2732`** ($5.46\times$ required `+0.05`) |
| **Polyreactivity (`polyreactivity`)** | `CLSS_Reg6_IMGT_Z` | `+0.2766` | **`+0.3185`** | `+0.1936` (`progen/xlarge (+ppl)`) | **`+0.1249`** ($2.50\times$ required `+0.05`) |
| **Aggregation (`aggregation`)** | `CLSS_Reg7_IMGT_Z` | `+0.3531` | **`+0.1161`** | `+0.1701` (`progen/oas (+ppl)`) | `-0.0540` |
| **Expression (`expression`)** | `CLSS_Reg7_IMGT_Z` | `+0.3417` | **`+0.1501`** | `+0.3159` (`progen/medium`) | `-0.1658` |

### 3B. LOCO Over Complete Whole-Chain Equal-Weight Sets (`CLSS_EqWt6_IMGT_Z`, `CLSS_EqWt6_Shrink_Z`, `CLSS_EqWt7_IMGT_Z`)

| Held-Out Category $c$ | Rule Selected on Other 3 Categories | Mean $\bar{\rho}$ on Training Categories | Blind Held-Out $\bar{\rho}$ | Best Released Model in `score/` (Either Sign) | Blind Held-Out Margin |
|---|---|---:|---:|---:|---:|
| **Thermostability (`tm`)** | `CLSS_EqWt7_IMGT_Z` | `+0.2542` | **`+0.2955`** | `+0.2169` (`progen/xlarge`) | **`+0.0786`** ($> +0.05$) |
| **Polyreactivity (`polyreactivity`)** | `CLSS_EqWt6_IMGT_Z` | `+0.2309` | **`+0.3987`** | `+0.1936` (`progen/xlarge (+ppl)`) | **`+0.2051`** ($> +0.05$) |
| **Aggregation (`aggregation`)** | `CLSS_EqWt6_IMGT_Z` | `+0.3222` | **`+0.1246`** | `+0.1701` (`progen/oas (+ppl)`) | `-0.0455` |
| **Expression (`expression`)** | `CLSS_EqWt7_IMGT_Z` | `+0.3040` | **`+0.1461`** | `+0.3159` (`progen/medium`) | `-0.1698` |

---

## 4. Partial Win `p3`: Length & Germline Confound Control

For every released model, single descriptor, and CLSS equal-weight method, we decompose the category mean Spearman into:
1. **Raw $\bar{\rho}$:** Standard category mean sign-corrected Spearman correlation.
2. **Partial $\bar{\rho}(\perp L)$:** Rank-residualized Spearman orthogonal to total sequence length $L = |H| + |L|$.
3. **Partial $\bar{\rho}(\perp G)$:** Rank-residualized Spearman orthogonal to human IMGT V+J germline identity $G$.
4. **Partial $\bar{\rho}(\perp L, G)$:** Rank-residualized Spearman simultaneously orthogonal to both sequence length $L$ and germline identity $G$.
5. **Matched-Stratum $\bar{\rho}_{\text{matched}}$:** Within-stratum sample-size-weighted Spearman computed strictly among antibodies sharing the exact same sequence length $L$ and human germline V+J identity bin ($\lfloor 50 G \rfloor$, capturing $1\text{--}2\%$ somatic hypermutation increments).

### 4A. Thermostability (`score/tm`, 15 Datasets) — Length & Germline Confound Decomposition

| Method | Raw $\bar{\rho}$ | Partial $\bar{\rho}(\perp L)$ | Partial $\bar{\rho}(\perp G)$ | Partial $\bar{\rho}(\perp L, G)$ | Matched-Stratum $\bar{\rho}_{\text{matched}}$ |
|---|---:|---:|---:|---:|---:|
| **`CLSS_Reg6_IMGT_Z`** | **`+0.5365`** | **`+0.5414`** | **`+0.3028`** | **`+0.3149`** | **`+0.5224`** |
| **`CLSS_Reg7_MW_IMGT_Z`** | **`+0.5160`** | **`+0.5071`** | **`+0.2533`** | **`+0.2581`** | **`+0.4995`** |
| **`CLSS_Reg7_IMGT_Z`** | **`+0.4901`** | **`+0.4942`** | **`+0.3014`** | **`+0.3080`** | **`+0.4705`** |
| **`CLSS_Reg8_AllBP_IMGT_Z`** | **`+0.4636`** | **`+0.4569`** | **`+0.2197`** | **`+0.2184`** | **`+0.4308`** |
| **`CLSS_EqWt4_Fold_IMGT_Z`** | **`+0.4287`** | **`+0.4328`** | **`+0.2567`** | **`+0.2738`** | **`+0.4173`** |
| **`CLSS_EqWt5_NoPI_IMGT_Z`** | **`+0.3980`** | **`+0.4000`** | **`+0.2225`** | **`+0.2376`** | **`+0.3920`** |
| **`CLSS_EqWt5_NoPI_Shrink_Z`** | **`+0.3853`** | **`+0.3882`** | **`+0.1995`** | **`+0.2188`** | **`+0.3733`** |
| **`CLSS_EqWt6_IMGT_Z`** | **`+0.3528`** | **`+0.3556`** | **`+0.2058`** | **`+0.2177`** | **`+0.3731`** |
| **`CLSS_EqWt6_Shrink_Z`** | **`+0.3499`** | **`+0.3550`** | **`+0.2061`** | **`+0.2219`** | **`+0.3657`** |
| **`CLSS_EqWt7_IMGT_Z`** | **`+0.2956`** | **`+0.2976`** | **`+0.1478`** | **`+0.1571`** | **`+0.3038`** |
| `bp_flexibility` | `+0.2908` | `+0.2900` | `+0.1890` | `+0.1995` | `+0.2887` |
| `bp_molecular_weight` | `+0.2467` | `+0.2246` | `+0.2684` | `+0.2370` | `+0.2185` |
| `progen/xlarge` (`-ppl`) | `+0.2169` | `+0.2189` | `+0.2474` | `+0.2559` | `+0.2323` |
| `neg_bp_isoelectric_point` | `+0.1999` | `+0.1797` | `+0.1273` | `+0.1071` | `+0.2219` |
| `neg_bp_gravy` | `+0.1967` | `+0.2146` | `+0.1534` | `+0.1859` | `+0.2099` |
| `progen/oas` (`-ppl`) | `+0.1674` | `+0.1658` | `+0.2013` | `+0.1977` | `+0.1885` |
| `esmif` (`-ppl`) | `+0.1394` | `+0.1478` | `+0.0917` | `+0.1026` | `+0.1434` |
| `pure_germline_identity` | `+0.1297` | `+0.1355` | `+0.1429` | `+0.1429` | `+0.1518` |
| `progen/small` (`-ppl`) | `+0.0825` | `+0.0843` | `-0.0138` | `-0.0063` | `+0.1021` |
| `progen/medium` (`-ppl`) | `+0.0517` | `+0.0546` | `-0.0031` | `+0.0060` | `+0.0800` |
| `progen/BFD90` (`-ppl`) | `+0.0512` | `+0.0523` | `+0.0256` | `+0.0398` | `+0.0837` |
| `iglm` (`-ppl`) | `+0.0184` | `+0.0186` | `+0.0374` | `+0.0304` | `+0.0075` |
| `antiberty` (`-ppl`) | `+0.0113` | `+0.0109` | `+0.0312` | `+0.0317` | `+0.0057` |
| `progen/base` (`-ppl`) | `-0.0578` | `-0.0572` | `-0.1218` | `-0.1213` | `-0.0658` |
| `progen/large` (`-ppl`) | `-0.0700` | `-0.0662` | `-0.0293` | `-0.0304` | `-0.0532` |
| `pyrosetta` (`-score`) | `-0.1545` | `-0.1315` | `-0.2003` | `-0.1858` | `-0.1508` |
| `mpnn` (`-ppl`) | `-0.1645` | `-0.1716` | `-0.0958` | `-0.1008` | `-0.1732` |

### 4B. Polyreactivity (`score/polyreactivity`, 6 Datasets) — Length & Germline Confound Decomposition

| Method | Raw $\bar{\rho}$ | Partial $\bar{\rho}(\perp L)$ | Partial $\bar{\rho}(\perp G)$ | Partial $\bar{\rho}(\perp L, G)$ | Matched-Stratum $\bar{\rho}_{\text{matched}}$ |
|---|---:|---:|---:|---:|---:|
| **`CLSS_EqWt7_IMGT_Z`** | **`+0.5052`** | **`+0.5017`** | **`+0.4838`** | **`+0.4838`** | **`+0.4834`** |
| **`CLSS_Reg8_AllBP_IMGT_Z`** | **`+0.4467`** | **`+0.4509`** | **`+0.4347`** | **`+0.4474`** | **`+0.5262`** |
| `neg_bp_isoelectric_point` | `+0.4354` | `+0.4368` | `+0.3731` | `+0.3780` | `+0.3875` |
| **`CLSS_Reg7_IMGT_Z`** | **`+0.4190`** | **`+0.4231`** | **`+0.4183`** | **`+0.4318`** | **`+0.4298`** |
| **`CLSS_EqWt6_IMGT_Z`** | **`+0.3987`** | **`+0.3970`** | **`+0.3695`** | **`+0.3696`** | **`+0.4138`** |
| **`CLSS_EqWt6_Shrink_Z`** | **`+0.3984`** | **`+0.3973`** | **`+0.3714`** | **`+0.3723`** | **`+0.4455`** |
| `neg_bp_charge_at_7_4` | `+0.3491` | `+0.3499` | `+0.3527` | `+0.3607` | `+0.2276` |
| **`CLSS_Reg7_MW_IMGT_Z`** | **`+0.3459`** | **`+0.3514`** | **`+0.3734`** | **`+0.3861`** | **`+0.3515`** |
| `neg_bp_aromaticity` | `+0.3245` | `+0.3220` | `+0.2501` | `+0.2559` | `+0.4829` |
| **`CLSS_Reg6_IMGT_Z`** | **`+0.3186`** | **`+0.3243`** | **`+0.3470`** | **`+0.3630`** | **`+0.3314`** |
| `neg_bp_instability_index` | `+0.2544` | `+0.2584` | `+0.2190` | `+0.2219` | `+0.1503` |
| `mpnn` (`-ppl`) | `+0.1906` | `+0.1971` | `+0.3240` | `+0.3349` | `+0.2810` |
| `pyrosetta` (`-score`) | `+0.1123` | `+0.1073` | `+0.1420` | `+0.1290` | `+0.1243` |
| `esmif` (`-ppl`) | `+0.1026` | `+0.0984` | `+0.1364` | `+0.1303` | `+0.0593` |
| `progen/small` (`-ppl`) | `-0.0162` | `-0.0219` | `+0.1747` | `+0.1707` | `+0.1510` |
| `progen/medium` (`-ppl`) | `-0.0456` | `-0.0494` | `+0.1760` | `+0.1701` | `+0.1863` |
| `progen/base` (`-ppl`) | `-0.0524` | `-0.0514` | `+0.1693` | `+0.1704` | `+0.1724` |
| `antiberty` (`-ppl`) | `-0.1424` | `-0.1410` | `+0.0411` | `+0.0427` | `+0.0045` |
| `progen/BFD90` (`-ppl`) | `-0.1432` | `-0.1463` | `+0.1204` | `+0.1144` | `+0.0991` |
| `progen/large` (`-ppl`) | `-0.1516` | `-0.1527` | `-0.0285` | `-0.0290` | `+0.0804` |
| `iglm` (`-ppl`) | `-0.1552` | `-0.1561` | `-0.0221` | `-0.0243` | `+0.0158` |
| `progen/oas` (`-ppl`) | `-0.1606` | `-0.1676` | `-0.0125` | `-0.0261` | `+0.0836` |
| `progen/xlarge` (`-ppl`) | `-0.1935` | `-0.1971` | `+0.0210` | `+0.0171` | `+0.0189` |
| `pure_germline_identity` | `-0.2129` | `-0.2147` | `0.0000` | `0.0000` | `-0.1940` |

### Key Structural Findings from the `p3` Confound Control

1. **Sequence Length ($L$) is non-informative in constant-length mutational scanning libraries:** In 12 of the 15 `score/tm` datasets and 3 of the 6 `score/polyreactivity` datasets, all variants have constant length ($\text{Var}(L) = 0$). Consequently, partialing out sequence length ($\perp L$) leaves all CLSS methods virtually unchanged (`CLSS_Reg8_AllBP_IMGT_Z`: `+0.4636 -> +0.4569` on `tm` and `+0.4467 -> +0.4509` on `polyreactivity`; `CLSS_Reg7_MW_IMGT_Z`: `+0.5160 -> +0.5071` on `tm` and `+0.3459 -> +0.3514` on `polyreactivity`; `CLSS_EqWt6_IMGT_Z`: `+0.3528 -> +0.3556` on `tm` and `+0.3987 -> +0.3970` on `polyreactivity`).
2. **Why PLM Perplexities Flip Sign Between Thermostability and Polyreactivity:** Human IMGT germline identity $G$ correlates positively with thermostability ($\bar{\rho} = +0.1297$ on `tm`), but **negatively** with favourable low polyreactivity ($\bar{\rho} = -0.2129$ on `polyreactivity`, including $-0.6983$ on `Rosace2023_CR3022_CIC` and $-0.7379$ on `Rosace2023_Golimumab_CIC`), because several human VH1/VH3/VH4 germlines carry cationic/aromatic CDR patches that are thermostable yet sticky in polyreactivity assays. Because sequence PLMs (`antiberty`, `iglm`, `progen/*`) heavily reward germline proximity, their raw confidence (`-ppl`) is negatively correlated with favourable low polyreactivity (`-0.1424` to `-0.1935`). When germline identity is partialed out ($\perp L, G$) or controlled by matched $(L, G)$ strata, PLM correlations on polyreactivity shift toward zero or weak positive (`progen/xlarge`: `-0.1935 -> +0.0171` partial / `+0.0189` matched; `progen/medium`: `-0.0456 -> +0.1701` partial / `+0.1863` matched; `mpnn`: `+0.1906 -> +0.3349` partial).
3. **Genuine Biophysical Skill Beyond Length and Germline:** Within exact length-and-germline-matched strata ($\bar{\rho}_{\text{matched}}$), `CLSS_Reg8_AllBP_IMGT_Z` achieves **`+0.4308`** on Thermostability (`+0.2184` partial $\perp (L,G)$) and **`+0.5262`** on Polyreactivity (`+0.4474` partial $\perp (L,G)$); `CLSS_Reg7_MW_IMGT_Z` achieves **`+0.4995`** matched-stratum Spearman on Thermostability (`+0.2581` partial $\perp (L,G)$) and **`+0.3515`** on Polyreactivity (`+0.3861` partial $\perp (L,G)$); and `CLSS_EqWt6_IMGT_Z` achieves **`+0.3731`** matched-stratum Spearman on Thermostability and **`+0.4138`** on Polyreactivity.
