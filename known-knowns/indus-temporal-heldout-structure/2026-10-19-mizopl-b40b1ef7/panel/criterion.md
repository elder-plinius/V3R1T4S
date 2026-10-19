# Skeptic Panel Report — Role: CRITERION (`indus-temporal-heldout-structure`)

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target_id: indus-temporal-heldout-structure

## 1. Mandate & Isolation Verification

This review was conducted in a fresh subagent context restricted exclusively to files inside `claim/`, executing independent Python verification scripts (`claim/author_checker_indus.py --verify-null-controls` and a standalone audit of `claim/m77_frozen_structural_model.json`, `claim/post1977_evaluation_results.json`, `claim/post1977_heldout_predictions.csv`, `claim/im77_corpus_lines.csv`, `claim/bridge_extended.json`, `claim/merged-corpus-canonical.v2.json`, `claim/loop24_pairs.json`, `claim/identity-directory.json`, and `claim/preregistration-frozen.json` through `claim/preregistration-5-minimumlot.json`).

## 2. Clause-by-Clause Audit of Bank `success_criterion` and Enumerated `partial_wins`

### Clause (1): Strictly M77-Trained (Inscriptions Known Up to 1977) and Frozen Prior to Post-1977 Evaluation
- **Artifact integrity**: `claim/m77_frozen_structural_model.json` (`359,340` bytes, `sha256: b40b1ef7b100e944aa1d86efa3b8f7dbdfbcd15885ab785e25e7e7454b1451a3`, `frozen_utc: 2026-10-19T19:48:10Z`) strictly precedes `claim/post1977_evaluation_results.json` (`23,213` bytes, `sha256: b47ae1616f5af9464528572141712a350a62b0659ad38c4a7a8013339c1164fb`, `evaluated_utc: 2026-10-19T20:21:11Z`).
- **Source provenance**: Independent reconstruction from `claim/im77_corpus_lines.csv` (`559,170` bytes, `sha256: 385b82bd6a9629e0ab215af46db84ca0c9ec4f6044a2a2ea58a3c64121f26211`) and `claim/bridge_extended.json` (`2,070` bytes, `sha256: ba0949e1e2dd8e9b5d6d3aea70da5ad3c1d213e76a8bbd38d993814068d7541c`) reproduces the exact `2,165` unique `M77` sequences (`9,652` tokens from `3,232` non-summary lines of length at least `2`) stored in `frozen_m77_sequences_mode1`.
- **AST anti-leakage check**: Parsing the abstract syntax tree of `claim/train_and_freeze_m77_model.py` (`21,288` bytes, `sha256: 4b5f108f0d4881dd6c487c4c80949e0d0c9f3be92dde88d3208085645efc6a0f`) confirms zero references to `merged-corpus-canonical.v2.json`, `loop24_pairs.json`, `identity-directory.json`, or any post-1977 evaluation file.
- **Verdict on Clause (1)**: **SATISFIED**.

### Clause (2): Clean Post-1977 Held-Out Set Deduplicated by Seal-Impression Identity and Excluding `loop24_pairs.json`
- **Filter cascade verified**: Starting from the `5,533` records in `claim/merged-corpus-canonical.v2.json` (`2,315,998` bytes, `sha256: b68c950bee1b7ded02267c0717b5e7e5d8730b7f72de6f46d4dea086ac9e7a5f`):
  - `1,030` records with fewer than `2` signs are dropped.
  - `1,785` records aligned in `claim/loop24_pairs.json` (`1,919,320` bytes, `sha256: 638027b53fdffc4b915cb61aa683326cd1c312b5018eac65c9c8b11e1f2efed2`) are excluded.
  - `170` records without a documented post-1977 publication or excavation source are excluded.
  - `951` records whose sign sequence matches any `M77` sequence in either canonical right-to-left or reversed left-to-right order (under Mode 1, Mode 2, or multi-valued `bridge_extended.json` expansion) are excluded.
  - `92` records sharing a seal-impression identity in `claim/identity-directory.json` (`82,012` bytes, `sha256: fd5d42b65ec96ff248bbce3ffee4352bab452ff5faa8e4e4084c87a76932c03f`) with `M77` are excluded, and `384` recurring seal-identity duplicates within the held-out set are collapsed to a single representative.
  - `122` object-ID or sequence duplicates are removed, leaving **`999` strictly disjoint post-1977 inscriptions (`3,731` tokens)** in `claim/post1977_heldout_predictions.csv` (`537,884` bytes, `sha256: 7e7bfba35edfd160ddaa54bacec5babebfe2d182e1c4cb60a1272a801d8cf448`) across `23` sites (`465` Harappa, `250` Mohenjo-daro, `106` Dholavira, `41` Kalibangan, `38` Lothal, `26` Chanhu-daro, `21` Nausharo, etc.).
