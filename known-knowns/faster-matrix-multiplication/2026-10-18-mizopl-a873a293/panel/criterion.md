# Skeptic Panel Report — Role: CRITERION

context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target: fmm-ternary-integer-ring-upgrade
format: 9x12x14
ring: ZT
claimed_rank: 954
object_file: object/9x12x14_m954_ZT.json
object_sha256: a873a293abc4e1b7c659250591e544062ad26ca556af28f29b25e63998355b02
object_bytes: 915296
confirmed_scope: An explicit ternary (ZT, coefficients in {-1, 0, 1}) bilinear fast matrix multiplication scheme for format 9x12x14 of rank 954 (object/9x12x14_m954_ZT.json, 915296 bytes, sha256 a873a293abc4e1b7c659250591e544062ad26ca556af28f29b25e63998355b02), verified in exact integer arithmetic across all 2,286,144 Brent equations over Z with 0 mismatches, strictly improving on the Perminov table listed on 2026-10-18 (ZT 960, Z 960) in README.md / docs/ranks.md while remaining above the overall best Q rank of 940.

## 1. Clause-by-Clause Verification of the Bank's Verbatim `success_criterion`

### Format & Ring Preconditions
- **Format dimensions (`n = [9, 12, 14]`):** `max(9, 12, 14) = 14` (at most `16`) and `sorted(9, 12, 14) = (9, 12, 14) != (4, 4, 4)`.
- **Coefficient ring (`ZT = {-1, 0, 1}`):** All entries across `u` (`954 x 108`), `v` (`954 x 168`), and `w` (`954 x 126`) in `object/9x12x14_m954_ZT.json` are Python `int` values in `{-1, 0, 1}` (`max_abs = 1`), with `5,936` nonzeros in `u`, `7,599` nonzeros in `v`, and `5,124` nonzeros in `w` (`18,659` total nonzeros).
- **Rank & non-degeneracy (`r = 954`):** Every one of the `954` rank-1 terms has non-empty support in all three factors (`zero_terms = 0`), all `954` factor triples `(u_q, v_q, w_q)` are distinct (`distinct_triples = 954`), and all `954` projective `(u_q, v_q)` pairs up to sign are distinct (`distinct_projective_uv_pairs = 954`).

### Clause (1): Strict Improvement Over `ZT` (and `Z`) Rank Listed on 2026-10-18
- A live HTTP fetch of `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md` at filing (`2026-10-18T12:35:49Z`, `status = 200`, `112,671` bytes, sha256 `7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341`, table now at `docs/ranks.md`) records line 1350 in the main status table:
  `| 9x12x14 | 960 (?) | 960 (?) | 940 (945) | **2.805232985** |`
- The rank listed on 2026-10-18 (`ZT 960, Z 960`) in `README.md` / `docs/ranks.md` is `960` (also published upstream by the contributor on 2026-10-19 as `schemes/known/mizopl/9x12x14_m954_ZT.json`; `docs/ranks.md` now lists `ZT 954 / Z 954`). Our verified rank `r = 954` is strictly less than `960`, a strict improvement of `6` multiplications in both `ZT` and `Z`.

### Clause (2): Does Not Beat Overall Best (`Q`) Rank
- In the Perminov table (`README.md` / `docs/ranks.md`), `min(ZT, Z, Q) = min(960, 960, 940) = 940`.
- In `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` (`343,798` bytes, sha256 `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1`), `{ "format": [9,12,14], "rank": 940, "exponent": 2.805233 }` gives SOTA rank `940`.
- Since `r = 954` is at least `940`, the scheme does not beat the overall best `Q` rank of `940` and properly belongs to `fmm-ternary-integer-ring-upgrade` rather than `fmm-catalogue-small-format-rank`.

### Clause (3): Absence of Rank at Most `954` in `ZT` (or `Z`) in Repositories as of Filing (2026-10-18)
- Querying the full recursive Git tree of `dronperminov/FastMatrixMultiplication` on 2026-10-18 (`6,637` total entries, `truncated = False`) for all six permutations of `(9, 12, 14)` returned only:
  - `schemes/results/ZT/9x12x14_m960_ZT.json` (and `.m`), sha256 `9623f6306e30a9d33d83a8b6e621250c4adf1848cc666ef2e655c7d6f9c3ec83` (rank `960`, strictly above `954`)
  - `schemes/results/Q/9x12x14_m940_Q.json` (and `.m`, `m942_Q`, `m944_Q`, rational `Q` schemes)
  - `schemes/known/tensor/9x12x14_tensor.mpl` (rational `Q` scheme of rank `945` containing fractional coefficients, sha256 `4a6b2125ea56f4cf350347b47d3e077dfbcca3369a794f9a8491dfe75b856a6c`)
  - Direct HTTP check of `schemes/results/ZT/9x12x14_m954_ZT.json` and `schemes/results/Z/9x12x14_m960_Z.json` on 2026-10-18 returned `HTTPError 404 (Not Found)`.
- Querying the full recursive Git tree of `MerlijnW70/fmm-schemes` (`39` total entries, sha256 `e6866337cf18c6f4bb9d2b950240341d901260e28b560a301853202c03b1a5fc`) returned `0` files matching any permutation of `(9, 12, 14)`.

### Clause (4): Exact Integer Verification of All `2,286,144` Brent Equations Over `Z`
- Running `verify-it-yourself/check_9x12x14.py` (`sh verify-it-yourself/run_checks.sh`) and an independent tensor contraction `np.einsum("qa,qb,qc->abc", U, V, W, dtype=np.int64)` plus pure-Python arbitrary-precision `int` arithmetic confirms all `108 x 168 x 126 = 2,286,144` Brent equations hold over `Z` (`1,512` ones on the matrix-multiplication diagonal, `2,284,632` zeros off-diagonal, `mismatches = 0`).

## 2. Hidden Quantifiers & Null-Model Checks

- **Null Model A (Indexing / Transposition Convention):** Testing column-major flattening `(i2*9 + i1, i3*12 + j2, j1*14 + j3)` against the contracted tensor `T` produces `3,020` mismatches out of `2,286,144`, confirming that `object/9x12x14_m954_ZT.json` satisfies Perminov's exact standard row-major trace convention `Tr(A B C^T)`.
- **Null Model B (1-Minimality / No Redundant Rank-1 Terms):** Deleting any single rank-1 term `q` in `0..953` breaks between `9` and `1,512` Brent equations over `Z` (`0` redundant terms).
- **Null Model C (Single-Entry Perturbation Sensitivity):** Zeroing a single nonzero entry (`U[0, 6] = 0`) breaks `8` Brent equations (`v_norms[0] * w_norms[0] = 8`), and both negative controls in `verify-it-yourself/check_9x12x14.py` fail as expected.

pass: true
