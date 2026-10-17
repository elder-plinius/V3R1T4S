# `4x5x5` Rank-76 Matrix Multiplication in 280 Reduced Additions (Was 299 in Live Table; Merged PR #222 at 281)

## What
An explicit ternary straight-line program in object/4x5x5_m76_cr280_ZT_reduced.json multiplies a 4x5 matrix by a 5x5 matrix over Z at the best known rank r = 76 using 280 reduced additions and subtractions (U 75, V 84, W 121), verified across all 10000 Brent equations over Z, strictly below Perminov's live addition_reduced_ZT record of 299 and merged V3R1T4S PR #222 at 281.

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last output line: `PASS` (runs in ~0.2 seconds on a laptop using only the Python 3 standard library).

## Compared To
All comparisons are against the live criterion sources fetched on `2026-10-17T16:45:59Z` (recorded in `the-record-we-beat/snapshot_2026-10-17.md`):

| Format | Rank `m` | `U` adds | `V` adds | `W` adds | Total Reduced Additions (`cr`) | Source |
|---|---:|---:|---:|---:|---:|---|
| `4x5x5` | 76 | 75 | 95 | 129 | **299** | Perminov live `4x5x5_m76_cr299_fv112_cn530_ZT_reduced.json` |
| `4x5x5` | 76 | — | — | — | **281** | Merged V3R1T4S PR [#222](https://github.com/elder-plinius/V3R1T4S/pull/222) |
| **`4x5x5`** | **76** | **75** | **84** | **121** | **280** | **`object/4x5x5_m76_cr280_ZT_reduced.json` (this package)** |

## Not Claimed
- We do not claim a new multiplicative rank (`76` is already the best known rank for `4x5x5` in `fmm_sota.json`).
- We do not claim a proof that 280 is the global minimum possible addition count for `4x5x5` at rank 76.
- Note that the margin over merged PR [#222](https://github.com/elder-plinius/V3R1T4S/pull/222) (`281`) is a single addition (`280` vs `281`), and `19` additions below Perminov's live repository (`299`). IACR ePrint 2026/849 (Mårtensson and Stankovski Wagner) could not be read by the panel or maintainers (its PDF is behind an interactive challenge page); the comparison here stands against Perminov's live repository, the Lille catalogue, `COVERAGE.md`, and merged PR #222.

## Credits
- **Contributor**: `Zerbytheboss` (GitHub account `HindsightWise` is operated by `Zerbytheboss`).
- **A. I. Perminov** (Andrew I. Perminov, [arXiv:2512.13365](https://arxiv.org/abs/2512.13365), [arXiv:2512.21980](https://arxiv.org/abs/2512.21980), [`FastMatrixMultiplication`](https://github.com/dronperminov/FastMatrixMultiplication) and [`ternary_addition_reducer`](https://github.com/dronperminov/ternary_addition_reducer)) for the baseline `4x5x5_m76_cr299_fv112_cn530_ZT_reduced.json` scheme, JSON format, and C++ CSE reducer.
- **A. Fawzi et al. / AlphaTensor** (Google DeepMind, *Nature* 610, 47–53, Oct 2022), whom the Lille catalogue (`https://fmm.univ-lille.fr/4x5x5.html`) cites for `4x5x5` at rank 76.
- **A. Sedoglavic** ([`fmm_digest`](https://github.com/sedoglavic/fmm_digest) and the [Lille FMM table](https://fmm.univ-lille.fr/4x5x5.html)).
- **Solven / Benoit Lacelle** ([`matmulcatalog`](https://github.com/solven-eu/matmulcatalog)) for `COVERAGE.md`.
- **M. Kauers and J. Moosbauer** (ISSAC 2023) for the flip-graph method.
