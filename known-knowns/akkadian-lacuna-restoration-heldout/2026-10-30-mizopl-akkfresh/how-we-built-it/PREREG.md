# Pre-Registration — Run `2026-10-30-mizopl-akkfresh` (`akkadian-lacuna-restoration-heldout`, `SEED = 20261031`)

- **Target ID**: `akkadian-lacuna-restoration-heldout` (`category: ancient-texts`, `disclosure: open`)
- **Pre-Registration Commit Protocol**: Committed and pushed to GitHub (`origin/submission/2026-10-30-mizopl-akkfresh` on `mizopl/V3R1T4S`) **BEFORE** any model (`MBERT+Akk` baseline or `CLSS-Akk`) is trained on this split.
- **null_test**: required
- **Primary Status Sources**:
  - `https://github.com/SLAB-NLP/Akk` (commit `dfd2a66d4305cf36981e4fd3fde823a5020161dd`, `data/akk_from_jsons.jsonl`, `21,156,545` bytes, `sha256: b970895b8be1ff6dfe8b569110b311d9d6f3b213e60d1a61e6b963da783623a3`)
  - `https://aclanthology.org/2021.emnlp-main.384.pdf` / `https://arxiv.org/abs/2109.04513` (Lazar et al., EMNLP 2021: `MBERT+Akk` overall `MRR = 0.83`, `Hit@5 = 0.89` / `0.895`, `Hit@10 = 0.92`; Table 2 genres `Lexical = 0.69 / 0.85`, `Astrological Report = 0.81 / 0.88`, `Royal or Monumental = 0.84 / 0.90`, `Royal Inscription = 0.83 / 0.90`).

## 1. Frozen Split, Composition-Disjoint Deduplication & Masking Digests (`SEED = 20261031`)

1. **`id_text` Deduplication Before Split**:
   - Raw `data/akk_from_jsons.jsonl` rows: `23,211`
   - Duplicate `id_text` rows removed before splitting: `8,781`
   - Unique `id_text` documents preprocessed with `main_preprocess.py` (`--remove_subscripts --remove_superscripts`, keeping hyphens `-` and `...`, turning `'x'` into `U+1F607` and `'+' -> '-'`, removing `'o'`, `'v'`, and backslash codes): `14,430`
2. **80/20 Split by Text (`train_test_split(test_size=0.2, random_state=20261031)`)**:
   - Initial 80% training split: `11,544` documents
   - Initial 20% test split: **`2,886` documents** (`0` empty records in test; the single empty record `P342168` lands in `train_raw` and is removed).
3. **Composition & Parallel-Exemplar Disjointness Filter on Training Set**:
   - Exact or empty `bert_input` matches with test removed from train: `23`
   - Training documents sharing $\ge 20\%$ of distinct word 8-grams with any test document (in either direction: `c / len(test_8g) >= 0.20` or `c / len(train_8g) >= 0.20`, catching composite/witness pairs such as `P229143` vs `Q002268` at `83.3%` 8-gram overlap) removed: `1,704`
   - Training documents sharing any contiguous block of $\ge 15$ words with any test document removed: `596`
   - **Total training documents removed for composition/parallel-exemplar disjointness**: `2,323`
   - **Final clean, composition-disjoint training set (`akk_train_clean.jsonl` / `bert_train_clean.txt`)**: **`9,221` documents (`707,197` words)** (`0` shared `id_text`, `0` shared $\ge 15$-word blocks, and maximum pairwise word 8-gram share `0.195122 < 0.20` across all `9,221 x 2,886` document pairs).
4. **Tokenizer (`MBERT+Akk`, 99 Injected Tokens Built Strictly from `bert_train_clean.txt`)**:
   - Built via `train_tokenizer(".", 990, "bert_train_clean.txt")` + `inject_new_tokens_to_tokenizer` into `bert-base-multilingual-cased` free slots `1..99` (`U+1F607` at slot ID `4`).
   - Resulting `main_tokenizer/vocab.txt` SHA-256: **`00bd3cdcd37cd9ad218eb872e61bef64bc19ec0b81d4aedea00c2356266bee3f`** (all 99 injected tokens listed in `object/prereg_split_and_mask_manifest.json`).
5. **Frozen Token-Level Masked Positions (`ORACCDataset(block_size=128)` + `DataCollatorForLanguageModelingAkkadian(mlm_probability=0.15)` at `torch.manual_seed(20261031)`)**:
   - Total masked word-piece positions (`label_ids != -100`, never masking special tokens or `U+1F607`): **`N = 38,151`** across `2,886` test documents (`30,545` shown as `[MASK]`, `3,833` shown unchanged, `3,773` shown as a random token).
   - `frozen_masked_positions.csv` (`1,273,281` bytes, recording `(mask_idx, doc_idx, id_text, token_pos, shown_input_id, shown_token_str)` for every masked position) SHA-256: **`5af36f37415efc204cde20cf4be2259abc9abaea88dc31be9b37b0ba72ca325f`**
   - `frozen_test_tensors_seed20261031.npz` (`452,760` bytes) SHA-256: **`f060ec0879152b9ab5fa95f9e9db126674d4cce9e6c7abcb1857843c6f8d4234`**
   - `object/prereg_split_and_mask_manifest.json` SHA-256: **`06ba9a82589d8eeb31433480b275e4821df574938d1104ea607558cc88104877`**
   - `bert_train_clean.txt` SHA-256: **`4905a304a059533aa39e2204cef1bc0c16ba77e4dc9a701d312db09a80cf4f91`**
   - `bert_test_heldout.txt` SHA-256: **`2813b573c52285d0ed636b41b6e725df66feeb424966653ebcd862e5f69eef14`**

## 2. Pre-Registered Attack Plan

1. **Clause (1) — Reproduced `MBERT+Akk` Baseline with Repository Code & Default Settings (`Zero Test Reference During Training`)**:
   - Train `MBERT+Akk` (`AutoModelForMaskedLM.from_pretrained("bert-base-multilingual-cased")` with full `119,547` vocabulary and `main_tokenizer`) using the repository's `ORACCDataset(block_size=128)` + `DataCollatorForLanguageModelingAkkadian(mlm_probability=0.15)` and default optimizer hyperparameters (`lr = 5e-5`, `weight_decay = 0.0`, `adam_beta1 = 0.9`, `adam_beta2 = 0.999`, `adam_epsilon = 1e-8`, `max_grad_norm = 1.0`, linear schedule) strictly on `bert_train_clean.txt` (`9,221` documents), with **zero reference to any test file or test tensor in the training script**.
   - After training finishes and the final model checkpoint is saved, evaluate once on the frozen `N = 38,151` masked positions (`eval_frozen_test.py`), freeze `mbert_akk_baseline_top5.csv` (hash), and verify `Hit@5 in [0.87, 0.91]`.
2. **Clause (2) — `CLSS-Akk-v3` Trained Strictly on `bert_train_clean.txt`**:
   - Build the training index strictly from `bert_train_clean.txt` (`9,221` documents, zero test labels in vocabulary construction), fuse with the trained `MBERT+Akk` log-probabilities in `clss_akk_engine_v3.c`, freeze `clss_akk_v3_top5.csv` (hash) before scoring, and verify that `CLSS-Akk-v3` beats both the paper (`Hit@5 > 0.895`, `MRR > 0.83`) and the reproduced baseline on the identical `38,151` masked positions.
3. **Null Control Protocol**:
   - Evaluate `400` deterministic label-permutation null controls (`np.random.default_rng(0)`) across all `N = 38,151` masked positions.
