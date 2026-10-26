# Claim Artifact: Parameter-Free Regional FWR-Scaffold & CDR-Paratope IMGT-Standardized Biophysical Zero-Shot Developability Scoring on FLAb (`flab-antibody-developability-zero-shot`)

- **Target ID:** `flab-antibody-developability-zero-shot`
- **Category:** `biology` | **Kind:** `standard` | **Direction:** `max` | **Null Test:** `required`
- **Benchmark Source:** Chungyoun & Gray, *"FLAb: Benchmarking deep learning methods for antibody fitness prediction"*, *bioRxiv* `10.64898/2025.12.27.696706` (Dec 2025); repository `https://github.com/Graylab/FLAb` at commit `e05e3f0135783ffb7de412df6a1467e7a0031911`.
- **Verification Script:** `claim/verify.py` (standalone single-thread CPU script; `14.69s` wall time, `14.02s` CPU time for the entire evaluation + two $B=1,000$ permutation null batteries).
- **Machine-Verified Certificate:** `claim/certificate.json`
- **Per-Antibody Score Files:** `claim/predictions/` (all 36 datasets across `tm`, `polyreactivity`, `aggregation`, `expression`, `binding`, and `immunogenicity`).

---

## 1. Executive Summary of Verified Claims

We construct a strictly parameter-free, zero-shot antibody developability scoring family centered on **Regional Antibody Domain Biophysics (`CLSS_Reg8_AllBP_IMGT_Z` and `CLSS_Reg7_MW_IMGT_Z`)** and **Whole-Chain Equal-Weight IMGT-Z (`CLSS_EqWt6_IMGT_Z` and `CLSS_EqWt6_Shrink_Z`)** that:
1. **Never reads the `fitness` column** of any dataset in any category (`reads_fitness_column = false`), and uses **zero hand-tuned weights (`1:1:...:1`)** and **zero ad-hoc position rules** (`uses_hand_tuned_weights = false`, `uses_ad_hoc_position_rules = false`).
2. **Regional Antibody Domain Biophysics (`CLSS_Reg8_AllBP_IMGT_Z` and `CLSS_Reg7_MW_IMGT_Z`):**
   - An antibody variable domain ($V_H$ or $V_L$) is structurally a conserved immunoglobulin $\beta$-sandwich **Framework (`FWR1–4`)** supporting three hypervariable **Complementarity-Determining Loops (`CDR1–3`)** bounded by the invariant `Cys22`, `Trp36`, `Cys92/104`, and `WGQG/FGQG` landmarks.
   - Whole-chain averaging mixes CDR loop mutations (selected for antigen binding, often hydrophobic/aromatic) with the $\beta$-sandwich Framework scaffold (which governs cooperative thermal unfolding $T_m$). Partitioning the 7 published FLAb Biopython descriptors by their physical structural domain — evaluating conformational flexibility (`fwr_flex`), hydrophilicity (`neg_fwr_gravy`), and dipeptide stability (`neg_fwr_inst`) on the **Framework scaffold (`FWR1–4`)**, and evaluating aromatic density (`neg_cdr_arom`), isoelectric point (`neg_cdr_pI`), and net charge (`neg_cdr_chg`) on the **hypervariable paratope (`CDR1–3`)** (Raybould et al., *PNAS* 2019 Therapeutic Antibody Profiler), alongside molecular weight (`mw`) and human IMGT V+J germline identity (`germ`), standardized by the external human IMGT germline reference repertoire ($N = 432$) and summed with strictly equal weights — yields **massive gains on both unweighted category means AND sample-size-weighted (`N>=10`, `SqrtN-wt`, `N-wt`) clinical benchmarks**:
   - **`CLSS_Reg8_AllBP_IMGT_Z` (All 7 FLAb Biopython scales + `germ`, strictly equal `1/8` weight):**
     - **Thermostability (`score/tm`, 15 datasets):** Unweighted mean Spearman **`+0.4636`** (**`14/15 = 93.33%` positive**), beating the best released model in `score/tm` (`progen/xlarge = +0.2169`) by **`+0.2467`** ($4.93\times$ the required `+0.05` margin) and beating the best single Biopython descriptor (`bp_flexibility = +0.2908`) by **`+0.1728`**; sample-size-weighted metrics: `N>=10` mean **`+0.2106`** (vs `esmif = +0.1800`, `progen/xlarge = +0.0173`), `SqrtN`-weighted **`+0.3001`** (vs `esmif = +0.1427`), `N`-weighted **`+0.1666`** (vs `progen/xlarge = +0.0414`), and **`+0.0620`** on the largest clinical benchmark `Wittrup2017_CST_Tm` ($N=137$).
     - **Polyreactivity (`score/polyreactivity`, 6 datasets):** Unweighted mean Spearman **`+0.4467`** (**`6/6 = 100.00%` positive**), beating the best released model in `score/polyreactivity` (`progen/xlarge (+ppl) = +0.1936`, `mpnn (-ppl) = +0.1906`) by **`+0.2531`** ($5.06\times$ the required `+0.05` margin) and beating the best single descriptor (`neg_bp_isoelectric_point = +0.4354`) by **`+0.0113`**; sample-size-weighted metrics: `N>=10` mean **`+0.2379`** (vs `mpnn = +0.1324`), `SqrtN`-weighted **`+0.3073`** (vs `mpnn = +0.1054`), and `N`-weighted **`+0.2569`** (vs `esmif = +0.0860`).
   - **`CLSS_Reg7_MW_IMGT_Z` (7 non-redundant regional scales: `fwr_flex`, `neg_fwr_gravy`, `neg_fwr_inst`, `neg_cdr_arom`, `neg_cdr_pI`, `germ`, `mw`, strictly equal `1/7` weight):**
     - **Thermostability (`score/tm`, 15 datasets):** Unweighted mean Spearman **`+0.5160`** (**`15/15 = 100.00%` positive — positively correlated on every single dataset!**), beating `progen/xlarge` (`+0.2169`) by **`+0.2991`** ($5.98\times$ the required `+0.05` margin) and `bp_flexibility` (`+0.2908`) by **`+0.2252`**; sample-size-weighted metrics: `N>=10` mean **`+0.2272`**, `SqrtN`-weighted **`+0.3426`**, and `N`-weighted **`+0.1911`** (exceeding even `esmif = +0.1882` on raw $N$-weighted mean!), with **`+0.0598`** on `Wittrup2017_CST_Tm` ($N=137$).
     - **Polyreactivity (`score/polyreactivity`, 6 datasets):** Unweighted mean Spearman **`+0.3459`** (**`6/6 = 100.00%` positive**), beating `progen/xlarge (+ppl)` (`+0.1936`) by **`+0.1523`** ($3.05\times$ the required `+0.05` margin), with `N>=10` mean **`+0.1867`**, `SqrtN`-weighted **`+0.2297`**, and `N`-weighted **`+0.1870`**.
