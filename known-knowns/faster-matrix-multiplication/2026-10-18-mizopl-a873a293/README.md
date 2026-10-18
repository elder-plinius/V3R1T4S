# `9x12x14` Rank 954 in `ZT = {-1, 0, 1}` (`fmm-ternary-integer-ring-upgrade`)

## What

An explicit ternary (ZT, coefficients in {-1, 0, 1}) bilinear fast matrix multiplication scheme for format 9x12x14 of rank 954 (claim/9x12x14_m954_ZT.json, 915296 bytes, sha256 a873a293abc4e1b7c659250591e544062ad26ca556af28f29b25e63998355b02), verified in exact integer arithmetic across all 2,286,144 Brent equations over Z with 0 mismatches, strictly improving on the live Perminov table ZT rank of 960 and Z rank of 960 while remaining above the overall best Q rank of 940.

- **Target:** `fmm-ternary-integer-ring-upgrade` (`algorithms`)
- **Claim level:** `solution_claim` (`CONFIRMED_SOLUTION`)
- **Object file:** `object/9x12x14_m954_ZT.json` (`915,296` bytes, Perminov standard JSON format with `u`, `v`, `w` integer arrays)
- **SHA-256:** `a873a293abc4e1b7c659250591e544062ad26ca556af28f29b25e63998355b02`
- **Properties:** Format `(9, 12, 14)`, rank `r = 954`, all coefficients in `{-1, 0, 1}` (`max_abs = 1`), `0` zero terms, `954` distinct rank-1 triples, `1`-minimal (`0` redundant rank-1 terms), `0` mismatches across all `108 * 168 * 126 = 2,286,144` exact integer Brent equations over `Z`.

## Check It Yourself

Run the standalone exhaustive checker from the root of this package (~0.2 seconds):

```sh
sh verify-it-yourself/run_checks.sh
```

It runs a positive control (Strassen `2x2x2` rank 7) and two negative controls (corrupted Brent tensor and non-ternary coefficient `2`), verifies the SHA-256, dimensions, ternary coefficient bound, non-degeneracy, and all `2,286,144` exact integer Brent equations over `Z` for `object/9x12x14_m954_ZT.json`, and prints `PASS` on its final line.

## Compared To

- **Perminov FastMatrixMultiplication table (`https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md`, fetched `2026-10-18T12:35:49Z`, `sha256: 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341`):** `ZT rank = 960`, `Z rank = 960`, `Q rank = 940`. Our ternary (`ZT`) scheme of rank `954` strictly improves both the `ZT` rank and the `Z` rank by **6 multiplications** (`954 < 960`).
- **Sedoglavic `fmm_sota.json` (`https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json`, fetched `2026-10-18T12:35:50Z`, `sha256: d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1`) & Lille FMM Catalogue (`https://fmm.univ-lille.fr/9x12x14.html`):** Overall best (`Q`) rank is `940` (`954 >= 940`).

## Not Claimed

- We do not claim a new overall (`Q`) rank record below `940` (which would belong to `fmm-catalogue-small-format-rank`).
- This package claims only the single format `9x12x14` (`r = 954` in `ZT = {-1, 0, 1}`).

## Credits

- **Contributor:** `mizopl`
- **External data & literature:** Ingredient schemes (`3x4x7_m64_ZT.json`, `2x3x3_tensor.mpl`, `3x3x4_tensor.mpl`) and status tables from A. Perminov's `FastMatrixMultiplication` repository (`https://github.com/dronperminov/FastMatrixMultiplication`, arXiv:2606.02480, arXiv:2603.18699) and A. Sedoglavic's `fmm_digest` / Universite de Lille FMM catalogue (`https://fmm.univ-lille.fr`).
