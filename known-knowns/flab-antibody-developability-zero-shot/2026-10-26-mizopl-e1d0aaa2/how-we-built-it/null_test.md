# Null-Test & Confound-Control Battery (`how-we-built-it/null_test.md`)

- **Target ID:** `flab-antibody-developability-zero-shot`
- `controls`: 1000
- **Single Frozen Zero-Shot Method:** **`CLSS_Reg8_AllBP_IMGT_Z`** (frozen at `2026-10-26T00:26:00Z` in commit `654c23f056b932c310723f591bc3fec89102ad73`; see `how-we-built-it/PREREG.md`; all other variants reported as exploratory ablations)
- **Claim Scope (`status: CONFIRMED_PARTIAL`):** **Partial Wins `p2` and `p3`** (Full Win, Binding, and `p1` are **not claimed**)
- `best_control`: +0.3468 (`CLSS_Reg8_AllBP_IMGT_Z` on `score/tm`, $B=1,000$ within-dataset fitness permutations; `+0.3333` on `score/polyreactivity`)
- `real`: +0.4636 (`CLSS_Reg8_AllBP_IMGT_Z` on `score/tm`; `+0.4467` on `score/polyreactivity`)
- `command`: `sh verify-it-yourself/run_checks.sh`
- `real_beats_all_controls`: yes
- **Verification Script:** `verify-it-yourself/verify.py` (`sha256: 3583f9700c89ba0c00bf1d9eaaaaca0566166859880727be705d7b5acf8fbd18`) and `how-we-built-it/verify_full_benchmark.py` (`sha256: 51a3a05a27708532df677cb5c49043998eff57b8fa6edfc12a85b841f50dcf45`)
- **Machine-Verified Certificate:** `object/certificate.json` (`sha256: b6be3abe5d0dcff18fcf18d8e7a16f64164d434290274613f79b76f80f598eb6`)

---

## 1. Zero-Shot Integrity Audit (No `fitness` Reads, Zero Hand-Tuned Weights)

1. **Zero `fitness` reads during scoring:** All CLSS score functions (`score_imgt_z_df`, `score_shrink_z_df`, `raw_descriptors`) read exclusively the `heavy` and `light` amino-acid sequence columns (`reads_fitness_column = false`). The `fitness` column is accessed only by the external evaluator after the full per-antibody score vector $\mathbf{x}$ has been computed and frozen.
2. **Zero hand-tuned weights (`1:1:...:1`):**
   - In **`CLSS_Reg8_AllBP_IMGT_Z`** (the complete 8-descriptor Regional FWR-Scaffold + CDR-Paratope formulation), all 7 Biopython descriptors from the FLAb benchmark (`flexibility`, `-gravy`, `-instability_index` on the $\beta$-sandwich Framework `FWR1–4`; `-aromaticity`, `-isoelectric_point`, `-charge_at_7_4` on the hypervariable `CDR1–3` loops; plus `molecular_weight`) and human IMGT germline sequence identity (`germ`) receive strictly equal weight $w_k = 1/8$.
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

On both `tm` and `polyreactivity`, **zero out of $1,000$ random fitness permutations** reach the observed category mean (`+0.4636` vs null max `+0.3468` on `tm`; `+0.4467` vs null max `+0.3333` on `polyreactivity`; empirical $p = 0.000999$ on both).

### 2B. Whole-Chain Equal-Weight (`CLSS_EqWt6_IMGT_Z`, `1/6` each, Exploratory)

| Category (`score/` universe) | Datasets ($D$) | Observed $\bar{\rho}$ (`CLSS_EqWt6_IMGT_Z`) | Null Mean $\mu_{\text{null}}$ | Null SD $\sigma_{\text{null}}$ | Null Max ($B=1,000$) | $Z$-Score | Empirical $p$-value |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Thermostability (`tm`)** | 15 | **`+0.3528`** | `+0.0024` | `0.1388` | `+0.4519` | **`+2.52`** | **`0.003996`** |
| **Polyreactivity (`polyreactivity`)** | 6 | **`+0.3987`** | `-0.0031` | `0.1169` | `+0.3297` | **`+3.44`** | **`0.000999`** (`0/1000` $\ge$ obs) |
| **Aggregation (`aggregation`)** | 6 | **`+0.1246`** | `+0.0001` | `0.0341` | `+0.1107` | **`+3.65`** | **`0.000999`** (`0/1000` $\ge$ obs) |
| **Expression (`expression`)** | 7 | **`+0.2152`** | `+0.0050` | `0.0712` | `+0.2155` | **`+2.95`** | **`0.001998`** |

---

## 3. Claimed Partial Win `p3`: Length & Germline Confound Control