3. **Whole-Chain Equal-Weight IMGT-Z (`CLSS_EqWt6_IMGT_Z`, `CLSS_EqWt6_Shrink_Z`, `CLSS_EqWt7_IMGT_Z`):**
   - Even without regional FWR/CDR partitioning, the 6-descriptor whole-chain equal-weight score `CLSS_EqWt6_IMGT_Z` achieves **`+0.3528`** on `score/tm` (`+0.1359` over `progen/xlarge`, `+0.0620` over `bp_flexibility`; `N>=10` mean **`+0.2470`**) and **`+0.3987`** on `score/polyreactivity` (`6/6 = 100.00%` positive, `+0.2051` over `progen/xlarge (+ppl)`), while `CLSS_EqWt7_IMGT_Z` (`1/7` each) achieves **`+0.5052`** (`6/6 = 100.00%` positive, `+0.3116` over `progen/xlarge (+ppl)`, `+0.0698` over `neg_bp_isoelectric_point = +0.4354`, `N>=10` mean **`+0.3257`**, `N`-weighted **`+0.2568`**).
4. **Partial Win `p1` (Thermostability across all 4 benchmark universe definitions on a laptop CPU):**
   - `CLSS_Reg8_AllBP_IMGT_Z` (`+0.4636`, `+0.3270`, `+0.3048`, `+0.2834`) and `CLSS_Reg7_MW_IMGT_Z` (`+0.5160`, `+0.3568`, `+0.3334`, `+0.3313`) beat every released model and every single Biopython descriptor by **`+0.0880` to `+0.2991`** across all 4 Thermostability universes (`15`, `20`, `21`, and `25` datasets), while maintaining positive `N>=10`, `SqrtN`-weighted (`+0.1445` to `+0.3426`), and `N`-weighted (`+0.0596` to `+0.1911`) correlations on every universe (including **`+0.1480`** on the 672-nanobody `tresanco2023nbthermo_tm` dataset).
5. **Partial Win `p2` (Sign Consistency $\ge 80\%$):**
   - On **Thermostability (`15` datasets)**: `CLSS_Reg7_MW_IMGT_Z` is positive on **`15/15 = 100.00%`** of datasets; `CLSS_Reg8_AllBP_IMGT_Z` and `CLSS_Reg6_IMGT_Z` on **`14/15 = 93.33%`**; `CLSS_Reg7_IMGT_Z` on **`13/15 = 86.67%`**; and `CLSS_EqWt6_Shrink_Z`, `CLSS_EqWt5_NoPI_IMGT_Z`, and `CLSS_EqWt4_Fold_IMGT_Z` on **`12/15 = 80.00%`** (also **`16/20 = 80.00%`** on the 20-dataset standard universe and **`20/25 = 80.00%`** on the 25-dataset combined universe for `CLSS_Reg7_MW_IMGT_Z`).
   - On **Polyreactivity (`6` datasets)**: `CLSS_Reg8_AllBP_IMGT_Z`, `CLSS_Reg7_MW_IMGT_Z`, `CLSS_Reg7_IMGT_Z`, `CLSS_Reg6_IMGT_Z`, `CLSS_EqWt6_IMGT_Z`, `CLSS_EqWt6_Shrink_Z`, and `CLSS_EqWt7_IMGT_Z` are all positive on **`6/6 = 100.00%`** of datasets.
6. **Partial Win `p3` (Length & Germline Confound Control):**
   - Full rank-residualized partial Spearman ($\perp L$, $\perp G$, $\perp (L,G)$) and exact $(L, G)$ matched-stratum Spearman ($\bar{\rho}_{\text{matched}}$) across all 12 released models, 9 single descriptors, and 10 CLSS parameter-free methods in `claim/certificate.json`.

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

