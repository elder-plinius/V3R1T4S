# Deterministic Regeneration Recipe for Tokenized Split & Frozen Masked Tensors (`SEED = 20261031`)

This document records the exact 100% deterministic command and cryptographic SHA-256 digests to regenerate the composition-disjoint `SLAB-NLP/Akk` split, the 99-slot `MBERT+Akk` tokenizer vocabulary, and the `N = 38,151` frozen masked test positions from upstream `https://github.com/SLAB-NLP/Akk` (commit `dfd2a66d4305cf36981e4fd3fde823a5020161dd`).

## 1. Chronological Pre-Registration Commit Before Training

The split, tokenizer vocabulary, and frozen masked test positions (`SEED = 20261031`, `torch.manual_seed(20261031)`) were generated and pushed to GitHub **before** any model training (`MBERT+Akk` or `CLSS-Akk-v3`) began:

- **Pre-Registration Commit (`Stage I`)**: [`e26fa2cb33964bfe549770d311120ba1f804d81f`](https://github.com/mizopl/V3R1T4S/commit/e26fa2cb33964bfe549770d311120ba1f804d81f) (`2026-10-30T08:24:24Z` on `mizopl/V3R1T4S` branch `submission/2026-10-30-mizopl-akkfresh`)
- **Frozen `MBERT+Akk` Baseline Commit (`Stage II`, before `CLSS-Akk-v3`)**: [`00db937`](https://github.com/mizopl/V3R1T4S/commit/00db937) (`2026-10-30T14:09Z` on `mizopl/V3R1T4S` branch `submission/2026-10-30-mizopl-akkfresh`)

## 2. Exact Regeneration Commands

```sh
git clone https://github.com/SLAB-NLP/Akk.git akk_repo
git -C akk_repo checkout dfd2a66d4305cf36981e4fd3fde823a5020161dd
AKK_WORK_DIR=. python3 how-we-built-it/stage1_freeze_split_and_masks.py
```

## 3. Cryptographic SHA-256 Digests of Generated Split, Tokenizer, and Tensors

| Artifact | Bytes | SHA-256 Digest | Description |
|---|---:|---|---|
| `akk_repo/data/akk_from_jsons.jsonl` | `21,156,545` | `b970895b8be1ff6dfe8b569110b311d9d6f3b213e60d1a61e6b963da783623a3` | Frozen upstream ORACC Akkadian corpus (`23,211` rows, `14,430` unique `id_text`) |
| `bert_train_clean.txt` | `4,724,183` | `4905a304a059533aa39e2204cef1bc0c16ba77e4dc9a701d312db09a80cf4f91` | `9,221` composition-disjoint training documents (`707,197` words; `0` shared `id_text`, `0` shared $\ge 15$-word blocks, max pairwise 8-gram share `0.195122 < 0.20`) |
| `bert_test_heldout.txt` | `1,636,084` | `2813b573c52285d0ed636b41b6e725df66feeb424966653ebcd862e5f69eef14` | `2,886` held-out 20% test documents (`SEED = 20261031`) |
| `main_tokenizer/vocab.txt` | `995,780` | `00bd3cdcd37cd9ad218eb872e61bef64bc19ec0b81d4aedea00c2356266bee3f` | `MBERT+Akk` `vocab.txt` (`119,547` tokens) with 99 top training tokens injected into `[unused1]..[unused99]` |
| `frozen_masked_positions.csv` | `1,401,574` | `5af36f37415efc204cde20cf4be2259abc9abaea88dc31be9b37b0ba72ca325f` | All `N = 38,151` frozen masked word-piece positions (`30,545` `[MASK]`, `3,833` unchanged, `3,773` random) |
| `frozen_test_tensors_seed20261031.npz` | `1,303,754` | `f060ec0879152b9ab5fa95f9e9db126674d4cce9e6c7abcb1857843c6f8d4234` | Frozen `input_ids`, `labels`, and `attention_mask` tensors (`shape = (2886, 128)`) at `torch.manual_seed(20261031)` |
| `object/prereg_split_and_mask_manifest.json` | `190,476` | `06ba9a82589d8eeb31433480b275e4821df574938d1104ea607558cc88104877` | Complete pre-registration manifest committed in `e26fa2cb33964bfe549770d311120ba1f804d81f` |
| `object/baseline_frozen_manifest.json` | `979` | `b30998900a380114736b025b5e1fc333754af49e59eafae456c8cddb358d82c4` | Stage II frozen baseline prediction manifest committed in `00db937` (`mbert_akk_baseline_top5_predictions.csv` `sha256: cbc4e1803b1933d03c7162c190ae5c077b0cb323f41d82d1016e0c38cc2a4c7e`) |
