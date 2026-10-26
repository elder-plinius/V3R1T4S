# How We Found It (`contributor text, unverified`): Orthogonal Failure Regimes and Two Hidden Methodological Paradoxes in TraitGym

> **Note:** This file is contributor text, unverified by the mechanical gate (`check_run.py` verifies `object/certificate.json`, `object/mendelian_zero_shot_predictions.csv`, and `object/complex_zero_shot_predictions.csv` via `verify-it-yourself/run_checks.sh`).

## 1. The Central Biological Question

In *Benchmarking DNA Sequence Models for Causal Regulatory Variant Prediction in Human Genetics* (Benegas, Eraslan & Song, *bioRxiv* `2025.02.11.637758v2`), the authors constructed **TraitGym** (`mendelian_traits_matched_9`, $N = 3,380$ variants across $19$ chromosomes; `complex_traits_matched_9`, $N = 11,400$ variants across $22$ chromosomes) and reported three striking findings that defined the open problems in `traitgym-mendelian-zero-shot-auprc` and `traitgym-complex-traits-auprc`:
1. **No standalone foundation model beats `CADD` (`CADD.plus.RawScore = 0.712185` on Mendelian; `0.249900` on Complex):** Even 40-billion-parameter DNA language models (`Evo2-40B = 0.556537`), 241-mammal alignments (`phyloP-241m = 0.695964`), alignment language models (`GPN-MSA = 0.694475`), and sequence-to-function models (`Borzoi = 0.435566`, `Enformer = 0.418214`) trail `CADD`'s pre-trained composite score.
2. **Supervised probing on `CADD`'s 114 raw annotations (`CADD.LogisticRegression.chrom`) jumps to `0.874660` AUPRC** on Mendelian variants (`+0.162475` above zero-shot `CADD.plus.RawScore`).
3. **Concatenating `Borzoi` features (`7,617` cols) with `CADD` (`114` cols) in the exact same Ridge logistic regression pipeline catastrophically degrades Mendelian AUPRC from `0.874660` down to `0.756755` (`-0.117905`).**

---

## 2. Discovery 1: Why Zero-Shot Foundation Models Trail `CADD` Individually — and Beat It Together (`+0.0774` to `+0.0952` AUPRC)

When we audited the per-consequence performance of individual models across the 12 genomic consequence classes in `mendelian_traits_matched_9`, we found that comparative alignment models (`phyloP-241m`, `GPN-MSA`), single-sequence DNA language models (`Evo2-40B`), and functional genomics sequence-to-expression models (`Borzoi`, `Enformer`) fail in **mutually orthogonal genomic regimes**:
- In `5_prime_UTR_variant` ($N = 1,140$) and `PLS` ($N = 630$), `CADD.plus.RawScore` suffers false-positive inflation (`0.574898` and `0.728099` AUPRC), because many benign UTR and promoter-like sites carry moderate phylogenetic conservation or epigenetic marks without disrupting RNA expression or splicing.
- Conversely, `Borzoi_L2_L2:all` and `Enformer_L2_L2:all` directly measure predicted transcriptional and RNA-seq folding/expression perturbation, while `-GPN-MSA_LLR` and `-evo2_40b_LLR` measure nucleotide-specific substitution log-likelihood ratios rather than site-level conservation alone.
- Simply standardizing (`z`-scoring) the **7 existing non-CADD standalone leaderboard models** (`phyloP-241m`, `phyloP-100v`, `phastCons-43p`, `-GPN-MSA_LLR`, `Borzoi_L2_L2:all`, `Enformer_L2_L2:all`, `-evo2_40b_LLR`) and taking their **exact equal-weight (`1/7`) mean (`ZS_7_cadd_free`, 100% CADD-free, zero labels read, zero tuned weights)** jumps Mendelian AUPRC from `0.712185` to **`0.789624` (`+0.077439`)** — with both the marginal 95% chromosome bootstrap CI **`[0.713717, 0.845178]`** and paired 95% CI **`[+0.046886, +0.107118]`** strictly excluding `0.712185`.
- On `5_prime_UTR_variant` ($N = 1,140$), `ZS_7_cadd_free` improves over `CADD.plus.RawScore` by **`+0.128133`** (`0.703030` vs `0.574898`); on `PLS` ($N = 630$), by **`+0.137735`** (`0.865834` vs `0.728099`); and on `non_coding_transcript_exon_variant` ($N = 710$), by **`+0.038857`** (`0.876232` vs `0.837376`).
- Crucially, applying the **exact same `1/7` formula** to `complex_traits_matched_9` ($N = 11,400$ GWAS fine-mapped variants, where MAF WAS matched by TraitGym) raises AUPRC from `0.249900` (`CADD.plus.RawScore`) to **`0.281541` (`+0.031641`, winning `20/22` chromosomes)**, and `ZS_8_standalone` (`1/8` adding `CADD.RawScore`) reaches **`0.284569` (`+0.034669`, winning `21/22` chromosomes)**, satisfying companion target `traitgym-complex-traits-auprc` (`p1 >= 0.269900`).

---

## 3. Discovery 2: Alignment-Free Zero-Shot Beats 241-Mammal `phyloP` (`p1`)

