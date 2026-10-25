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
[3/5] Masked-sign top-1 restoration accuracies and 10,000-resample paired bootstraps (vs KN3-Left & SIGIL p = 0.0001 across all strata; vs KN3-Bidir p = 0.0001 pooled, 0.0019 Mohenjo-daro, 0.0147 Harappa; vs KN3-BlanketF p = 0.0048 pooled, 0.2988 Mohenjo-daro, 0.0188 Harappa) verified.
[4/5] Partial Win p3 verified (30 shared parallel frames vs 10,000-permutation null mean 7.6427, max 23, p = 0.0001 < 0.001).
[5/5] 400 SIGIL matched-null controls verified (best_control = 0.096221 < real = 0.200482).
PASS
```

## 2. Rebuild the Frozen `M77` Model and Post-1977 Evaluation from Upstream Repositories

All upstream corpus files come from **`https://github.com/paragorth/Indus-`** at commit **`d62ec82d58642038640da25a97177d7a1fddc9d9`** (`2026-10-07T13:59:19Z`, branch `claude/indus-script-dictionary-u3dzf8`):

| Upstream File in `paragorth/Indus-` (`d62ec82d...`) | Byte Size | SHA-256 Digest |
|---|---:|---|
| `data/im77/im77_corpus_lines.csv` | `559,170` | `385b82bd6a9629e0ab215af46db84ca0c9ec4f6044a2a2ea58a3c64121f26211` |
| `data/derived/bridge_extended.json` | `2,070` | `ba0949e1e2dd8e9b5d6d3aea70da5ad3c1d213e76a8bbd38d993814068d7541c` |
| `data/derived/merged-corpus-canonical.v2.json` | `2,315,998` | `b68c950bee1b7ded02267c0717b5e7e5d8730b7f72de6f46d4dea086ac9e7a5f` |
| `data/derived/dark/loop24_pairs.json` | `1,919,320` | `638027b53fdffc4b915cb61aa683326cd1c312b5018eac65c9c8b11e1f2efed2` |
| `data/derived/identity-directory.json` | `82,012` | `fd5d42b65ec96ff248bbce3ffee4352bab452ff5faa8e4e4084c87a76932c03f` |

The full training and evaluation scripts are included in `how-we-built-it/`:
- `how-we-built-it/train_and_freeze_m77_model.py`: Reads only `data/im77/im77_corpus_lines.csv` (`sha256: 385b82bd6a9629e0ab215af46db84ca0c9ec4f6044a2a2ea58a3c64121f26211`) and `data/derived/bridge_extended.json` (`sha256: ba0949e1e2dd8e9b5d6d3aea70da5ad3c1d213e76a8bbd38d993814068d7541c`) from `paragorth/Indus-`, induces `32` Ward hierarchical distributional sign-equivalence classes (`C0..C31`), runs 5-fold cross-validation on the `2,165` deduplicated `M77` sequences (`9,652` tokens), and freezes `object/m77_frozen_structural_model.json`.
- `how-we-built-it/evaluate_post1977_heldout.py`: Loads the frozen `object/m77_frozen_structural_model.json` without refitting, applies the post-1977 filter and deduplication cascade on `data/derived/merged-corpus-canonical.v2.json`, `data/derived/dark/loop24_pairs.json`, and `data/derived/identity-directory.json`, and outputs `object/post1977_evaluation_results.json` and `object/post1977_heldout_predictions.csv`.
