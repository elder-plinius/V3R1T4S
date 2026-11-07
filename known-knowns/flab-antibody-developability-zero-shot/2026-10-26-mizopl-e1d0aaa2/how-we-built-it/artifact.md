# Claim Artifact: Parameter-Free Regional FWR-Scaffold & CDR-Paratope IMGT-Standardized Biophysical Zero-Shot Developability Scoring on FLAb (`flab-antibody-developability-zero-shot`)

- **Target ID:** `flab-antibody-developability-zero-shot`
- **Category:** `biology` | **Kind:** `standard` | **Direction:** `max` | **Null Test:** `required`
- **Claim Status:** `CONFIRMED_PARTIAL` (`claim_type: partial_win`, `partial_win: p2, p3`; Full Win, Binding, and `p1` are **not claimed**).
- **Benchmark Source:** Chungyoun & Gray, *"FLAb: Benchmarking deep learning methods for antibody fitness prediction"*, *bioRxiv* `10.64898/2025.12.27.696706` (Dec 2025); repository `https://github.com/Graylab/FLAb` at commit `e05e3f0135783ffb7de412df6a1467e7a0031911`.
- **Verification Script:** `how-we-built-it/verify_full_benchmark.py` (`sha256: 51a3a05a27708532df677cb5c49043998eff57b8fa6edfc12a85b841f50dcf45`, `45.95s` wall time across `54,131` unique antibody pairs and `190` upstream FLAb CSVs; offline certificate verifier: `verify-it-yourself/verify.py`, `sha256: 3583f9700c89ba0c00bf1d9eaaaaca0566166859880727be705d7b5acf8fbd18`).
- **Machine-Verified Certificate:** `object/certificate.json` (`sha256: b6be3abe5d0dcff18fcf18d8e7a16f64164d434290274613f79b76f80f598eb6`)
- **Per-Antibody Score Files (`109,236` Total Rows Across `172` Dataset Evaluations, Zero Sequence Columns):**
  - `object/predictions_tm_polyreactivity.csv` (`4,499` rows across `76` dataset evaluations in `score/tm` [15], `score/polyreactivity` [6], `data/thermostability` [21], `data/polyreactivity` [25], and `data/pharmacokinetics` [9]; `sha256: 63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e`)
  - `object/predictions_binding_part1..8.csv` (`104,737` rows across `96` binding dataset evaluations: `16` `score/binding` [`6,959` rows] + `80` `data/binding` [`97,778` rows]; `sha256: 8e748b57...` through `f41772d0...`)
- **Single Frozen Method:** **`CLSS_Reg8_AllBP_IMGT_Z`** (frozen at `2026-10-26T00:26:00Z` in commit `654c23f056b932c310723f591bc3fec89102ad73`, see `how-we-built-it/PREREG.md`; all other variants in this technical note are reported strictly as exploratory ablations).

---

## 1. Executive Summary of Claimed Partial Wins (`p2`, `p3`) and Non-Claimed Categories (`Binding`, `p1`, Full Win)