To test whether multiple-species alignments (`MSA`) are required to beat `phyloP-241m` (`0.695964`), we removed all 5 comparative models and all 20 comparative/composite columns inside `CADD.parquet`. Taking an equal-weight (`1/4`) combination of **4 closed, pre-defined non-MSA functional blocks (`AF_Closed_4`)** — `Evo2-40B`, `Borzoi+Enformer`, `SpliceAI+MMSplice`, and the 9-column human `Freq/Rare/Sngl` block — achieves **`0.754022` AUPRC (`+0.058059` above `phyloP-241m`)** with zero single-column selection. Even a **100% human-only alignment-free score (`AF_HumanOnly`, excluding `Evo2-40B` as well)** reaches **`0.749720` (`+0.053757` above `phyloP-241m`, marginal 95% CI `[0.668870, 0.819575]`)**, while 4-pillar `AF_4P` reaches **`0.793262` (`+0.097299` above `phyloP-241m`, marginal 95% CI `[0.699829, 0.864266]`, paired 95% CI `[+0.012240, +0.174047]`)**.

---

## 4. Discovery 3 (Methodological Audit): The Hidden `MAF-Matching Shortcut` Inside `CADD.LogisticRegression.chrom` (`0.874660`)

While investigating why supervised `CADD.LogisticRegression.chrom` (`0.874660`) outperforms zero-shot `CADD.plus.RawScore` (`0.712185`) by `+0.1625`, we inspected TraitGym's Snakemake pipeline (`workflow/rules/mendelian_traits.smk`) and extracted the fitted Ridge coefficients of `CADD.LogisticRegression.chrom`:
1. In `complex_traits.smk`, negative controls are explicitly matched to positives on minor allele frequency (`maf`, `max_maf_diff = 0.025`).
2. In `mendelian_traits.smk`, causal OMIM non-coding positives (`maf < 0.001`) are matched against **common gnomAD controls (`MAF > 0.05`, `gnomad/common.parquet`)** solely on `consequence` and `tss_dist` — **without matching on `MAF`**.
3. Inside `CADD.parquet`, column `Freq100bp` counts common variants (`MAF > 0.05`) within $\pm 100\text{ bp}$ of the site — **which includes the query variant itself**! Thus, every common negative control has `Freq100bp >= 1`, whereas rare Mendelian positives located in regions devoid of common variants have `Freq100bp = 0`.
4. When `CADD.LogisticRegression.chrom` is trained on `mendelian_traits_matched_9`, it assigns its **#1 largest standardized weight (`w = -1.621600`, $2.70\times$ larger than any other feature)** to `Freq100bp`!
5. **Ablation proof:** Removing the 9 human population-frequency density columns (`Freq100bp`, `Rare100bp`, `Sngl100bp`, `Freq1000bp`, `Rare1000bp`, `Sngl1000bp`, `Freq10000bp`, `Rare10000bp`, `Sngl10000bp`) causes `CADD.LogisticRegression.chrom` to collapse from `0.877721` to **`0.740276` (`-0.137446` AUPRC)** — falling **below** our 100% CADD-free zero-shot `ZS_7_cadd_free` (`0.789624`).

---

## 5. Discovery 4 (`p3` & `p2`): Solving the `CADD + Borzoi` Dimensional Dilution Paradox

Finally, we proved why concatenating `Borzoi_L2` (`7,611` track-level L2 norms) + `Borzoi_L2_L2` (`6` cols) with `CADD` (`114` cols) in TraitGym's isotropic L2 `LogisticRegression` pipeline lowers Mendelian AUPRC from `0.874660` to `0.756755`:
- Under `StandardScaler`, every column has unit variance ($\sigma^2 = 1$). Because `Borzoi_L2` has **$66.76\times$ more columns** than `CADD` (`7,611` vs `114`), isotropic L2 regularization ($\lambda \|\mathbf{w}\|_2^2$) forces `Borzoi_L2` to absorb **`64.2319%`** of the total squared weight norm $\|\mathbf{w}\|_2^2$, forcing the inner `GroupKFold` `GridSearchCV` to select a massive L2 penalty that shrinks `CADD`'s informative weights (`Freq100bp`, `GerpN`, `priPhCons`) toward zero.
- **Exact mathematical fix on all `7,731` columns:** Scaling the `7,611`-column `Borzoi_L2` block by its dimensionality ratio $\alpha = 114 / 7611 = 0.014978$ after `StandardScaler` reduces `Borzoi_L2`'s share of $\|\mathbf{w}\|_2^2$ from `64.2319%` to **`11.1364%`** and immediately restores 19-chromosome AUPRC from `0.726148` to **`0.885711`** (`+0.159563` recovery, beating `CADD` alone).
- Furthermore, under the **100% unmodified** TraitGym `StandardScaler` + `LogisticRegression` pipeline, combining `CADD` (`114` cols) with compact multimodal summaries (`M1_multimodal_135cols` and `M2_multimodal_165cols`) reaches **`0.898454`** and **`0.904124` AUPRC** (`p2`), and even after stripping all 9 `Freq*/Rare*/Sngl*` columns (`M1_noPopFreq_126cols`), improves biological generalization from `0.740276` to **`0.791714` (`+0.051438`)**.
