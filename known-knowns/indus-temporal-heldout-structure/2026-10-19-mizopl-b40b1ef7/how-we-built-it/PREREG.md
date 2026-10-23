# Preregistration: `indus-temporal-heldout-structure`

target: indus-temporal-heldout-structure
frozen: 2026-10-19T19:50:00Z
null_test: required

## 1. Frozen M77-Only Model Artifact

- **Artifact file**: `m77_frozen_structural_model.json`
- **Frozen UTC timestamp**: `2026-10-19T19:48:10Z`
- **SHA-256**: `b40b1ef7b100e944aa1d86efa3b8f7dbdfbcd15885ab785e25e7e7454b1451a3`
- **Training data**: Fitted strictly and exclusively on Mahadevan's 1977 concordance (`im77_corpus_lines.csv`, `sha256: b3033d085bf40c9757766fc76f1c05196215c2d95c686109cc9e6911671b16cf`) and the static sign-code crosswalk (`bridge_extended.json`, `sha256: 75ff10b9e2b33290e53d11a14a4f38dc8f0190c35bf883eb95d9693db3056384`). Zero post-1977 inscriptions were accessed during model construction or hyperparameter selection.

## 2. Structural Claims Registered Prior to Post-1977 Evaluation

1. **Primary Structural Claim (Full `success_criterion` and `p1`) — 5-Zone Positional Slot-Class & Bilateral Frame Grammar with Intra-Inscription Anti-Repetition (`M77-CLSS`)**:
   - Inscriptions in the Indus script follow a non-stationary 5-zone positional slot grammar $z(i, L) \in \{\text{INIT}, \text{SECOND}, \text{MID}, \text{PENULT}, \text{FINAL}\}$ combined with 32 `M77`-derived distributional sign-equivalence classes $C_0, \dots, C_{31}$, discounted slot-specific bigrams $P(v \mid s_{i\pm 1}, z(i, L))$, center-frame transitions $P(v \mid s_{i-1}, s_{i+1})$, bilateral Kneser-Ney blanket probabilities, and an intra-inscription anti-repetition law penalizing adjacent and non-adjacent repetition of non-geminate signs.
   - **Measurable Property**: Masked-sign top-1 restoration accuracy across all token positions $0 \le i < L$ on deduplicated, publication-dated post-1977 held-out inscriptions of length $L \ge 2$ (tested under both `Mode 1` exact `test_prereg.py` sign mapping and `Mode 2` canonical `bridge_extended.json` connected-component mapping, and on both the full publication-dated post-1977 held-out set and the strict post-1977 catalog-range subset).
   - **Pass Threshold**: Paired-bootstrap $p < 0.001$ (`10,000` resamples, `seed=0`) against BOTH:
     - (i) a tuned Kneser-Ney 3-gram trained on the same `M77` data (`D = 0.55`, evaluated against standard left-context `KN3-Left` as in `analysis/ngram.py`, bidirectional `KN3-Bidir`, and full forward Markov blanket `KN3-BlanketF`), and
     - (ii) a `SIGIL`-style non-linguistic synthetic control (`generate_matched_null_corpus` from `adversarial_null_model.py`, plus `400` independent `SIGIL` controls in `null_test.md`) matched on `M77` unigram, initial, final, and length distributions.
   - **Site Replication**: Must beat both baselines with paired-bootstrap $p < 0.001$ on the pooled held-out corpus, on **Mohenjo-daro** separately, on **Harappa** separately, and on **post-1977 excavated sites** (e.g. **Dholavira**) separately.
2. **Secondary Structural Claim (`p3`) — Frozen Top-25 `M77` Telescoping Composite/Bigram Substitutions ($C \leftrightarrow A\ B$) in Parallel Contexts**:
   - The frozen list of 25 `M77`-only composite/ligature signs $C$ and two-sign sequences $(A, B)$ stored in `m77_frozen_structural_model.json["frozen_m77_top25_telescoping_ligatures_p3"]` (excluding `R5` `226 <-> 220 520` and all trivial overlaps $C \in \{A, B\}$) achieves a parallel-context substitution count (shared flanking frames $(L, C, R) \leftrightarrow (L, A, B, R)$ in the post-1977 held-out corpus) strictly exceeding `10,000` frequency-matched random composite/bigram sets with permutation $p < 0.001$.

## 3. Null Control Protocol (`null_test.md`)

- Because `undeciphered-scripts` is in `NULL_CATEGORIES`, we run `400` independent `SIGIL` matched-null synthetic controls (`seed = 1..400`, matching `M77` length, initial, final, and unigram distributions) and record the exact control distribution (`controls: 400`, `best_control`, `real`, `real_beats_all_controls: yes`) in `null_test.md`.