We evaluate a strictly parameter-free, zero-shot antibody developability scoring family centered on **Regional Antibody Domain Biophysics (`CLSS_Reg8_AllBP_IMGT_Z`)** that:
1. **Never reads the `fitness` column** of any dataset in any category (`reads_fitness_column = false`), and uses **zero hand-tuned weights (`1:1:...:1`)** and **zero ad-hoc position rules** (`uses_hand_tuned_weights = false`, `uses_ad_hoc_position_rules = false`).
2. **Claim Scope (`status: CONFIRMED_PARTIAL`, `partial_win: p2, p3`):**
   - **Why Full Win, `p1`, and `Binding` are NOT claimed (`how-we-built-it/PREREG.md`):**
     - `CLSS_Reg8_AllBP_IMGT_Z` was defined at `00:13Z` after looking at per-dataset results on `Wittrup2017_CST_Tm` in `score/tm`, and its predecessor `CLSS_EqWt6_IMGT_Z` had been scored on `score/polyreactivity` at `23:51Z`. Thus Thermostability (`p1` and main category claim) and Polyreactivity are **not claimed** as a Full Win.
     - On Aggregation (`+0.0997` vs `+0.1701`), Expression (`+0.1205` vs `+0.3159`), and Immunogenicity (`-0.2584` vs `+0.0890`) in `score/`, `CLSS_Reg8_AllBP_IMGT_Z` is `0.0704`, `0.1954`, and `0.3474` below the best released method; Pharmacokinetics (`+0.2287` on `data/pharmacokinetics`) has no `score/` files.
     - On **Binding** (`16` `score/binding` datasets and `80` `data/binding` CSVs, evaluated blind with the unchanged rule from commit `654c23f0`), `CLSS_Reg8_AllBP_IMGT_Z` achieves **`-0.0060`** (`+0.0060` for $+K_d$) on `score/binding` vs best released `iglm = 0.1742` (`margin = -0.1802`), **`-0.0987`** (`36/80 > 0`) across all `80` `data/binding` CSVs, **`-0.1123`** (`5/12 > 0`) on the `12` primary `score/`-mapped `data/binding` CSVs (`-0.1640` [`5/15 > 0`] on the `15` study-mapped CSVs), and **`-0.0964`** (`31/68 > 0`) on the `68` excluded `data/binding` CSVs (`-0.0837` [`31/65 > 0`] on the `65` excluded CSVs). Therefore **Binding is not claimed**.
   - **Claimed Partial Win `p2` (Sign Consistency $\ge 80\%$):**
     - The single frozen method **`CLSS_Reg8_AllBP_IMGT_Z`** is positively correlated on **`14/15 = 93.33%`** of `score/tm` datasets, **`16/20 = 80.00%`** of standard `data/thermostability` datasets, **`6/6 = 100.00%`** of `score/polyreactivity` datasets, and **`4/4 = 100.00%`** of untouched `data/expression` datasets (all $\ge 80\%$).
   - **Claimed Partial Win `p3` (Length & Germline Confound Control):**
     - Full rank-residualized partial Spearman ($\perp L$, $\perp G$, $\perp (L,G)$) and exact $(L, G)$ matched-stratum Spearman ($\bar{\rho}_{\text{matched}}$) across all 12 released models, 9 single descriptors, and 10 CLSS parameter-free methods in `object/certificate.json` (`+0.4308` matched-stratum on `score/tm` and `+0.5262` on `score/polyreactivity` for `CLSS_Reg8_AllBP_IMGT_Z`).

---

## 2. Mathematical Formulation of Regional FWR-Scaffold & CDR-Paratope Scoring

### 2A. Conserved Immunoglobulin Landmark Partitioning (`partition_fwr_cdr`)

Every immunoglobulin variable domain ($V_H$ or $V_L$) is partitioned into its four $\beta$-sheet framework segments ($\text{FWR} = \text{FWR1} \mathbin{\|} \text{FWR2} \mathbin{\|} \text{FWR3} \mathbin{\|} \text{FWR4}$) and three hypervariable complementarity-determining loops ($\text{CDR} = \text{CDR1} \mathbin{\|} \text{CDR2} \mathbin{\|} \text{CDR3}$) using the four invariant sequence landmarks shared across vertebrate immunoglobulins (Kabat et al. 1991; Lefranc et al. 2003 IMGT):
1. **First Disulfide Cysteine (`Cys22/23`):** Located at index $c_1 \in [15, 30]$ (`FWR1` $= S[0:c_1+1]$).
2. **Conserved Tryptophan (`Trp36/41`):** First `W` located $10\text{--}22$ residues downstream of $c_1$, defining `CDR1` $= S[c_1+1 : w]$ and `FWR2` $= S[w : w+14]$.
3. **Second Disulfide Cysteine (`Cys92/104`):** Cysteine located near the C-terminus ($[L-45, L-8]$), defining `CDR2` $= S[w+14 : w+24]$ and `FWR3` $= S[w+24 : c_2+1]$.
4. **Conserved J-Segment Anchor (`WGQG / FGQG / WGRG / FGGG`):** Located at $j > c_2$, defining `CDR3` $= S[c_2+1 : j]$ and `FWR4` $= S[j : L]$.

Concatenating the heavy and light framework segments yields $S_{\text{FWR}} = \text{FWR}(H) \mathbin{\|} \text{FWR}(L)$ and concatenating the CDR loops yields $S_{\text{CDR}} = \text{CDR}(H) \mathbin{\|} \text{CDR}(L)$.

### 2B. Regional Biophysical Descriptors and External IMGT Standardization