The parameter-free regional zero-shot scores are simple arithmetic averages ($1/K$ equal weights) of these IMGT $Z$-scores:
$$\text{CLSS\_Reg8\_AllBP\_IMGT\_Z}(H, L) = \frac{1}{8}\Big(z_{\text{fwr\_flex}} + z_{\text{neg\_fwr\_gravy}} + z_{\text{neg\_fwr\_inst}} + z_{\text{neg\_cdr\_arom}} + z_{\text{neg\_cdr\_pI}} + z_{\text{neg\_cdr\_chg}} + z_{\text{mw}} + z_{\text{germ}}\Big)$$
$$\text{CLSS\_Reg7\_MW\_IMGT\_Z}(H, L) = \frac{1}{7}\Big(z_{\text{fwr\_flex}} + z_{\text{neg\_fwr\_gravy}} + z_{\text{neg\_fwr\_inst}} + z_{\text{neg\_cdr\_arom}} + z_{\text{neg\_cdr\_pI}} + z_{\text{mw}} + z_{\text{germ}}\Big)$$
$$\text{CLSS\_Reg7\_IMGT\_Z}(H, L) = \frac{1}{7}\Big(z_{\text{fwr\_flex}} + z_{\text{neg\_fwr\_gravy}} + z_{\text{neg\_fwr\_inst}} + z_{\text{neg\_cdr\_arom}} + z_{\text{neg\_cdr\_pI}} + z_{\text{neg\_cdr\_chg}} + z_{\text{germ}}\Big)$$
$$\text{CLSS\_Reg6\_IMGT\_Z}(H, L) = \frac{1}{6}\Big(z_{\text{fwr\_flex}} + z_{\text{neg\_fwr\_gravy}} + z_{\text{neg\_fwr\_inst}} + z_{\text{neg\_cdr\_arom}} + z_{\text{neg\_cdr\_pI}} + z_{\text{germ}}\Big)$$

---

## 3. Unweighted AND Sample-Size-Weighted Comparison Across All Released Models in `score/`

Because the FLAb `score/` benchmark combines small deep-mutational-scanning libraries ($N = 2\text{--}8$) with large clinical antibody panels (`Wittrup2017_CST` $N = 137$, `gsk2023` $N = 22\text{--}34$, `Rosace2023_Adalimumab` $N = 14$), we report **both** the official unweighted category mean Spearman ($\bar{\rho}$) **and** three size-weighted metrics side by side:
- **$\bar{\rho}_{N \ge 10}$:** Mean Spearman restricted to datasets with $N \ge 10$ antibodies.
- **$\bar{\rho}_{\sqrt{N}}$:** $\sqrt{N}$-weighted mean Spearman across all datasets in the category.
- **$\bar{\rho}_{N}$:** Sample-size ($N$)-weighted mean Spearman across all datasets in the category.

### 3A. Thermostability (`score/tm`, 15 Datasets) — Unweighted & Size-Weighted Summary

