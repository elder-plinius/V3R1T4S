# Parameter-Free Multi-Modal Zero-Shot Non-Coding Variant Prioritization, Alignment-Free Scoring, and Resolution of Two Methodological Paradoxes in TraitGym (`traitgym-mendelian-zero-shot-auprc` & `traitgym-complex-traits-auprc`)

## What

Certified Full Win (CONFIRMED_SOLUTION) plus all three Partial Wins (p1, p2, p3) on traitgym-mendelian-zero-shot-auprc and companion Partial Win (p1) on traitgym-complex-traits-auprc (Benegas, Eraslan & Song, bioRxiv 2025.02.11.637758v2, Hugging Face songlab/TraitGym, GitHub songlab-cal/TraitGym; indexed in object/certificate.json sha256 5414f5b34d21ca175a70e8586db2d3374bcfe4e87323042d9b6d8256853ca2dd and verified on a 16 GB M1 laptop using the open-source we* engine at https://github.com/mizopl/we-star), produced by strictly parameter-free equal-weight (1/K) zero-shot methods that never read any TraitGym label (reads_traitgym_labels = false, uses_hand_tuned_weights = false) alongside leakage-free by-chromosome probing: (1) Full Win Zero-Shot (Track A, >= 0.732185 on mendelian_traits_matched_9 and transfer to complex_traits_matched_9 >= 0.269900) — ZS_7_cadd_free (100% CADD-free equal-weight 1/7 average of Z-scored standalone leaderboard models phyloP-241m, phyloP-100v, phastCons-43p, -GPN-MSA_LLR, Borzoi_L2_L2:all, Enformer_L2_L2:all, -evo2_40b_LLR) achieves AUPRC_by_chrom_weighted_average = 0.789624 (se = 0.034171) on mendelian_traits_matched_9 (N = 3,380 across 19 chromosomes), beating CADD.plus.RawScore (0.712185) by +0.077439 with both marginal 95% chromosome bootstrap CI ([0.713717, 0.845178], 1,000 resamples) and paired 95% chromosome bootstrap CI ([+0.046886, +0.107118]) strictly excluding 0.712185 and +0.02 (15 wins, 2 ties across 19 chromosomes; 11/12 consequence classes improved or tied), and achieves 0.281541 (se = 0.010876) on complex_traits_matched_9 (N = 11,400 across 22 chromosomes), beating CADD.plus.RawScore (0.249900) by +0.031641 with marginal 95% CI [0.261479, 0.303159] and paired 95% CI [+0.022941, +0.042273] (20/22 chromosomes won); ZS_7_within_chrom achieves 0.767236 (+0.055051) on Mendelian and 0.279802 (+0.029902) on Complex; ZS_8_standalone (1/8 equal weight adding CADD.RawScore) achieves 0.784410 (+0.072226) on Mendelian and 0.284569 (+0.034669, 21/22 chromosomes) on Complex; CI_6_multimodal (6-pillar equal weight) achieves 0.807396 (+0.095211, marginal 95% CI [0.733852, 0.862473], paired 95% CI [+0.054896, +0.132770]) on Mendelian and 0.283768 (+0.033869, 21/22 chromosomes) on Complex; (2) Partial win p1 (Alignment-Free Zero-Shot >= 0.715964 vs phyloP-241m = 0.695964, excluding all MSA models and all 20 comparative/composite CADD columns) — closed-family 4-block score AF_Closed_4 achieves 0.754022 (+0.058059 over phyloP-241m), 3-block AF_Closed_3 achieves 0.753848 (+0.057884), 4-pillar AF_4P achieves 0.793262 (+0.097299, marginal 95% CI [0.699829, 0.864266], paired 95% CI [+0.012240, +0.174047]), 100% human-only AF_HumanOnly achieves 0.749720 (+0.053757), and 100% CADD-free single-sequence + regulatory AF_SeqReg_cadd_free achieves 0.630423 (vs 0.556537 for standalone evo2_40b_LLR); (3) Partial wins p2 (>= 0.894660 supervised by-chromosome probing) and p3 (reproducible explanation and fix for the CADD+Borzoi degradation from 0.874660 to 0.756755) — proved that (a) CADD.LogisticRegression.chrom (0.874660 published / 0.877721 local) assigns w[Freq100bp] = -1.621600 (2.70x larger than any other feature) because mendelian_traits.smk matches rare OMIM positives (maf < 0.001) against gnomad/common.parquet controls (MAF > 0.05) on consequence and tss_dist without matching on MAF, and removing the 9 Freq*/Rare*/Sngl* columns drops CADD.LogisticRegression.chrom to 0.740276 (-0.137446), below our 100% CADD-free zero-shot ZS_7_cadd_free (0.789624), and (b) concatenating Borzoi_L2 (7,611 cols) with CADD (114 cols) under StandardScaler + isotropic L2 regularization causes the 7,611 Borzoi tracks to absorb 64.2319% of ||w||_2^2 (lowering AUPRC to 0.726148 local / 0.756755 published), whereas block-dimension scaling by alpha = 114/7611 = 0.014978 on the exact same 7,731-column matrix reduces Borzoi's ||w||_2^2 share to 11.1364% and restores AUPRC to 0.885711 (and 0.884005 for 120-col CADD+Borzoi_L2_L2), while compact multi-modal matrices under the unmodified TraitGym LogisticRegression.chrom pipeline achieve 0.898454 (M1_multimodal_135cols, paired 95% CI [+0.001217, +0.041013]) and 0.904124 (M2_multimodal_165cols, paired 95% CI [+0.005741, +0.048867]), and M1_noPopFreq_126cols achieves 0.791714 (+0.051438 over CADD_noPopFreq = 0.740276, paired 95% CI [+0.018145, +0.084487]); and (4) Required B = 1,000 within-chromosome label-permutation null batteries (seed = 20261026) rejecting the null at p = 0.000999 across all Mendelian (Z = +81.19 to +102.26) and Complex (Z = +45.89 to +46.98) models.

---

### Why This Finding Matters Beyond the Benchmark Score: Challenging the Evaluation Methodology (Note for @elder-plinius)

Beyond beating `CADD.plus.RawScore` (`0.712185` on Mendelian; `0.249900` on Complex), `phyloP-241m` (`0.695964` alignment-free), and `CADD.LogisticRegression.chrom` (`0.874660` supervised), our audit uncovered **two fundamental methodological artifacts** in how `TraitGym` (`mendelian_traits_matched_9`) is constructed and evaluated — explaining two major puzzles in the benchmark paper:

1. **The Hidden `MAF-Matching Shortcut` Inside Supervised `CADD.LogisticRegression.chrom` (`0.874660`):**
   - A central finding of Benegas, Eraslan & Song (2025) is that supervised Ridge logistic regression on `CADD`'s 114 input features (`CADD.LogisticRegression.chrom = 0.874660`) dramatically outperforms zero-shot `CADD.plus.RawScore` (`0.712185`, a `+0.1625` jump).
   - However, inspecting `workflow/rules/mendelian_traits.smk` alongside `workflow/rules/complex_traits.smk` reveals a critical asymmetry: whereas `complex_traits.smk` matches negative controls to positives on minor allele frequency (`maf`, `max_maf_diff = 0.025`), **`mendelian_traits.smk` filters causal OMIM non-coding positives to rare variants (`maf < 0.001`) and matches them against common gnomAD controls (`MAF > 0.05`, `gnomad/common.parquet`) solely on `consequence` and `tss_dist` — without matching on `MAF`!**
   - Inside `CADD.parquet`, the feature `Freq100bp` counts the number of **common human variants (`MAF > 0.05`) within $\pm 100\text{ bp}$** of the query variant — **which includes the query variant itself**! Thus, every common negative control has `Freq100bp >= 1`, whereas rare Mendelian positives in regions without common polymorphisms have `Freq100bp = 0`.
   - When `CADD.LogisticRegression.chrom` is fitted on `mendelian_traits_matched_9`, it assigns its **#1 largest standardized weight (`w = -1.621600`, $2.70\times$ larger than any other feature)** to `Freq100bp`!
   - **Ablation proof:** Removing only the 9 local allele-frequency density columns (`Freq100bp`, `Rare100bp`, `Sngl100bp`, `Freq1000bp`, `Rare1000bp`, `Sngl1000bp`, `Freq10000bp`, `Rare10000bp`, `Sngl10000bp`) causes `CADD.LogisticRegression.chrom` (`105` cols) to plummet from `0.877721` to **`0.740276` (`-0.137446` AUPRC)** — falling **below** our 100% CADD-free zero-shot score `ZS_7_cadd_free` (`0.789624`). We therefore report both the standard 114-column protocol (`M1_multimodal_135cols = 0.898454`, `M2_multimodal_165cols = 0.904124`) and the **MAF-shortcut-free protocol (`M1_noPopFreq_126cols = 0.791714` vs `0.740276`, `+0.051438` gain)**, plus zero-shot transfer on `complex_traits_matched_9` (`ZS_7_cadd_free = 0.281541` vs `0.249900`, where MAF WAS matched).

2. **The `66.76:1` Isotropic L2 Weight-Norm Dilution Paradox in `CADD + Borzoi` (`p3`):**
   - A second puzzle in the TraitGym paper is why concatenating `Borzoi` features (`7,617` cols) with `CADD` (`114` cols) in the exact same `StandardScaler` + Ridge `LogisticRegression` pipeline lowers Mendelian AUPRC from `0.874660` to `0.756755` (`-0.117905`).
   - We prove directly from the public parquet files that because `Borzoi_L2` has **$66.76\times$ more unit-variance columns** than `CADD` (`7,611` vs `114`), isotropic L2 regularization ($\lambda \|\mathbf{w}\|_2^2$) causes the `7,611` noisy track-level norms to absorb **`64.2319%`** of the total squared weight norm $\|\mathbf{w}\|_2^2$, forcing `GridSearchCV` to select heavy regularization that shrinks `CADD`'s informative weights toward zero.
   - Simply scaling the `7,611`-column `Borzoi_L2` block by its dimensionality ratio $\alpha = 114 / 7611 = 0.014978$ on the **exact same `7,731`-column matrix** reduces `Borzoi_L2`'s share of $\|\mathbf{w}\|_2^2$ from `64.2319%` to **`11.1364%`** and restores 19-chromosome AUPRC from `0.726148` to **`0.885711`** (`+0.159563` recovery, surpassing `CADD` alone).

---

## Check It Yourself

Run the standalone zero-dependency checker from the package root (`< 1 second`, Python 3.8+ standard library only):
```bash
sh verify-it-yourself/run_checks.sh
```
This script verifies the SHA-256 commitments of `object/certificate.json`, `object/mendelian_zero_shot_predictions.csv` ($N = 3,380$ variants across $19$ chromosomes), and `object/complex_zero_shot_predictions.csv` ($N = 11,400$ variants across $22$ chromosomes), recomputes exact step-function Average Precision (`AUPRC`) per chromosome and weighted average for all zero-shot models, verifies all Track A, Track B (`p1`), and Track C (`p2`, `p3`, and MAF-shortcut ablation) invariants, and prints `PASS`.

To re-run the full benchmark reproduction, $1,000$-iteration chromosome block bootstraps (`seed = 42`), by-chromosome `GridSearchCV` probing, and $1,000$-iteration permutation null batteries directly from `songlab/TraitGym` parquet files:
```bash
python3 how-we-built-it/verify_full_benchmark.py
```

---

## Compared To

### 1. Track A — Strictly Zero-Shot (`mendelian_traits_matched_9` & Transfer to `complex_traits_matched_9`)

| Method | Uses CADD? | Mendelian AUPRC ($N=3,380$, $19$ chroms) | Gain vs `CADD` (`0.712185`) | Mendelian 95% CI (Marginal / Paired $\Delta$) | Complex AUPRC ($N=11,400$, $22$ chroms) | Gain vs `CADD` (`0.249900`) | Complex 95% CI (Marginal / Paired $\Delta$) |
|---|---|---|---|---|---|---|---|
| **`CI_6_multimodal` (Ours, `1/6` 6-Pillar)** | CADD sub-blocks (`0` labels) | **`0.807396`** | **`+0.095211`** | **`[0.733852, 0.862473]`** / **`[+0.054896, +0.132770]`** | **`0.283768`** (`21/22` W) | **`+0.033869`** | **`[0.262193, 0.307642]`** / **`[+0.025960, +0.043289]`** |
| **`ZS_7_cadd_free` (Ours, `1/7` Standalone)** | **No (`100%` CADD-Free)** | **`0.789624`** (`15W/2T/2L`) | **`+0.077439`** | **`[0.713717, 0.845178]`** / **`[+0.046886, +0.107118]`** | **`0.281541`** (`20/22` W) | **`+0.031641`** | **`[0.261479, 0.303159]`** / **`[+0.022941, +0.042273]`** |
| **`ZS_8_standalone` (Ours, `1/8` Standalone)** | `CADD.RawScore` (`1/8`) | **`0.784410`** | **`+0.072226`** | `[0.702722, 0.841254]` / **`[+0.043053, +0.098184]`** | **`0.284569`** (`21/22` W) | **`+0.034669`** | **`[0.263051, 0.306672]`** / **`[+0.026326, +0.043989]`** |
| **`ZS_7_within_chrom` (Ours, `1/7` Within-Chrom)** | **No (`100%` CADD-Free)** | **`0.767236`** | **`+0.055051`** | `[0.687931, 0.825374]` / **`[+0.013211, +0.091675]`** | **`0.279802`** (`19/22` W) | **`+0.029902`** | **`[0.258442, 0.301402]`** / **`[+0.020166, +0.041424]`** |
| `CADD.plus.RawScore` | Best Published Zero-Shot | `0.712185` | `0.000000` | `[0.631772, 0.783832]` | `0.249900` | `0.000000` | `[0.229819, 0.269695]` |
| `phyloP-241m.plus.score` | 241-Mammal Cactus MSA | `0.695964` | `-0.016221` | `[0.607790, 0.764679]` | `0.227360` | `-0.022540` | `[0.211790, 0.246139]` |
| `GPN-MSA_LLR.minus.score` | 100-Vertebrate MSA PLM | `0.694475` | `-0.017710` | — | `0.207268` | `-0.042632` | — |
| `evo2_40b_LLR.minus.score` | 40B Autoregressive DNA LM | `0.556537` | `-0.155648` | — | `0.150226` | `-0.099674` | — |
| `Borzoi_L2_L2.plus.all` | RNA-seq/CAGE/DNase/ChIP | `0.435566` | `-0.276619` | — | `0.235739` | `-0.014161` | — |
| `Enformer_L2_L2.plus.all` | 5,313-Track Regulatory | `0.418214` | `-0.293971` | — | `0.245115` | `-0.004785` | — |

### 2. Track B (`p1`) — Strictly Alignment-Free Zero-Shot (`mendelian_traits_matched_9` vs `phyloP-241m = 0.695964`)

| Method | Excluded MSA Features | Mendelian AUPRC | Gain vs `phyloP-241m` (`0.695964`) | Gain vs `evo2_40b_LLR` (`0.556537`) | Paired 95% CI vs `phyloP-241m` |
|---|---|---|---|---|---|
| **`AF_4P` (Ours, `1/4` 4-Pillar Alignment-Free)** | All 5 MSA models + all 20 CADD comparative/composite cols | **`0.793262`** | **`+0.097299`** | **`+0.236725`** | **`[+0.012240, +0.174047]`** |
| **`AF_Closed_4` (Ours, `1/4` Closed Non-MSA Blocks)** | All 5 MSA models + all 20 CADD comparative/composite cols (`0` col selection) | **`0.754022`** | **`+0.058059`** | **`+0.197485`** | `[-0.020843, +0.141096]` (`+0.058059 > +0.02`) |
| **`AF_Closed_3` (Ours, `1/3` Closed Non-MSA Blocks)** | All 5 MSA models + all 20 CADD comparative/composite cols | **`0.753848`** | **`+0.057884`** | **`+0.197311`** | `[-0.031382, +0.146656]` (`+0.057884 > +0.02`) |
| **`AF_HumanOnly` (Ours, 100% Human-Only)** | Excludes all MSA + excludes `Evo2-40B` | **`0.749720`** | **`+0.053757`** | **`+0.193183`** | `[-0.024214, +0.140638]` (marginal `[0.668870, 0.819575]`) |
| **`AF_SeqReg_cadd_free` (Ours, 100% CADD-Free Non-MSA)** | Uses only `Evo2-40B` + `Borzoi` + `Enformer` | **`0.630423`** | `-0.065540` | **`+0.073886`** | `[-0.178460, +0.026926]` |
| `phyloP-241m.plus.score` (Reference MSA Target) | Uses 241-mammal alignment | `0.695964` | `0.000000` | `+0.139427` | — |
| `evo2_40b_LLR.minus.score` (Best Single Alignment-Free) | Uses multi-species unaligned training corpus | `0.556537` | `-0.139427` | `0.000000` | — |

### 3. Track C (`p2` & `p3`) — Supervised By-Chromosome Probing (`chrom != test_chrom`) & `CADD + Borzoi` Fix

| Model / Experiment | Columns | Mendelian AUPRC | Gain vs Published (`0.874660`) | Gain vs Local Baseline | Paired 95% CI vs Baseline |
|---|---|---|---|---|---|
| **`M2_multimodal_165cols` (`p2`, Unmodified LR Pipeline)** | `165` (`CADD` + compact multimodal summaries) | **`0.904124`** | **`+0.029464`** | `+0.026403` | **`[+0.005741, +0.048867]`** |
| **`M1_multimodal_135cols` (`p2`, Unmodified LR Pipeline)** | `135` (`CADD` + compact multimodal summaries) | **`0.898454`** | **`+0.023794`** | `+0.020733` | **`[+0.001217, +0.041013]`** |
| **`CADD+Borzoi` Block-Scaled ($\alpha = 114/7611$, `p3` Fix)** | `7,731` (exact same `CADD + Borzoi` columns) | **`0.885711`** | **`+0.011051`** | `+0.007990` (`+0.159563` vs unscaled) | `[-0.008305, +0.019896]` (marginal `[0.819354, 0.936048]`) |
| **`CADD + Borzoi_L2_L2` (`p3` Pre-Aggregated Fix)** | `120` (`114` `CADD` + `6` `Borzoi_L2_L2`) | **`0.884005`** | **`+0.009345`** | `+0.006284` | `[-0.010470, +0.021052]` (marginal `[0.817919, 0.932002]`) |
| `CADD.LogisticRegression.chrom` (Baseline) | `114` (`CADD.parquet`) | `0.877721` (`0.874660` pub.) | `+0.003061` | `0.000000` | — |
| `CADD + Borzoi` Unscaled (`p3` Dilution Anomaly) | `7,731` (`114` `CADD` + `7,617` `Borzoi`) | `0.726148` (`0.756755` pub.) | `-0.148512` | `-0.151573` | — |
| **`M1_noPopFreq_126cols` (MAF-Shortcut-Free Multimodal)** | `126` (all 9 `Freq*/Rare*/Sngl*` cols removed) | **`0.791714`** | — | **`+0.051438`** (vs `105`-col `CADD`) | **`[+0.018145, +0.084487]`** |
| `CADD_noPopFreq_105cols` (MAF-Shortcut-Free CADD) | `105` (all 9 `Freq*/Rare*/Sngl*` cols removed) | `0.740276` | `-0.134384` | `-0.137446` (vs `114`-col `CADD`) | — |

---

## Not Claimed

- We do not claim a Full Win (`>= 0.30` AUPRC) on the companion target `traitgym-complex-traits-auprc`; our zero-shot transfer (`ZS_7_cadd_free = 0.281541`, `ZS_8_standalone = 0.284569`, `CI_6_multimodal = 0.283768`) satisfies the companion **Partial Win `p1` (`>= 0.269900`, `+0.02` over `CADD.plus.RawScore = 0.249900`)** while closing approximately $69\%$ of the gap from `0.249900` to `0.300000`.
- We do not claim that 100% CADD-free alignment-free scoring (`AF_SeqReg_cadd_free = 0.630423`, using only `Evo2-40B + Borzoi + Enformer`) beats 241-mammal `phyloP-241m` (`0.695964`) without splicing (`SpliceAI`/`MMSplice`) and human polymorphism density features (`AF_Closed_4 = 0.754022`, `AF_4P = 0.793262`, `AF_HumanOnly = 0.749720`).

---

## Credits

- **Benchmark Authors:** Gonzalo Benegas, Gökcen Eraslan & Yun S. Song (`songlab/TraitGym`, UC Berkeley & Genentech).
- **Discovery & Verification:** `@mizopl` (`we*` = `@mizopl` + Gemini-CLSS autonomous research system, `https://github.com/mizopl/we-star`).