Let $\mathcal{R}_{\text{IMGT}}$ denote the $24 \times 18 = 432$ human IMGT germline Fv pairs. Each descriptor $f_k$ is standardized exclusively by its mean $\mu_k^{\text{IMGT}}$ and standard deviation $\sigma_k^{\text{IMGT}}$ on $\mathcal{R}_{\text{IMGT}}$, $z_k(H, L) = (f_k(H, L) - \mu_k^{\text{IMGT}}) / \sigma_k^{\text{IMGT}}$:
- **Framework Scaffold Descriptors (governing $\beta$-sandwich thermal unfolding $T_m$):**
  1. $f_{\text{fwr\_flex}}(H, L) = \text{VihinenFlexibility}(S_{\text{FWR}})$ ($\mu = 1.00190, \sigma = 0.00166$)
  2. $f_{\text{neg\_fwr\_gravy}}(H, L) = -\text{GRAVY}_{\text{KD}}(S_{\text{FWR}})$ ($\mu = 0.26350, \sigma = 0.07062$)
  3. $f_{\text{neg\_fwr\_inst}}(H, L) = -\text{InstabilityIndex}_{\text{Guruprasad}}(S_{\text{FWR}})$ ($\mu = -36.62248, \sigma = 5.25908$)
- **CDR Paratope Descriptors (governing paratope stickiness, self-association, and polyreactivity; Raybould et al. *PNAS* 2019 TAP):**
  4. $f_{\text{neg\_cdr\_arom}}(H, L) = -\text{Aromaticity}_{\text{Lobry}}(S_{\text{CDR}})$ ($\mu = -0.18513, \sigma = 0.03062$)
  5. $f_{\text{neg\_cdr\_pI}}(H, L) = -\text{pI}_{\text{Bjellqvist}}(S_{\text{CDR}})$ ($\mu = -6.47349, \sigma = 1.72940$)
  6. $f_{\text{neg\_cdr\_chg}}(H, L) = -\text{ChargeAt7.4}_{\text{Bjellqvist}}(S_{\text{CDR}})$ ($\mu = 0.74237, \sigma = 1.91695$)
- **Global Domain Descriptors:**
  7. $f_{\text{mw}}(H, L) = \text{MolecularWeight}(S) / (1 + \mathbb{I}[|L| > 0])$ ($\mu = 11821.96976, \sigma = 161.30884$)
  8. $f_{\text{germ}}(H, L) = \text{IMGTGermlineIdentity}(H, L)$ ($\mu = 0.75307, \sigma = 0.06521$)

The parameter-free regional zero-shot score is the simple arithmetic average ($1/8$ equal weight) of these IMGT $Z$-scores:
$$\text{CLSS\_Reg8\_AllBP\_IMGT\_Z}(H, L) = \frac{1}{8}\Big(z_{\text{fwr\_flex}} + z_{\text{neg\_fwr\_gravy}} + z_{\text{neg\_fwr\_inst}} + z_{\text{neg\_cdr\_arom}} + z_{\text{neg\_cdr\_pI}} + z_{\text{neg\_cdr\_chg}} + z_{\text{mw}} + z_{\text{germ}}\Big)$$

---

## 3. Unweighted AND Sample-Size-Weighted Comparison Across `score/` Categories (`tm`, `polyreactivity`, `binding`)

### 3A. Thermostability (`score/tm`, 15 Datasets; `p1` and Full Win Not Claimed)

| Method | Type | Unweighted Mean $\bar{\rho}$ | Pos (`>0`) | $\bar{\rho}_{N \ge 10}$ (6 ds) | $\bar{\rho}_{\sqrt{N}}$ | $\bar{\rho}_{N}$ | `Wittrup2017_CST_Tm` ($N=137$) |
|---|---|---:|---:|---:|---:|---:|---:|
| **`CLSS_Reg8_AllBP_IMGT_Z` (Regional All 8)** | **Single Frozen (`1/8`)** | **`+0.4636`** | **`14/15` (`93.3%`)** | **`+0.2106`** | **`+0.3001`** | **`+0.1666`** | **`+0.0620`** |
| `CLSS_Reg6_IMGT_Z` (Regional 6-desc) | Exploratory Ablation (`1/6`) | `+0.5365` | `14/15` (`93.3%`) | `+0.2328` | `+0.3451` | `+0.1683` | `+0.0160` |
| `CLSS_Reg7_MW_IMGT_Z` (Regional 7-desc) | Exploratory Ablation (`1/7`) | `+0.5160` | `15/15` (`100.0%`) | `+0.2272` | `+0.3426` | `+0.1911` | `+0.0598` |
| `CLSS_Reg7_IMGT_Z` (Regional 7-desc) | Exploratory Ablation (`1/7`) | `+0.4901` | `13/15` (`86.7%`) | `+0.2236` | `+0.3122` | `+0.1577` | `+0.0360` |
| `CLSS_EqWt6_IMGT_Z` (Whole-Chain 6) | Exploratory Ablation (`1/6`) | `+0.3528` | `11/15` (`73.3%`) | `+0.2470` | `+0.2542` | `+0.1328` | `-0.0028` |
| `progen/xlarge` (`-ppl`) | Released General PLM (3B) | `+0.2169` | `10/15` (`66.7%`) | `+0.0173` | `+0.0964` | `+0.0414` | `+0.0743` |
| `progen/oas` (`-ppl`) | Released Ab PLM | `+0.1674` | `9/15` (`60.0%`) | `-0.0755` | `+0.0338` | `-0.0368` | `-0.0512` |
| `esmif` (`-ppl`) | Released Inverse Folding | `+0.1394` | `9/15` (`60.0%`) | `+0.1800` | `+0.1427` | `+0.1882` | `+0.3516` |
| `bp_flexibility` | Single Biopython Scale | `+0.2908` | `11/15` (`73.3%`) | `+0.2511` | `+0.1954` | `+0.0630` | `-0.1454` |