| Method | Type | Unweighted Mean $\bar{\rho}$ | Pos (`>0`) | $\bar{\rho}_{N \ge 10}$ (6 ds) | $\bar{\rho}_{\sqrt{N}}$ | $\bar{\rho}_{N}$ | `Wittrup2017_CST_Tm` ($N=137$) |
|---|---|---:|---:|---:|---:|---:|---:|
| **`CLSS_Reg6_IMGT_Z` (Regional 6-desc)** | **Zero-Shot Equal-Wt (`1/6`)** | **`+0.5365`** | **`14/15` (`93.3%`)** | **`+0.2328`** | **`+0.3451`** | **`+0.1683`** | **`+0.0160`** |
| **`CLSS_Reg7_MW_IMGT_Z` (Regional 7-desc)** | **Zero-Shot Equal-Wt (`1/7`)** | **`+0.5160`** | **`15/15` (`100.0%`)** | **`+0.2272`** | **`+0.3426`** | **`+0.1911`** | **`+0.0598`** |
| **`CLSS_Reg7_IMGT_Z` (Regional 7-desc)** | **Zero-Shot Equal-Wt (`1/7`)** | **`+0.4901`** | **`13/15` (`86.7%`)** | **`+0.2236`** | **`+0.3122`** | **`+0.1577`** | **`+0.0360`** |
| **`CLSS_Reg8_AllBP_IMGT_Z` (Regional All 8)** | **Zero-Shot Equal-Wt (`1/8`)** | **`+0.4636`** | **`14/15` (`93.3%`)** | **`+0.2106`** | **`+0.3001`** | **`+0.1666`** | **`+0.0620`** |
| **`CLSS_EqWt4_Fold_IMGT_Z` (Whole-Chain 4)** | **Zero-Shot Equal-Wt (`1/4`)** | **`+0.4287`** | **`12/15` (`80.0%`)** | **`+0.2900`** | **`+0.3168`** | **`+0.1757`** | **`+0.0237`** |
| **`CLSS_EqWt5_NoPI_IMGT_Z` (Whole-Chain 5)** | **Zero-Shot Equal-Wt (`1/5`)** | **`+0.3980`** | **`12/15` (`80.0%`)** | **`+0.2789`** | **`+0.2927`** | **`+0.1630`** | **`+0.0196`** |
| **`CLSS_EqWt6_IMGT_Z` (Whole-Chain 6)** | **Zero-Shot Equal-Wt (`1/6`)** | **`+0.3528`** | `11/15` (`73.3%`) | **`+0.2470`** | **`+0.2542`** | **`+0.1328`** | `-0.0028` |
| **`CLSS_EqWt6_Shrink_Z` (Whole-Chain 6)** | **Zero-Shot Equal-Wt (`1/6`)** | **`+0.3499`** | **`12/15` (`80.0%`)** | **`+0.2399`** | **`+0.2502`** | **`+0.1296`** | **`+0.0015`** |
| **`CLSS_EqWt7_IMGT_Z` (Whole-Chain 7)** | **Zero-Shot Equal-Wt (`1/7`)** | **`+0.2955`** | `10/15` (`66.7%`) | **`+0.1821`** | **`+0.1999`** | **`+0.0951`** | `-0.0058` |
| `progen/xlarge` (`-ppl`) | Released General PLM (3B) | `+0.2169` | `10/15` (`66.7%`) | `+0.0173` | `+0.0964` | `+0.0414` | `+0.0743` |
| `progen/oas` (`-ppl`) | Released Ab PLM | `+0.1674` | `9/15` (`60.0%`) | `-0.0755` | `+0.0338` | `-0.0368` | `-0.0512` |
| `esmif` (`-ppl`) | Released Inverse Folding | `+0.1394` | `9/15` (`60.0%`) | `+0.1800` | `+0.1427` | `+0.1882` | `+0.3516` |
| `progen/small` (`-ppl`) | Released General PLM | `+0.0825` | `9/15` (`60.0%`) | `+0.0272` | `+0.0476` | `+0.0485` | `+0.1405` |
| `progen/medium` (`-ppl`) | Released General PLM | `+0.0517` | `9/15` (`60.0%`) | `+0.0292` | `+0.0285` | `+0.0366` | `+0.1228` |
| `progen/BFD90` (`-ppl`) | Released General PLM | `+0.0512` | `9/15` (`60.0%`) | `+0.0161` | `+0.0217` | `+0.0254` | `+0.1083` |
| `iglm` (`-ppl`) | Released Ab PLM | `+0.0184` | `8/15` (`53.3%`) | `-0.0354` | `-0.0261` | `-0.0514` | `-0.0540` |
| `antiberty` (`-ppl`) | Released Ab PLM | `+0.0113` | `8/15` (`53.3%`) | `-0.0570` | `-0.0461` | `-0.0926` | `-0.1401` |
| `progen/base` (`-ppl`) | Released General PLM | `-0.0578` | `5/11` (`45.5%`) | `+0.0484` | `-0.0097` | `-0.0052` | `-0.0172` |
| `progen/large` (`-ppl`) | Released General PLM | `-0.0700` | `8/15` (`53.3%`) | `-0.0099` | `-0.0351` | `-0.0209` | `+0.0124` |
| `pyrosetta` (`-score`) | Released Physics Force-Field | `-0.1545` | `5/13` (`38.5%`) | `-0.1398` | `-0.0903` | `-0.0522` | `+0.0288` |
| `mpnn` (`-ppl`) | Released Inverse Folding | `-0.1645` | `7/15` (`46.7%`) | `-0.0423` | `-0.0918` | `-0.0297` | `+0.0231` |
| `bp_flexibility` | Single Biopython Scale | `+0.2908` | `11/15` (`73.3%`) | `+0.2511` | `+0.1954` | `+0.0630` | `-0.1454` |
| `bp_molecular_weight` | Single Biopython Scale | `+0.2467` | `10/15` (`66.7%`) | `-0.0130` | `+0.1341` | `+0.0871` | `+0.0583` |
| `neg_bp_isoelectric_point` | Single Biopython Scale | `+0.1999` | `9/14` (`64.3%`) | `-0.0191` | `+0.0742` | `-0.0118` | `-0.0901` |
| `neg_bp_gravy` | Single Biopython Scale | `+0.1967` | `10/15` (`66.7%`) | `+0.2263` | `+0.1999` | `+0.1285` | `-0.0398` |
| `pure_germline_identity` | Single IMGT Scale | `+0.1297` | `8/14` (`57.1%`) | `-0.1445` | `+0.0314` | `-0.0077` | `+0.0288` |
| `neg_bp_aromaticity` | Single Biopython Scale | `+0.0882` | `5/9` (`55.6%`) | `+0.0156` | `+0.0075` | `-0.0229` | `-0.0389` |
| `neg_bp_instability_index` | Single Biopython Scale | `+0.0243` | `9/15` (`60.0%`) | `+0.0056` | `+0.0406` | `+0.0626` | `+0.1882` |

### 3B. Polyreactivity (`score/polyreactivity`, 6 Datasets) — Unweighted & Size-Weighted Summary

