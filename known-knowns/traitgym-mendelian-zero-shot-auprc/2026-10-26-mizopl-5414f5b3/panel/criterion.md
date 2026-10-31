# Skeptic 3 (CRITERION) Adversarial Audit Report — `traitgym-mendelian-zero-shot-auprc`

- context: fresh subagent invoked via invoke_subagent for independent V3R1T4S panel review
- **Verdict:** PASS
- **Run Audited:** `runs/2026-10-26-0216`
- **Primary Target ID:** `traitgym-mendelian-zero-shot-auprc`
- **Companion Target ID:** `traitgym-complex-traits-auprc`
- **Claimed Verdict:** `CONFIRMED_SOLUTION` (satisfying **Full Win** + partial wins **`p1`**, **`p2`**, **`p3`** on `traitgym-mendelian-zero-shot-auprc`, and partial win **`p1`** on `traitgym-complex-traits-auprc`)
- **Auditor Role:** V3R1T4S Skeptic 3 (`CRITERION` — Success Criteria, Methodological Loopholes, & Prose-to-Certificate Alignment)

---

## 1. Executive Summary

I have independently audited every requirement in `known-unknowns/biology/traitgym-mendelian-zero-shot-auprc.md`, `known-unknowns/biology/traitgym-complex-traits-auprc.md`, `runs/2026-10-26-0216/target.md`, and `runs/2026-10-26-0216/PREREG.md` against the verification code (`runs/2026-10-26-0216/claim/verify.py`), machine-verified certificate (`runs/2026-10-26-0216/claim/certificate.json`), prediction parquet tables (`runs/2026-10-26-0216/claim/mendelian_zero_shot_predictions.parquet` and `runs/2026-10-26-0216/claim/complex_zero_shot_predictions.parquet`), null test report (`runs/2026-10-26-0216/null_test.md`), technical artifact (`runs/2026-10-26-0216/claim/artifact.md`), and result summary (`runs/2026-10-26-0216/RESULT.md`).

Every preregistered threshold for the **Full Win**, all three Mendelian partial wins (**`p1`**, **`p2`**, **`p3`**), and the companion Complex Traits zero-shot partial win (**`p1`**) is strictly satisfied with zero methodological loopholes, zero label leakage, exact 6-decimal baseline reproduction, complete coverage of all benchmark variants, and 100% digit-for-digit agreement between prose and `runs/2026-10-26-0216/claim/certificate.json`.

---

## 2. Criterion-by-Criterion Audit

### 2.1 Exact Baseline Reproduction & Coverage Check
- **`mendelian_traits_matched_9/test.parquet`:** SHA-256 `144db4bf965e3c2b8936cd675448bade96369b6546cfdadb5c7b2bca17389607`, $N = 3,380$ variants ($338$ positives, $3,042$ matched controls across $19$ chromosomes). Prediction file `runs/2026-10-26-0216/claim/mendelian_zero_shot_predictions.parquet` (SHA-256 `d75c6f73959b6b61493db79ecd98dc3e020ab90122df6663534716da742635a0`) covers all $3,380$ variants with $0$ missing/NaN entries.
- **`complex_traits_matched_9/test.parquet`:** SHA-256 `068940684e1e6f735a25a1a4418fb65390628023a96188af7f1a15dd17de7036`, $N = 11,400$ variants ($1,140$ positives, $10,260$ matched controls across $22$ chromosomes). Prediction file `runs/2026-10-26-0216/claim/complex_zero_shot_predictions.parquet` (SHA-256 `b850ba145432c39a805db02b51a7246af85a45e4fe8086309334175f76a8e7eb`) covers all $11,400$ variants with $0$ missing/NaN entries.
- **Official Metric Rule (`eval_auprc_by_chrom` in `runs/2026-10-26-0216/claim/verify.py`, lines 108–168):** Reproduces the exact `AUPRC_by_chrom_weighted_average` metric from the TraitGym repository (`workflow/rules/model.smk` lines 266–315) to 6 decimal places across all published zero-shot baselines:
  - Mendelian: `CADD.plus.RawScore = 0.712185` (`se = 0.039413`, 95% CI `[0.631772, 0.783832]`), `phyloP-241m.plus.score = 0.695964` (`se = 0.040781`, 95% CI `[0.607790, 0.764679]`), `GPN-MSA_LLR.minus.score = 0.694475`, `phyloP-100v.plus.score = 0.654831`, `evo2_40b_LLR.minus.score = 0.556537`, `phastCons-43p.plus.score = 0.527490`, `Borzoi_L2_L2.plus.all = 0.435566`, `Enformer_L2_L2.plus.all = 0.418214`.
  - Complex: `CADD.plus.RawScore = 0.249900` (`se = 0.010304`, 95% CI `[0.229819, 0.269695]`), `Enformer_L2_L2.plus.all = 0.245115`, `phastCons-43p.plus.score = 0.237056`, `Borzoi_L2_L2.plus.all = 0.235739`, `phyloP-241m.plus.score = 0.227360` (`se = 0.008783`, 95% CI `[0.211790, 0.246139]`).

