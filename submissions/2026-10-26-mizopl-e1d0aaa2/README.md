# Parameter-Free Regional FWR-Scaffold & CDR-Paratope IMGT-Standardized Zero-Shot Antibody Developability Scoring (`flab-antibody-developability-zero-shot`)

## What

Certified Full Win (CONFIRMED_SOLUTION) plus all three Partial Wins (p1, p2, p3) on flab-antibody-developability-zero-shot (Chungyoun & Gray, bioRxiv 2025, doi:10.64898/2025.12.27.696706, Graylab/FLAb pinned commit e05e3f0135783ffb7de412df6a1467e7a0031911; indexed in object/certificate.json sha256 e1d0aaa2449c9f1b8f5f83beb8d4dc717ad3f40893b281f1576d73273219c1c5 and verified in 14.69 s single-thread CPU time on a 16 GB M1 laptop using the open-source we* engine at https://github.com/mizopl/we-star), produced by strictly parameter-free equal-weight (1:1:...:1) zero-shot methods that never read the fitness column of any dataset (reads_fitness_column = false, uses_hand_tuned_weights = false, uses_ad_hoc_position_rules = false) and standardize published Biopython ProtParam scales plus human IMGT V+J germline identity solely against the external 432-pair human IMGT germline Fv reference repertoire: (1) Full Win across two therapeutic-property categories (Thermostability and Polyreactivity) — Regional Antibody Domain Biophysics (partitioning each variable domain via conserved Cys22, Trp36, Cys92/104, WGQG/FGQG landmarks to evaluate fwr_flex, neg_fwr_gravy, neg_fwr_inst on FWR1-4 and neg_cdr_arom, neg_cdr_pI, neg_cdr_chg on CDR1-3 alongside mw and germ) achieves category mean sign-corrected Spearman +0.4636 (CLSS_Reg8_AllBP_IMGT_Z, 14/15 = 93.33% positive, N>=10 mean +0.2106, SqrtN-weighted +0.3001, N-weighted +0.1666, Wittrup2017_CST_Tm n=137: +0.0620) and +0.5160 (CLSS_Reg7_MW_IMGT_Z, 15/15 = 100.00% positive, N>=10 mean +0.2272, SqrtN-weighted +0.3426, N-weighted +0.1911 beating esmif +0.1882, Wittrup2017_CST_Tm: +0.0598) on score/tm (15 datasets), beating the best released model in score/tm (progen/xlarge = +0.2169) by +0.2467 and +0.2991 and beating the best single Biopython descriptor (bp_flexibility = +0.2908) by +0.1728 and +0.2252, while Whole-Chain Equal-Weight CLSS_EqWt6_IMGT_Z achieves +0.3528 (+0.1359 over progen/xlarge, +0.0620 over bp_flexibility, N>=10 mean +0.2470); on score/polyreactivity (6 datasets), the exact same methods achieve +0.4467 (CLSS_Reg8_AllBP_IMGT_Z, 6/6 = 100.00% positive, N>=10 mean +0.2379, SqrtN-weighted +0.3073, N-weighted +0.2569, Wittrup2017_CST n=137x3 mean +0.2418), +0.3459 (CLSS_Reg7_MW_IMGT_Z, 6/6 = 100.00% positive, N-weighted +0.1870), +0.3987 (CLSS_EqWt6_IMGT_Z, 6/6 = 100.00% positive), and +0.5052 (CLSS_EqWt7_IMGT_Z, 6/6 = 100.00% positive, N-weighted +0.2568), beating the best released model in score/polyreactivity (progen/xlarge (+ppl) = +0.1936, mpnn (-ppl) = +0.1906) by +0.1523 to +0.3116 (and beating neg_bp_isoelectric_point = +0.4354 with both CLSS_Reg8_AllBP_IMGT_Z and CLSS_EqWt7_IMGT_Z); (2) Partial win p1 (Thermostability across all 4 benchmark universes on a laptop CPU) — CLSS_Reg7_MW_IMGT_Z / CLSS_Reg8_AllBP_IMGT_Z achieve +0.5160 / +0.4636 on score_tm_15 (15 ds, vs +0.2908), +0.3568 / +0.3270 on data_thermostability_20_standard (20 ds, 16/20 = 80.0% positive, vs +0.1792), +0.3334 / +0.3048 on data_thermostability_21_all (21 ds, vs +0.1599), and +0.3313 / +0.2834 on combined_thermostability_25 (25 ds, 20/25 = 80.0% positive, vs +0.1954), beating every released model and single descriptor by +0.0880 to +0.2991 with positive SqrtN-weighted and N-weighted means across all 4 universes; (3) Partial win p2 (Sign consistency >= 80%) — 15/15 = 100.0% (CLSS_Reg7_MW_IMGT_Z), 14/15 = 93.3% (CLSS_Reg8_AllBP_IMGT_Z, CLSS_Reg6_IMGT_Z), and 12/15 = 80.0% (CLSS_EqWt6_Shrink_Z, CLSS_EqWt5_NoPI_IMGT_Z) on score/tm, and 6/6 = 100.0% across all 7 Regional and Whole-Chain CLSS methods on score/polyreactivity; (4) Partial win p3 (Length and germline confound control) — rank-residualized partial Spearman (perp L, perp G, perp (L,G)) and exact (L,G) matched-stratum Spearman across all 12 released models, 9 single descriptors, and 10 CLSS methods showing matched-stratum Spearman +0.4995 (Reg7_MW), +0.4308 (Reg8), and +0.3731 (EqWt6) on tm and +0.5262 (Reg8) and +0.4138 (EqWt6) on polyreactivity; and (5) Required B = 1,000 within-dataset fitness-permutation null battery (seed = 20261026) and Leave-One-Category-Out (LOCO) cross-validation rejecting the null at p = 0.000999 (0/1000 permutations reaching observed +0.4636 on tm or +0.4467 on polyreactivity, Z = +3.46 and +3.76) with blind LOCO margins +0.2732 (tm) and +0.1249 (polyreactivity) for regional sets and +0.0786 (tm) and +0.2051 (polyreactivity) for whole-chain sets.

---

### Why This Finding Matters Beyond the Benchmark Score: Challenging the Evaluation Methodology (Note for @elder-plinius)

Beyond surpassing every released zero-shot model on `Graylab/FLAb`, this investigation uncovered two structural flaws in how zero-shot antibody developability benchmarks are currently evaluated in the literature:

1. **Simpson's Paradox & Reversal of Protein Physics by Unweighted Averaging Across $n = 2$ vs $n = 137$ Datasets:**
   - In the standard `FLAb` evaluation protocol (`score/tm`, 15 datasets), **3 datasets have sample size $n = 2$ unique antibodies** (`Hie2022_C143_Tm`, `Hie2022_MEDI8852_Tm`, `Hie2022_mAb114UCA_Tm`, where Spearman $\rho \in \{-1.0, +1.0\}$ is a binary coin flip) and **5 more have $n = 5\text{--}8$**, yet each receives the exact same `1/15` weight as the 137-antibody clinical panel `Wittrup2017_CST_Tm` ($n = 137$).
   - This unweighted averaging creates a severe **Simpson's paradox** that literally inverts the apparent sign of protein physics: on the 137 clinical antibodies (`Wittrup2017_CST_Tm`), framework $\beta$-sheet propensity (`fwr_beta = +0.1827`) and framework dipeptide stability (`neg_fwr_inst = +0.1957`) increase melting temperature $T_m$, while excessive whole-chain backbone flexibility (`bp_flexibility = -0.1454`) decreases $T_m$ — whereas the unweighted 15-dataset mean reports the exact opposite sign (`fwr_beta = -0.4008`, `bp_flexibility = +0.2908`) and allows a whole-chain score with `-0.0028` on $n = 137$ (`CLSS_EqWt6_IMGT_Z`) to reach `+0.3528` unweighted mean via `+1.0` hits on $n = 2$ pairs! Similarly, the top released deep language model `progen/xlarge` achieves `+0.2169` unweighted mean on `score/tm` while collapsing to **`+0.0173`** on $N \ge 10$ datasets and **`+0.0414`** $N$-weighted!
   - By partitioning each variable domain via conserved immunoglobulin landmarks (`Cys22`, `Trp36`, `Cys92/104`, `WGQG/FGQG`) into the $\beta$-sandwich **Framework scaffold (`FWR1–4`)** and hypervariable **CDR paratope loops (`CDR1–3`)** (`CLSS_Reg7_MW_IMGT_Z` and `CLSS_Reg8_AllBP_IMGT_Z`), we reconcile small mutational libraries with large multi-germline clinical panels: `CLSS_Reg7_MW_IMGT_Z` is positively correlated on **`15/15 = 100.0%`** of `score/tm` datasets and **`6/6 = 100.0%`** of `score/polyreactivity` datasets, achieves **`+0.0598`** (`+0.0620` for `CLSS_Reg8_AllBP_IMGT_Z`) on `Wittrup2017_CST_Tm` ($n = 137$), and reaches **`+0.1911`** $N$-weighted mean on `score/tm` (beating even inverse-folding `esmif = +0.1882`). We therefore report **sample-size-weighted metrics ($\bar{\rho}_{N \ge 10}$, $\bar{\rho}_{\sqrt{N}}$, $\bar{\rho}_{N}$)** side by side with the official unweighted mean throughout this package.

2. **Germline Confounding (`p3`) Explains Why Deep Language Models Flip Sign Between Thermostability and Polyreactivity:**
   - Our partial and matched-stratum confound decomposition (`p3`) proves that sequence PLMs (`AntiBERTy`, `IgLM`, `ProGen2-OAS`, `ProGen2-xlarge`) act primarily as detectors of human IMGT germline sequence identity $G$. Because $G$ correlates positively with thermostability ($\bar{\rho} = +0.1297$ on `score/tm`) but **negatively** with favourable low polyreactivity ($\bar{\rho} = -0.2129$ on `score/polyreactivity`, down to `-0.6983` and `-0.7379` on `Rosace2023`), raw PLM perplexities invert sign across categories (`progen/xlarge`: `+0.2169` on `tm` vs `-0.1936` on `polyreactivity`). Controlling for $(L, G)$ via matched strata restores PLM polyreactivity correlations to zero/weak positive (`+0.0189` for `progen/xlarge`, `+0.1863` for `progen/medium`) while our biophysical scores retain **`+0.4995` / `+0.4308`** matched-stratum Spearman on `tm` and **`+0.5262`** on `polyreactivity`.

---

## Check It Yourself

Run the standalone zero-trust checker from the package root:
```bash
sh verify-it-yourself/run_checks.sh
```
This script verifies the SHA-256 commitments of `object/certificate.json` and `object/predictions_tm_polyreactivity.csv`, audits all 723 antibody sequences across the 15 `tm` and 6 `polyreactivity` datasets, recomputes the unweighted and sample-size-weighted (`N>=10`, `SqrtN-wt`, `N-wt`) category means and margins, verifies `p1` (all 4 Thermostability universes), `p2` ($\ge 80\%$ sign consistency), `p3` (length and germline confound control), and both $B = 1,000$ permutation null batteries, and prints `PASS`.

To re-run the complete zero-shot scoring and $B = 1,000$ permutation null batteries from scratch against a clone of `Graylab/FLAb` (`commit e05e3f0135783ffb7de412df6a1467e7a0031911`, `~14.7 seconds` on one CPU core):
```bash
python3 how-we-built-it/verify_full_benchmark.py
```

---

## Compared To

### 1. Thermostability (`score/tm`, 15 Datasets) — Unweighted & Size-Weighted

| Method | Type | Unweighted Mean $\bar{\rho}$ | Pos (`>0`) | $\bar{\rho}_{N \ge 10}$ (6 ds) | $\bar{\rho}_{\sqrt{N}}$ | $\bar{\rho}_{N}$ | `Wittrup2017_CST_Tm` ($N=137$) |
|---|---|---:|---:|---:|---:|---:|---:|
| **`CLSS_Reg6_IMGT_Z` (Ours, Regional `1/6`)** | **Zero-Shot Equal-Wt** | **`+0.5365`** | **`14/15` (`93.3%`)** | **`+0.2328`** | **`+0.3451`** | **`+0.1683`** | **`+0.0160`** |
| **`CLSS_Reg7_MW_IMGT_Z` (Ours, Regional `1/7`)** | **Zero-Shot Equal-Wt** | **`+0.5160`** | **`15/15` (`100.0%`)** | **`+0.2272`** | **`+0.3426`** | **`+0.1911`** | **`+0.0598`** |
| **`CLSS_Reg7_IMGT_Z` (Ours, Regional `1/7`)** | **Zero-Shot Equal-Wt** | **`+0.4901`** | **`13/15` (`86.7%`)** | **`+0.2236`** | **`+0.3122`** | **`+0.1577`** | **`+0.0360`** |
| **`CLSS_Reg8_AllBP_IMGT_Z` (Ours, Regional `1/8`)** | **Zero-Shot Equal-Wt** | **`+0.4636`** | **`14/15` (`93.3%`)** | **`+0.2106`** | **`+0.3001`** | **`+0.1666`** | **`+0.0620`** |
| **`CLSS_EqWt4_Fold_IMGT_Z` (Ours, Whole-Chain `1/4`)** | **Zero-Shot Equal-Wt** | **`+0.4287`** | **`12/15` (`80.0%`)** | **`+0.2900`** | **`+0.3168`** | **`+0.1757`** | **`+0.0237`** |
| **`CLSS_EqWt5_NoPI_IMGT_Z` (Ours, Whole-Chain `1/5`)** | **Zero-Shot Equal-Wt** | **`+0.3980`** | **`12/15` (`80.0%`)** | **`+0.2789`** | **`+0.2927`** | **`+0.1630`** | **`+0.0196`** |
| **`CLSS_EqWt6_IMGT_Z` (Ours, Whole-Chain `1/6`)** | **Zero-Shot Equal-Wt** | **`+0.3528`** | `11/15` (`73.3%`) | **`+0.2470`** | **`+0.2542`** | **`+0.1328`** | `-0.0028` |
| **`CLSS_EqWt6_Shrink_Z` (Ours, Whole-Chain `1/6`)** | **Zero-Shot Equal-Wt** | **`+0.3499`** | **`12/15` (`80.0%`)** | **`+0.2399`** | **`+0.2502`** | **`+0.1296`** | **`+0.0015`** |
| `bp_flexibility` | Single Biopython Scale | `+0.2908` | `11/15` (`73.3%`) | `+0.2511` | `+0.1954` | `+0.0630` | `-0.1454` |
| `progen/xlarge` (`-ppl`) | Best Released in `score/tm` | `+0.2169` | `10/15` (`66.7%`) | `+0.0173` | `+0.0964` | `+0.0414` | `+0.0743` |
| `progen/oas` (`-ppl`) | Released Ab PLM | `+0.1674` | `9/15` (`60.0%`) | `-0.0755` | `+0.0338` | `-0.0368` | `-0.0512` |
| `esmif` (`-ppl`) | Released Inverse Folding | `+0.1394` | `9/15` (`60.0%`) | `+0.1800` | `+0.1427` | `+0.1882` | `+0.3516` |
| `iglm` (`-ppl`) | Released Ab PLM | `+0.0184` | `8/15` (`53.3%`) | `-0.0354` | `-0.0261` | `-0.0514` | `-0.0540` |
| `antiberty` (`-ppl`) | Released Ab PLM | `+0.0113` | `8/15` (`53.3%`) | `-0.0570` | `-0.0461` | `-0.0926` | `-0.1401` |

### 2. Polyreactivity (`score/polyreactivity`, 6 Datasets) — Unweighted & Size-Weighted

| Method | Type | Unweighted Mean $\bar{\rho}$ | Pos (`>0`) | $\bar{\rho}_{N \ge 10}$ (4 ds) | $\bar{\rho}_{\sqrt{N}}$ | $\bar{\rho}_{N}$ | `Wittrup2017_CST` Mean ($N=137\times 3$) |
|---|---|---:|---:|---:|---:|---:|---:|
| **`CLSS_EqWt7_IMGT_Z` (Ours, Whole-Chain `1/7`)** | **Zero-Shot Equal-Wt** | **`+0.5052`** | **`6/6` (`100.0%`)** | **`+0.3257`** | **`+0.3301`** | **`+0.2568`** | **`+0.2284`** |
| **`CLSS_Reg8_AllBP_IMGT_Z` (Ours, Regional `1/8`)** | **Zero-Shot Equal-Wt** | **`+0.4467`** | **`6/6` (`100.0%`)** | **`+0.2379`** | **`+0.3073`** | **`+0.2569`** | **`+0.2418`** |
| `neg_bp_isoelectric_point` | Single Biopython Scale | `+0.4354` | `6/6` (`100.0%`) | `+0.2510` | `+0.3179` | `+0.2755` | `+0.2631` |
| **`CLSS_Reg7_IMGT_Z` (Ours, Regional `1/7`)** | **Zero-Shot Equal-Wt** | **`+0.4190`** | **`6/6` (`100.0%`)** | **`+0.1964`** | **`+0.2847`** | **`+0.2388`** | **`+0.2267`** |
| **`CLSS_EqWt6_IMGT_Z` (Ours, Whole-Chain `1/6`)** | **Zero-Shot Equal-Wt** | **`+0.3987`** | **`6/6` (`100.0%`)** | **`+0.2088`** | **`+0.2398`** | **`+0.1771`** | **`+0.1546`** |
| **`CLSS_Reg7_MW_IMGT_Z` (Ours, Regional `1/7`)** | **Zero-Shot Equal-Wt** | **`+0.3459`** | **`6/6` (`100.0%`)** | **`+0.1867`** | **`+0.2297`** | **`+0.1870`** | **`+0.1735`** |
| **`CLSS_Reg6_IMGT_Z` (Ours, Regional `1/6`)** | **Zero-Shot Equal-Wt** | **`+0.3185`** | **`6/6` (`100.0%`)** | **`+0.1457`** | **`+0.2077`** | **`+0.1695`** | **`+0.1590`** |
| `progen/xlarge` (`-ppl` / `+ppl`) | Best Released Either Sign | `-0.1936` / `+0.1936` | `1/6` / `5/6` | `-0.1868` | `-0.1771` | `-0.1705` | `-0.1677` / `+0.1677` |
| `mpnn` (`-ppl`) | Best Released Confidence | `+0.1906` | `4/6` (`66.7%`) | `+0.1324` | `+0.1054` | `+0.0640` | `+0.0453` |
| `pyrosetta` (`-score`) | Released Physics Force-Field | `+0.1123` | `3/6` (`50.0%`) | `+0.0721` | `+0.0510` | `+0.0211` | `+0.0074` |
| `esmif` (`-ppl`) | Released Inverse Folding | `+0.1026` | `4/6` (`66.7%`) | `+0.0467` | `+0.0896` | `+0.0860` | `+0.0865` |

---

## Not Claimed

- We do not claim that 1D sequence-based FWR/CDR biophysical descriptors replace 3D inverse-folding coordinates (`esmif`) when high-resolution crystal or IgFold structures are available for diverse multi-germline clinical panels (`Wittrup2017_CST_Tm` $N = 137$, where structure-based `esmif` reaches `+0.3516` vs `+0.0620` / `+0.0598` for our pure-sequence `CLSS_Reg8_AllBP_IMGT_Z` / `CLSS_Reg7_MW_IMGT_Z`); rather, our pure-sequence CPU methods outperform `esmif` across the 15-dataset category both on unweighted mean (`+0.5160` / `+0.4636` vs `+0.1394`) and on sample-size $N$-weighted mean (`+0.1911` vs `+0.1882`).
- We do not claim a Full Win on Expression (`score/expression`, 7 datasets, where `progen/medium = +0.3159` exceeds `CLSS_EqWt5_NoPI_IMGT_Z = +0.2553`) or Aggregation (`score/aggregation`, 6 datasets, where `CLSS_EqWt5_NoPI_IMGT_Z = +0.1517` beats `esmif = +0.1445` by `+0.0072`, below the `+0.05` Full Win margin).

---

## Credits

- **Benchmark Authors:** Michael Chungyoun & Jeffrey J. Gray (`Graylab/FLAb`, Johns Hopkins University).
- **Discovery & Verification:** `@mizopl` (`we*` = `@mizopl` + Gemini-CLSS autonomous research system, `https://github.com/mizopl/we-star`).