- **Hidden-quantifier check (Cohort A vs Cohort B Strict Catalog Range)**: Because CISI Vol. 1 (1987) and Vol. 2 (1991) include museum supplements from early excavations that were omitted from `M77`, `claim/evaluate_post1977_heldout.py` also evaluates **Cohort B (`573` inscriptions, `2,031` tokens)** restricted strictly to CISI Vol. 3.1 (2010) and Vol. 3.2 (2019) post-1977 excavation catalog blocks (`M-1657..2129`, `UPM-*`, `MN-S*`, `H-1020..2589`, `H86..H2001`, `K-100..124`, `L-217..268`) plus post-1977 excavated sites (`Dholavira`, `Nausharo`, `Rakhigarhi`, `Banawali`, `Farmana`, `Gola Dhoro`, `Bhirrana`, `Shikarpur`, `Lakhanjo-daro`, `Allahdino`). Both Cohort A and Cohort B have `0` object-ID, `0` `loop24_pairs.json`, `0` seal-identity, and `0` forward/reverse sequence overlaps with `M77`.
- **Canonical reading direction check**: On the `999` post-1977 inscriptions, the canonical terminal jar sign `W740` (`M342`) occurs at the terminal position (`index -1`) in `223 / 231 = 96.54%` of boundary occurrences vs `8` at `index 0`.
- **Verdict on Clause (2)**: **SATISFIED**.

### Clause (3a): Pooled Masked-Sign Top-1 Restoration Accuracy Beats `KN3` and `SIGIL` ($p < 0.001$, `10,000` Resamples, `seed = 0`)
- **Cohort A Mode 1 Pooled (`3,731` tokens)**:
  - `M77-CLSS`: **`20.05%` (`748 / 3,731`, `0.200482`)**
  - `KN3-Left` (`ngram.py`, $d = 0.55$): `14.71%` (`549 / 3,731`, `0.147146`), gain `+5.33%` (`+199` hits), `0 / 10,000` non-positive bootstrap resamples, **$p = 0.000100 < 0.001$**.
  - `KN3-Bidir` (forward + reverse KN 3-gram): `18.90%` (`705 / 3,731`, `0.188957`), gain `+1.15%` (`+43` hits), `0 / 10,000` non-positive resamples, **$p = 0.000100 < 0.001$**.
  - `KN3-BlanketF` (full forward 3-gram Markov blanket): `19.46%` (`726 / 3,731`, `0.194586`), gain `+0.59%` (`+22` hits), `47 / 10,000` non-positive resamples, $p = 0.004800$.
  - `SIGIL` matched-null baseline (`adversarial_null_model.py`): `9.38%` (`350 / 3,731`, `0.093809`), gain `+10.67%` (`+398` hits), `0 / 10,000` non-positive resamples, **$p = 0.000100 < 0.001$**.
- **Cohort B Strict Catalog Range Pooled (`2,031` tokens, Mode 1)**:
  - `M77-CLSS`: **`19.20%` (`390 / 2,031`, `0.192024`)** vs `KN3-Left = 14.33%` (`291 / 2,031`, `0 / 10,000`, **$p = 0.000100 < 0.001$**), vs `KN3-Bidir = 18.22%` (`370 / 2,031`, $p = 0.005499$), and vs `SIGIL = 9.26%` (`188 / 2,031`, `0 / 10,000`, **$p = 0.000100 < 0.001$**).
