# Skeptic Panel Report: REPRODUCE (`indus-temporal-heldout-structure`)

role: REPRODUCE
context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
target_id: indus-temporal-heldout-structure
claim_type: partial_win
partial_win: p3

---

## 1. Quoted Definition & Success Criterion from Target Specification

Prior to inspecting the author's Python scripts (`verify-it-yourself/check_indus_claim.py`, `how-we-built-it/train_and_freeze_m77_model.py`, `how-we-built-it/evaluate_post1977_heldout.py`), an independent standalone checker was written directly from the target definition and structural finding specification in `README.md` and `RUN_IT_YOURSELF.md`:

- **Success Criterion**:
  "A structural model (functional sign equivalence classes, slot grammar, or positional dependency rules) trained strictly on the Mahadevan 1977 concordance (M77; inscriptions known at or before 1977, `data/im77/im77_corpus_lines.csv` in `Indus-`) and evaluated without refitting on a clean held-out set of inscriptions excavated or published strictly after 1977 (e.g., Dholavira, post-1977 Harappa excavations, CISI Vol. 2 1991 and Vol. 3.1 2010 entries absent from M77, after deduplicating seal-impression identity groups via `identity-directory.json` and excluding any object aligned in `loop24_pairs.json`), achieving both: (a) masked-sign top-1 restoration accuracy on the post-1977 held-out set that beats an M77-trained Kneser-Ney 3-gram baseline (`ngram.py`) AND the `SIGIL` matched-null baseline (`adversarial_null_model.py`) with paired-bootstrap p ≤ 0.001 (10,000 resamples, seed=0), and (b) site-stratified evaluation showing the gain holds separately on Mohenjo-daro and Harappa post-1977 finds (ruling out site-distribution shift). Must not subsume any existing preregistered test P1-P9, Q1-Q14, or R1-R13 in `Indus-`."

- **Partial Wins**:
  - **`p1`**: `"A verified M77-vs-post-1977 masked-sign restoration benchmark on deduplicated post-1977 CISI entries where a frozen M77 positional/equivalence-class model beats the M77 Kneser-Ney 3-gram baseline with paired-bootstrap p ≤ 0.01 on the pooled held-out set."`
  - **`p3`**: `"A preregistered composite-sign decomposition test: composite signs listed in M77 / Wells behave distributionally as their constituent two-sign bigrams in parallel contexts on the post-1977 held-out set (permutation p ≤ 0.001 against random bigram pairings of matched frequency)."`

---

## 2. Independent Checker Verification

Executed in `2.10` seconds before reading the author's code, the independent checker verified every artifact, anti-leakage property, statistical test, and negative control directly from the saved files in this package (`object/`, `how-we-built-it/`, `verify-it-yourself/`) and the upstream `https://github.com/paragorth/Indus-` repository (commit `d62ec82d58642038640da25a97177d7a1fddc9d9`):

### 2.1 Exact Byte Sizes and SHA-256 Digests

| Artifact / Upstream File | Byte Size | Verified SHA-256 Digest | Status |
|---|---:|---|---|
| `object/m77_frozen_structural_model.json` | `359,340` | `b40b1ef7b100e944aa1d86efa3b8f7dbdfbcd15885ab785e25e7e7454b1451a3` | PASS |
| `object/post1977_evaluation_results.json` | `23,213` | `b47ae1616f5af9464528572141712a350a62b0659ad38c4a7a8013339c1164fb` | PASS |
| `object/post1977_heldout_predictions.csv` | `537,884` | `7e7bfba35edfd160ddaa54bacec5babebfe2d182e1c4cb60a1272a801d8cf448` | PASS |
| `paragorth/Indus-`: `data/im77/im77_corpus_lines.csv` | `559,170` | `385b82bd6a9629e0ab215af46db84ca0c9ec4f6044a2a2ea58a3c64121f26211` | PASS |
| `paragorth/Indus-`: `data/derived/bridge_extended.json` | `2,070` | `ba0949e1e2dd8e9b5d6d3aea70da5ad3c1d213e76a8bbd38d993814068d7541c` | PASS |
| `paragorth/Indus-`: `data/derived/merged-corpus-canonical.v2.json` | `2,315,998` | `b68c950bee1b7ded02267c0717b5e7e5d8730b7f72de6f46d4dea086ac9e7a5f` | PASS |
| `paragorth/Indus-`: `data/derived/dark/loop24_pairs.json` | `1,919,320` | `638027b53fdffc4b915cb61aa683326cd1c312b5018eac65c9c8b11e1f2efed2` | PASS |
| `paragorth/Indus-`: `data/derived/identity-directory.json` | `82,012` | `fd5d42b65ec96ff248bbce3ffee4352bab452ff5faa8e4e4084c87a76932c03f` | PASS |
| `paragorth/Indus-`: `prereg/preregistration-frozen.json` | `2,594` | `214964e5bf2d15d960f6d3ba6496d7a4a4d312dba6c60b641de64d81acfb8631` | PASS |
| `paragorth/Indus-`: `prereg/preregistration-2-frozen.json` | `5,124` | `1774b7c76d9d047f463c7d583169fa369ae8c3b80ff725cfd9b0ab28bdc20df4` | PASS |
| `paragorth/Indus-`: `prereg/preregistration-3-frozen.json` | `5,227` | `f31a81f11d58ee0e05216cfb3b17b83e6baea303012fd07488ebec38c08dccee` | PASS |
| `how-we-built-it/train_and_freeze_m77_model.py` | `21,288` | `4b5f108f0d4881dd6c487c4c80949e0d0c9f3be92dde88d3208085645efc6a0f` | PASS |
| `how-we-built-it/evaluate_post1977_heldout.py` | `43,689` | `780975cf326ad902f2e86f85cdc464cf326c85157c335e44d5d4ea0d935d67d2` | PASS |