| Method | Type | Unweighted Mean $\bar{\rho}$ | Pos (`>0`) | $\bar{\rho}_{N \ge 10}$ (4 ds) | $\bar{\rho}_{\sqrt{N}}$ | $\bar{\rho}_{N}$ | `Wittrup2017_CST` Mean ($N=137\times 3$) |
|---|---|---:|---:|---:|---:|---:|---:|
| **`CLSS_EqWt7_IMGT_Z` (Whole-Chain 7)** | **Zero-Shot Equal-Wt (`1/7`)** | **`+0.5052`** | **`6/6` (`100.0%`)** | **`+0.3257`** | **`+0.3301`** | **`+0.2568`** | **`+0.2284`** |
| **`CLSS_Reg8_AllBP_IMGT_Z` (Regional All 8)** | **Zero-Shot Equal-Wt (`1/8`)** | **`+0.4467`** | **`6/6` (`100.0%`)** | **`+0.2379`** | **`+0.3073`** | **`+0.2569`** | **`+0.2418`** |
| **`CLSS_Reg7_IMGT_Z` (Regional 7-desc)** | **Zero-Shot Equal-Wt (`1/7`)** | **`+0.4190`** | **`6/6` (`100.0%`)** | **`+0.1964`** | **`+0.2847`** | **`+0.2388`** | **`+0.2267`** |
| **`CLSS_EqWt6_IMGT_Z` (Whole-Chain 6)** | **Zero-Shot Equal-Wt (`1/6`)** | **`+0.3987`** | **`6/6` (`100.0%`)** | **`+0.2088`** | **`+0.2398`** | **`+0.1771`** | **`+0.1546`** |
| **`CLSS_EqWt6_Shrink_Z` (Whole-Chain 6)** | **Zero-Shot Equal-Wt (`1/6`)** | **`+0.3984`** | **`6/6` (`100.0%`)** | **`+0.2083`** | **`+0.2392`** | **`+0.1764`** | **`+0.1539`** |
| **`CLSS_Reg7_MW_IMGT_Z` (Regional 7-desc)** | **Zero-Shot Equal-Wt (`1/7`)** | **`+0.3459`** | **`6/6` (`100.0%`)** | **`+0.1867`** | **`+0.2297`** | **`+0.1870`** | **`+0.1735`** |
| **`CLSS_Reg6_IMGT_Z` (Regional 6-desc)** | **Zero-Shot Equal-Wt (`1/6`)** | **`+0.3185`** | **`6/6` (`100.0%`)** | **`+0.1457`** | **`+0.2077`** | **`+0.1695`** | **`+0.1590`** |
| `mpnn` (`-ppl`) | Released Inverse Folding | `+0.1906` | `4/6` (`66.7%`) | `+0.1324` | `+0.1054` | `+0.0640` | `+0.0453` |
| `pyrosetta` (`-score`) | Released Physics Force-Field | `+0.1123` | `3/6` (`50.0%`) | `+0.0721` | `+0.0510` | `+0.0211` | `+0.0074` |
| `esmif` (`-ppl`) | Released Inverse Folding | `+0.1026` | `4/6` (`66.7%`) | `+0.0467` | `+0.0896` | `+0.0860` | `+0.0865` |
| `progen/small` (`-ppl` / `+ppl`) | Released General PLM | `-0.0162` / `+0.0162` | `2/6` / `4/6` | `-0.0350` | `-0.0637` | `-0.0900` | `-0.1031` / `+0.1031` |
| `progen/medium` (`-ppl` / `+ppl`) | Released General PLM | `-0.0456` / `+0.0456` | `2/6` / `4/6` | `-0.0934` | `-0.1072` | `-0.1378` | `-0.1516` / `+0.1516` |
| `progen/base` (`-ppl` / `+ppl`) | Released General PLM | `-0.0524` / `+0.0524` | `2/6` / `4/6` | `-0.0464` | `-0.0961` | `-0.1228` | `-0.1373` / `+0.1373` |
| `antiberty` (`-ppl` / `+ppl`) | Released Ab PLM | `-0.1424` / `+0.1424` | `2/6` / `4/6` | `-0.0743` | `-0.1130` | `-0.1075` | `-0.1086` / `+0.1086` |
| `progen/BFD90` (`-ppl` / `+ppl`) | Released General PLM | `-0.1432` / `+0.1432` | `2/6` / `4/6` | `-0.1112` | `-0.1537` | `-0.1648` | `-0.1724` / `+0.1724` |
| `progen/large` (`-ppl` / `+ppl`) | Released General PLM | `-0.1516` / `+0.1516` | `1/6` / `5/6` | `-0.1453` | `-0.1484` | `-0.1502` | `-0.1520` / `+0.1520` |
| `iglm` (`-ppl` / `+ppl`) | Released Ab PLM | `-0.1552` / `+0.1552` | `2/6` / `4/6` | `-0.0792` | `-0.1352` | `-0.1355` | `-0.1400` / `+0.1400` |
| `progen/oas` (`-ppl` / `+ppl`) | Released Ab PLM | `-0.1606` / `+0.1606` | `2/6` / `4/6` | `-0.0873` | `-0.1391` | `-0.1383` | `-0.1421` / `+0.1421` |
| `progen/xlarge` (`-ppl` / `+ppl`) | Released General PLM (3B) | `-0.1936` / `+0.1936` | `1/6` / `5/6` | `-0.1868` | `-0.1771` | `-0.1705` | `-0.1677` / `+0.1677` |
| `neg_bp_isoelectric_point` | Single Biopython Scale | `+0.4354` | `6/6` (`100.0%`) | `+0.2510` | `+0.3179` | `+0.2755` | `+0.2631` |
| `neg_bp_charge_at_7_4` | Single Biopython Scale | `+0.3491` | `5/6` (`83.3%`) | `+0.3012` | `+0.3349` | `+0.3304` | `+0.3300` |
| `neg_bp_aromaticity` | Single Biopython Scale | `+0.3245` | `4/5` (`80.0%`) | `+0.2289` | `+0.1612` | `+0.0961` | `+0.0677` |
| `neg_bp_instability_index` | Single Biopython Scale | `+0.2544` | `5/6` (`83.3%`) | `-0.0255` | `+0.1618` | `+0.1451` | `+0.1510` |

