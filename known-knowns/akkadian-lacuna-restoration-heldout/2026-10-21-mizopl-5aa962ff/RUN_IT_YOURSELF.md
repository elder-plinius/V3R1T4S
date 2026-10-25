# Run It Yourself (`2026-10-21-mizopl-5aa962ff`)

## 1. Verify the Saved Claim Objects (`< 1` second)

From this package folder (`2026-10-21-mizopl-5aa962ff/`), run:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```text
[1/5] Object SHA-256 digests and byte sizes verified (6/6 files).
[2/5] Verified 27,650 frozen positions (22,205 [MASK]-only, 2,723 kept-token, 2,722 random-token; 0 mismatches).
[3/5] Verified all (MBERT=0.87700, CLSS=0.92156), [MASK]-only (0.86463 vs 0.91263), single-word (0.86770 vs 0.91356), whole-word (0.87777 vs 0.92223), and Q-filtered (0.88239 vs 0.92162) subsets.
[4/5] Verified Partial Win p1 (> +0.01 overall margin and Table 2 genre subsets Lexical, Astrological Report, Royal or Monumental).
[5/5] Verified 400 label-permutation null controls (best_control Hit@5 = 0.25378 << real = 0.92156).
PASS
```

## 2. Rebuild the Tokenized Test Tensors and Models from Upstream `SLAB-NLP/Akk`

- See `object/test_tensors_recipe.md` for the exact regeneration recipe and SHA-256 digests of `bert_test_strict_1875.txt` (`sha256: 65e7fe8a338048e3a373f0061bbf435154e4e2a49845513c8074abd48fa9fd4c`) and `frozen_test_tensors_seed42.npz` (`sha256: 8033d870bd9d8787627690fc26771693a6acc112be17c7d94f204ed4a9654ec4`) from `https://github.com/SLAB-NLP/Akk` (commit `dfd2a66d4305cf36981e4fd3fde823a5020161dd`).
- The full C engine (`how-we-built-it/clss_akk_engine_v3.c`), PyTorch `MBERT+Akk` baseline training script (`how-we-built-it/train_mbert_akk_fast.py`), and upstream rebuild verifier (`how-we-built-it/author_checker_akkadian.py`) are included in `how-we-built-it/`.
