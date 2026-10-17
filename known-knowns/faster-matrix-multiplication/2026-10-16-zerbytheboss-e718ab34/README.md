# `<2,4,7>` rank-45 matrix multiplication in 161 additions (was 174 in live table; open PR #229 at 169; withdrawn PR #11 at 164)

## What this is

A straight-line program that multiplies a 2x4 matrix `A` by a 4x7 matrix `B` over the integers using **45 scalar multiplications** (the best known rank for `<2,4,7>`) and **161 additions/subtractions** (`35` on the inputs of `A`, `58` on the inputs of `B`, `68` when assembling the 14 entries of `C`), with all coefficients in `{-1, 0, +1}`. The live table record for `<2,4,7>` at rank 45 in Perminov's `addition_reduced_ZT` collection is **174** additions (`35 + 69 + 70`), open pull request [#229](https://github.com/elder-plinius/V3R1T4S/pull/229) reports **169** additions, and withdrawn pull request [#11](https://github.com/elder-plinius/V3R1T4S/pull/11) (which maintainers confirmed valid) reports **164** additions.

| Format | Rank `m` | `U` adds | `V` adds | `W` adds | Total reduced additions |
|---|---:|---:|---:|---:|---:|
| `<2,4,7>` (Perminov live `2x4x7_m45_cr174_cn308_ZT_reduced.json`) | 45 | 35 | 69 | 70 | **174** |
| `<2,4,7>` (open PR #229) | 45 | — | — | — | **169** |
| `<2,4,7>` (withdrawn PR #11, verified valid) | 45 | — | — | — | **164** |
| `<2,4,7>` (`object/2x4x7_m45_cr161_ZT_reduced.json`) | 45 | 35 | 58 | 68 | **161** |

## Verify in 5 seconds

```sh
sh verify-it-yourself/run_checks.sh
```

Needs only `python3` (standard library). It checks the file's SHA-256 against `INDEX.csv`, expands the straight-line program, checks all `8 * 28 * 14 = 3136` Brent equations over `Z` and random integer matrix products, confirms every expanded coefficient is in `{-1, 0, 1}`, confirms the reduced addition count is `35 + 58 + 68 = 161`, and checks that flipping one sign makes both checkers fail. Output is in `verify-it-yourself/RECEIPTS.md`.

## Files

- `object/2x4x7_m45_cr161_ZT_reduced.json` — the straight-line program (Perminov JSON layout; output `C` indexed `(k, i)` as in Perminov's files).
- `INDEX.csv` — target id, cell, 161 vs 174, fetch timestamp, file path, sha256.
- `verify-it-yourself/` — two independent stdlib-only checkers (`check_slp.py`, `brent_check.py`), `run_checks.sh`, and `RECEIPTS.md`.
- `the-record-we-beat/README.md` — URLs, UTC timestamps, HTTP codes and SHA-256 hashes of the live sources fetched on 2026-10-17.
- `how-we-built-it/` — walk script (`flip4.py`), helper (`lib.py`, `mk.py`), algebraic DAG exclusive-cone reduction (`dag_cone_collapse.py`), and pre-registration note.
- `HOW_WE_FOUND_IT.md`, `RUN_IT_YOURSELF.md` — short overview and commands.
- `panel/` — outputs of the four review steps (`reproduce.md`, `novelty.md`, `criterion.md`, `gate.md`).
- `SHA256SUMS` — SHA-256 of every file in this folder.

## Not claimed

- No improvement to multiplicative rank (`45` is already the best known rank for `<2,4,7>`).
- No proof that 161 is the minimum possible addition count for `<2,4,7>` at rank 45.
- IACR ePrint 2026/849 (Mårtensson and Stankovski Wagner) could not be read by the panel or maintainers (its PDF is behind an interactive challenge page); the comparison here stands against Perminov's live repository (`174`), the Lille catalogue, `COVERAGE.md`, open PR #229 (`169`), and withdrawn PR #11 (`164`).
- Only `<2,4,7>` at rank 45 is claimed here.

## Credits

- **Contributor**: `Zerbytheboss` (GitHub account `HindsightWise` is operated by `Zerbytheboss`; submitted via the V3R1T4S contribution kit following the maintainer's invitation on [PR #241](https://github.com/elder-plinius/V3R1T4S/pull/241#issuecomment-6227566357)).
- **Prior work on the target and tools**:
  - **A. I. Perminov** (Andrew I. Perminov, [arXiv:2512.13365](https://arxiv.org/abs/2512.13365)), [`FastMatrixMultiplication`](https://github.com/dronperminov/FastMatrixMultiplication) (the `2x4x7_m45_cr174_cn308_ZT_reduced.json` baseline scheme and JSON format) and [`ternary_addition_reducer`](https://github.com/dronperminov/ternary_addition_reducer) (the C++ common-subexpression reducer called inside our search loop).
  - **A. Sedoglavic**, [`fmm_digest`](https://github.com/sedoglavic/fmm_digest) and the [Lille FMM table](https://fmm.univ-lille.fr/2x4x7.html).
  - **Solven / `matmulcatalog`**, [`COVERAGE.md`](https://github.com/solven-eu/matmulcatalog).
  - **M. Kauers and J. Moosbauer** (flip-graph method for matrix multiplication schemes, ISSAC 2023) and **A. Novikov et al. / AlphaEvolve** (Google DeepMind, May 2025, [arXiv:2506.13131](https://arxiv.org/abs/2506.13131), whom the Lille catalogue cites for the `<2,4,7>` rank-45 bilinear scheme).