For every released model, single descriptor, and CLSS equal-weight method, we decompose the category mean Spearman into:
1. **Raw $\bar{\rho}$:** Standard category mean sign-corrected Spearman correlation.
2. **Partial $\bar{\rho}(\perp L)$:** Rank-residualized Spearman orthogonal to total sequence length $L = |H| + |L|$.
3. **Partial $\bar{\rho}(\perp G)$:** Rank-residualized Spearman orthogonal to human IMGT V+J germline identity $G$.
4. **Partial $\bar{\rho}(\perp L, G)$:** Rank-residualized Spearman simultaneously orthogonal to both sequence length $L$ and germline identity $G$.
5. **Matched-Stratum $\bar{\rho}_{\text{matched}}$:** Within-stratum sample-size-weighted Spearman computed strictly among antibodies sharing the exact same sequence length $L$ and human germline V+J identity bin ($\lfloor 50 G \rfloor$, capturing $1\text{--}2\%$ somatic hypermutation increments).

### 3A. Thermostability (`score/tm`, 15 Datasets) — Length & Germline Confound Decomposition

| Method | Raw $\bar{\rho}$ | Partial $\bar{\rho}(\perp L)$ | Partial $\bar{\rho}(\perp G)$ | Partial $\bar{\rho}(\perp L, G)$ | Matched-Stratum $\bar{\rho}_{\text{matched}}$ |
|---|---:|---:|---:|---:|---:|
| **`CLSS_Reg8_AllBP_IMGT_Z` (Single Frozen)** | **`+0.4636`** | **`+0.4569`** | **`+0.2197`** | **`+0.2184`** | **`+0.4308`** |
| `CLSS_Reg6_IMGT_Z` (Exploratory) | `+0.5365` | `+0.5414` | `+0.3028` | `+0.3149` | `+0.5224` |
| `CLSS_Reg7_MW_IMGT_Z` (Exploratory) | `+0.5160` | `+0.5071` | `+0.2533` | `+0.2581` | `+0.4995` |
| `CLSS_Reg7_IMGT_Z` (Exploratory) | `+0.4901` | `+0.4942` | `+0.3014` | `+0.3080` | `+0.4705` |
| `CLSS_EqWt6_IMGT_Z` (Exploratory) | `+0.3528` | `+0.3556` | `+0.2058` | `+0.2177` | `+0.3731` |
| `bp_flexibility` | `+0.2908` | `+0.2900` | `+0.1890` | `+0.1995` | `+0.2887` |
| `progen/xlarge` (`-ppl`) | `+0.2169` | `+0.2189` | `+0.2474` | `+0.2559` | `+0.2323` |
| `progen/oas` (`-ppl`) | `+0.1674` | `+0.1658` | `+0.2013` | `+0.1977` | `+0.1885` |
| `esmif` (`-ppl`) | `+0.1394` | `+0.1478` | `+0.0917` | `+0.1026` | `+0.1434` |
| `pure_germline_identity` | `+0.1297` | `+0.1355` | `+0.1429` | `+0.1429` | `+0.1518` |

### 3B. Polyreactivity (`score/polyreactivity`, 6 Datasets) — Length & Germline Confound Decomposition

| Method | Raw $\bar{\rho}$ | Partial $\bar{\rho}(\perp L)$ | Partial $\bar{\rho}(\perp G)$ | Partial $\bar{\rho}(\perp L, G)$ | Matched-Stratum $\bar{\rho}_{\text{matched}}$ |
|---|---:|---:|---:|---:|---:|
| **`CLSS_Reg8_AllBP_IMGT_Z` (Single Frozen)** | **`+0.4467`** | **`+0.4509`** | **`+0.4347`** | **`+0.4474`** | **`+0.5262`** |
| `CLSS_EqWt7_IMGT_Z` (Exploratory) | `+0.5052` | `+0.5017` | `+0.4838` | `+0.4838` | `+0.4834` |
| `neg_bp_isoelectric_point` | `+0.4354` | `+0.4368` | `+0.3731` | `+0.3780` | `+0.3875` |
| `CLSS_Reg7_IMGT_Z` (Exploratory) | `+0.4190` | `+0.4231` | `+0.4183` | `+0.4318` | `+0.4298` |
| `CLSS_EqWt6_IMGT_Z` (Exploratory) | `+0.3987` | `+0.3970` | `+0.3695` | `+0.3696` | `+0.4138` |
| `CLSS_Reg7_MW_IMGT_Z` (Exploratory) | `+0.3459` | `+0.3514` | `+0.3734` | `+0.3861` | `+0.3515` |
| `mpnn` (`-ppl`) | `+0.1906` | `+0.1971` | `+0.3240` | `+0.3349` | `+0.2810` |
| `pyrosetta` (`-score`) | `+0.1123` | `+0.1073` | `+0.1420` | `+0.1290` | `+0.1243` |
| `esmif` (`-ppl`) | `+0.1026` | `+0.0984` | `+0.1364` | `+0.1303` | `+0.0593` |
| `progen/xlarge` (`-ppl`) | `-0.1935` | `-0.1971` | `+0.0210` | `+0.0171` | `+0.0189` |
| `pure_germline_identity` | `-0.2129` | `-0.2147` | `0.0000` | `0.0000` | `-0.1940` |
