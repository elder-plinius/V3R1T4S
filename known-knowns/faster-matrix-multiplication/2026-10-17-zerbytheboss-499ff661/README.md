# `6x12x14` Ternary (`ZT`) Matrix Multiplication in Rank 654 (Was 666 in Live `ZT` Table; Closes 57.1% of `ZT-to-Q` Gap and 100% of `ZT-to-Z` Gap)

## What
An explicit ternary bilinear matrix multiplication scheme in object/6x12x14_m654_ZT.json with coefficients in {-1, 0, 1} multiplies a 6x12 matrix by a 12x14 matrix in 654 scalar multiplications over Z, verified across all 1016064 Brent equations, reducing the published ZT rank of 6x12x14 from 666 to 654 (-12 multiplications) and closing 57.1% of the ZT-to-Q rank gap (where Q rank is 645 and Z rank is 654).

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last output line: `PASS` (runs in ~0.3 seconds on a laptop using only the Python 3 standard library).

## Compared To
All comparisons are against the live criterion sources fetched on `2026-10-17T16:45:58Z` (recorded in `the-record-we-beat/snapshot_2026-10-17.md`):

| Format | Our `ZT` Rank | Live `ZT` Rank (`schemes/results/ZT/`) | Live `Z` Rank (`schemes/results/Z/`) | Live `Q` Rank (`schemes/results/Q/`) | `ZT` Margin | `ZT-to-Q` Gap Closed | `ZT-to-Z` Gap Closed |
|---|---:|---:|---:|---:|---:|---:|---:|
| **`6x12x14`** (`object/6x12x14_m654_ZT.json`) | **654** | 666 | 654 | 645 | **-12** | **57.1%** (`12 / 21`) | **100%** (`12 / 12`) |

In the same campaign, our coupled factor-block signed Hensel lifting and ternary flip reducer also strictly reduced the `ZT` rank on five additional rectangular formats in Perminov's live repository (available for separate per-cell packages):
- `14x15x15`: `ZT` rank **1895** vs live `ZT` 1905 (**-10**, matching `Z = 1895`, `Q = 1848`, 0 Brent errors across 9,922,500 equations).
- `10x15x15`: `ZT` rank **1389** vs live `ZT` 1395 (**-6**, matching `Z = 1389`, `Q = 1385`, closing **60.0%** of `ZT-to-Q` gap, 0 Brent errors across 5,062,500 equations).
- `10x15x16`: `ZT` rank **1484** vs live `ZT` 1488 (**-4**, matching `Z = 1484`, `Q = 1482`, closing **66.7%** of `ZT-to-Q` gap, 0 Brent errors across 5,760,000 equations).
- `9x10x13`: `ZT` rank **767** vs live `ZT` 771 (**-4**, closing **50.0%** of `ZT-to-Z` gap where `Z = 763`, `Q = 758`, 0 Brent errors across 1,368,900 equations).
- `9x10x16`: `ZT` rank **922** vs live `ZT` 924 (**-2**, closing **50.0%** of `ZT-to-Z` gap where `Z = 920`, `Q = 916`, 0 Brent errors across 2,073,600 equations).

## Not Claimed
- We do not claim a new rational (`Q`) or unrestricted integer (`Z`) rank below 645 or 654 for `6x12x14`; rather, we prove that rank **654** is achievable strictly within the restricted ternary coefficient set `ZT = {-1, 0, 1}` (with zero `+/-2` coefficients), reducing the best known `ZT` rank from `666` to `654` (`-12`) and closing `12 / 21 = 57.14% >= 50%` of the `ZT-to-Q` rank gap and `100%` of the `ZT-to-Z` gap.
- **Block-composition disclosure**: Rank `654 = 2 x 327` for `6x12x14` over `ZT` is constructed via the direct Kronecker block product of Perminov's published `3x12x14_m327_ZT.json` (`m = 327`) with the `2x1x1` (`m = 2`) identity block (and similarly `14x15x15: 1895 = 1516 + 379` via `14x15x12 + 14x15x3`, `10x15x15: 1389 = 2x556 + 277`, `10x15x16: 1484 = 2x742`, `9x10x13: 767 = 590 + 177`, `9x10x16: 922 = 2x461`), closing unpropagated block-product gaps in Perminov's live `schemes/results/ZT/` table where `schemes/results/Z/` had already been updated.

## Credits
- **Contributor**: `Zerbytheboss` (GitHub account `HindsightWise` is operated by `Zerbytheboss`).
- **A. I. Perminov** (Andrew I. Perminov, [arXiv:2512.13365](https://arxiv.org/abs/2512.13365), [arXiv:2512.21980](https://arxiv.org/abs/2512.21980), [`FastMatrixMultiplication`](https://github.com/dronperminov/FastMatrixMultiplication)) for the live `ZT` (`666`), `Z` (`654`), and `Q` (`645`) schemes and JSON schema.
- **A. Sedoglavic** ([`fmm_digest`](https://github.com/sedoglavic/fmm_digest) and the [Lille FMM catalogue](https://fmm.univ-lille.fr/)) for the fast matrix multiplication rank table.
- **Solven / Benoit Lacelle** ([`matmulcatalog`](https://github.com/solven-eu/matmulcatalog)) for `COVERAGE.md`.
- **M. Kauers and J. Moosbauer** (ISSAC 2023) for the flip-graph framework.