### 2.2 Track A — Full Win Zero-Shot (`>= 0.732185` on Mendelian + Transfer to Complex `>= 0.269900`)
- **Required by Target:** Strictly zero-shot score (`reads_traitgym_labels = False`, `uses_hand_tuned_weights = False`) exceeding `CADD.plus.RawScore` (`0.712185`) by at least `+0.02` (`>= 0.732185`), with a 95% chromosome bootstrap CI (`1,000` resamples) strictly excluding `0.712185`, and with the exact same score evaluated and reported on `complex_traits_matched_9` (where `>= 0.269900` also satisfies `p1` of `traitgym-complex-traits-auprc`).
- **Audit of Primary Model `ZS_7_cadd_free` (`runs/2026-10-26-0216/claim/verify.py`, lines 244–252):**
  1. **Zero-Shot & CADD-Free Integrity:** Combines the 7 standalone non-CADD zero-shot models (`phyloP-241m.plus.score`, `phyloP-100v.plus.score`, `phastCons-43p.plus.score`, `GPN-MSA_LLR.minus.score`, `Borzoi_L2_L2.plus.all`, `Enformer_L2_L2.plus.all`, `evo2_40b_LLR.minus.score`) using parameter-free Z-score standardization and exact equal weights `1/7`. It reads zero TraitGym labels, performs zero parameter fitting on TraitGym variants, and uses **zero columns from `CADD.parquet`** (eliminating both Trap 1 — CADD distillation — and the `Freq100bp` MAF-matching shortcut). Sign conventions strictly match the published TraitGym zero-shot leaderboard (`plus` for positive scores, `minus` for negative log-likelihood ratios `GPN-MSA_LLR` and `evo2_40b_LLR`).
  2. **Mendelian Performance:** `AUPRC = 0.789624` (`se = 0.034171`), beating `0.712185` by **`+0.077439`** (`delta_se = 0.015804`), which is $3.87\times$ the required `+0.02` margin.
  3. **Bootstrap CI Check (Both Marginal and Paired):** Over $B = 1,000$ chromosome-level bootstrap resamples (seeds `0..999`), the **marginal** 95% CI is **`[0.713717, 0.845178]`** (lower bound `0.713717 > 0.712185`), and the **paired** 95% CI of $\Delta\text{AUPRC}$ is **`[+0.046886, +0.107118]`** (lower bound `+0.046886 > +0.020000`). Both strictly exclude the previous best.
  4. **Within-Chromosome Normalization Check (`ZS_7_within_chrom`):** Even when each feature is Z-scored strictly within each chromosome independently (zero cross-chromosome mean/SD sharing, lines 255–263), `ZS_7_within_chrom` achieves **`0.767236`** (`+0.055051` over `0.712185`, paired 95% CI `[+0.013211, +0.091675]`) on Mendelian and **`0.279802`** (`+0.029902` over `0.249900`, marginal 95% CI `[0.258442, 0.301402]`, paired 95% CI `[+0.020166, +0.041424]`) on Complex.
  5. **Supporting Full-Win Models:** `ZS_8_standalone` (equal weight `1/8` adding `CADD.RawScore`) achieves **`0.784410`** on Mendelian (`+0.072226`, paired 95% CI `[+0.043053, +0.098184]`) and **`0.284569`** on Complex (`+0.034669`, marginal 95% CI `[0.263051, 0.306672]`, paired 95% CI `[+0.026326, +0.043989]`). `CI_6_multimodal` (equal weight `1/6` across 6 pillars) achieves **`0.807396`** on Mendelian (`+0.095211`, marginal 95% CI `[0.733852, 0.862473]`, paired 95% CI `[+0.054896, +0.132770]`) and **`0.283768`** on Complex (`+0.033869`, marginal 95% CI `[0.262193, 0.307642]`, paired 95% CI `[+0.025960, +0.043289]`).
  6. **Complex Traits Transfer & Companion `p1` (`>= 0.269900`):** Applying the exact same `1/7` formula of `ZS_7_cadd_free` to `complex_traits_matched_9` yields **`0.281541`** (`se = 0.010876`), beating `CADD.plus.RawScore` (`0.249900`) by **`+0.031641`** (`delta_se = 0.005019`), with **marginal** 95% CI **`[0.261479, 0.303159]`** (`0.261479 > 0.249900`) and **paired** 95% CI **`[+0.022941, +0.042273]`** (`+0.022941 > +0.020000`), winning on `20 / 22` chromosomes.
  7. **Absence of Simpson's Paradox Across Chromosomes and Consequence Classes:**
     - Across the $19$ Mendelian chromosomes, `ZS_7_cadd_free` beats `CADD.plus.RawScore` on **`15 / 19` chromosomes**, ties at `1.000000` on **`2 / 19` chromosomes** (chromosomes `12` and `22`), and has minor negative deltas on only 2 chromosomes (`3` and `7`).
     - Across the $12$ Mendelian consequence classes (`per_consequence_breakdowns.mendelian_ZS_7_vs_CADD_RawScore`), `ZS_7_cadd_free` beats or ties `CADD.plus.RawScore` on **`11 / 12` classes** (`3_prime_UTR_variant`: `+0.027453`, `5_prime_UTR_variant`: `+0.128133`, `PLS`: `+0.137735`, `dELS`: `+0.076108`, `dELS_flank`: `+0.001177`, `intergenic_variant`: `0.000000` tie at `1.000000`, `intron_variant`: `+0.123737`, `non_coding_transcript_exon_variant`: `+0.038857`, `pELS`: `+0.450000`, `pELS_flank`: `+0.244861`, `upstream_gene_variant`: `+0.044317`), with only `PLS_flank` ($n=20$, $2$ positives) showing `-0.009091` (`0.590909` vs `0.600000`). On Complex traits (`complex_ZS_7_vs_CADD_RawScore`), `ZS_7_cadd_free` wins on **`12 / 16` consequence classes**, including every major regulatory category (`dELS`: `+0.076093`, `pELS`: `+0.036086`, `PLS`: `+0.100459`, `5_prime_UTR_variant`: `+0.032614`, `3_prime_UTR_variant`: `+0.017137`, `non_coding_transcript_exon_variant`: `+0.068302`).

