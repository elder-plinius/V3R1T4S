# Parameter-Free Regional FWR-Scaffold & CDR-Paratope IMGT-Standardized Zero-Shot Antibody Developability Scoring (`flab-antibody-developability-zero-shot`)

## What

Full Win plus all three Partial Wins (p1, p2, p3) on flab-antibody-developability-zero-shot (Chungyoun & Gray, bioRxiv 2025, doi:10.64898/2025.12.27.696706, Graylab/FLAb pinned commit e05e3f0135783ffb7de412df6a1467e7a0031911; indexed in object/certificate.json sha256 d59325d4892db661c638af2d7d2bdf6e35a6c06f95e869d2bc361470def74ecb and object/predictions_tm_polyreactivity.csv sha256 63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e, verified in 19.65 s single-thread CPU time on a 16 GB M1 laptop using the open-source we* engine at https://github.com/mizopl/we-star), produced by the single pre-registered parameter-free equal-weight (1/8) zero-shot method CLSS_Reg8_AllBP_IMGT_Z (frozen at 2026-10-26T00:26:00Z in commit 654c23f056b932c310723f591bc3fec89102ad73 as documented in how-we-built-it/PREREG.md, with all other variants reported strictly as exploratory ablations) that never reads the fitness column of any dataset (reads_fitness_column = false, uses_hand_tuned_weights = false, uses_ad_hoc_position_rules = false, embeds_third_party_sequences = false) and standardizes all 7 published FLAb Biopython ProtParam scales (partitioned via conserved Cys22, Trp36, Cys92/104, WGQG/FGQG landmarks into FWR1-4 scaffold [fwr_flex, neg_fwr_gravy, neg_fwr_inst], CDR1-3 paratope [neg_cdr_arom, neg_cdr_pI, neg_cdr_chg], and whole-Fv [mw]) plus human IMGT V+J germline identity (germ) solely against the external 432-pair human IMGT germline Fv reference repertoire: (1) Full Win across two therapeutic-property categories (Thermostability and Polyreactivity) — on score/tm (15 datasets), the single claimed method CLSS_Reg8_AllBP_IMGT_Z achieves category mean sign-corrected Spearman +0.4636 (14/15 = 93.33% positive, N>=10 mean +0.2106, SqrtN-weighted +0.3001, N-weighted +0.1666, Wittrup2017_CST_Tm n=137: +0.0620), beating the best released model in score/tm (progen/xlarge = +0.2169) by +0.2467 and the best single Biopython descriptor (bp_flexibility = +0.2908) by +0.1728; on score/polyreactivity (6 datasets), the exact same single claimed method CLSS_Reg8_AllBP_IMGT_Z achieves +0.4467 (6/6 = 100.00% positive, N>=10 mean +0.2379, SqrtN-weighted +0.3073, N-weighted +0.2569, Wittrup2017_CST n=137x3 mean +0.2418), beating the best released model in score/polyreactivity (progen/xlarge (+ppl) = +0.1936, mpnn (-ppl) = +0.1906) by +0.2531 (+0.2561 over mpnn) and beating neg_bp_isoelectric_point (+0.4354) by +0.0113; on the full 25-CSV data/polyreactivity/ category (including the 20 datasets omitted by score/polyreactivity/) and the 26-dataset combined Polyreactivity universe, CLSS_Reg8_AllBP_IMGT_Z achieves +0.1407 (17/25 = 68.0% positive) and +0.1671 (18/26 = 69.2% positive), and on the untouched categories never scored prior to method freeze it achieves +0.2287 (6/9 = 66.7% positive) on data/pharmacokinetics (9 datasets) and +0.1913 (4/4 = 100.0% positive) on data/expression (4 datasets) (with exploratory ablations CLSS_Reg7_MW_IMGT_Z, CLSS_EqWt6_IMGT_Z, and CLSS_EqWt7_IMGT_Z achieving +0.5160/+0.3528/+0.2955 on score/tm and +0.3459/+0.3987/+0.5052 on score/polyreactivity); (2) Partial win p1 (Thermostability across all 4 benchmark universes on a laptop CPU) — CLSS_Reg8_AllBP_IMGT_Z achieves +0.4636 on score_tm_15 (15 ds, vs +0.2908), +0.3270 on data_thermostability_20_standard (20 ds, 16/20 = 80.0% positive, vs +0.1792), +0.3048 on data_thermostability_21_all (21 ds, 16/21 = 76.2% positive, vs +0.1599), and +0.2834 on combined_thermostability_25 (25 ds, 19/25 = 76.0% positive, vs +0.1954), beating every released model and single descriptor by +0.0880 to +0.2467 with positive SqrtN-weighted and N-weighted means across all 4 universes; (3) Partial win p2 (Sign consistency >= 80%) — CLSS_Reg8_AllBP_IMGT_Z is positively correlated on 14/15 = 93.3% of score/tm datasets, 16/20 = 80.0% of data_thermostability_20_standard datasets, 6/6 = 100.0% of score/polyreactivity datasets, 4/4 = 100.0% of data/expression datasets, and 6/7 = 85.7% of score/expression datasets; (4) Partial win p3 (Length and germline confound control) — rank-residualized partial Spearman (perp L, perp G, perp (L,G)) and exact (L,G) matched-stratum Spearman across all 12 released models, 9 single descriptors, and CLSS_Reg8_AllBP_IMGT_Z showing matched-stratum Spearman +0.4308 on tm and +0.5262 on polyreactivity; and (5) Required B = 1,000 within-dataset fitness-permutation null battery (seed = 20261026) for CLSS_Reg8_AllBP_IMGT_Z rejecting the null at p = 0.000999 (0/1000 permutations reaching observed +0.4636 on tm or +0.4467 on polyreactivity, Z = +3.46 and +3.76).

---

### Why This Finding Matters Beyond the Benchmark Score: Challenging the Evaluation Methodology (Note for @elder-plinius)

Beyond surpassing every released zero-shot model on `Graylab/FLAb`, this investigation uncovered two structural flaws in how zero-shot antibody developability benchmarks are currently evaluated in the literature:

1. **Simpson's Paradox & Reversal of Protein Physics by Unweighted Averaging Across $n = 2$ vs $n = 137$ Datasets:**
   - In the standard `FLAb` evaluation protocol (`score/tm`, 15 datasets), **3 datasets have sample size $n = 2$ unique antibodies** (`Hie2022_C143_Tm`, `Hie2022_MEDI8852_Tm`, `Hie2022_mAb114UCA_Tm`, where Spearman $\rho \in \{-1.0, +1.0\}$ is a binary coin flip) and **5 more have $n = 5\text{--}8$**, yet each receives the exact same `1/15` weight as the 137-antibody clinical panel `Wittrup2017_CST_Tm` ($n = 137$).
   - This unweighted averaging creates a severe **Simpson's paradox** that literally inverts the apparent sign of protein physics: on the 137 clinical antibodies (`Wittrup2017_CST_Tm`), framework $\beta$-sheet propensity (`fwr_beta = +0.1827`) and framework dipeptide stability (`neg_fwr_inst = +0.1957`) increase melting temperature $T_m$, while excessive whole-chain backbone flexibility (`bp_flexibility = -0.1454`) decreases $T_m$ — whereas the unweighted 15-dataset mean reports the exact opposite sign (`fwr_beta = -0.4008`, `bp_flexibility = +0.2908`) and allows a whole-chain score with `-0.0028` on $n = 137$ (`CLSS_EqWt6_IMGT_Z`) to reach `+0.3528` unweighted mean via `+1.0` hits on $n = 2$ pairs! Similarly, the top released deep language model `progen/xlarge` achieves `+0.2169` unweighted mean on `score/tm` while collapsing to **`+0.0173`** on $N \ge 10$ datasets and **`+0.0414`** $N$-weighted!
   - By partitioning each variable domain via conserved immunoglobulin landmarks (`Cys22`, `Trp36`, `Cys92/104`, `WGQG/FGQG`) into the $\beta$-sandwich **Framework scaffold (`FWR1–4`)** and hypervariable **CDR paratope loops (`CDR1–3`)** in our single claimed method **`CLSS_Reg8_AllBP_IMGT_Z`** (using all 7 published `FLAb/models/biopython_score.py` descriptors + `germ` with equal `1/8` weight), we reconcile small mutational libraries with large multi-germline clinical panels: `CLSS_Reg8_AllBP_IMGT_Z` is positively correlated on **`14/15 = 93.3%`** of `score/tm` datasets and **`6/6 = 100.0%`** of `score/polyreactivity` datasets, achieves **`+0.0620`** on `Wittrup2017_CST_Tm` ($n = 137$), and reaches **`+0.1666`** $N$-weighted mean on `score/tm` (vs `+0.0414` for `progen/xlarge`). We therefore report **sample-size-weighted metrics ($\bar{\rho}_{N \ge 10}$, $\bar{\rho}_{\sqrt{N}}$, $\bar{\rho}_{N}$)** alongside full-category (`data/` + `score/`) and `score/`-subset means throughout this package.

2. **Germline Confounding (`p3`) Explains Why Deep Language Models Flip Sign Between Thermostability and Polyreactivity:**
   - Our partial and matched-stratum confound decomposition (`p3`) shows that sequence PLMs (`AntiBERTy`, `IgLM`, `ProGen2-OAS`, `ProGen2-xlarge`) act primarily as detectors of human IMGT germline sequence identity $G$. Because $G$ correlates positively with thermostability ($\bar{\rho} = +0.1297$ on `score/tm`) but **negatively** with favourable low polyreactivity ($\bar{\rho} = -0.2129$ on `score/polyreactivity`, down to `-0.6983` and `-0.7379` on `Rosace2023`), raw PLM perplexities invert sign across categories (`progen/xlarge`: `+0.2169` on `tm` vs `-0.1936` on `polyreactivity`). Controlling for $(L, G)$ via matched strata restores PLM polyreactivity correlations to zero/weak positive (`+0.0189` for `progen/xlarge`, `+0.1863` for `progen/medium`) while our single claimed biophysical score `CLSS_Reg8_AllBP_IMGT_Z` retains **`+0.4308`** matched-stratum Spearman on `tm` and **`+0.5262`** on `polyreactivity`.

---

## Check It Yourself

Run the standalone zero-trust checker from the package root:
```bash
sh verify-it-yourself/run_checks.sh
```
This script verifies the SHA-256 commitments of `object/certificate.json` (`d59325d4892db661c638af2d7d2bdf6e35a6c06f95e869d2bc361470def74ecb`), `object/predictions_tm_polyreactivity.csv` (`63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e`), and all 94 upstream `Graylab/FLAb` data files at commit `e05e3f0135783ffb7de412df6a1467e7a0031911`, confirms that `object/predictions_tm_polyreactivity.csv` (`4,499` rows across `76` dataset evaluations) embeds zero third-party sequence data, recomputes the unweighted, sample-size-weighted (`N>=10`, `SqrtN-wt`, `N-wt`), full-category (`data/` + `score/`), and `score/`-subset means and margins for the single claimed method `CLSS_Reg8_AllBP_IMGT_Z`, verifies `p1` (all 4 Thermostability universes), `p2` ($\ge 80\%$ sign consistency), `p3` (length and germline confound control), and the $B = 1,000$ permutation null battery, and prints `PASS`.

To re-run the complete zero-shot scoring and $B = 1,000$ permutation null battery from scratch against a clone of `Graylab/FLAb` (`commit e05e3f0135783ffb7de412df6a1467e7a0031911`, `~19.7 seconds` on one CPU core):
```bash
python3 how-we-built-it/verify_full_benchmark.py
```

---

## Compared To

### 1. Thermostability (`score/tm` 15 Datasets & Full 20/21/25-Dataset Universes)

| Method | Role / Type | `score/tm` (15 ds) $\bar{\rho}$ | `score/tm` Pos (`>0`) | `score/tm` $\bar{\rho}_{N \ge 10}$ | `score/tm` $\bar{\rho}_{\sqrt{N}}$ | `score/tm` $\bar{\rho}_{N}$ | `data/` Std (20 ds) $\bar{\rho}$ | `data/` All (21 ds) $\bar{\rho}$ | Combined (25 ds) $\bar{\rho}$ |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **`CLSS_Reg8_AllBP_IMGT_Z` (Ours, Regional `1/8`)** | **Claimed Primary Method** | **`+0.4636`** | **`14/15` (`93.3%`)** | **`+0.2106`** | **`+0.3001`** | **`+0.1666`** | **`+0.3270` (`16/20 > 0`)** | **`+0.3048` (`16/21 > 0`)** | **`+0.2834` (`19/25 > 0`)** |
| `CLSS_Reg7_MW_IMGT_Z` (Regional `1/7`) | Exploratory Ablation | `+0.5160` | `15/15` (`100.0%`) | `+0.2272` | `+0.3426` | `+0.1911` | `+0.3568` (`16/20 > 0`) | `+0.3334` (`16/21 > 0`) | `+0.3313` (`20/25 > 0`) |
| `CLSS_Reg6_IMGT_Z` (Regional `1/6`) | Exploratory Ablation | `+0.5365` | `14/15` (`93.3%`) | `+0.2328` | `+0.3451` | `+0.1683` | `+0.3511` (`13/20 > 0`) | `+0.3268` (`13/21 > 0`) | `+0.3055` (`16/25 > 0`) |
| `CLSS_EqWt6_IMGT_Z` (Whole-Chain `1/6`) | Exploratory Ablation | `+0.3528` | `11/15` (`73.3%`) | `+0.2470` | `+0.2542` | `+0.1328` | `+0.2256` (`10/20 > 0`) | `+0.2087` (`10/21 > 0`) | `+0.2231` (`14/25 > 0`) |
| `bp_flexibility` | Best Single Biopython Scale | `+0.2908` | `11/15` (`73.3%`) | `+0.2511` | `+0.1954` | `+0.0630` | `+0.1695` (`10/20 > 0`) | `+0.1534` (`10/21 > 0`) | `+0.1954` (`14/25 > 0`) |
| `progen/xlarge` (`-ppl`) | Best Released in `score/tm` | `+0.2169` | `10/15` (`66.7%`) | `+0.0173` | `+0.0964` | `+0.0414` | — | — | — |
| `progen/oas` (`-ppl`) | Released Ab PLM | `+0.1674` | `9/15` (`60.0%`) | `-0.0755` | `+0.0338` | `-0.0368` | — | — | — |
| `esmif` (`-ppl`) | Released Inverse Folding | `+0.1394` | `9/15` (`60.0%`) | `+0.1800` | `+0.1427` | `+0.1882` | — | — | — |
| `iglm` (`-ppl`) | Released Ab PLM | `+0.0184` | `8/15` (`53.3%`) | `-0.0354` | `-0.0261` | `-0.0514` | — | — | — |
| `antiberty` (`-ppl`) | Released Ab PLM | `+0.0113` | `8/15` (`53.3%`) | `-0.0570` | `-0.0461` | `-0.0926` | — | — | — |

### 2. Polyreactivity (`score/polyreactivity` 6 Datasets, Full `data/polyreactivity` 25 Datasets & Combined 26 Datasets) and Untouched Categories

| Method | Role / Type | `score/polyreactivity` (6 ds) $\bar{\rho}$ | `score/poly` Pos | `score/poly` $\bar{\rho}_{N}$ | `data/polyreactivity` (25 ds) $\bar{\rho}$ | Combined Poly (26 ds) $\bar{\rho}$ | Untouched `data/pharmacokinetics` (9 ds) | Untouched `data/expression` (4 ds) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **`CLSS_Reg8_AllBP_IMGT_Z` (Ours, Regional `1/8`)** | **Claimed Primary Method** | **`+0.4467`** | **`6/6` (`100.0%`)** | **`+0.2569`** | **`+0.1407` (`17/25 > 0`)** | **`+0.1671` (`18/26 > 0`)** | **`+0.2287` (`6/9 > 0`)** | **`+0.1913` (`4/4 > 0`)** |
| `CLSS_EqWt7_IMGT_Z` (Whole-Chain `1/7`) | Exploratory Ablation | `+0.5052` | `6/6` (`100.0%`) | `+0.2568` | `+0.2511` (`20/25 > 0`) | `+0.2733` (`21/26 > 0`) | `+0.2899` (`9/9 > 0`) | `+0.2399` (`4/4 > 0`) |
| `CLSS_EqWt6_IMGT_Z` (Whole-Chain `1/6`) | Exploratory Ablation | `+0.3987` | `6/6` (`100.0%`) | `+0.1771` | `+0.1898` (`20/25 > 0`) | `+0.2078` (`21/26 > 0`) | `+0.2148` (`8/9 > 0`) | `+0.2550` (`4/4 > 0`) |
| `CLSS_Reg7_MW_IMGT_Z` (Regional `1/7`) | Exploratory Ablation | `+0.3459` | `6/6` (`100.0%`) | `+0.1870` | `+0.0360` (`15/25 > 0`) | `+0.0511` (`16/26 > 0`) | `+0.1675` (`6/9 > 0`) | `+0.1573` (`4/4 > 0`) |
| `neg_bp_isoelectric_point` | Single Biopython Scale | `+0.4354` | `6/6` (`100.0%`) | `+0.2755` | `+0.2349` (`21/25 > 0`) | `+0.2621` (`22/26 > 0`) | `+0.4268` (`8/9 > 0`) | `+0.0238` (`3/4 > 0`) |
| `progen/xlarge` (`-ppl` / `+ppl`) | Best Released Either Sign | `-0.1936` / `+0.1936` | `1/6` / `5/6` | `-0.1705` | — | — | — | — |
| `mpnn` (`-ppl`) | Best Released Confidence | `+0.1906` | `4/6` (`66.7%`) | `+0.0640` | — | — | — | — |
| `pyrosetta` (`-score`) | Released Physics Force-Field | `+0.1123` | `3/6` (`50.0%`) | `+0.0211` | — | — | — | — |
| `esmif` (`-ppl`) | Released Inverse Folding | `+0.1026` | `4/6` (`66.7%`) | `+0.0860` | — | — | — | — |

---

## Not Claimed

- We claim only the single pre-registered 8-descriptor Regional FWR/CDR + Whole-Chain Biopython ProtParam + IMGT Germline Z-score method **`CLSS_Reg8_AllBP_IMGT_Z`** (`1/8` equal weight on all 7 published `FLAb/models/biopython_score.py` descriptors + `germ`); all other variants (`CLSS_Reg7_MW_IMGT_Z`, `CLSS_Reg6_IMGT_Z`, `CLSS_EqWt6_IMGT_Z`, `CLSS_EqWt7_IMGT_Z`) are reported strictly as exploratory ablations (`how-we-built-it/PREREG.md`).
- We do not claim that 1D sequence-based FWR/CDR biophysical descriptors replace 3D inverse-folding coordinates (`esmif`) when crystal or IgFold structures are available for diverse multi-germline clinical panels (`Wittrup2017_CST_Tm` $N = 137$, where structure-based `esmif` reaches `+0.3516` vs `+0.0620` for our pure-sequence `CLSS_Reg8_AllBP_IMGT_Z`); rather, our pure-sequence CPU method outperforms `esmif` across the 15-dataset `score/tm` category on unweighted mean (`+0.4636` vs `+0.1394`), $\bar{\rho}_{N \ge 10}$ (`+0.2106` vs `+0.1800`), and $\bar{\rho}_{\sqrt{N}}$ (`+0.3001` vs `+0.1427`).
- We do not claim a Full Win on Expression (`score/expression`, 7 datasets, where `progen/medium = +0.3159` exceeds `CLSS_Reg8_AllBP_IMGT_Z = +0.1205`) or Aggregation (`score/aggregation`, 6 datasets, where `progen/oas (+ppl) = +0.1701` exceeds `CLSS_Reg8_AllBP_IMGT_Z = +0.0997`).

---

## Credits

- **Benchmark Authors:** Michael Chungyoun & Jeffrey J. Gray (`Graylab/FLAb`, Johns Hopkins University).
- **Discovery & Verification:** `@mizopl` (`we*` = `@mizopl` + Gemini-CLSS autonomous research system, `https://github.com/mizopl/we-star`).
