# The Record We Beat: TraitGym Non-Coding Variant Prioritization (`mendelian_traits_matched_9` & `complex_traits_matched_9`)

## 1. Benchmark & Source Reference

- **Primary Target:** `traitgym-mendelian-zero-shot-auprc` (*"TraitGym Mendelian traits: beat CADD zero-shot AUPRC on causal non-coding variants for rare disease"*)
- **Companion Target:** `traitgym-complex-traits-auprc` (*"TraitGym complex traits: close the gap to 0.30 AUPRC on putative causal non-coding variants"*, partial win `p1`)
- **Paper:** Gonzalo Benegas, Gökcen Eraslan, Yun S. Song (2025), *"Benchmarking DNA Sequence Models for Causal Regulatory Variant Prediction in Human Genetics"*, *bioRxiv* `2025.02.11.637758v2` ([DOI: 10.1101/2025.02.11.637758](https://doi.org/10.1101/2025.02.11.637758)).
- **Official Dataset & Code:** Hugging Face [`songlab/TraitGym`](https://huggingface.co/datasets/songlab/TraitGym) and GitHub [`songlab-cal/TraitGym`](https://github.com/songlab-cal/TraitGym).
- **UTC Fetch Time:** `2026-10-26T02:16:00Z`
- **Fetched Dataset Table (`mendelian_traits_matched_9/test.parquet`) SHA-256:** `144db4bf965e3c2b8936cd675448bade96369b6546cfdadb5c7b2bca17389607`
- **Fetched Dataset Table (`complex_traits_matched_9/test.parquet`) SHA-256:** `068940684e1e6f735a25a1a4418fb65390628023a96188af7f1a15dd17de7036`
- **Evaluation Metric:** Exact TraitGym evaluation protocol (`workflow/notebooks/utils.py`): step-function `average_precision_score(label, score)` computed within each chromosome (`19` chromosomes on `mendelian_traits_matched_9`, $N = 3,380$ variants, $338$ positives, $1:9$ positive-to-control ratio; `22` chromosomes on `complex_traits_matched_9`, $N = 11,400$ variants, $1,140$ positives, $1:9$ ratio), weighted by the number of variants per chromosome (`AUPRC_by_chrom_weighted_average`), with $1,000$-iteration chromosome-level block bootstrap standard errors (`seed = 42`).

---

## 2. Published Records vs. Our Certified Results

### Track A — Strictly Zero-Shot (`reads_traitgym_labels = false`, `uses_hand_tuned_weights = false`)

| Dataset | Metric / Baseline | Published Record | Our Reproduced Baseline | **Our `ZS_7_cadd_free` (100% CADD-Free, `1/7`)** | **Our `CI_6_multimodal` (`1/6` 6-Pillar)** | Required Win Threshold |
|---|---|---|---|---|---|---|
| `mendelian_traits_matched_9` ($N=3,380$, $19$ chroms) | `CADD.plus.RawScore` (Best zero-shot) | `0.712185` | `0.712185` (`[0.631772, 0.783832]`) | **`0.789624`** (`+0.077439`, marginal CI **`[0.713717, 0.845178]`**, paired CI **`[+0.046886, +0.107118]`**) | **`0.807396`** (`+0.095211`, marginal CI **`[0.733852, 0.862473]`**, paired CI **`[+0.054896, +0.132770]`**) | `>= 0.732185` (`+0.02`, 95% CI excluding `0.712185`) |
| `complex_traits_matched_9` ($N=11,400$, $22$ chroms) | `CADD.plus.RawScore` (Best zero-shot) | `0.249900` | `0.249900` (`[0.229819, 0.269695]`) | **`0.281541`** (`+0.031641`, marginal CI **`[0.261479, 0.303159]`**, paired CI **`[+0.022941, +0.042273]`**) | **`0.283768`** (`+0.033869`, marginal CI **`[0.262193, 0.307642]`**, paired CI **`[+0.025960, +0.043289]`**) | `>= 0.269900` (`+0.02` transfer) |

*(Note: Adding `CADD.RawScore` as an 8th equal-weight arm (`ZS_8_standalone`, `1/8`) yields **`0.784410`** (`+0.072226`) on Mendelian and **`0.284569`** (`+0.034669`, winning `21/22` chromosomes) on Complex traits.)*

### Track B — Alignment-Free Zero-Shot (`p1`, Zero Multiple-Species Alignments)

| Dataset | Reference MSA Baseline | Published Record | **Our `AF_Closed_4` (4 Closed Non-MSA Blocks, `1/4`)** | **Our `AF_HumanOnly` (100% Human-Only)** | **Our `AF_4P` (4-Pillar Alignment-Free)** | Required `p1` Threshold |
|---|---|---|---|---|---|---|
| `mendelian_traits_matched_9` ($N=3,380$, $19$ chroms) | `phyloP-241m.plus.score` (241-mammal cactus MSA) | `0.695964` | **`0.754022`** (`+0.058059` vs `phyloP-241m`, `+0.197485` vs `evo2_40b_LLR = 0.556537`) | **`0.749720`** (`+0.053757` vs `phyloP-241m`, marginal CI `[0.668870, 0.819575]`, paired CI `[-0.024214, +0.140638]`) | **`0.793262`** (`+0.097299` vs `phyloP-241m`, paired CI `[+0.012240, +0.174047]`) | `>= 0.715964` (`+0.02` over `phyloP-241m`) |

### Track C — Supervised By-Chromosome Probing (`p2`) & `CADD + Borzoi` Dilution Fix (`p3`)

| Track | Published Record | Our Reproduced Baseline | **Our Certified Result** | Required Threshold |
|---|---|---|---|---|
| `p2` Supervised By-Chrom (`chrom != test_chrom`) | `CADD.LogisticRegression.chrom = 0.874660` | `0.877721` (114-col `CADD.parquet`) | **`M1_multimodal_135cols = 0.898454`** (`+0.023794` vs published, paired CI `[+0.001217, +0.041013]`); **`M2_multimodal_165cols = 0.904124`** (`+0.029464` vs published, paired CI `[+0.005741, +0.048867]`) | `>= 0.894660` (`+0.02` over `0.874660`) |
| `p3` `CADD + Borzoi` (`7,731` cols) Dilution Fix | `CADD+Borzoi.LogisticRegression.chrom = 0.756755` (`-0.117905` drop) | `0.726148` (`Borzoi_L2` absorbs `64.2319%` of $\|\mathbf{w}\|_2^2$) | **Block-scaled (`114/7611`) `7,731`-col `CADD+Borzoi = 0.885711`** (`Borzoi_L2` norm share `11.1364%`); **`CADD + Borzoi_L2_L2` (`120` cols) = `0.884005`** | Recover & beat `0.874660` |
| **Methodology Audit (MAF-Matching Shortcut Removed)** | — | `CADD_noPopFreq_105cols = 0.740276` (`-0.137446` drop when 9 `Freq*/Rare*/Sngl*` cols removed) | **`M1_noPopFreq_126cols = 0.791714`** (`+0.051438` over `105`-col `CADD`, paired CI `[+0.018145, +0.084487]`) | Genuine biological generalization without MAF leakage |