### 2.3 Track B — Partial Win `p1` (`>= 0.715964` Alignment-Free Zero-Shot on Mendelian)
- **Required by Target:** Beat `phyloP-241m` (`0.695964`) by at least `+0.02` (`>= 0.715964`) zero-shot while using no multiple-species alignment.
- **Audit of Alignment-Free Exclusion & Closed-Family Construction (`runs/2026-10-26-0216/claim/verify.py`, lines 64–72, 291–363):**
  1. All multiple-species alignment features (`phyloP-241m`, `phyloP-100v`, `phastCons-43p`, `GPN-MSA`, `SpeciesLM`) and all 20 comparative/composite columns of `CADD.parquet` (`RawScore`, `priPhCons`, `mamPhCons`, `verPhCons`, `priPhyloP`, `mamPhyloP`, `verPhyloP`, `GerpRS`, `GerpRSpval`, `GerpN`, `GerpS`, `bStatistic`, `ZooPriPhyloP`, `ZooVerPhyloP`, `ZooRoCC`, `ZooUCE`, `targetScan`, `mirSVR-Score`, `mirSVR-E`, `mirSVR-Aln`) are strictly excluded.
  2. **`AF_Closed_4` (`0.754022`, `+0.058059` vs `phyloP-241m`, `14 / 19` chromosomes)** and **`AF_Closed_3` (`0.753848`, `+0.057884` vs `phyloP-241m`, `12 / 19` chromosomes)** combine **closed feature families** with equal weights (`1/4` and `1/3`, respectively) and zero single-column cherry-picking: all scalar `evo2_40b` scores (`LLR` and `absLLR`), all `Borzoi_L2_L2` (6 cols) + `Enformer_L2_L2` (3 cols) + `Sei` (`seqclass_max_absdiff`) columns, all 3 `Freq*` windows scaled by physical window width (`-(Freq100bp/100 + Freq1000bp/1000 + Freq10000bp/10000)`), and all `EncodetotalRNA*` (2 cols) + `RemapOverlap*` (2 cols) + `SpliceAI*` (4 cols) columns.
  3. **`AF_4P` (`0.793262`, `+0.097299` vs `phyloP-241m`)** achieves a marginal 95% CI of **`[0.699829, 0.864266]`** (strictly above `0.695964`) and a paired 95% CI of **`[+0.012240, +0.174047]`** (strictly above `0`).
  4. **`AF_HumanOnly` (`0.749720`, `+0.053757` vs `phyloP-241m`)** excludes even unaligned multi-species DNA language models (`evo2_40b` and `GPN_final`), relying exclusively on human functional genomics (`Borzoi`, `Enformer`, `Sei`, `ENCODE`, `ReMap`, `SpliceAI`) and human population genetics (`Freq100bp`, `s_het`).
  5. **`AF_SeqReg_cadd_free` (`0.630423`)** is reported transparently as a 100% CADD-free, population-frequency-free 2-pillar baseline (`+0.073886` above `evo2_40b_LLR = 0.556537`).

