# `14x15x15` Rank 1,894 in `ZT = {-1, 0, 1}` (`fmm-ternary-integer-ring-upgrade`)

## What

An explicit ternary (ZT, coefficients in {-1, 0, 1}) bilinear fast matrix multiplication scheme claim/14x15x15_m1894_ZT.json (944,884 bytes, sha256 bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb) for format 14x15x15 of rank 1,894, verified in exact integer arithmetic across all 9,922,500 Brent equations over Z, strictly improving on the live Perminov table ZT rank of 1,905 (-11) and Z rank of 1,895 (-1) while remaining above the overall best Q rank of 1,848.

- **Target:** `fmm-ternary-integer-ring-upgrade` (`algorithms`)
- **Claim level:** `solution_claim` (`CONFIRMED_SOLUTION`)
- **Object file:** `object/14x15x15_m1894_ZT.json` (`944,884` bytes, sparse ternary JSON + algebraic `multiplications`/`elements` strings)
- **SHA-256:** `bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb`
- **Properties:** Format `(14, 15, 15)`, rank `r = 1,894`, all coefficients in `{-1, 0, 1}` (`max_abs = 1`), `0` zero terms, `1,894` distinct rank-1 triples, `1`-minimal (`0` redundant rank-1 terms), `0` mismatches across all `210 * 225 * 210 = 9,922,500` exact integer Brent equations over `Z`.

## Check It Yourself

Run the standalone exhaustive checker from the root of this package (~0.4 seconds):

```sh
sh verify-it-yourself/run_checks.sh
```

It runs a positive control (Strassen `2x2x2` rank 7) and two negative controls (corrupted Brent tensor and non-ternary coefficient `2`), verifies the SHA-256, dimensions, ternary coefficient bound, non-degeneracy, and all `9,922,500` exact integer Brent equations over `Z` for `object/14x15x15_m1894_ZT.json`, and prints `PASS` on its final line.

## Compared To

- **Perminov FastMatrixMultiplication table (`https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md`, fetched `2026-10-18T17:19:53Z`, `sha256: 0dc78efcb144382ef7b703d37563722f5d328b83a42eddc17c0018e9bd628ca8`):** `ZT rank = 1,905`, `Z rank = 1,895`, `Q rank = 1,848`. Our ternary (`ZT`) scheme of rank `1,894` strictly improves the `ZT` rank by **11 multiplications** (`1,894 < 1,905`) and the `Z` rank by **1 multiplication** (`1,894 < 1,895`).
- **Sedoglavic `fmm_sota.json` (`https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json`, fetched `2026-10-18T17:19:55Z`, `sha256: 256d5753d1ff2640c11b3b1e5a1faaf21dc22c98055e1429a319f89e4e2a3c24`) & Lille FMM Catalogue (`https://fmm.univ-lille.fr/14x15x15.html`):** Overall best (`Q`) rank is `1,848` (`1,894 >= 1,848`).

## Not Claimed

- We do not claim a new overall (`Q`) rank record below `1,848` (which would belong to `fmm-catalogue-small-format-rank`).
- This package claims only the single format `14x15x15` (`r = 1,894` in `ZT = {-1, 0, 1}`).

## Credits

- **Contributor:** `mizopl`
- **External data & literature:** Starting ternary scheme `14x15x15_m1905_ZT.json` and status tables from A. Perminov's `FastMatrixMultiplication` repository (`https://github.com/dronperminov/FastMatrixMultiplication`, arXiv:2606.02480, arXiv:2603.18699) and A. Sedoglavic's `fmm_digest` / Universite de Lille FMM catalogue (`https://fmm.univ-lille.fr`).