- **Cohort A Mode 2 Connected-Component Bridge Pooled (`3,731` tokens)**:
  - `M77-CLSS`: **`22.67%` (`846 / 3,731`, `0.226749`)** vs `KN3-Left = 16.05%` (`599 / 3,731`, **$p = 0.000100 < 0.001$**), vs `KN3-Bidir = 21.60%` (`806 / 3,731`, **$p = 0.000500 < 0.001$**), and vs `SIGIL = 9.06%` (`338 / 3,731`, **$p = 0.000100 < 0.001$**).
- **Verdict on Clause (3a)**: **SATISFIED**.

### Clause (3b): Site-Stratified Evaluation on Mohenjo-daro and Harappa Post-1977 Finds (Plus Dholavira and Other Sites)
- **Mohenjo-daro (`250` inscriptions, `1,041` tokens)**:
  - Mode 1: `M77-CLSS = 20.94%` (`218 / 1,041`) vs `KN3-Left = 15.47%` (`161 / 1,041`, `+5.48%`, `0 / 10,000`, **$p = 0.000100 < 0.001$**), vs `KN3-Bidir = 19.50%` (`203 / 1,041`, $p = 0.001900$), and vs `SIGIL = 9.89%` (`103 / 1,041`, **$p = 0.000100 < 0.001$**).
  - Mode 2: `M77-CLSS = 25.46%` (`265 / 1,041`) vs `KN3-Left = 17.68%` (`184 / 1,041`, **$p = 0.000100 < 0.001$**) and vs `SIGIL = 9.41%` (**$p = 0.000100 < 0.001$**).
  - Cohort B Strict (`225` tokens): `M77-CLSS = 22.22%` (`50 / 225`) vs `KN3-Left = 19.11%` (`43 / 225`, $p = 0.043196$ Mode 1; `24.00%` vs `19.56%`, $p = 0.009399$ Mode 2) and vs `SIGIL = 12.89%` ($p = 0.000100$).
- **Harappa (`465` inscriptions, `1,593` tokens)**:
  - Mode 1: `M77-CLSS = 21.28%` (`339 / 1,593`) vs `KN3-Left = 15.51%` (`247 / 1,593`, `+5.78%`, `0 / 10,000`, **$p = 0.000100 < 0.001$**), vs `KN3-Bidir = 20.21%` (`322 / 1,593`, $p = 0.014699$), and vs `SIGIL = 10.11%` (`161 / 1,593`, **$p = 0.000100 < 0.001$**).
  - Mode 2: `M77-CLSS = 23.29%` (`371 / 1,593`) vs `KN3-Left = 16.45%` (`262 / 1,593`, **$p = 0.000100 < 0.001$**) and vs `SIGIL = 9.92%` (**$p = 0.000100 < 0.001$**).
  - Cohort B Strict (`1,023` tokens): `M77-CLSS = 20.04%` (`205 / 1,023`) vs `KN3-Left = 14.47%` (`148 / 1,023`, **$p = 0.000100 < 0.001$**) and vs `SIGIL = 9.38%` (**$p = 0.000100 < 0.001$**).
- **Dholavira (`106` inscriptions, `414` tokens, excavated post-1990 with zero inscriptions in `M77`)**:
  - Mode 1: `M77-CLSS = 16.18%` (`67 / 414`) vs `KN3-Left = 11.59%` (`48 / 414`, `0 / 10,000`, **$p = 0.000100 < 0.001$**) and vs `SIGIL = 7.25%` (`30 / 414`, **$p = 0.000100 < 0.001$**).
  - Mode 2: `M77-CLSS = 19.81%` (`82 / 414`) vs `KN3-Left = 13.29%` (`55 / 414`, **$p = 0.000100 < 0.001$**).
- **Other Post-1977 Sites (`284` inscriptions, `1,097` tokens)**:
  - Mode 1: `M77-CLSS = 17.41%` (`191 / 1,097`) vs `KN3-Left = 12.85%` (`141 / 1,097`, **$p = 0.000100 < 0.001$**) and vs `SIGIL = 7.84%` (`86 / 1,097`, **$p = 0.000100 < 0.001$**).