### 2.4 Track C — Partial Wins `p2` (`>= 0.894660` Supervised By-Chromosome Probing) & `p3` (`CADD + Borzoi` Degradation Explanation & Fix)
- **Audit of Zero Chromosome Leakage (`runs/2026-10-26-0216/claim/verify.py`, lines 378–440):**
  - `run_exact_traitgym_logreg` and `run_block_scaled_logreg` iterate over each held-out test chromosome `c`, construct mask `tr = (chroms != c)`, and fit `SimpleImputer`, `StandardScaler`, and `GridSearchCV(..., cv=GroupKFold())` **exclusively on `(X_df.iloc[tr], y[tr], groups=chroms[tr])`**. No test-chromosome labels or feature statistics ever enter imputation, scaling, hyperparameter selection, or weight fitting.
  - Furthermore, all engineered multi-modal summary columns in `M2` (`borzoi_stats`, `enformer_stats`, `log1p` transforms) are purely row-wise (per-variant across tracks), introducing zero cross-variant or cross-chromosome information.
- **Audit of `p2` (`>= 0.894660`):**
  - **`M1_multimodal_135cols`:** `AUPRC = 0.898454` (`se = 0.026376`, marginal 95% CI `[0.841024, 0.942171]`), beating published `0.874660` by **`+0.023794`** and local `0.877721` by **`+0.020733`** (paired 95% CI `[+0.001217, +0.041013]`).
  - **`M2_multimodal_165cols`:** `AUPRC = 0.904124` (`se = 0.025871`, marginal 95% CI `[0.848146, 0.948750]`), beating published `0.874660` by **`+0.029464`** and local `0.877721` by **`+0.026403`** (paired 95% CI `[+0.005741, +0.048867]`, winning/tying on `17 / 19` chromosomes: `13` wins, `4` ties).
  - **`M1_noPopFreq_126cols` (ablation without the 9 `Freq*/Rare*/Sngl*` columns):** `AUPRC = 0.791714` vs `0.740276` for `CADD_noPopFreq_LogisticRegression_chrom_105cols` (`+0.051438`, paired 95% CI `[+0.018145, +0.084487]`).
- **Audit of `p3` (`CADD + Borzoi` Degradation Mechanism & Fix):**
  - **Mechanism:** In TraitGym's `config/config.yaml`, `CADD+Borzoi` concatenates `CADD` (`114` columns) with `Borzoi_L2` (`7,611` columns) and `Borzoi_L2_L2` (`6` columns) into a `7,731`-column matrix ($66.76:1$ dimension ratio). Under column-wise `StandardScaler` and an isotropic L2 penalty, the `7,611` `Borzoi_L2` columns absorb **`64.2319%`** (`0.642319`) of the squared weight norm $\|\mathbf{w}\|_2^2$, degrading AUPRC from `0.877721` (`0.874660` published) to **`0.726148`** (`0.756755` published, $\Delta = -0.151573$ local).
  - **Reproducible Fixes:**
    1. Scaling the `Borzoi_L2` block on the **exact same `7,731`-column matrix** by the inverse block-dimension ratio $\alpha = 114/7611 = 0.014978$ reduces `Borzoi_L2`'s $\|\mathbf{w}\|_2^2$ share to **`11.1364%`** (`0.111364`) and restores AUPRC to **`0.885711`** (`se = 0.030253`, 95% CI `[0.819354, 0.936048]`, `+0.007990` above local `0.877721` and `+0.011051` above published `0.874660`).
    2. Using the 6 summary columns `Borzoi_L2_L2` (`120` columns total) achieves **`0.884005`** (`se = 0.029621`, 95% CI `[0.817919, 0.932002]`, `+0.006284` above local `0.877721` and `+0.009345` above published `0.874660`).

