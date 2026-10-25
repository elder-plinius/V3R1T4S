# CRITERION Panel Report — `14x15x15` Rank-1894 Ternary (`ZT`) Fast Matrix Multiplication Scheme

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target: fmm-ternary-integer-ring-upgrade
format: 14x15x15
claimed_rank: 1894
claimed_ring: ZT
object_file: object/14x15x15_m1894_ZT.json
confirmed_scope: An explicit ternary (ZT, coefficients in {-1, 0, 1}) bilinear fast matrix multiplication scheme object/14x15x15_m1894_ZT.json (944,884 bytes, sha256 bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb) for format 14x15x15 of rank 1,894, verified in exact integer arithmetic across all 9,922,500 Brent equations over Z, improving on the table as of filing (2026-10-18: ZT 1,905, Z 1,895; -11 in ZT and -1 in Z) while remaining above the rational Q ranks (1,848 in Perminov / fmm_sota.json, and 1,842 over Q already merged in V3R1T4S).

## 1. Independent Verification Execution

An independent verification script and the package's standalone verifier (`verify-it-yourself/check_14x15x15.py`) were executed against `object/14x15x15_m1894_ZT.json` and the upstream repositories.

### File Integrity Verified
- `object/14x15x15_m1894_ZT.json`: `944,884` bytes, SHA-256 `bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb`
- Perminov `README.md` as of filing (`2026-10-18`): `112,671` bytes, SHA-256 `0dc78efcb144382ef7b703d37563722f5d328b83a42eddc17c0018e9bd628ca8` (table now at `docs/ranks.md`, SHA-256 `77203a718e82fec693578d193c9ccbb2332edcf41f086088a8405cd403666c5a`)
- Sedoglavic `fmm_sota.json`: `343,798` bytes, SHA-256 `256d5753d1ff2640c11b3b1e5a1faaf21dc22c98055e1429a319f89e4e2a3c24`

## 2. Clause-by-Clause Audit Against Verbatim Bank Criterion

### Preconditions: Format Bounds, Coefficient Ring, and Rank Well-Definedness
- **Format bounds:** `n = [14, 15, 15]`, so `max(14, 15, 15) = 15` (at most `16`) and `sorted(14, 15, 15) = (14, 15, 15) != (4, 4, 4)`.
- **Ternary ring (`ZT`):** All entries in `u_sparse`, `v_sparse`, and `w_sparse` are Python `int` values in `{-1, 1}` with valid in-range indices (`0..209` for `U`, `0..224` for `V`, `0..209` for `W`) and zero duplicate index entries per term. The reconstructed dense matrices `U` (`1894 x 210`), `V` (`1894 x 225`), and `W` (`1894 x 210`) have unique values `[-1, 0, 1]` (`max_abs = 1`), with `20,861`, `17,726`, and `22,370` nonzeros respectively (`60,957` total nonzeros).
- **Rank and non-degeneracy:** `m = 1894`. Zero rank-1 terms: `0` (`zero_terms = 0`). All `1,894` rank-1 terms `(U_q, V_q, W_q)` are distinct (`1894 / 1894`) and projectively distinct up to factor sign flips (`1894 / 1894`).

### Clause (1): Strictly Less Than `ZT` Rank Listed as of Filing (`2026-10-18: ZT 1,905, Z 1,895`)
- In the Perminov table as of filing (`2026-10-18: ZT 1,905, Z 1,895`, `README.md` / `docs/ranks.md`):
  `| 14x15x15 | 1905 (32) | 1895 (33) | 1848 (99) | **2.811404586** |`
- The `ZT` rank as of filing was `1,905` and the `Z` rank was `1,895` (also published upstream by the contributor on 2026-10-19 as `schemes/known/mizopl/14x15x15_m1894_ZT.json`; `docs/ranks.md` now lists `ZT 1,894 / Z 1,894`).
- The claimed ternary scheme has rank `r = 1894`, improving on the table as of filing (`2026-10-18: ZT 1,905, Z 1,895`) by `11` multiplications in `ZT` and `1` multiplication in `Z`.
- **Verdict on Clause (1):** SATISFIED.

### Clause (2): Greater Than or Equal to Minimum Over `ZT`/`Z`/`Q` and `fmm_sota.json`
- The minimum over the `ZT`/`Z`/`Q` columns for `14x15x15` in Perminov (`README.md` / `docs/ranks.md`) is `1,848` (over `Q`), and `fmm_sota.json` lists `{"format": [14, 15, 15], "rank": 1848, "exponent": 2.811405}` (note that `1,848` is not the overall best: a rational rank-`1,842` scheme is already merged here in `V3R1T4S` `TROPHY_CASE.md`).
- Since `r = 1894 >= 1848 > 1842`, the scheme does not beat the overall best `Q` rank and properly belongs to `fmm-ternary-integer-ring-upgrade` rather than `fmm-catalogue-small-format-rank`.
- **Verdict on Clause (2):** SATISFIED.

### Clause (3): No Scheme of Rank at Most `1894` in `ZT` (or `Z`) Existed in Repositories as of Filing (`2026-10-18`)
- Querying `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/status.json` as of filing (`2026-10-18`) for `14x15x15` returned `"ranks": {"Z": 1895, "Q": 1848, "ZT": 1905}`, with only `schemes/results/ZT/14x15x15_m1905_ZT.json` (rank `1905`) in `ZT` and `schemes/results/Z/14x15x15_m1895_Z.json` (rank `1895`, values `[-2, -1, 0, 1, 2]`) plus `14x15x15_m1905_Z.json` (rank `1905`) in `Z`. As of filing (`2026-10-18`), no scheme of rank `<= 1894` in `ZT` or `Z` existed in `dronperminov/FastMatrixMultiplication`.
- Querying `https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1` (`39` items total) confirms no scheme for `14x15x15` exists in `MerlijnW70/fmm-schemes`.
- **Verdict on Clause (3):** SATISFIED.

### Clause (4): Exact Verification of All Brent Equations Over `Z` and Null/Sensitivity Checks
- **All `9,922,500` Brent equations over `Z`:** Exhaustively evaluated in exact 64-bit integer arithmetic across all `210 x 225 x 210 = 9,922,500` index sextuples `(i1, i2, j2, i3, j3, j1)`:
  - `mismatches = 0`
  - `identity_ones = 3,150` (`14 x 15 x 15 = 3,150`)
  - `zero_entries = 9,919,350` (`9,922,500 - 3,150 = 9,919,350`)
- **1-minimality and negative controls:** Every single rank-1 term `q` (`0..1893`) has support size `||U_q||_0 * ||V_q||_0 * ||W_q||_0` between `3` and `9,702`, so deleting any single term `q` immediately creates between `3` and `9,702` nonzero Brent equation errors.
- **Functional matrix multiplication check:** Tested on `20` independent random integer matrix pairs `(A, B)` of shapes `(14, 15)` and `(15, 15)` with entries drawn uniformly from `[-50, 50]`; all `20 / 20` bilinear products reconstructed from `object/14x15x15_m1894_ZT.json` matched `A @ B` in every entry.
- **Verdict on Clause (4):** SATISFIED.

pass: true
