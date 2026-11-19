# Run It Yourself (`2026-10-30-mizopl-akkfresh`)

## 1. Verify the Saved Claim Objects (`< 1` second)

From this package folder (`2026-10-30-mizopl-akkfresh/`), run:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```text
[1/5] Object SHA-256 digests and byte sizes verified (10/10 files).
[2/5] Verified 38,151 frozen positions (30,545 [MASK]-only, 3,833 kept-token, 3,773 random-token; 0 mismatches).
[3/5] Verified all (MBERT=0.88158, CLSS=0.91421), [MASK]-only (0.86855 vs 0.90506), single-word (0.91944 vs 0.93514), whole-word (0.87594 vs 0.90963), and D8/Q-filtered (0.88143 vs 0.91411) subsets.
[4/5] Verified Full Win (Clause 1 & 2) and Partial Win p1 (> +0.01 overall margin and Table 2 genres Lexical, Astrological Report, Royal Inscription).
[5/5] Verified 400 label-permutation null controls (best_control Hit@5 = 0.21918 << real = 0.91421).
PASS
```

## 2. Rebuild the Pre-Registered Split, Tokenizer, Models, and Predictions from Upstream `SLAB-NLP/Akk`

- See `object/test_tensors_recipe.md` and `how-we-built-it/PREREG.md` for the exact chronological pre-registration commits pushed to GitHub before training:
  1. **Stage I Pre-Registration Commit (`e26fa2cb33964bfe549770d311120ba1f804d81f`, `2026-10-30T08:24:24Z`)**: Published `object/prereg_split_and_mask_manifest.json` (`sha256: 06ba9a82589d8eeb31433480b275e4821df574938d1104ea607558cc88104877`) and `how-we-built-it/stage1_freeze_split_and_masks.py` before any model training started.
  2. **Stage II Frozen `MBERT+Akk` Baseline Commit (`00db937`, `2026-10-30T14:09Z`)**: Published `object/baseline_frozen_manifest.json` (`mbert_akk_baseline_top5_predictions.csv` `sha256: cbc4e1803b1933d03c7162c190ae5c077b0cb323f41d82d1016e0c38cc2a4c7e`, `Hit@5 = 0.88158`, `MRR = 0.83160`) before Stage III `CLSS-Akk-v3` ran.
- All Stage I, II, and III build scripts (`stage1_freeze_split_and_masks.py`, `train_mbert_akk_baseline.py`, `continue_mbert_akk_baseline.py`, `eval_mbert_baseline_frozen.py`, `build_corpus_bin.py`, `clss_akk_engine_v3.c`, and `stage3_run_clss_and_export.py`) are shipped in `how-we-built-it/`.