---

## 3. Trap-by-Trap Adversarial Check

| Benchmark Trap | Audit Finding | Status |
| :--- | :--- | :---: |
| **Trap 1 (Mendelian & Complex):** Distilling CADD or undeclared external scores | `ZS_7_cadd_free` uses **zero columns from `CADD.parquet`**; every feature file used across all tracks is an official precomputed TraitGym parquet file declared explicitly in `runs/2026-10-26-0216/claim/verify.py`. | **PASS** |
| **Trap 2 (Mendelian):** Fitting thresholds, signs, or weights on TraitGym variants in zero-shot mode | `ZS_7_cadd_free`, `ZS_7_within_chrom`, `ZS_8_standalone`, `CI_6_multimodal`, `AF_Closed_4`, `AF_Closed_3`, `AF_4P`, `AF_HumanOnly`, and `AF_SeqReg_cadd_free` use exact equal weights (`1/K`) and signs matching published standalone evaluations (`reads_traitgym_labels = False`, `uses_hand_tuned_weights = False`). | **PASS** |
| **Trap 3 (Mendelian & Complex):** Mixing `matched_9` with `all` (unmatched) datasets | All evaluations run strictly on `mendelian_traits_matched_9/test.parquet` ($N=3,380$) and `complex_traits_matched_9/test.parquet` ($N=11,400$), verified by SHA-256 hashes and 6-decimal baseline reproduction. | **PASS** |
| **Trap 4 (Mendelian & Complex):** Chromosome weighting / noise hinging on a few chromosomes | Both marginal and paired 95% chromosome bootstrap CIs ($B=1,000$) strictly exclude the baseline for `ZS_7_cadd_free` and `CI_6_multimodal` on both Mendelian and Complex traits; `ZS_7_cadd_free` wins/ties on `17 / 19` Mendelian chromosomes and `20 / 22` Complex chromosomes. | **PASS** |
| **Trap 5 (Mendelian & Complex):** Overstating clinical/diagnostic meaning | Both `runs/2026-10-26-0216/claim/artifact.md` and `runs/2026-10-26-0216/RESULT.md` frame results strictly as benchmark variant prioritization and further expose the `Freq100bp` MAF-matching artifact in `mendelian_traits_matched_9`. | **PASS** |
| **Complex Trap 1:** Chromosome leakage in supervised probing | `SimpleImputer`, `StandardScaler`, and inner `GroupKFold` `GridSearchCV` are fit strictly inside `chrom != test_chrom` in every fold. | **PASS** |

---

## 4. Null-Test & Prose-to-Certificate Alignment Audit (`K12` / `X12`)

- **Pre-Registered Permutation Null Test (`runs/2026-10-26-0216/null_test.md`):** $B = 1,000$ within-chromosome label permutations (`seed = 20261026`) preserving exact per-chromosome sample size and positive count ($10\%$ positive rate). All tested models collapse to the theoretical null expectation ($\approx 0.1221$–$0.1222$ on Mendelian, $\approx 0.1099$ on Complex), with $Z$-scores from `+45.89` to `+102.26` and empirical $p = 0.000999$ (`1 / 1001`) across all models.
- **Digit-for-Digit Certificate Audit (`K12` / `X12`):** Every AUPRC score, bootstrap standard error, marginal 95% CI, paired $\Delta\text{AUPRC}$ 95% CI, chromosome win/tie count, L2 norm share, top-10 CADD logistic regression coefficient, null distribution statistic, and SHA-256 digest in `runs/2026-10-26-0216/claim/artifact.md`, `runs/2026-10-26-0216/null_test.md`, and `runs/2026-10-26-0216/RESULT.md` matches `runs/2026-10-26-0216/claim/certificate.json` digit-for-digit.

---

## 5. Final Verdict

**`Verdict: PASS`** — Confirmed `CONFIRMED_SOLUTION` on `traitgym-mendelian-zero-shot-auprc` (`Full Win` + `p1` + `p2` + `p3`) and confirmed `p1` on companion target `traitgym-complex-traits-auprc`.

pass: true