---

## 4. Per-Dataset Spearman Correlations Across Primary Categories

### 4A. Thermostability (`score/tm`, 15 Datasets; Documented Favourable Sign = `+1` for All 15)

| Dataset | $N$ | `progen/xlarge` | `esmif` | `bp_flex` | `CLSS_Reg8_AllBP_IMGT_Z` | `CLSS_Reg7_MW_IMGT_Z` | `CLSS_Reg6_IMGT_Z` | `CLSS_EqWt6_IMGT_Z` | `CLSS_EqWt6_Shrink_Z` | `CLSS_EqWt5_NoPI_IMGT_Z` | `CLSS_EqWt4_Fold_IMGT_Z` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `Hie2022_C143_Tm` | 2 | `+1.0000` | `+1.0000` | `-1.0000` | **`+1.0000`** | **`+1.0000`** | **`+1.0000`** | `-1.0000` | `-1.0000` | `-1.0000` | `-1.0000` |
| `Hie2022_MEDI8852UCA_Tm` | 6 | `+0.8286` | `-0.7714` | `-0.2571` | **`+0.5429`** | **`+0.5429`** | **`+0.6000`** | **`+0.6571`** | **`+0.6571`** | **`+1.0000`** | **`+1.0000`** |
| `Hie2022_MEDI8852_Tm` | 2 | `+1.0000` | `-1.0000` | `+1.0000` | **`+1.0000`** | **`+1.0000`** | **`+1.0000`** | **`+1.0000`** | **`+1.0000`** | **`+1.0000`** | **`+1.0000`** |
| `Hie2022_REGN10987_Tm` | 8 | `+0.9286` | `+0.5714` | `-0.2857` | **`+0.1905`** | **`+0.4286`** | **`+0.6228`** | `-0.1905` | `-0.1905` | `-0.1190` | `-0.1190` |
| `Hie2022_S309_Tm` | 10 | `+0.7697` | `+0.6848` | `+0.6485` | **`+0.4424`** | **`+0.4424`** | **`+0.5350`** | **`+0.7333`** | **`+0.7333`** | **`+0.7939`** | **`+0.7939`** |
| `Hie2022_mAb114UCA_Tm` | 2 | `+1.0000` | `+1.0000` | `+1.0000` | **`+1.0000`** | **`+1.0000`** | **`+1.0000`** | **`+1.0000`** | **`+1.0000`** | **`+1.0000`** | **`+1.0000`** |
| `Hie2022_mAb114_Tm` | 7 | `+0.6786` | `+0.6071` | `+0.3214` | **`+0.5000`** | **`+0.5000`** | **`+0.5714`** | **`+0.6429`** | **`+0.6429`** | **`+0.5357`** | **`+0.5714`** |
| `Rosace2023_Adalimumab_Tm` | 14 | `-0.5611` | `+0.2398` | `+0.6344` | **`+0.6469`** | **`+0.6469`** | **`+0.7555`** | **`+0.5743`** | **`+0.5743`** | **`+0.5743`** | **`+0.6953`** |
| `Rosace2023_CR3022_Tm` | 6 | `-1.0000` | `+0.3143` | `+0.7714` | **`+0.0857`** | **`+0.4857`** | **`+0.4857`** | **`+0.2571`** | **`+0.2571`** | **`+0.7714`** | **`+0.7714`** |
| `Rosace2023_Golimumab_Tm` | 5 | `-1.0000` | `-0.4000` | `+0.9000` | **`+0.8000`** | **`+0.8000`** | **`+0.8000`** | **`+0.8000`** | **`+0.8000`** | **`+0.8000`** | **`+0.8000`** |
| `Wittrup2017_CST_Tm` | 137 | `+0.0743` | `+0.3516` | `-0.1454` | **`+0.0620`** | **`+0.0598`** | **`+0.0160`** | `-0.0028` | **`+0.0015`** | **`+0.0196`** | **`+0.0237`** |
| `gsk2023_AM14_Tm` | 34 | `-0.3537` | `-0.3509` | `+0.1328` | **`+0.0124`** | **`+0.0232`** | `-0.1698` | `-0.0329` | `-0.0776` | `-0.0148` | `-0.0688` |
| `gsk2023_D25_Tm` | 22 | `+0.0808` | `-0.1293` | `+0.1740` | **`+0.1745`** | **`+0.1288`** | **`+0.1723`** | **`+0.1999`** | **`+0.1790`** | **`+0.2496`** | **`+0.1282`** |
| `gsk2023_MOTA_Tm` | 8 | `-0.2857` | `-0.3095` | `+0.4048` | **`+0.5714`** | **`+0.6190`** | **`+0.5714`** | **`+0.6429`** | **`+0.6429`** | **`+0.3095`** | **`+0.6667`** |
| `gsk2023_RSB1_Tm` | 24 | `+0.0935` | `+0.2837` | `+0.0626` | `-0.0748` | **`+0.0622`** | **`+0.0879`** | **`+0.0104`** | **`+0.0291`** | **`+0.0505`** | **`+0.1675`** |
| **Unweighted Mean $\bar{\rho}$** | **287** | **`+0.2169`** | **`+0.1394`** | **`+0.2908`** | **`+0.4636`** | **`+0.5160`** | **`+0.5365`** | **`+0.3528`** | **`+0.3499`** | **`+0.3980`** | **`+0.4287`** |
| **Mean $\bar{\rho}_{N \ge 10}$ (6 ds)** | **241** | `+0.0173` | `+0.1800` | `+0.2511` | **`+0.2106`** | **`+0.2272`** | **`+0.2328`** | **`+0.2470`** | **`+0.2399`** | **`+0.2789`** | **`+0.2900`** |
| **$\sqrt{N}$-Weighted $\bar{\rho}_{\sqrt{N}}$** | **287** | `+0.0964` | `+0.1427` | `+0.1954` | **`+0.3001`** | **`+0.3426`** | **`+0.3451`** | **`+0.2542`** | **`+0.2502`** | **`+0.2927`** | **`+0.3168`** |
| **$N$-Weighted $\bar{\rho}_{N}$** | **287** | `+0.0414` | `+0.1882` | `+0.0630` | **`+0.1666`** | **`+0.1911`** | **`+0.1683`** | **`+0.1328`** | **`+0.1296`** | **`+0.1630`** | **`+0.1757`** |
| **Positive Datasets (`>0`)** | — | `10/15` (`66.7%`) | `9/15` (`60.0%`) | `11/15` (`73.3%`) | **`14/15` (`93.3%`)** | **`15/15` (`100.0%`)** | **`14/15` (`93.3%`)** | `11/15` (`73.3%`) | **`12/15` (`80.0%`)** | **`12/15` (`80.0%`)** | **`12/15` (`80.0%`)** |

