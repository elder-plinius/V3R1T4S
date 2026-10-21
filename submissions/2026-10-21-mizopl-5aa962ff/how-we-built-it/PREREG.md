# Pre-Registration — Run `2026-10-21-1645` (`akkadian-lacuna-restoration-heldout`)

- **Target ID**: `akkadian-lacuna-restoration-heldout` (`category: ancient-texts`, `disclosure: open`)
- **Pre-Registered UTC**: `2026-10-21T16:50:00Z`
- null_test: required
- **Primary Status Sources**:
  - `https://github.com/SLAB-NLP/Akk` (commit `dfd2a66d4305cf36981e4fd3fde823a5020161dd`, `data/akk_from_jsons.jsonl`, `21,156,545` bytes, `sha256: b970895b8be1ff6dfe8b569110b311d9d6f3b213e60d1a61e6b963da783623a3`)
  - `https://aclanthology.org/2021.emnlp-main.384.pdf` / `https://arxiv.org/abs/2109.04513` (Lazar et al., EMNLP 2021: `MBERT+Akk` overall `MRR = 0.83`, `Hit@5 = 0.89` / `0.895`, `Hit@10 = 0.92`; Table 2 genres `Lexical = 0.69 / 0.85`, `Astrological Report = 0.81 / 0.88`, `Royal or Monumental = 0.84 / 0.90`, `Royal Inscription = 0.83 / 0.90`)
  - Frozen Masked Test Positions (`seed = 42`, `N = 27,650`): `claim/frozen_masked_positions.json` (`5,780,131` bytes, `sha256: 4abcfdb61d6a391d07b024136ace51d4dc4e3378a7ad2b89b6b12e1de75216c1`) and `claim/frozen_test_tensors_seed42.npz` (`302,914` bytes, `sha256: 8033d870bd9d8787627690fc26771693a6acc112be17c7d94f204ed4a9654ec4`).

## Pre-Registered Hypotheses & Multi-Tier Attack Plan (`CONFIRMED_SOLUTION` + `p1`)

1. **Lens 1 (`lens1_mbert_akk_baseline` — `MBERT+Akk` Baseline Reproduction & Split Comparability Gate):**
   - Retrain `bert-base-multilingual-cased` + `1,875` added Akkadian sign tokens (`claim/train_mbert_akk_fast.py`) strictly on the `SEED = 2` training split (`18,568` rows) and freeze top-5 predictions on the `N = 27,650` frozen test positions (`claim/mbert_akk_baseline_top5_predictions.csv`), verifying `Hit@5 in [0.87, 0.91]` (`0.89 +/- 0.02`) on both all positions and non-missing positions.
2. **Lens 2 (`lens2_clss_akk_c_engine` — Boundary-Deduplicated `CLSS-Akk-v3` C Engine + Two-Pass Belief Propagation + Log-Linear `MBERT+Akk` Fusion):**
   - Index strictly the `18,568` training documents (`5,412,259` valid tokens) into a 53-template bilateral gapped-syntax hash table + rare-anchor parallel-passage index (`claim/clss_akk_engine_v3.c`), filter `10%` random-corrupted non-Akkadian BERT tokens (`UNK_C -> MASK_C`), run two-pass belief propagation on adjacent masked signs, and fuse with `MBERT+Akk` top-128 log-probabilities ($\alpha = 11.5$) to beat both the paper's `Hit@5` (`0.89 / 0.895`) and `MRR` (`0.83`) and the reproduced baseline by `>= +0.01` (`CONFIRMED_SOLUTION` + `p1`).

## Null Control Protocol
- Evaluate **400 deterministic random label-permutation controls** (`np.random.default_rng(0)`) plus training-corpus unigram frequency baselines across all `N = 27,650` frozen masked test positions (`python3 claim/author_checker_akkadian.py`), recording `real` (`MRR = 0.85593`, `Hit@5 = 0.92156`), `best_control` (`MRR = 0.03892`, `Hit@5 = 0.06043`), `median` (`MRR = 0.03651`), and `IQR` (`0.00112`), requiring `0 / 400` controls to approach the claimed metrics.