### 2.2 Independent Verification of Chronological Anti-Leakage & Disjointness

1. **Timestamp Ordering**: `frozen_utc` in `object/m77_frozen_structural_model.json` (`2026-10-19T19:48:10Z`) strictly precedes `evaluated_utc` in `object/post1977_evaluation_results.json` (`2026-10-19T20:21:11Z`).
2. **Pre-1977 `M77` Sequence Reconstruction**: Parsing `data/im77/im77_corpus_lines.csv` directly (`3,917` data rows), excluding `line == '9'` summary rows, dropping `0` (damaged/illegible sign markers), filtering to length $\ge 2$ (`3,232` lines), mapping via `m2g_mode1`, and deduplicating exact sequences reproduces the exact **`2,165` unique sequences (`9,652` tokens)** stored in `frozen_m77_sequences_mode1`.
3. **End-to-End Post-1977 Held-Out Corpus Reconstruction**: Re-running the filtering pipeline on the `5,533` records in `data/derived/merged-corpus-canonical.v2.json` reproduces the exact filter cascade (`dropped_len_lt_2 = 1,030`, `excluded_in_im77_loop24 = 1,785`, `excluded_no_post1977_pub_source = 170`, `excluded_sequence_in_im77 = 951`, `excluded_seal_identity_in_im77 = 92`, `deduped_seal_identity = 384`, `deduped_object_or_sequence = 122`, `kept_heldout = 999`) and matches all `3,731` token rows in `object/post1977_heldout_predictions.csv` `100%` token-for-token.
4. **Zero-Overlap Audit (`2,165` `M77` vs `999` Held-Out Inscriptions)**:
   - Object-ID overlaps with `M77` (`text_no`): **`0`**
   - Accepted `data/derived/dark/loop24_pairs.json` (`cisi` stripped) overlaps: **`0`**
   - `data/derived/identity-directory.json` seal-identity overlaps with `M77`: **`0`**
   - Duplicate seal identities within the `999` held-out inscriptions: **`0`** (at most 1 inscription per recurring seal identity)
   - Forward or reverse sign-sequence overlaps with `M77`: **`0`**
   - Duplicate sequences within the `999` held-out inscriptions: **`0`**
5. **Canonical Right-to-Left Reading Direction Check**: Across the `999` held-out inscriptions, the canonical terminal jar sign `W740` occurs at final position `index -1` in **`223 / 231 = 96.54%`** (`0.965368`) of boundary appearances vs **`8`** at initial position `index 0`.

### 2.3 Independent Recomputation of Masked-Sign Restoration & Paired Bootstrap (`10,000` Resamples, `seed = 0`)

Every row in `object/post1977_heldout_predictions.csv` (`3,731` tokens) was verified to satisfy `hit_* == int(int(pred_*) == int(target))` across all five models (`clss`, `kn3_left`, `kn3_bidir`, `kn3_blanket_f`, `sigil`). Recomputing hit counts, accuracies, and `10,000`-resample paired bootstrap $p$-values (`seed = 0`, `p = (nonpos + 1) / 10001`) yielded exact agreement with `object/post1977_evaluation_results.json`:

| Stratum (Mode 1) | Tokens ($n$) | `M77-CLSS` Hits (Acc) | `KN3-Left` ($p_{\text{boot}}$, `nonpos`) | `KN3-Bidir` ($p_{\text{boot}}$, `nonpos`) | `KN3-BlanketF` ($p_{\text{boot}}$, `nonpos`) | `SIGIL` ($p_{\text{boot}}$, `nonpos`) |
|---|---:|---:|---:|---:|---:|---:|
| **Pooled** | `3,731` | `748` (`0.200482`) | `549` (`0.000100`, `0/10k`) | `705` (`0.000100`, `0/10k`) | `726` (`0.004800`, `47/10k`) | `350` (`0.000100`, `0/10k`) |
| **Mohenjo-daro** | `1,041` | `218` (`0.209414`) | `161` (`0.000100`, `0/10k`) | `203` (`0.001900`, `18/10k`) | `215` (`0.298770`, `2987/10k`) | `103` (`0.000100`, `0/10k`) |
| **Harappa** | `1,593` | `339` (`0.212806`) | `247` (`0.000100`, `0/10k`) | `322` (`0.014699`, `146/10k`) | `328` (`0.018798`, `187/10k`) | `161` (`0.000100`, `0/10k`) |
| **Dholavira** | `414` | `67` (`0.161836`) | `48` (`0.000100`, `0/10k`) | `64` (`0.245175`, `2451/10k`) | `65` (`0.369563`, `3695/10k`) | `30` (`0.000100`, `0/10k`) |
| **Other Post-1977 Sites** | `1,097` | `191` (`0.174111`) | `141` (`0.000100`, `0/10k`) | `180` (`0.030897`, `308/10k`) | `183` (`0.053695`, `536/10k`) | `86` (`0.000100`, `0/10k`) |
| **Cohort B Strict** | `2,031` | `390` (`0.192024`) | `291` (`0.000100`, `0/10k`) | `370` (`0.005499`, `54/10k`) | `380` (`0.067993`, `679/10k`) | `188` (`0.000100`, `0/10k`) |

