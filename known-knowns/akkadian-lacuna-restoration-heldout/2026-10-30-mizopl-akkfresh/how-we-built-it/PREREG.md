# Pre-Registration — Run `2026-10-30-mizopl-akkfresh` (`akkadian-lacuna-restoration-heldout`)

- **Target ID**: `akkadian-lacuna-restoration-heldout` (`category: ancient-texts`, `disclosure: open`)
- **Pre-Registration Commit Protocol**: Committed and pushed to GitHub (`origin/submission/2026-10-30-mizopl-akkfresh` on `mizopl/V3R1T4S`) **BEFORE** any model (`MBERT+Akk` baseline or `CLSS-Akk`) is trained on this split.
- **null_test**: required
- **Primary Status Sources**:
  - `https://github.com/SLAB-NLP/Akk` (commit `dfd2a66d4305cf36981e4fd3fde823a5020161dd`, `data/akk_from_jsons.jsonl`, `21,156,545` bytes, `sha256: b970895b8be1ff6dfe8b569110b311d9d6f3b213e60d1a61e6b963da783623a3`)
  - `https://aclanthology.org/2021.emnlp-main.384.pdf` / `https://arxiv.org/abs/2109.04513` (Lazar et al., EMNLP 2021: `MBERT+Akk` overall `MRR = 0.83`, `Hit@5 = 0.89` / `0.895`, `Hit@10 = 0.92`; Table 2 genres `Lexical = 0.69 / 0.85`, `Astrological Report = 0.81 / 0.88`, `Royal or Monumental = 0.84 / 0.90`, `Royal Inscription = 0.83 / 0.90`).

## 1. Frozen Split, Composition-Disjoint Deduplication & Masking Digests (`SEED = 20261030`)

1. **`id_text` Deduplication Before Split**:
   - Raw `data/akk_from_jsons.jsonl` rows: `23,211`
   - Duplicate `id_text` rows removed before splitting: `8,781`
   - Unique `id_text` documents preprocessed with `main_preprocess.py` (`--remove_subscripts --remove_superscripts`, keeping hyphens `-` and `...`, turning `'x'` into `U+1F607` and `'+' -> '-'`, removing `'o'`, `'v'`, and backslash codes): `14,430`
2. **80/20 Split by Text (`train_test_split(test_size=0.2, random_state=20261030)`)**:
   - Initial 80% training split: `11,544` documents
   - Initial 20% test split: `2,886` documents (`2,885` non-empty documents after `ORACCDataset` drops the single empty document `P342168`).
3. **Strict Composition & Word 8-Gram Disjointness Filter on Training Set**:
   - Exact or empty `bert_input` matches with test removed from train: `23`
   - Training documents sharing `title` or `display_name` in `data/Finished/PreWork/textdata.csv` with any test document removed: `832`
   - Training documents sharing any $\ge 1$ word 8-gram (`bert_input` or normalized `raw_text`) with any test document removed: `3,973`
   - Training documents containing any full short ($< 8$-word) test document as a contiguous word span removed: `333`
   - **Total training documents removed for composition/duplicate disjointness**: `5,161`
   - **Final clean, composition-disjoint training set (`akk_train_clean.jsonl` / `bert_train_clean.txt`)**: **`6,383` documents** (`0` shared `id_text`, `0` shared `textdata.csv` titles/display names, and **`0.00000%` word 8-gram overlap** across all `2,885` test documents).
4. **Tokenizer (`MBERT+Akk`, 99 Injected Tokens Built Strictly from `bert_train_clean.txt`)**:
   - Built via `train_tokenizer(".", 990, "bert_train_clean.txt")` + `inject_new_tokens_to_tokenizer` into `bert-base-multilingual-cased` free slots `1..99` (`U+1F607` at slot ID `4`).
   - Resulting `main_tokenizer/vocab.txt` SHA-256: **`fec4cba72bbee7a92c7d6a3ef115dc2f692e94d7b3f58b0d770a523de94ec7e9`** (all 99 injected tokens listed in `object/prereg_split_and_mask_manifest.json`).
5. **Frozen Token-Level Masked Positions (`ORACCDataset(block_size=128)` + `DataCollatorForLanguageModelingAkkadian(mlm_probability=0.15)` at `torch.manual_seed(20261030)`)**:
   - Total masked word-piece positions (`label_ids != -100`, never masking special tokens or `U+1F607`): **`N = 37,228`** across `2,885` test documents (`29,716` shown as `[MASK]`, `3,723` shown unchanged, `3,789` shown as a random token).
   - `frozen_masked_positions.csv` (`1,243,260` bytes, recording `(mask_idx, doc_idx, id_text, token_pos, shown_input_id, shown_token_str)` for every masked position) SHA-256: **`001ab799bbf9e4e917584ed3ff394b605d0bdce4da1aeb27a7a8d64c47dbc0fb`**
   - `frozen_test_tensors_seed20261030.npz` (`444,867` bytes) SHA-256: **`ac380ccf4759815f20ab8808c73f7c2272f59dba02ffb3e18596212fd3a70fcc`**
   - `object/prereg_split_and_mask_manifest.json` SHA-256: **`1b83b3167feec600fa79c77e3a4fa16d9db73ab64e103372f0d7816523c43ecf`**
   - `bert_train_clean.txt` SHA-256: **`75955a242d792006eb4ad2faceda5ac11e8e5b62d330458c6264fda0dfd445e6`**
   - `bert_test_heldout.txt` SHA-256: **`b1d0e636d4a05f62b172f28245d6d06b1eaa96102c8f43ad3209b4759fa49ccf`**

## 2. Pre-Registered Attack Plan

1. **Clause (1) — Reproduced `MBERT+Akk` Baseline with Repository Code & Default Hyperparameters**:
   - Train `MBERT+Akk` (`bert-base-multilingual-cased` with `main_tokenizer` built above) using the repository's `akkadian_bert/train_bert.py` default hyperparameters (`epochs = 30`, `per_device_train_batch_size = 2`, `gradient_accumulation_steps = 4`, `learning_rate = 5e-5` AdamW default in HuggingFace `TrainingArguments`, `block_size = 128`, `mlm_probability = 0.15`) strictly on `bert_train_clean.txt` (`6,383` documents).
   - Freeze its top-5 predictions on the `N = 37,228` masked positions (`mbert_akk_baseline_top5.csv`), compute and commit its SHA-256 hash, and verify that its token-level `Hit@5` lands within `0.02` of `0.89` (`[0.87, 0.91]`).
2. **Clause (2) — `CLSS-Akk-v3` Trained Strictly on `bert_train_clean.txt`**:
   - Index strictly the `6,383` composition-disjoint training documents into `clss_akk_engine_v3.c` (83 bilateral gapped word-piece templates + 3-gram rare-anchor parallel-passage alignment + two-pass belief propagation + log-linear fusion with the clean-trained `MBERT+Akk` log-probabilities, tuned exclusively on internal training split validation without touching `bert_test_heldout.txt`).
   - Freeze `clss_akk_v3_top5.csv` (hash) before scoring and verify that `CLSS-Akk-v3` beats both the paper (`Hit@5 > 0.895`, `MRR > 0.83`) and the reproduced baseline on the identical `37,228` masked positions.
3. **Null Control Protocol**:
   - Evaluate `400` deterministic label-permutation null controls (`np.random.default_rng(0)`) across all `N = 37,228` masked positions.
