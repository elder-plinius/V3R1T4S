# CRITERION Panel Report — `14x15x15` Rank-1894 Ternary (`ZT`) Fast Matrix Multiplication Scheme

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target: fmm-ternary-integer-ring-upgrade
format: 14x15x15
claimed_rank: 1894
claimed_ring: ZT
confirmed_scope: An explicit ternary (ZT, coefficients in {-1, 0, 1}) bilinear fast matrix multiplication scheme claim/14x15x15_m1894_ZT.json (944,884 bytes, sha256 bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb) for format 14x15x15 of rank 1,894, verified in exact integer arithmetic across all 9,922,500 Brent equations over Z, strictly improving on the live Perminov table ZT rank of 1,905 (-11) and Z rank of 1,895 (-1) while remaining above the overall best Q rank of 1,848.

## 1. Independent Verification Execution

An independent verification script (`panel/fmm_14x15x15/criterion_work/verify_criterion.py`) and the claim's standalone verifier (`claim/author_checker_brent_check.py`) were executed against `claim/14x15x15_m1894_ZT.json`, `claim/perminov_README.md`, `claim/fmm_sota.json`, and the live upstream repositories.

### File Integrity Verified
- `claim/14x15x15_m1894_ZT.json`: `944,884` bytes, SHA-256 `bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb`
- `claim/perminov_README.md`: `112,671` bytes, SHA-256 `7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341` (matches live `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md` byte-for-byte, HTTP 200)
- `claim/fmm_sota.json`: `343,798` bytes, SHA-256 `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1`

## 2. Clause-by-Clause Audit Against Verbatim Bank Criterion

### Preconditions: Format Bounds, Coefficient Ring, and Rank Well-Definedness
- **Format bounds:** `n = [14, 15, 15]`, so `max(14, 15, 15) = 15` (at most `16`) and `sorted(14, 15, 15) = (14, 15, 15) != (4, 4, 4)`.
- **Ternary ring (`ZT`):** All entries in `u_sparse`, `v_sparse`, and `w_sparse` are Python `int` values in `{-1, 1}` with valid in-range indices (`0..209` for `U`, `0..224` for `V`, `0..209` for `W`) and zero duplicate index entries per term. The reconstructed dense matrices `U` (`1894 x 210`), `V` (`1894 x 225`), and `W` (`1894 x 210`) have unique values `[-1, 0, 1]` (`max_abs = 1`), with `20,861`, `17,726`, and `22,370` nonzeros respectively (`60,957` total nonzeros).
- **Rank and non-degeneracy:** `m = 1894`. Zero rank-1 terms: `0` (`zero_terms = 0`). All `1,894` rank-1 terms `(U_q, V_q, W_q)` are distinct (`1894 / 1894`) and projectively distinct up to factor sign flips (`1894 / 1894`).

### Clause (1): Strictly Less Than Live `ZT` Rank
- In `claim/perminov_README.md` (line 765 table header `| Format | ZT rank | Z rank | Q rank | ω |`, line 1440 row for `14x15x15`):
  `| 14x15x15 | 1905 (?) | 1895 (1905) | 1848 (1905) | **2.801382482** |`
- The live `ZT` rank is `1905` and the live `Z` rank is `1895`.
- The claimed ternary scheme has rank `r = 1894`, which is strictly less than `1905` by `11` multiplications (and also strictly less than the live integer `Z` rank `1895` by `1` multiplication).
- **Verdict on Clause (1):** SATISFIED.

### Clause (2): Greater Than or Equal to Minimum Over `ZT`/`Z`/`Q` and `fmm_sota.json`
- The minimum over the live `ZT`/`Z`/`Q` columns for `14x15x15` in `claim/perminov_README.md` is `min(1905, 1895, 1848) = 1848` (achieved over `Q`).
- In `claim/fmm_sota.json`, the single entry for `[14, 15, 15]` is `{"format": [14, 15, 15], "rank": 1848, "exponent": 2.801382}`.
- Since `r = 1894` is at least `1848` (`1894 - 1848 = +46`), the scheme does not beat the overall best `Q` rank of `1848` and properly belongs to `fmm-ternary-integer-ring-upgrade` rather than `fmm-catalogue-small-format-rank`.
- **Verdict on Clause (2):** SATISFIED.

### Clause (3): No Scheme of Rank at Most `1894` in `ZT` (or `Z`) Exists in Live Repositories
- Live query of `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/status.json` for `14x15x15` returns `"ranks": {"Z": 1895, "Q": 1848, "ZT": 1905}`, with only `schemes/results/ZT/14x15x15_m1905_ZT.json` (rank `1905`) in `ZT` and `schemes/results/Z/14x15x15_m1895_Z.json` (rank `1895`, values `[-2, -1, 0, 1, 2]`) plus `14x15x15_m1905_Z.json` (rank `1905`) in `Z`. Direct fetch of `schemes/results/ZT/14x15x15_m1894_ZT.json` returns HTTP 404.
- Live query of `https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1` (`39` items total) and `MerlijnW70/fmm-schemes/main/README.md` (`2,697` bytes, SHA-256 `6ef17ff86e9a74b710e4e6173f67187b735ecdef760d2634a16d33bdf73b904b` — verified no `14x15x15` entry) confirms no scheme for `14x15x15` exists in `MerlijnW70/fmm-schemes`.
- **Verdict on Clause (3):** SATISFIED.

### Clause (4): Exact Verification of All Brent Equations Over `Z` and Null/Sensitivity Checks
- **All `9,922,500` Brent equations over `Z`:** Exhaustively evaluated in exact 64-bit integer arithmetic across all `210 x 225 x 210 = 9,922,500` index sextuples `(i1, i2, j2, i3, j3, j1)`:
  - `mismatches = 0`
  - `identity_ones = 3,150` (`14 x 15 x 15 = 3,150`)
  - `zero_entries = 9,919,350` (`9,922,500 - 3,150 = 9,919,350`)
- **1-minimality and negative controls:** Every single rank-1 term `q` (`0..1893`) has support size `||U_q||_0 * ||V_q||_0 * ||W_q||_0` between `3` and `9,702`, so deleting any single term `q` immediately creates between `3` and `9,702` nonzero Brent equation errors. Explicit deletion tests on `q = 0`, `q = 947`, and `q = 1893` produced `144`, `144`, and `16` mismatches respectively in a single matrix slice `a`.
- **Functional matrix multiplication check:** Tested on `20` independent random integer matrix pairs `(A, B)` of shapes `(14, 15)` and `(15, 15)` with entries drawn uniformly from `[-50, 50]`; all `20 / 20` bilinear products reconstructed from `claim/14x15x15_m1894_ZT.json` matched `A @ B` in every entry.
- **Verdict on Clause (4):** SATISFIED.

pass: true