### 3B. Polyreactivity (`score/polyreactivity`, 6 Datasets; Full Win Not Claimed)

| Method | Type | Unweighted Mean $\bar{\rho}$ | Pos (`>0`) | $\bar{\rho}_{N \ge 10}$ (4 ds) | $\bar{\rho}_{\sqrt{N}}$ | $\bar{\rho}_{N}$ | `Wittrup2017_CST` Mean ($N=137\times 3$) |
|---|---|---:|---:|---:|---:|---:|---:|
| **`CLSS_Reg8_AllBP_IMGT_Z` (Regional All 8)** | **Single Frozen (`1/8`)** | **`+0.4467`** | **`6/6` (`100.0%`)** | **`+0.2379`** | **`+0.3073`** | **`+0.2569`** | **`+0.2418`** |
| `CLSS_EqWt7_IMGT_Z` (Whole-Chain 7) | Exploratory Ablation (`1/7`) | `+0.5052` | `6/6` (`100.0%`) | `+0.3257` | `+0.3301` | `+0.2568` | `+0.2284` |
| `CLSS_EqWt6_IMGT_Z` (Whole-Chain 6) | Exploratory Ablation (`1/6`) | `+0.3987` | `6/6` (`100.0%`) | `+0.2088` | `+0.2398` | `+0.1771` | `+0.1546` |
| `CLSS_Reg7_MW_IMGT_Z` (Regional 7-desc) | Exploratory Ablation (`1/7`) | `+0.3459` | `6/6` (`100.0%`) | `+0.1867` | `+0.2297` | `+0.1870` | `+0.1735` |
| `mpnn` (`-ppl`) | Released Inverse Folding | `+0.1906` | `4/6` (`66.7%`) | `+0.1324` | `+0.1054` | `+0.0640` | `+0.0453` |
| `progen/xlarge` (`-ppl` / `+ppl`) | Released General PLM (3B) | `-0.1936` / `+0.1936` | `1/6` / `5/6` | `-0.1868` | `-0.1771` | `-0.1705` | `-0.1677` / `+0.1677` |
| `neg_bp_isoelectric_point` | Single Biopython Scale | `+0.4354` | `6/6` (`100.0%`) | `+0.2510` | `+0.3179` | `+0.2755` | `+0.2631` |

### 3C. Binding (`score/binding` 16 Datasets & `data/binding` 80 CSVs; Not Claimed)

