# Run It Yourself (`2026-10-19-mizopl-b40b1ef7`)

## 1. Verify the Saved Claim Objects (`~3` seconds)

From this package folder (`2026-10-19-mizopl-b40b1ef7/`), run:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```text
[1/5] Object SHA-256 digests and byte sizes verified (3/3 files).
[2/5] Chronological disjointness (2,165 M77 vs 999 post-1977 inscriptions, 3,731 tokens) and W740 reading direction (223/231 = 96.54%) verified.
[3/5] Masked-sign top-1 restoration accuracies and 10,000-resample paired bootstraps (p = 0.0001 < 0.001 across Pooled, Mohenjo-daro, Harappa, Dholavira, and Cohort B Strict) verified.
[4/5] Partial Win p3 verified (30 shared parallel frames vs 10,000-permutation null mean 7.6427, max 23, p = 0.0001 < 0.001).
[5/5] 400 SIGIL matched-null controls verified (best_control = 0.096221 < real = 0.200482).
PASS
```

## 2. Rebuild the Frozen `M77` Model and Post-1977 Evaluation from Upstream Repositories

The full training and evaluation scripts are included in `how-we-built-it/`:
- `how-we-built-it/train_and_freeze_m77_model.py`: Reads only `data/im77/im77_corpus_lines.csv` (`sha256: 385b82bd6a9629e0ab215af46db84ca0c9ec4f6044a2a2ea58a3c64121f26211`) and `data/derived/bridge_extended.json` (`sha256: ba0949e1e2dd8e9b5d6d3aea70da5ad3c1d213e76a8bbd38d993814068d7541c`) from the `Indus-` repository, runs 5-fold cross-validation on the `2,165` deduplicated `M77` sequences (`9,652` tokens), and freezes `object/m77_frozen_structural_model.json`.
- `how-we-built-it/evaluate_post1977_heldout.py`: Loads the frozen `m77_frozen_structural_model.json` without refitting, applies the post-1977 filter and deduplication cascade on `data/derived/merged-corpus-canonical.v2.json`, `data/derived/dark/loop24_pairs.json`, and `data/derived/identity-directory.json`, and outputs `object/post1977_evaluation_results.json` and `object/post1977_heldout_predictions.csv`.