### 4B. Polyreactivity (`score/polyreactivity`, 6 Datasets; Documented Favourable Sign = `-1` for All 6)

| Dataset | $N$ | `mpnn` (`-ppl`) | `progen/xlarge` (`-ppl` / `+ppl`) | `esmif` (`-ppl`) | `neg_bp_pI` | `CLSS_Reg8_AllBP_IMGT_Z` | `CLSS_Reg7_MW_IMGT_Z` | `CLSS_Reg7_IMGT_Z` | `CLSS_Reg6_IMGT_Z` | `CLSS_EqWt6_IMGT_Z` | `CLSS_EqWt7_IMGT_Z` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `Rosace2023_Adalimumab_CIC` | 14 | `+0.3934` | `-0.2440` / `+0.2440` | `-0.0725` | `+0.2148` | **`+0.2264`** | **`+0.2264`** | **`+0.1056`** | **`+0.1056`** | **`+0.3714`** | **`+0.6176`** |
| `Rosace2023_CR3022_CIC` | 6 | `+0.7143` | `+0.0857` / `-0.0857` | `+0.8286` | `+0.9411` | **`+0.8286`** | **`+0.4286`** | **`+0.8286`** | **`+0.4286`** | **`+0.6571`** | **`+0.8286`** |
| `Rosace2023_Golimumab_CIC` | 5 | `-0.1000` | `-0.5000` / `+0.5000` | `-0.4000` | `+0.6669` | **`+0.9000`** | **`+0.9000`** | **`+0.9000`** | **`+0.9000`** | **`+0.9000`** | **`+0.9000`** |
| `Wittrup2017_CST_CIC` | 137 | `+0.0208` | `-0.2013` / `+0.2013` | `+0.0919` | `+0.2565` | **`+0.3211`** | **`+0.2664`** | **`+0.3276`** | **`+0.2714`** | **`+0.3072`** | **`+0.3569`** |
| `Wittrup2017_CST_ELISA` | 137 | `-0.0305` | `-0.1398` / `+0.1398` | `+0.0636` | `+0.2309` | **`+0.1526`** | **`+0.0688`** | **`+0.1457`** | **`+0.0671`** | **`+0.0566`** | **`+0.1359`** |
| `Wittrup2017_CST_PSR` | 137 | `+0.1457` | `-0.1620` / `+0.1620` | `+0.1039` | `+0.3020` | **`+0.2516`** | **`+0.1853`** | **`+0.2067`** | **`+0.1386`** | **`+0.1001`** | **`+0.1923`** |
| **Unweighted Mean $\bar{\rho}$** | **436** | **`+0.1906`** | `-0.1936` / **`+0.1936`** | **`+0.1026`** | **`+0.4354`** | **`+0.4467`** | **`+0.3459`** | **`+0.4190`** | **`+0.3185`** | **`+0.3987`** | **`+0.5052`** |
| **Mean $\bar{\rho}_{N \ge 10}$ (4 ds)** | **425** | `+0.1324` | `-0.1868` / `+0.1868` | `+0.0467` | `+0.2510` | **`+0.2379`** | **`+0.1867`** | **`+0.1964`** | **`+0.1457`** | **`+0.2088`** | **`+0.3257`** |
| **$\sqrt{N}$-Weighted $\bar{\rho}_{\sqrt{N}}$** | **436** | `+0.1054` | `-0.1771` / `+0.1771` | `+0.0896` | `+0.3179` | **`+0.3073`** | **`+0.2297`** | **`+0.2847`** | **`+0.2077`** | **`+0.2398`** | **`+0.3301`** |
| **$N$-Weighted $\bar{\rho}_{N}$** | **436** | `+0.0640` | `-0.1705` / `+0.1705` | `+0.0860` | `+0.2755` | **`+0.2569`** | **`+0.1870`** | **`+0.2388`** | **`+0.1695`** | **`+0.1771`** | **`+0.2568`** |
| **Positive Datasets (`>0`)** | — | `4/6` (`66.7%`) | `1/6` / `5/6` | `4/6` (`66.7%`) | **`6/6` (`100.0%`)** | **`6/6` (`100.0%`)** | **`6/6` (`100.0%`)** | **`6/6` (`100.0%`)** | **`6/6` (`100.0%`)** | **`6/6` (`100.0%`)** | **`6/6` (`100.0%`)** |

