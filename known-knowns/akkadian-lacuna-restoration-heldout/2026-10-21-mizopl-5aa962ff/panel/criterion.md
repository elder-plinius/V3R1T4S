# Panel Report — CRITERION (`akkadian-lacuna-restoration-heldout`)

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
claim_type: partial_win
partial_win: p1
confirmed_scope: On the released SLAB-NLP/Akk ORACC dataset (commit dfd2a66d4305cf36981e4fd3fde823a5020161dd, 80/20 document split at SEED=2 with 18,568 training rows and 1,875 strictly zero-overlap held-out test documents documented in object/test_tensors_recipe.md, bert_test_strict_1875.txt sha256 65e7fe8a338048e3a373f0061bbf435154e4e2a49845513c8074abd48fa9fd4c) under the repository's 15% random masking protocol at torch.manual_seed(42) (N = 27,650 frozen masked positions across object/akkadian_predictions_part1..4.csv and object/akkadian_audit_manifest.json, sha256 85b52d7c8093065a051cb06fb6306684d9f69c6f719f246bc6c13ae56d655ee9), the reproduced MBERT+Akk baseline trained strictly on the training split achieves Hit@5 = 0.87700 (24,249/27,650) on all positions, Hit@5 = 0.86463 (19,199/22,205) on [MASK]-only positions, Hit@5 = 0.87032 (22,591/25,957) on the non-missing sign subset, Hit@5 = 0.86770 (18,620/21,459) on single-token whole words, and Hit@5 = 0.87777 (23,893/27,220) on all whole-word units with MRR = 0.82369 (MRR@5 = 0.81617) and Hit@1 = 0.77693, while the hybrid slot-syntax, parallel-passage, and two-pass belief-propagation model CLSS-Akk-v3 indexed solely on the training split (how-we-built-it/clss_akk_engine_v3.c, sha256 af810ea742cfb86033065e2875781354670f4cb6fe15a531bc3e5821856d7041) achieves Hit@5 = 0.92156 (25,481/27,650, +0.03156 over the paper's 0.89, +0.02656 over 0.895, and +0.04456 over MBERT+Akk), MRR = 0.85593 (MRR@5 = 0.85071, +0.02593 over the paper's 0.83 and +0.03224 over MBERT+Akk), Hit@1 = 0.80098 (22,147/27,650), and Hit@10 = 0.94517 (26,134/27,650) with a 10,000/10,000 (100.00%, p = 0.0001) paired bootstrap win rate, simultaneously beating both the paper and the reproduced baseline on [MASK]-only positions (N = 22,205: Hit@5 = 0.91263 vs 0.86463, MRR = 0.84015 vs 0.80587), on the 25,957 non-missing subset (Hit@5 = 0.91729 vs 0.87032, MRR = 0.85139 vs 0.81856), on the 21,459 single-token whole-word subset (Hit@5 = 0.91356 vs 0.86770, MRR = 0.84790 vs 0.81827), on all 27,220 whole-word units (Hit@5 = 0.92223 vs 0.87777, MRR = 0.85760 vs 0.82628), on [MASK]-only whole-word units (N = 21,935: Hit@5 = 0.91329 vs 0.86560, MRR = 0.84163 vs 0.80842), under 100% [MASK] replacement (Hit@5 = 0.92007, MRR = 0.84737), with the zero-neural-parameter symbolic engine CLSS-C-v3 on Hit@5 (Hit@5 = 0.89638, MRR = 0.82480), across all Q-composition and shared-witness deduplicated subsets (e.g., N = 23,781 excluding Q-composites and >=6-word Q-witness spans: Hit@5 = 0.92162 vs 0.88239, MRR = 0.85482 vs 0.82842), and across the Table 2 genre subsets Lexical (MRR = 0.86091 vs 0.69, Hit@5 = 0.92920 vs 0.85), Astrological Report (MRR = 0.86704 vs 0.81, Hit@5 = 0.92527 vs 0.88), and Royal or Monumental (MRR = 0.90375 vs 0.84, Hit@5 = 0.93785 vs 0.90), thereby satisfying the full success criterion and partial win p1.

---

## 1. Artifact Integrity and SHA-256 Verification

All shipped package artifacts were independently hashed and checked against `SHA256SUMS` and `object/akkadian_audit_manifest.json` (`135,817` bytes, `sha256: 85b52d7c8093065a051cb06fb6306684d9f69c6f719f246bc6c13ae56d655ee9`):

| Artifact | Bytes | Verified SHA-256 | Status |
|---|---:|---|---|
| `object/akkadian_audit_manifest.json` | `135,817` | `85b52d7c8093065a051cb06fb6306684d9f69c6f719f246bc6c13ae56d655ee9` | Exact match |
| `object/akkadian_predictions_part1.csv` | `881,312` | `674fa60f65097b553aaa1fd8e8f946a7e1f8544eebf344447f5fa262dbfbd91d` | Exact match |
| `object/akkadian_predictions_part2.csv` | `885,457` | `7bd071b2de004066cf47d95b0b2ec23ed43b8b4e3c66d4524fc4cbd3c604a9ca` | Exact match |
| `object/akkadian_predictions_part3.csv` | `891,053` | `d57a42df831d4d1615b39ac38dac9dae70aed739a1535ab45851813cfaa6838b` | Exact match |
| `object/akkadian_predictions_part4.csv` | `852,229` | `9af89e1e184092e5d46c3fea2ff464891a332dbcf6f55b84a70a7674aa9b5aed` | Exact match |
| `object/test_tensors_recipe.md` | `2,923` | `ecabe4b801fa6214d1f50f95943488318a5373722ce11b5617a2ee3f5eac18a4` | Exact match |
| `how-we-built-it/clss_akk_engine_v3.c` | `36,049` | `af810ea742cfb86033065e2875781354670f4cb6fe15a531bc3e5821856d7041` | Exact match |
| `how-we-built-it/train_mbert_akk_fast.py` | `13,223` | `fe91325f47484745e9a08986390899096c9ec2c0011ffefc44ee25e6893017fa` | Exact match |
| `how-we-built-it/author_checker_akkadian.py` | `13,796` | `4d78aff7ae90b78fbc3bbf15079a723f23d8e5b8a10d8b7d0ebe32570db80787` | Exact match |
| `verify-it-yourself/check_akkadian_package.py` | `9,338` | `571c93d25dedb8b3264c0bc2697f123e1081c1eff040786db104d2d444777cc3` | Exact match |

---

## 2. Clause-by-Clause Audit of the Success Criterion and Partial Win `p1`

### Clause (1): Released `SLAB-NLP/Akk` Split, Zero Test-Train Leakage, and Deterministic Seed=42 Masking
- **Corpus and Split (`SEED = 2`):** The released `SLAB-NLP/Akk` split contains `N_train = 18,568` training documents (`5,412,259` valid training tokens across `V = 1,875` active Akkadian vocabulary IDs) and `N_test = 1,875` non-empty unique test documents (`bert_test_strict_1875.txt`, documented in `object/test_tensors_recipe.md`).
- **Pre-Training Mask Note:** `how-we-built-it/PREREG.md` (`2026-10-21T16:50:00Z`) was written locally prior to training and was **not** published in a separate public commit or PR before training; it first appeared publicly in this PR together with the results.
- **Collator Breakdown (`COLLATOR_80_10_10`):** In `SLAB-NLP/Akk/akkadian_bert/evaluate_bert.py` (`eval_compute_metrics` lines 251–281 and `compute_mrr_and_all_hit_ks` lines 305–323), `Trainer.evaluate()` applies `DataCollatorForLanguageModelingAkkadian` (`data_collators_bert.py` lines 68–81: 80% `[MASK]`, 10% random token, 10% unchanged token) and scores all `masked_indices = pred.label_ids != -100` (`N = 27,650`). Consequently, the upstream repository's evaluation **does** score the 10% kept-token positions (`N = 2,723`), along with `N = 22,205` `[MASK]`-only positions (`corrupted_input_id == 103`) and `N = 2,722` random-token positions.

### Clause (2): Reproduced `MBERT+Akk` Baseline Inside `[0.87, 0.91]`
- Rescoring `object/akkadian_predictions_part1..4.csv` directly confirms:
  - **All `27,650` frozen positions (`COLLATOR_80_10_10`):** `Hit@5 = 0.87700` (`24,249 / 27,650`), `MRR = 0.82369` (`MRR@5 = 0.81617`), `Hit@1 = 0.77693` (`21,482 / 27,650`), `Hit@10 = 0.90901` (`25,134 / 27,650`).
  - **`[MASK]`-only positions (`N = 22,205`, `corrupted_input_id == 103`):** `Hit@5 = 0.86463` (`19,199 / 22,205`), `MRR = 0.80587` (`MRR@5 = 0.79761`), `Hit@1 = 0.75433` (`16,750 / 22,205`), `Hit@10 = 0.89948` (`19,973 / 22,205`).
  - **Non-missing `25,957` positions (`label_id not in {4, 5}`, directly from CSVs):** `Hit@5 = 0.87032` (`22,591 / 25,957`, inside `[0.87, 0.91]`; `0.87152` = `22,622 / 25,957` when missing-sign candidate IDs `{4, 5, 17}` are also suppressed from top-128 logits), `MRR = 0.81856` (`MRR@5 = 0.81089`), `Hit@1 = 0.77170` (`20,031 / 25,957`), `Hit@10 = 0.90361` (`23,455 / 25,957`).
  - **Single-token whole words (`N = 21,459`, `is_single_word == 1`, directly from CSVs):** `Hit@5 = 0.86770` (`18,620 / 21,459`; `0.86905` = `18,649 / 21,459` with missing-sign candidate suppression), `MRR = 0.81827` (`MRR@5 = 0.81039`), `Hit@1 = 0.77361` (`16,601 / 21,459`), `Hit@10 = 0.90018` (`19,317 / 21,459`).
  - **All whole-word units (`N = 27,220` words with $\ge 1$ masked token, requiring all masked tokens in the word to be hit):** `Hit@5 = 0.87777` (`23,893 / 27,220`), `MRR = 0.82628`, `Hit@1 = 0.77858` (`21,193 / 27,220`), `Hit@10 = 0.90970` (`24,762 / 27,220`).

### Clause (3): `CLSS-Akk-v3` Beats Both Paper and Reproduced Baseline Across All Subsets and Regimes

| Evaluation Regime / Subset | Positions ($N$) | Model | `MRR` (top-100) | `MRR@5` | `Hit@1` | `Hit@5` | `Hit@10` |
|---|---:|---|---:|---:|---:|---:|---:|
| Published Paper (Lazar et al. 2021) | ~20% split | `MBERT+Akk` (Paper) | `0.83000` | — | — | `0.89000` (`0.895`) | `0.92000` |
| All Frozen Positions (`COLLATOR_80_10_10`) | `27,650` | `MBERT+Akk` Baseline | `0.82369` | `0.81617` | `0.77693` (`21,482`) | `0.87700` (`24,249`) | `0.90901` (`25,134`) |
| All Frozen Positions (`COLLATOR_80_10_10`) | `27,650` | `CLSS-C-v3` Pure (`0` Neural) | `0.82480` | `0.81807` | `0.76470` (`21,144`) | **`0.89638`** (`24,785`) | **`0.92705`** (`25,633`) |
| All Frozen Positions (`100%_MASK`) | `27,650` | `CLSS-Akk-v3` (`100%_MASK`) | **`0.84737`** | **`0.84205`** | `0.78684` (`21,756`) | **`0.92007`** (`25,440`) | **`0.94409`** (`26,104`) |
| All Frozen Positions (`COLLATOR_80_10_10`) | `27,650` | **`CLSS-Akk-v3` Full** | **`0.85593`** | **`0.85071`** | **`0.80098`** (`22,147`) | **`0.92156`** (`25,481`) | **`0.94517`** (`26,134`) |
| `[MASK]`-Only Positions (`input_id == 103`) | `22,205` | `MBERT+Akk` Baseline | `0.80587` | `0.79761` | `0.75433` (`16,750`) | `0.86463` (`19,199`) | `0.89948` (`19,973`) |
| `[MASK]`-Only Positions (`input_id == 103`) | `22,205` | **`CLSS-Akk-v3` Full** | **`0.84015`** | **`0.83426`** | **`0.77924`** (`17,303`) | **`0.91263`** (`20,265`) | **`0.93943`** (`20,860`) |
| Non-Missing Subset (`label not in {4,5}`, raw CSV) | `25,957` | `MBERT+Akk` Baseline | `0.81856` | `0.81089` | `0.77170` (`20,031`) | `0.87032` (`22,591`) | `0.90361` (`23,455`) |
| Non-Missing Subset (`label not in {4,5}`, raw CSV) | `25,957` | **`CLSS-Akk-v3` Full** | **`0.85139`** | **`0.84599`** | **`0.79593`** (`20,660`) | **`0.91729`** (`23,810`) | **`0.94156`** (`24,440`) |
| Single-Token Whole Words (`is_single_word == 1`, raw CSV) | `21,459` | `MBERT+Akk` Baseline | `0.81827` | `0.81039` | `0.77361` (`16,601`) | `0.86770` (`18,620`) | `0.90018` (`19,317`) |
| Single-Token Whole Words (`is_single_word == 1`, raw CSV) | `21,459` | **`CLSS-Akk-v3` Full** | **`0.84790`** | **`0.84229`** | **`0.79244`** (`17,005`) | **`0.91356`** (`19,604`) | **`0.93849`** (`20,139`) |
| All Whole-Word Units (all masked tokens hit) | `27,220` | `MBERT+Akk` Baseline | `0.82628` | `0.81887` | `0.77858` (`21,193`) | `0.87777` (`23,893`) | `0.90970` (`24,762`) |
| All Whole-Word Units (all masked tokens hit) | `27,220` | **`CLSS-Akk-v3` Full** | **`0.85760`** | **`0.85245`** | **`0.80180`** (`21,825`) | **`0.92223`** (`25,103`) | **`0.94537`** (`25,733`) |
| `[MASK]`-Only Whole-Word Units | `21,935` | `MBERT+Akk` Baseline | `0.80842` | `0.80025` | `0.75582` (`16,579`) | `0.86560` (`18,987`) | `0.90034` (`19,749`) |
| `[MASK]`-Only Whole-Word Units | `21,935` | **`CLSS-Akk-v3` Full** | **`0.84163`** | **`0.83579`** | **`0.77967`** (`17,102`) | **`0.91329`** (`20,033`) | **`0.93982`** (`20,615`) |
| Excl. `46` `Q`-Composite Docs (`1,829` P/X docs) | `27,122` | `MBERT+Akk` Baseline | `0.82518` | `0.81769` | `0.77845` (`21,113`) | `0.87844` (`23,825`) | `0.91048` (`24,694`) |
| Excl. `46` `Q`-Composite Docs (`1,829` P/X docs) | `27,122` | **`CLSS-Akk-v3` Full** | **`0.85618`** | **`0.85094`** | **`0.80086`** (`21,721`) | **`0.92235`** (`25,016`) | **`0.94558`** (`25,646`) |
| Excl. `242` `Q`-Docs & $\ge 6$-Word `Q`-Witness Docs (`1,633` docs) | `23,781` | `MBERT+Akk` Baseline | `0.82842` | `0.82112` | `0.78193` (`18,595`) | `0.88239` (`20,984`) | `0.91401` (`21,736`) |
| Excl. `242` `Q`-Docs & $\ge 6$-Word `Q`-Witness Docs (`1,633` docs) | `23,781` | **`CLSS-Akk-v3` Full** | **`0.85482`** | **`0.84950`** | **`0.79959`** (`19,015`) | **`0.92162`** (`21,917`) | **`0.94512`** (`22,476`) |
| Excl. `530` Docs w/ Any $\ge 10$-Word Train Overlap (`1,345` docs) | `18,628` | `MBERT+Akk` Baseline | `0.81456` | `0.80657` | `0.76541` (`14,258`) | `0.86885` (`16,185`) | `0.90321` (`16,825`) |
| Excl. `530` Docs w/ Any $\ge 10$-Word Train Overlap (`1,345` docs) | `18,628` | **`CLSS-Akk-v3` Full** | **`0.83410`** | **`0.82807`** | **`0.77464`** (`14,430`) | **`0.90836`** (`16,921`) | **`0.93515`** (`17,420`) |

---

## 3. Null Models and Negative Controls

1. **400 Random Label-Permutation Controls (`N = 27,650`, `rng = np.random.default_rng(0)`):**
   - Permuting the `27,650` empirical ground-truth `label_id` values directly from `object/akkadian_predictions_part1..4.csv` with `np.random.default_rng(0)` against the frozen `CLSS-Akk-v3` top-5 predictions yields `mean Hit@5 = 0.24852 +/- 0.00178` (`median = 0.24846`, `IQR = 0.00260`, `best_control = 0.25378` vs real `0.92156`, $z = +378.11\sigma$) and `mean MRR@5 = 0.14616 +/- 0.00130` (`median = 0.14617`, `IQR = 0.00169`, `best_control = 0.15072` vs real `MRR@5 = 0.85071`, $z = +541.96\sigma$).
2. **Training-Corpus Unigram Frequency Baselines (`N = 27,650`):**
   - Predicting the global most frequent training tokens yields `Hit@1 = 0.20644`, `Hit@5 = 0.44658`, `MRR = 0.32166` (`MRR@5 = 0.30707`) when punctuation (`-`, `.`) and missing-sign tokens are included, and `Hit@1 = 0.02297`, `Hit@5 = 0.06322`, `MRR = 0.04880` (`MRR@5 = 0.03605`) when punctuation and missing-sign tokens are excluded.

---

## 4. Verdict

Every clause of the success criterion and partial win `p1` is independently verified from the shipped prediction CSVs and audit manifest.

pass: true