| Universe | Datasets ($D$) | Rows | `CLSS_Reg8_AllBP_IMGT_Z` Mean $\bar{\rho}$ | Positive Datasets (`>0`) | $\bar{\rho}_{N \ge 10}$ | $\bar{\rho}_{\sqrt{N}}$ | $\bar{\rho}_{N}$ | Best Released / Single | Margin |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| **`score/binding` (`-Kd` favourable)** | `16` | `6,959` | **`-0.0060`** | `6/16` (`37.5%`) | `-0.0038` | `-0.0017` | `+0.0058` | `iglm` (`+0.1742`) / `bp_mw` (`+0.2314`) | `-0.1802` |
| **`score/binding` (`+Kd` raw)** | `16` | `6,959` | **`+0.0060`** | `10/16` (`62.5%`) | `+0.0038` | `+0.0017` | `-0.0058` | `iglm (+ppl)` (`+0.1742`) | `-0.1682` |
| **`data/binding` (all 80 CSVs)** | `80` | `97,778` | **`-0.0987`** | `36/80` (`45.0%`) | `-0.1046` | `-0.0882` | `-0.0566` | `bp_flexibility` (`+0.0725`) | `-0.1712` |
| **`data/binding` (77 standard CSVs)** | `77` | `89,922` | **`-0.1012`** | `35/77` (`45.5%`) | `-0.1074` | `-0.0954` | `-0.0680` | `bp_flexibility` (`+0.0789`) | `-0.1801` |
| **`data/binding` (12 primary `score/`-mapped CSVs)** | `12` | `6,987` | **`-0.1123`** | `5/12` (`41.7%`) | `-0.0910` | `-0.0604` | `-0.0046` | `bp_flexibility` (`+0.1518`) | `-0.2641` |
| **`data/binding` (15 study-mapped CSVs)** | `15` | `7,024` | **`-0.1640`** | `5/15` (`33.3%`) | `-0.1304` | `-0.0811` | `-0.0067` | `bp_flexibility` (`+0.1795`) | `-0.3435` |
| **`data/binding` (68 excluded CSVs vs 12-CSV map)** | `68` | `90,791` | **`-0.0964`** | `31/68` (`45.6%`) | `-0.1069` | `-0.0914` | `-0.0606` | `bp_flexibility` (`+0.0585`) | `-0.1549` |
| **`data/binding` (65 excluded CSVs vs 15-CSV map)** | `65` | `90,754` | **`-0.0837`** | `31/65` (`47.7%`) | `-0.0998` | `-0.0890` | `-0.0605` | `bp_flexibility` (`+0.0478`) | `-0.1315` |
| **`score/binding` plus `data/binding` union** | `84` | `97,729` | **`-0.0809`** | `37/84` (`44.0%`) | `-0.0897` | `-0.0824` | `-0.0562` | `bp_flexibility` (`+0.0764`) | `-0.1573` |

---

## 4. Thermostability Universe Definitions (`15`, `20`, `21`, and the `score/tm` plus `data/thermostability` 25-Dataset Union; `p1` Not Claimed)

Because `p1` is a thermostability statement and `CLSS_Reg8_AllBP_IMGT_Z` was defined at `00:13Z` after looking at per-dataset results on `Wittrup2017_CST_Tm` in `score/tm`, **`p1` is not claimed**. For completeness, we report the 4 Thermostability benchmark universe definitions in `object/certificate.json`, labeling the 25-dataset figure as the **`score/tm` plus `data/thermostability` union**:

| Thermostability Universe (`p1` not claimed) | Datasets ($D$) | Best Single Descriptor | `CLSS_Reg8_AllBP_IMGT_Z` (Unwt / $\sqrt{N}$ / $N$-wt) | `CLSS_Reg7_MW_IMGT_Z` (Exploratory) | `CLSS_EqWt6_IMGT_Z` (Exploratory) |
|---|---:|---|---:|---:|---:|
| **1. `score_tm_15` (`score/tm/`)** | 15 | `bp_flexibility` (`+0.2908`) [Best LLM: `progen/xlarge = +0.2169`] | **`+0.4636`** (`14/15 > 0` \| `+0.3001` \| `+0.1666`) | `+0.5160` (`15/15 > 0` \| `+0.3426` \| `+0.1911`) | `+0.3528` (`11/15 > 0`) |
| **2. `data_thermostability_20_standard`** | 20 | `neg_bp_aromaticity` (`+0.1792`) [`bp_flexibility = +0.1695`] | **`+0.3270`** (**`16/20 = 80% > 0`** \| `+0.1328` \| `+0.0663`) | `+0.3568` (`16/20 = 80% > 0` \| `+0.1607` \| `+0.0896`) | `+0.2256` (`10/20 > 0`) |
| **3. `data_thermostability_21_all` (incl. `jain2024`)** | 21 | `neg_bp_aromaticity` (`+0.1599`) [`bp_flexibility = +0.1534`] | **`+0.3048`** (`16/21 = 76.2% > 0` \| `+0.1178` \| `+0.0596`) | `+0.3334` (`16/21 = 76.2% > 0` \| `+0.1445` \| `+0.0824`) | `+0.2087` (`10/21 > 0`) |
| **4. `combined_thermostability_25` (`score/tm` plus `data/thermostability` union)** | 25 | `bp_flexibility` (`+0.1954`) | **`+0.2834`** (`19/25 = 76.0% > 0` \| `+0.1196` \| `+0.0596`) | `+0.3313` (`20/25 = 80% > 0` \| `+0.1597` \| `+0.0891`) | `+0.2231` (`14/25 > 0`) |