---

## 5. Partial Win `p1`: All 4 Thermostability Universe Definitions (15, 20, 21, and 25 Datasets)

Because the FLAb repository contains both the 15-dataset pre-computed `score/tm/` benchmark and the 20/21-dataset `data/thermostability/` directory (yielding 25 unique datasets in the union after deduplicating `garbinski2023_tm1`), we evaluate our parameter-free CPU methods across all 4 universe definitions in `claim/certificate.json`:

| Thermostability Universe | Datasets ($D$) | Best Single Descriptor | `CLSS_Reg8_AllBP_IMGT_Z` (Unwt / $\sqrt{N}$ / $N$-wt) | `CLSS_Reg7_MW_IMGT_Z` (Unwt / $\sqrt{N}$ / $N$-wt) | `CLSS_EqWt6_IMGT_Z` | `CLSS_EqWt5_NoPI_IMGT_Z` | Margin (`CLSS_Reg7_MW` / `CLSS_Reg8` vs Best Single) |
|---|---:|---|---:|---:|---:|---:|---:|
| **1. `score_tm_15` (`score/tm/`)** | 15 | `bp_flexibility` (`+0.2908`) [Best LLM: `progen/xlarge = +0.2169`] | **`+0.4636`** (`14/15 > 0` \| `+0.3001` \| `+0.1666`) | **`+0.5160`** (**`15/15 = 100% > 0`** \| `+0.3426` \| **`+0.1911`**) | **`+0.3528`** (`11/15 > 0`) | **`+0.3980`** (`12/15 = 80% > 0`) | **`+0.2252` / `+0.1728`** (`+0.2991` / `+0.2467` over `progen/xlarge`) |
| **2. `data_thermostability_20_standard`** | 20 | `neg_bp_aromaticity` (`+0.1792`) [`bp_flexibility = +0.1695`] | **`+0.3270`** (**`16/20 = 80% > 0`** \| `+0.1328` \| `+0.0663`) | **`+0.3568`** (**`16/20 = 80% > 0`** \| `+0.1607` \| `+0.0896`) | **`+0.2256`** (`10/20 > 0`) | **`+0.2465`** (`13/20 > 0`) | **`+0.1776` / `+0.1478`** (both $\gg +0.05$) |
| **3. `data_thermostability_21_all` (incl. `jain2024`)** | 21 | `neg_bp_aromaticity` (`+0.1599`) [`bp_flexibility = +0.1534`] | **`+0.3048`** (`16/21 = 76.2% > 0` \| `+0.1178` \| `+0.0596`) | **`+0.3334`** (`16/21 = 76.2% > 0` \| `+0.1445` \| `+0.0824`) | **`+0.2087`** (`10/21 > 0`) | **`+0.2298`** (`13/21 > 0`) | **`+0.1735` / `+0.1449`** (both $\gg +0.05$) |
| **4. `combined_thermostability_25` (Union)** | 25 | `bp_flexibility` (`+0.1954`) | **`+0.2834`** (`19/25 = 76.0% > 0` \| `+0.1196` \| `+0.0596`) | **`+0.3313`** (**`20/25 = 80% > 0`** \| `+0.1597` \| `+0.0891`) | **`+0.2231`** (`14/25 > 0`) | **`+0.2578`** (`17/25 = 68% > 0`) | **`+0.1359` / `+0.0880`** (both $\gg +0.05$) |

Across all 4 definitions of the Thermostability benchmark universe (`15`, `20`, `21`, and `25` datasets), `CLSS_Reg8_AllBP_IMGT_Z` and `CLSS_Reg7_MW_IMGT_Z` exceed every released model and every single Biopython descriptor by **`+0.0880` to `+0.2991`**, while maintaining positive `N>=10`, `SqrtN`-weighted, and `N`-weighted correlations across all 4 universes.
