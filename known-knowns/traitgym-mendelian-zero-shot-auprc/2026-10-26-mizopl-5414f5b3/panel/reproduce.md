# V3R1T4S Skeptic 1 (REPRODUCE) Audit Report

- context: fresh subagent invoked via invoke_subagent for independent V3R1T4S panel review
- **Verdict:** PASS
- **Target ID:** `traitgym-mendelian-zero-shot-auprc`
- **Companion Target ID:** `traitgym-complex-traits-auprc`
- **Run Directory:** `runs/2026-10-26-0216`
- **Verification Script Audited:** `runs/2026-10-26-0216/claim/verify.py`
- **Certificate Audited:** `runs/2026-10-26-0216/claim/certificate.json`

---

## 1. Cryptographic Integrity & SHA-256 Verification

Independently computed SHA-256 hashes of all raw benchmark variant files and saved zero-shot prediction artifacts match `runs/2026-10-26-0216/claim/certificate.json` byte-for-byte:

| File Path | Computed SHA-256 | Certificate Match |
| :--- | :--- | :---: |
| `runs/2026-10-26-0216/data/mendelian_traits_matched_9/test.parquet` | `144db4bf965e3c2b8936cd675448bade96369b6546cfdadb5c7b2bca17389607` | **PASS** |
| `runs/2026-10-26-0216/data/complex_traits_matched_9/test.parquet` | `068940684e1e6f735a25a1a4418fb65390628023a96188af7f1a15dd17de7036` | **PASS** |
| `runs/2026-10-26-0216/claim/mendelian_zero_shot_predictions.parquet` | `d75c6f73959b6b61493db79ecd98dc3e020ab90122df6663534716da742635a0` | **PASS** |
| `runs/2026-10-26-0216/claim/complex_zero_shot_predictions.parquet` | `b850ba145432c39a805db02b51a7246af85a45e4fe8086309334175f76a8e7eb` | **PASS** |

Furthermore, recomputing all 9 zero-shot score vectors from the raw feature parquets in `runs/2026-10-26-0216/data/` and comparing them against the saved columns in `runs/2026-10-26-0216/claim/mendelian_zero_shot_predictions.parquet` ($N = 3,380$) and `runs/2026-10-26-0216/claim/complex_zero_shot_predictions.parquet` ($N = 11,400$) yielded `max_abs_diff = 0.0` across every variant and every score column.

---

## 2. Zero-Shot Label-Isolation & Equal-Weight Code Audit

Static inspection and runtime verification of `load_features_only` (lines 191–229) and `compute_zero_shot_scores` (lines 232–375) in `runs/2026-10-26-0216/claim/verify.py` confirm:

1. **Zero Label Access (`reads_traitgym_labels = False`):** `load_features_only` reads exclusively the precomputed feature parquets under `runs/2026-10-26-0216/data/<dataset>/features/` and does not load `test.parquet` or any `label` column. Runtime assertion confirmed `"label" not in v.columns` for every feature DataFrame passed into `compute_zero_shot_scores(F, chroms)`.
2. **Zero Hand-Tuned Weights (`uses_hand_tuned_weights = False`):** Every composite zero-shot score in `compute_zero_shot_scores` combines standardized model/block outputs using exact uniform weights $1/K$:
   - `ZS_7_cadd_free` and `ZS_7_within_chrom`: exact $1/7$ average of 7 standalone leaderboard models (`phyloP-241m`, `phyloP-100v`, `phastCons-43p`, `-GPN-MSA_LLR`, `Borzoi_L2_L2.all`, `Enformer_L2_L2.all`, `-evo2_40b_LLR`).
   - `ZS_8_standalone`: exact $1/8$ average adding `CADD.RawScore`.
   - `CI_6_multimodal`: exact $1/6$ average across 6 functional/conservation pillars, with exact $1/m$ within-pillar averaging.
   - `AF_Closed_4`, `AF_Closed_3`, `AF_4P`, `AF_HumanOnly`, `AF_SeqReg_cadd_free`: exact $1/4$, $1/3$, $1/4$, $1/3$, and $1/2$ equal-weight block averages, containing zero multiple-sequence alignment (MSA) features.

---

## 3. Independent 6-Decimal Reproduction of All Metrics

Using the official TraitGym `AUPRC_by_chrom_weighted_average` metric rule and $B = 1,000$ chromosome-level bootstrap resamples (seeds `0..999`), all baselines and claimed results were independently recomputed from `runs/2026-10-26-0216/data/`:

### A. Published Zero-Shot Baseline Reproductions

| Dataset | Baseline Model | Published AUPRC | Independently Reproduced | Certificate Match (6 d.p.) |
| :--- | :--- | :---: | :---: | :---: |
| `mendelian_traits_matched_9` ($N=3,380$, $19$ chroms) | `CADD.plus.RawScore` | `0.712185` | `0.712185` (`se = 0.039413`, CI `[0.631772, 0.783832]`) | **PASS** |
| `mendelian_traits_matched_9` ($N=3,380$, $19$ chroms) | `phyloP-241m.plus.score` | `0.695964` | `0.695964` (`se = 0.040781`, CI `[0.607790, 0.764679]`) | **PASS** |
| `complex_traits_matched_9` ($N=11,400$, $22$ chroms) | `CADD.plus.RawScore` | `0.249900` | `0.249900` (`se = 0.010304`, CI `[0.229819, 0.269695]`) | **PASS** |
| `complex_traits_matched_9` ($N=11,400$, $22$ chroms) | `phyloP-241m.plus.score` | `0.227360` | `0.227360` (`se = 0.008783`, CI `[0.211790, 0.246139]`) | **PASS** |

