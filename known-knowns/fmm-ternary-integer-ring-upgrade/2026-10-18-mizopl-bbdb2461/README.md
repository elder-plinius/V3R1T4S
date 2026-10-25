# `14x15x15` Rank 1,894 in `ZT = {-1, 0, 1}` (`fmm-ternary-integer-ring-upgrade`)

## What

An explicit ternary (`ZT`, coefficients in `{-1, 0, 1}`) bilinear fast matrix multiplication scheme `object/14x15x15_m1894_ZT.json` (`944,884` bytes, `sha256: bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb`) for format `14x15x15` of rank `1,894`, verified in exact integer arithmetic across all `9,922,500` Brent equations over `Z`, improving on the table as of filing (`2026-10-18: ZT 1,905, Z 1,895`, `-11` in `ZT` and `-1` in `Z`) while remaining above the rational `Q` ranks (`1,848` in Perminov / `fmm_sota.json`, and `1,842` over `Q` already merged in `V3R1T4S` `TROPHY_CASE.md`).

- **Also published upstream by the contributor (`@mizopl`) on 2026-10-19 (`schemes/known/mizopl/14x15x15_m1894_ZT.json`); `docs/ranks.md` now lists `ZT 1,894 / Z 1,894`.**
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

- **Perminov FastMatrixMultiplication table as of filing (`2026-10-18: ZT 1,905, Z 1,895`) (`https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md`, fetched `2026-10-18T17:19:53Z`, `sha256: 0dc78efcb144382ef7b703d37563722f5d328b83a42eddc17c0018e9bd628ca8`; moved upstream to `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md`, `sha256: 77203a718e82fec693578d193c9ccbb2332edcf41f086088a8405cd403666c5a`):** Listed at filing (`2026-10-18: ZT 1,905, Z 1,895`), `Q rank = 1,848`. Also published upstream by the contributor (`@mizopl`) on 2026-10-19 (`schemes/known/mizopl/14x15x15_m1894_ZT.json`); `docs/ranks.md` now lists `ZT 1,894 / Z 1,894`. Our ternary (`ZT`) scheme of rank `1,894` improves on the table as of filing (`2026-10-18: ZT 1,905, Z 1,895`) by **11 multiplications in `ZT`** (`1,894 < 1,905`) and **1 multiplication in `Z`** (`1,894 < 1,895`).
- **Sedoglavic `fmm_sota.json` (`https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json`, fetched `2026-10-18T17:19:55Z`, `sha256: 256d5753d1ff2640c11b3b1e5a1faaf21dc22c98055e1429a319f89e4e2a3c24`), Lille FMM Catalogue (`https://fmm.univ-lille.fr/14x15x15.html`), & `V3R1T4S` `TROPHY_CASE.md`:** `fmm_sota.json` / Perminov list rational (`Q`) rank `1,848`, which is not the overall best because a rational (`Q`) rank-`1,842` scheme for `14x15x15` is already merged here in `V3R1T4S` (`TROPHY_CASE.md`). Our ternary (`ZT`) rank `1,894` remains above both (`1,894 >= 1,848 > 1,842`).

## Not Claimed

- We do not claim a new overall (`Q`) rank record (Perminov / `fmm_sota.json` list `1,848` over `Q`, and a rational rank-`1,842` scheme is already merged here in `V3R1T4S`).
- This package claims only the single format `14x15x15` (`r = 1,894` in `ZT = {-1, 0, 1}`).

## Credits

- **Contributor:** `mizopl`
- **External data & literature:** Upstream ingredient schemes from A. Perminov's `FastMatrixMultiplication` repository (`https://github.com/dronperminov/FastMatrixMultiplication`, arXiv:2606.02480, arXiv:2603.18699):
  - `5x5x7_m127_ZT.json`: `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/serendipitous_base/5x5x7_m127_b28a738efa3c009809fa587f4d39fe232f7f6ce1_ZT.json` (`55,660` bytes, `sha256: 9b0b3f9bcb650290e22c338ddf777199d199b5017e9d12ec7d8e5d19fdec05a9`)
  - `2x3x3_tensor.mpl`: `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/known/tensor/2x3x3_tensor.mpl` (`2,235` bytes, `sha256: c98747b97b6a386978770e627bc3e0482dc8cabea9cad47f5963ca40f7330d5d`)
  - `3x3x4_tensor.mpl`: `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/known/tensor/3x3x4_tensor.mpl` (`4,806` bytes, `sha256: 597a7fafb994ee15ea3472ab9c03b5823c34767f5bc376ab738965229684eabb`)
  and status tables from `dronperminov/FastMatrixMultiplication` (`README.md` / `docs/ranks.md`) and A. Sedoglavic's `fmm_digest` / Universite de Lille FMM catalogue (`https://fmm.univ-lille.fr`).