### 2.4 Independent Verification of Partial Win `p3` (Telescoping Composite/Bigram Substitutions)

- Re-deriving the Top-25 telescoping single-sign vs two-sign bigram candidates ($C \leftrightarrow A\ B$) directly from the `2,165` `M77` sequences reproduced `frozen_m77_top25_telescoping_ligatures_p3` in `object/m77_frozen_structural_model.json` with `100%` identity (`25 / 25` pairs, exact `m77_shared_frames`, `m77_expected_frames`, and `m77_z_score`).
- Re-deriving the `32` distributional Ward sign-equivalence classes (`C0..C31`) on `M77` reproduced both `frozen_m77_clusters_mode1` and `frozen_m77_clusters_mode2` with `100%` identity.
- Evaluating the `25` frozen `M77` pairs on the `999` post-1977 held-out inscriptions confirmed **`19 / 25` pairs with shared parallel frames** and **`30` total shared exact flanking frames $(l_1, r_1)$** (where boundary positions are padded with `[BOS]` and `[EOS]`).
- Across `10,000` frequency-matched random permutations (`seed = 0`, sampling within the `15` nearest `M77` log-frequency neighbors with `M77` count $\ge 5$), the null distribution has **mean `7.6427`**, **standard deviation `3.1291`**, **maximum `23`**, and **`0 / 10,000` permutations $\ge 30$ (`p = 0.000100 < 0.001`)**. Under an unrestricted active held-out neighbor pool (without the `M77` count $\ge 5$ filter), the null distribution similarly has **mean `7.6396`**, **standard deviation `3.1330`**, **maximum `23`**, and **`0 / 10,000` permutations $\ge 30$ (`p = 0.000100 < 0.001`)**.

### 2.5 Negative Controls (Checker Sensitivity Verification)

1. **Negative Control 1 (Permuted Held-Out Targets, `seed = 42`)**: Randomly permuting the `3,731` held-out target tokens collapses `M77-CLSS` accuracy from `0.200482` (`748 / 3,731`) to **`0.037255` (`139 / 3,731`)** (`p_boot_vs_kn3_left = 1.000000`), which the independent checker properly rejects.
2. **Negative Control 2 (Single Majority Unigram `W740` Predictor)**: Predicting the single most frequent unigram `W740` (`740`) at every position yields **`0.093809` (`350 / 3,731`)**, which is `5.33` percentage points below `KN3-Left` (`0.147146`, `p_boot_vs_kn3_left = 1.000000`) and `10.67` percentage points below `M77-CLSS` (`0.200482`), and is properly rejected.

---

## 3. Code Audit & Double-Run Determinism of `verify-it-yourself/check_indus_claim.py`

1. **Code Inspection of `how-we-built-it/train_and_freeze_m77_model.py`**:
   - Direct code and AST inspection confirms that `how-we-built-it/train_and_freeze_m77_model.py` reads **only** `im77_corpus_lines.csv` and `bridge_extended.json`, and writes `m77_frozen_structural_model.json`. Zero references to `merged-corpus-canonical.v2.json`, `loop24_pairs.json`, `identity-directory.json`, or any post-1977 file exist anywhere in `how-we-built-it/train_and_freeze_m77_model.py`.
2. **Code Inspection of `how-we-built-it/evaluate_post1977_heldout.py` and `verify-it-yourself/check_indus_claim.py`**:
   - `how-we-built-it/evaluate_post1977_heldout.py` loads `object/m77_frozen_structural_model.json` without refitting, constructs the deduplicated post-1977 held-out corpus (`999` inscriptions, `3,731` tokens), evaluates Mode 1, Cohort B Strict, Mode 2, Partial Win `p3`, and `400` independent `SIGIL` matched-null controls (`controls = 400`, `best_control = 0.096221`, `median = 0.088984`, `IQR = 0.002948` vs `real = 0.200482`), and saves `object/post1977_evaluation_results.json` and `object/post1977_heldout_predictions.csv`.
3. **Double-Run Determinism Check**:
   - Running `sh verify-it-yourself/run_checks.sh` twice back-to-back exited with code `0` on both runs and produced byte-for-byte identical stdout (`PASS`).

pass: true
