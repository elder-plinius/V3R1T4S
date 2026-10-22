# `<2,5,6>` rank-47 matrix multiplication in 177 additions (was 181 in live table; merged #230 at 179))

## What this is

A straight-line program that multiplies a 2x5 matrix `A` by a 5x6 matrix `B` over the integers using **47 scalar multiplications** (the best known rank for `<2,5,6>`) and **177 additions/subtractions** (`38` on the inputs of `A`, `64` on the inputs of `B`, `75` when assembling the entries of `C`), with all coefficients in `{-1, 0, +1}`. The live table record for `<2,5,6>` at rank 47 in Perminov's `addition_reduced_ZT` collection is **181** additions (`40 + 65 + 76`), and merged pull request [#230](https://github.com/elder-plinius/V3R1T4S/pull/230) reports **179** additions (`38 + 65 + 76`).

| Format | Rank `m` | `U` adds | `V` adds | `W` adds | Total reduced additions |
|---|---:|---:|---:|---:|---:|
| `<2,5,6>` (Perminov live `2x5x6_m47_cr181_fv63_cn332_ZT_reduced.json`) | 47 | 40 | 65 | 76 | **181** |
| `<2,5,6>` (merged PR #230) | 47 | 38 | 65 | 76 | **179** |
| `<2,5,6>` (`object/2x5x6_m47_cr177_ZT_reduced.json`) | 47 | 38 | 64 | 75 | **177** |

## Verify in 5 seconds

```sh
sh verify-it-yourself/run_checks.sh
```

Needs only `python3` (standard library). It checks the file's SHA-256 against `INDEX.csv`, expands the straight-line program, checks all `3600` Brent equations over `Z` and random integer matrix products, confirms every expanded coefficient is in `{-1, 0, 1}`, confirms the reduced addition count is `38 + 64 + 75 = 177`, and checks that flipping one sign makes both checkers fail. Output is in `verify-it-yourself/RECEIPTS.md`.

## Files

- `object/2x5x6_m47_cr177_ZT_reduced.json` — the straight-line program (Perminov JSON layout; output `C` indexed `(k, i)` as in Perminov's files).
- `INDEX.csv` — target id, cell, 177 vs 181, fetch timestamp, file path, sha256.
- `verify-it-yourself/` — two independent stdlib-only checkers (`check_slp.py`, `brent_check.py`), `run_checks.sh`, and `RECEIPTS.md`.
- `the-record-we-beat/README.md` — URLs, UTC timestamps, HTTP codes and SHA-256 hashes of the live sources fetched on 2026-10-17.
- `how-we-built-it/` — walk script (`flip4.py`), helper (`lib.py`, `mk.py`), algebraic DAG exclusive-cone reduction (`dag_cone_collapse.py`), and pre-registration note.
- `HOW_WE_FOUND_IT.md`, `RUN_IT_YOURSELF.md` — short overview and commands.
- `panel/` — outputs of the four review steps (`reproduce.md`, `novelty.md`, `criterion.md`, `gate.md`).
- `SHA256SUMS` — SHA-256 of every file in this folder.

## Not claimed

- No improvement to multiplicative rank (`47` is already the best known rank for `<2,5,6>`).
- No proof that 177 is the minimum possible addition count for `<2,5,6>` at rank 47.
- IACR ePrint 2026/849 (Mårtensson and Stankovski Wagner) could not be read by the panel or maintainers (its PDF is behind an interactive challenge page); the comparison here stands against Perminov's live repository (`181`), the Lille catalogue, and `COVERAGE.md`, and merged PR #230 (`179`).
- Only `<2,5,6>` at rank 47 is claimed here.

## Credits

- **Contributor**: `Zerbytheboss` (GitHub account `HindsightWise` is operated by `Zerbytheboss`; submitted via the V3R1T4S contribution kit).
- **Prior work on the target and tools**:
  - **A. I. Perminov** (Andrew I. Perminov, [arXiv:2512.13365](https://arxiv.org/abs/2512.13365)), [`FastMatrixMultiplication`](https://github.com/dronperminov/FastMatrixMultiplication) (the `2x5x6_m47_cr181_fv63_cn332_ZT_reduced.json` baseline scheme and JSON format) and [`ternary_addition_reducer`](https://github.com/dronperminov/ternary_addition_reducer).
  - **A. Sedoglavic**, [`fmm_digest`](https://github.com/sedoglavic/fmm_digest) and the [Lille FMM table](https://fmm.univ-lille.fr/2x5x6.html).
  - **Solven / `matmulcatalog`**, [`COVERAGE.md`](https://github.com/solven-eu/matmulcatalog).
  - **M. Kauers and J. Moosbauer** (flip-graph method for matrix multiplication schemes, ISSAC 2023), **Boyar and Peralta** (cancellation-guided linear program search), **Bshouty / Kaminski / Kirkpatrick** (transposition principle for linear straight-line programs), and **A. Novikov et al. / AlphaEvolve** (Google DeepMind, May 2025, [arXiv:2506.13131](https://arxiv.org/abs/2506.13131), whom the Lille catalogue cites for the `<2,5,6>` rank-47 bilinear scheme).