### B. Track A — Full Win Zero-Shot (`>= 0.732185` on Mendelian & Transfer to Complex `>= 0.269900`)

| Zero-Shot Model | Mendelian AUPRC (95% CI) | Mendelian $\Delta$ vs CADD (Paired 95% CI) | Complex AUPRC (95% CI) | Complex $\Delta$ vs CADD (Paired 95% CI) | Certificate Match |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`ZS_7_cadd_free`** | **`0.789624`** (`[0.713717, 0.845178]`) | **`+0.077439`** (`[+0.046886, +0.107118]`) | **`0.281541`** (`[0.261479, 0.303159]`) | **`+0.031641`** (`[+0.022941, +0.042273]`) | **PASS** |
| **`ZS_7_within_chrom`** | **`0.767236`** (`[0.687931, 0.825374]`) | **`+0.055051`** (`[+0.013211, +0.091675]`) | **`0.279802`** (`[0.258442, 0.301402]`) | **`+0.029902`** (`[+0.020166, +0.041424]`) | **PASS** |
| **`ZS_8_standalone`** | **`0.784410`** (`[0.702722, 0.841254]`) | **`+0.072226`** (`[+0.043053, +0.098184]`) | **`0.284569`** (`[0.263051, 0.306672]`) | **`+0.034669`** (`[+0.026326, +0.043989]`) | **PASS** |
| **`CI_6_multimodal`** | **`0.807396`** (`[0.733852, 0.862473]`) | **`+0.095211`** (`[+0.054896, +0.132770]`) | **`0.283768`** (`[0.262193, 0.307642]`) | **`+0.033869`** (`[+0.025960, +0.043289]`) | **PASS** |

Both `ZS_7_cadd_free` and `CI_6_multimodal` exceed the Mendelian Full Win threshold (`0.732185`) by wide margins (`+0.077439` and `+0.095211`), have marginal 95% chromosome bootstrap CIs (`[0.713717, 0.845178]` and `[0.733852, 0.862473]`) that strictly exclude `0.712185`, and simultaneously satisfy the companion complex-traits zero-shot win (`>= 0.269900`, with marginal 95% CIs strictly excluding `0.249900`).

### C. Track B — Partial Win `p1` (Strictly Alignment-Free Zero-Shot vs `phyloP-241m = 0.695964`, Threshold `>= 0.715964`)

| Alignment-Free Zero-Shot Model | Mendelian AUPRC | 95% Bootstrap CI | $\Delta$ vs `phyloP-241m` (`0.695964`) | Complex AUPRC | Certificate Match |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`AF_Closed_4`** | **`0.754022`** | `[0.664533, 0.828406]` | **`+0.058059`** | `0.214425` | **PASS** |
| **`AF_Closed_3`** | **`0.753848`** | `[0.656221, 0.827793]` | **`+0.057884`** | `0.215487` | **PASS** |
| **`AF_4P`** | **`0.793262`** | `[0.699829, 0.864266]` | **`+0.097299`** | `0.211564` | **PASS** |
| **`AF_HumanOnly`** | **`0.749720`** | `[0.668870, 0.819575]` | **`+0.053757`** | `0.220943` | **PASS** |
| **`AF_SeqReg_cadd_free`** | **`0.630423`** | `[0.512529, 0.727316]` | `-0.065540` (`+0.073886` vs `evo2_40b_LLR`) | `0.210057` | **PASS** |

### D. Track C — Partial Wins `p2` & `p3` (Supervised By-Chromosome Probing, Threshold `>= 0.894660`)

| Supervised Probing Model (`LogisticRegression.chrom`) | Reproduced Mendelian AUPRC | Certificate Value | Match (6 d.p.) |
| :--- | :---: | :---: | :---: |
| **`CADD_LogisticRegression_chrom_local`** (114 cols) | `0.877721` | `0.877721` | **PASS** |
| **`CADD_noPopFreq_LogisticRegression_chrom_105cols`** (105 cols) | `0.740276` | `0.740276` | **PASS** |
| **`M1_multimodal_135cols`** (`p2` win, $+0.023794$ vs published `0.874660`) | **`0.898454`** | **`0.898454`** | **PASS** |
| **`M2_multimodal_165cols`** (`p2` win, $+0.029464$ vs published `0.874660`) | **`0.904124`** | **`0.904124`** | **PASS** |
| **`M1_noPopFreq_126cols`** ($+0.051438$ vs `CADD_noPopFreq`) | **`0.791714`** | **`0.791714`** | **PASS** |

---

## 4. Final Audit Conclusion

All SHA-256 hashes, zero-shot label-isolation invariants, equal-weight combination formulas, baseline reproductions, Track A Full Win zero-shot scores, Track B alignment-free zero-shot scores, and Track C by-chromosome supervised probing scores are independently reproduced to 6 decimal places. **Verdict: PASS.**

pass: true
