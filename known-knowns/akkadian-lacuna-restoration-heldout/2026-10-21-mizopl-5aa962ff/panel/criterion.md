# Panel Report — CRITERION (`akkadian-lacuna-restoration-heldout`)

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
confirmed_scope: On the released SLAB-NLP/Akk ORACC dataset (commit dfd2a66d4305cf36981e4fd3fde823a5020161dd, 80/20 document split at SEED=2 with 18,568 training rows and 1,875 strictly zero-overlap held-out test documents in claim/bert_test_strict_1875.txt, sha256 65e7fe8a338048e3a373f0061bbf435154e4e2a49845513c8074abd48fa9fd4c) under the repository's 15% random masking protocol at torch.manual_seed(42) (N = 27,650 frozen masked positions in claim/frozen_masked_positions.json, sha256 4abcfdb61d6a391d07b024136ace51d4dc4e3378a7ad2b89b6b12e1de75216c1, and claim/frozen_test_tensors_seed42.npz, sha256 8033d870bd9d8787627690fc26771693a6acc112be17c7d94f204ed4a9654ec4), the reproduced MBERT+Akk baseline trained strictly on the training split (claim/mbert_akk_baseline_top5_predictions.csv, sha256 e0dbc99d781c410800484a693143fe1bfc027631e4714cf498d59845bfcb9e48) achieves Hit@5 = 0.87700 (24,249/27,650) on all positions and Hit@5 = 0.87152 (22,622/25,957) on the non-missing sign subset (both inside the required [0.87, 0.91] calibration window) with MRR = 0.82369 (MRR@5 = 0.81617) and Hit@1 = 0.77693, while the hybrid slot-syntax, parallel-passage, and two-pass belief-propagation model CLSS-Akk-v3 indexed solely on the training split (claim/clss_akk_engine_v3.c, sha256 af810ea742cfb86033065e2875781354670f4cb6fe15a531bc3e5821856d7041; claim/clss_akk_top5_predictions.csv, sha256 4d974bb65acd8993a726065a4626cee8d96f0ea1bd01539e49c3dac1dac7ad9d) achieves Hit@5 = 0.92156 (25,481/27,650, +0.03156 over the paper's 0.89, +0.02656 over 0.895, and +0.04456 over MBERT+Akk), MRR = 0.85593 (MRR@5 = 0.85071, +0.02593 over the paper's 0.83 and +0.03224 over MBERT+Akk), Hit@1 = 0.80098 (22,147/27,650), and Hit@10 = 0.94517 (26,134/27,650) with a 10,000/10,000 (100.00%, p = 0.0001) paired bootstrap win rate, simultaneously beating both the paper and the reproduced baseline on the 25,957 non-missing subset (Hit@5 = 0.91983, MRR = 0.85981), on the 21,459 single-token whole-word subset (Hit@5 = 0.91617, MRR = 0.85708), under 100% [MASK] replacement (claim/clss_akk_100mask_top5_predictions.csv, Hit@5 = 0.92007, MRR = 0.84737), with the zero-neural-parameter symbolic engine CLSS-C-v3 on Hit@5 (claim/clss_c_v3_pure_top5_predictions.csv, Hit@5 = 0.89638, MRR = 0.82480), and across the Table 2 genre subsets Lexical (MRR = 0.86091 vs 0.69, Hit@5 = 0.92920 vs 0.85), Astrological Report (MRR = 0.86704 vs 0.81, Hit@5 = 0.92527 vs 0.88), and Royal or Monumental (MRR = 0.90375 vs 0.84, Hit@5 = 0.93785 vs 0.90), thereby satisfying the full success criterion and subsuming partial win p1.

---

## 1. Artifact Integrity and SHA-256 Verification

All 12 artifacts in `claim/` were independently hashed and checked against `claim/akkadian_audit_manifest.json` (`11,351` bytes, `sha256: 5aa962ffd7f53168a043fa8477d88ffd10ab00afa296614869d3c5c3381e8db0`):

| Artifact | Bytes | Verified SHA-256 | Status |
|---|---:|---|---|
| `claim/akkadian_audit_manifest.json` | `11,351` | `5aa962ffd7f53168a043fa8477d88ffd10ab00afa296614869d3c5c3381e8db0` | Exact match |
| `claim/frozen_masked_positions.json` | `5,780,131` | `4abcfdb61d6a391d07b024136ace51d4dc4e3378a7ad2b89b6b12e1de75216c1` | Exact match |
| `claim/frozen_test_tensors_seed42.npz` | `302,914` | `8033d870bd9d8787627690fc26771693a6acc112be17c7d94f204ed4a9654ec4` | Exact match |
| `claim/bert_test_strict_1875.txt` | `1,256,550` | `65e7fe8a338048e3a373f0061bbf435154e4e2a49845513c8074abd48fa9fd4c` | Exact match |
| `claim/clss_akk_corpus_full.bin` | `12,112,120` | `bac96e1142ff5d9a4bf6fb8c3c638b494747294415e89d12f2646fa0acf27b05` | Exact match |
| `claim/mbert_ep34_top128.npz` | `9,482,211` | `88d8549dc6f74913949a1a6448fea6aa11b2393aab49a70f4a28f75961a29126` | Exact match |
| `claim/clss_akk_engine_v3.c` | `36,049` | `af810ea742cfb86033065e2875781354670f4cb6fe15a531bc3e5821856d7041` | Exact match |
| `claim/train_mbert_akk_fast.py` | `13,223` | `fe91325f47484745e9a08986390899096c9ec2c0011ffefc44ee25e6893017fa` | Exact match |
| `claim/mbert_akk_baseline_top5_predictions.csv` | `2,270,741` | `e0dbc99d781c410800484a693143fe1bfc027631e4714cf498d59845bfcb9e48` | Exact match |
| `claim/clss_akk_top5_predictions.csv` | `2,236,752` | `4d974bb65acd8993a726065a4626cee8d96f0ea1bd01539e49c3dac1dac7ad9d` | Exact match |
| `claim/clss_akk_100mask_top5_predictions.csv` | `2,237,053` | `38b4df5dbfbc087e61a541d92b66e46c089ec1420524087eff294790c1b58879` | Exact match |
| `claim/clss_c_v3_pure_top5_predictions.csv` | `2,217,235` | `3bbf26c6a421a93cabe1881d3a49ac7acb8d811b9239652af1821ce5e6657b3e` | Exact match |
| `claim/author_checker_akkadian.py` | `11,297` | `ea7278246bc04f61742855bfee399098c0bf85d1289b5514357e158fc3563bd9` | Exact match |

---

## 2. Clause-by-Clause Audit of the Success Criterion and Partial Win `p1`

### Clause (1): Released `SLAB-NLP/Akk` Split, Zero Test-Train Leakage, and Deterministic Seed=42 Masking
- **Corpus and Split (`SEED = 2`):** `claim/clss_akk_corpus_full.bin` contains `N_train = 18,568` training documents (`5,412,259` valid training tokens across `V = 1,875` active Akkadian vocabulary IDs) and `N_test = 1,875` non-empty unique test documents (`claim/bert_test_strict_1875.txt`).
- **Zero Overlap Verification:** Reconstructing all `1,875` unmasked test token sequences and checking membership against all `18,568` training sequences in `claim/clss_akk_corpus_full.bin` confirms `0` full-sequence overlaps (`overlap == 0`), as well as `0` `id_text`, `0` 6-digit P/Q/X ID, and `0` `bert_input` string overlaps.
- **Deterministic `torch.manual_seed(42)` Masking:** Running the official `ORACCDataset` and `DataCollatorForLanguageModelingAkkadian` (`claim/akk_repo_ref/akkadian_bert/`, `block_size = 128`, `mlm_probability = 0.15`) at `torch.manual_seed(42)` on `claim/bert_test_strict_1875.txt` and `claim/main_tokenizer` reproduces `claim/frozen_test_tensors_seed42.npz` and `claim/frozen_masked_positions.json` bit-for-bit (`N = 27,650` masked positions). Setting `missing_sign = MISSING_SIGN_CHAR` (token ID `4`) at `torch.manual_seed(42)` produces `N = 25,958` positions bit-for-bit identical in coordinates, labels, and corrupted inputs to filtering `label_id != 4` on `claim/frozen_test_tensors_seed42.npz`; further excluding the single subword missing-sign token (token ID `5`, count `1`) yields the `N = 25,957` non-missing subset.

### Clause (2): Reproduced `MBERT+Akk` Baseline Inside `[0.87, 0.91]`
- Rescoring `claim/mbert_akk_baseline_top5_predictions.csv` (and cross-checking against the top-128 logits in `claim/mbert_ep34_top128.npz`) by both exact token ID and exact token string (`convert_ids_to_tokens`) confirms:
  - **All `27,650` frozen positions (`COLLATOR_80_10_10`):** `Hit@5 = 0.87700` (`24,249 / 27,650`), `MRR = 0.82369` (`MRR@5 = 0.81617`), `Hit@1 = 0.77693` (`21,482 / 27,650`), `Hit@10 = 0.90901` (`25,134 / 27,650`).
  - **Non-missing `25,957` positions (`missing_sign` excluded from targets and candidates):** `Hit@5 = 0.87152` (`22,622 / 25,957`, and `0.87032` = `22,591 / 25,957` without candidate filtering; `0.87029` = `22,591 / 25,958` on `label_id != 4`), `MRR = 0.82008` (`MRR@5 = 0.81221`), `Hit@1 = 0.77451` (`20,104 / 25,957`), `Hit@10 = 0.90488` (`23,488 / 25,957`).
  - Both `0.87700` and `0.87152` fall squarely within the required `[0.87000, 0.91000]` (`0.89 +/- 0.02`) comparability window around Lazar et al. (2021)'s published `Hit@5 = 0.89` (`0.895`).

### Clause (3): Full Success Criterion — `CLSS-Akk-v3` Beats Both Paper and Reproduced Baseline on Both `MRR` and `Hit@5`
- Recompiling `claim/clss_akk_engine_v3.c` from scratch (`arch -x86_64 clang -O3 -pthread`) and running two-pass inference over `claim/clss_akk_corpus_full.bin` with `alpha = 11.5` (`claim/mbert_ep34_top128.npz`) and `alpha = 0.0` (pure symbolic) reproduces `claim/clss_akk_top5_predictions.csv`, `claim/clss_akk_100mask_top5_predictions.csv`, and `claim/clss_c_v3_pure_top5_predictions.csv` 100% bit-for-bit across all `27,650` rows.
- Across every evaluation regime and subset, `CLSS-Akk-v3` strictly exceeds both the paper's published numbers (`MRR = 0.83`, `Hit@5 = 0.89 / 0.895`, `Hit@10 = 0.92`) and the reproduced `MBERT+Akk` baseline:

| Evaluation Regime / Subset | Positions ($N$) | Model | `MRR` (top-100) | `MRR@5` | `Hit@1` | `Hit@5` | `Hit@10` |
|---|---:|---|---:|---:|---:|---:|---:|
| Published Paper (Lazar et al. 2021) | ~20% split | `MBERT+Akk` (Paper) | `0.83000` | — | — | `0.89000` (`0.895`) | `0.92000` |
| All Frozen Positions (`COLLATOR_80_10_10`) | `27,650` | `MBERT+Akk` Baseline | `0.82369` | `0.81617` | `0.77693` (`21,482`) | `0.87700` (`24,249`) | `0.90901` (`25,134`) |
| All Frozen Positions (`COLLATOR_80_10_10`) | `27,650` | `CLSS-C-v3` Pure (`0` Neural) | `0.82480` | `0.81807` | `0.76470` (`21,144`) | **`0.89638`** (`24,785`) | **`0.92705`** (`25,633`) |
| All Frozen Positions (`100%_MASK`) | `27,650` | `CLSS-Akk-v3` (`100%_MASK`) | **`0.84737`** | **`0.84205`** | `0.78684` (`21,756`) | **`0.92007`** (`25,440`) | **`0.94409`** (`26,104`) |
| All Frozen Positions (`COLLATOR_80_10_10`) | `27,650` | **`CLSS-Akk-v3` Full** | **`0.85593`** | **`0.85071`** | **`0.80098`** (`22,147`) | **`0.92156`** (`25,481`) | **`0.94517`** (`26,134`) |
| Non-Missing Subset (`label not in {4,5}`) | `25,957` | `MBERT+Akk` Baseline | `0.82008` | `0.81221` | `0.77451` (`20,104`) | `0.87152` (`22,622`) | `0.90488` (`23,488`) |
| Non-Missing Subset (`label not in {4,5}`) | `25,957` | **`CLSS-Akk-v3` Full** | **`0.85981`** | **`0.85453`** | **`0.80899`** (`20,999`) | **`0.91983`** (`23,876`) | **`0.94387`** (`24,500`) |
| Single-Token Whole Words (non-missing) | `21,459` | `MBERT+Akk` Baseline | `0.82305` | `0.81520` | `0.78093` (`16,758`) | `0.86905` (`18,649`) | `0.90130` (`19,341`) |
| Single-Token Whole Words (non-missing) | `21,459` | **`CLSS-Akk-v3` Full** | **`0.85708`** | **`0.85165`** | **`0.80670`** (`17,311`) | **`0.91617`** (`19,660`) | **`0.94058`** (`20,184`) |

### Clause (4): Enumerated Partial Win `p1` Simultaneously Satisfied and Subsumed
- **Overall `at least +0.01` Margin:** On all `27,650` frozen positions, `CLSS-Akk-v3` beats the paper's `MRR = 0.83` by **`+0.02593`** (`+2.59` pts, at least `0.01`) and the reproduced `MBERT+Akk` baseline (`0.82369`) by **`+0.03224`** (`+3.22` pts, at least `0.01`), and beats the paper's `Hit@5 = 0.89 / 0.895` by **`+0.03156` / `+0.02656`** (`+3.16` / `+2.66` pts, at least `0.01`) and the reproduced `MBERT+Akk` baseline (`0.87700`) by **`+0.04456`** (`+4.46` pts, at least `0.01`). Across `10,000` paired bootstrap resamples (`seed = 42`), `CLSS-Akk-v3` wins `10,000 / 10,000` times (`100.00%`, $p = 0.0001$) on `MRR`, `MRR@5`, and `Hit@5`.
- **Table 2 Genre Breakdown:** `CLSS-Akk-v3` outperforms the reproduced `MBERT+Akk` baseline across all 8 Oracc genres in both `MRR` and `Hit@5`, and exceeds both published Table 2 metrics (`MRR` and `Hit@5`) on `Lexical` (`N = 10,240`: `MRR = 0.86091` vs `0.69`, `Hit@5 = 0.92920` vs `0.85`), `Astrological Report` (`N = 1,753`: `MRR = 0.86704` vs `0.81`, `Hit@5 = 0.92527` vs `0.88`), and `Royal or Monumental` (`N = 177`: `MRR = 0.90375` vs `0.84`, `Hit@5 = 0.93785` vs `0.90`), while on `Royal Inscription` (`N = 230`) it beats the paper's `MRR` (`0.84377` vs `0.83`) and beats the reproduced `MBERT+Akk` baseline by `+0.16396` `MRR` (`0.84377` vs `0.67981`) and `+0.14348` `Hit@5` (`0.88696` vs `0.74348`).

---

## 3. Null Models and Negative Controls

1. **400 Random Label-Permutation Controls (`N = 27,650`, `rng = default_rng(0)`):**
   - Permuting the `27,650` ground-truth labels against the frozen `CLSS-Akk-v3` top-5 predictions yields `mean Hit@5 = 0.24855 +/- 0.00178` (`max = 0.25606` vs real `0.92156`, $z = +378.22\sigma$) and `mean MRR@5 = 0.14618 +/- 0.00131` (`max = 0.15016` vs real `MRR = 0.85593`, $z = +540.00\sigma$; vs real `MRR@5 = 0.85071`, $z = +536.02\sigma$).
2. **Training-Corpus Unigram Frequency Baselines (`N = 27,650`):**
   - Predicting the global most frequent training tokens yields `Hit@1 = 0.20644`, `Hit@5 = 0.44658`, `MRR = 0.32166` (`MRR@5 = 0.30707`) when punctuation (`-`, `.`) and missing-sign tokens are included, and `Hit@1 = 0.02297`, `Hit@5 = 0.06322`, `MRR = 0.04880` (`MRR@5 = 0.03605`) when punctuation and missing-sign tokens are excluded.

---

## 4. Verdict

Every clause of the full success criterion and enumerated partial win `p1` is independently verified from the frozen artifacts and re-compiled C engine with zero test-set leakage.

pass: true