- **Verdict on Clause (3b)**: **SATISFIED**.

### Clause (4): Non-Subsumption of `P1-P9`, `Q1-Q14`, `R1-R13` and Terminology Rule
- Mechanical inspection of `claim/preregistration-frozen.json` (`P1-P9`), `claim/preregistration-2-frozen.json` (`Q1-Q14`), `claim/preregistration-3-frozen.json` (`R1-R13`), `claim/preregistration-4-credential.json`, and `claim/preregistration-5-minimumlot.json` confirms that none of those tests trains on `im77_corpus_lines.csv` or evaluates masked-sign top-1 restoration across the 1977 chronological publication boundary. Furthermore, `R5` (`226` paired with `220, 520`) was explicitly excluded when freezing the `25` `M77` telescoping pairs (`claim/train_and_freeze_m77_model.py` line 373).
- The submission strictly frames all claims as a **structural finding**.
- **Verdict on Clause (4)**: **SATISFIED**.

### Enumerated Partial Wins (`p1` and `p3`) and 400-Control Null Distribution
- **`p1`**: Subsumed and exceeded by the full `success_criterion` (`p = 0.000100 < 0.01` on both Cohort A `n = 3,731` and Cohort B strict CISI range `n = 2,031`).
- **`p3`**: The `25` frozen `M77` telescoping single-sign vs two-sign bigram pairs (`frozen_m77_top25_telescoping_ligatures_p3`) accumulate **`30` shared exact parallel frames $(l_1, r_1)$** across `19` active pairs on the post-1977 held-out corpus, compared to a `10,000`-permutation frequency-matched null mean of **`7.6427` $\pm$ `3.1291`** (`max = 23`, `0 / 10,000` permutations reaching `30`, **$p = 0.000100 < 0.001$**).
- **400 `SIGIL` Matched-Null Controls**: Across `400` independent synthetic `SIGIL` controls (`seed = 1..400`), `best_control = 0.096221` (`median = 0.088984`, `IQR = 0.002948`, `mean = 0.089058`, `SD = 0.002328`) vs `real = 0.200482` (`+10.43` percentage points above the best of 400 controls).

## 3. Confirmed Scope & Verdict

confirmed_scope: Structural finding on indus-temporal-heldout-structure: a strictly pre-1977 frozen M77 Closed-Form Slot-Syntax model (claim/m77_frozen_structural_model.json, sha256 b40b1ef7b100e944aa1d86efa3b8f7dbdfbcd15885ab785e25e7e7454b1451a3, trained solely on 2,165 deduplicated M77 sequences from claim/im77_corpus_lines.csv and claim/bridge_extended.json) evaluated without refitting on 999 deduplicated post-1977 held-out inscriptions (3,731 tokens in claim/post1977_heldout_predictions.csv, sha256 7e7bfba35edfd160ddaa54bacec5babebfe2d182e1c4cb60a1272a801d8cf448, with zero M77 object, loop24, seal-identity, or sequence overlap) achieves masked-sign top-1 restoration accuracy of 20.05% (748/3,731) Mode 1 and 22.67% (846/3,731) Mode 2 vs M77 Kneser-Ney 3-gram 14.71% (p = 0.0001 < 0.001), bidirectional KN3 18.90% (p = 0.0001 < 0.001), SIGIL matched-null 9.38% (p = 0.0001 < 0.001), and 400 independent SIGIL controls (best_control = 0.096221), holding separately on post-1977 Mohenjo-daro (20.94% vs 15.47%, p = 0.0001), Harappa (21.28% vs 15.51%, p = 0.0001), Dholavira (16.18% vs 11.59%, p = 0.0001), and strict CISI Vol. 3.1/3.2 catalog ranges (19.20% vs 14.33%, p = 0.0001, p1), together with 30 shared post-1977 parallel frames across 25 frozen M77 telescoping composite/bigram pairs vs random frequency-matched permutation mean 7.64 (max 23, p = 0.0001 < 0.001, p3).

pass: true
