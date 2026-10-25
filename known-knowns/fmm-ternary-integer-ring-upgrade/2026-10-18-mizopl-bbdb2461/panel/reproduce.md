# Panelist Report — REPRODUCE

role: REPRODUCE
context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
target: fmm-ternary-integer-ring-upgrade
format: 14x15x15
claimed_rank: 1894
ring: ZT
claimed_object: object/14x15x15_m1894_ZT.json

## 1. Quoted Definition and Bank Criterion

Verbatim bank criterion (`fmm-ternary-integer-ring-upgrade`):

> Success means an explicit bilinear scheme for a format `(n,m,p)` with `max(n,m,p) <= 16` and `sorted(n,m,p) != (4,4,4)`, whose coefficients all lie in `{-1,0,1}` (ternary, `ZT`) or all in `Z` (integer), with rank `r` such that:
> 1. `r` is STRICTLY LESS (direction: min) than the `ZT rank` (for a ternary claim) or the `Z rank` (for an integer claim) listed for that format in `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md` re-fetched live immediately before claiming;
> 2. `r` is GREATER THAN OR EQUAL to the minimum over the live `ZT`/`Z`/`Q` columns for that format and to the live `fmm_sota.json` rank, i.e. the scheme does NOT beat the overall best rank (a scheme that does is the catalogue target `fmm-catalogue-small-format-rank`, never both);
> 3. no scheme of rank `<= r` in the same coefficient class already exists in the live `schemes/results/ZT` (or `/Z`) directory of that repository or in `https://github.com/MerlijnW70/fmm-schemes`;
> 4. the Brent equations are verified exactly over `Z` with integer arithmetic (so the scheme is valid over every ring), not merely mod 2. Equalling the format's `Q` rank is the natural goal but any strict `ZT` or `Z` improvement satisfying (1)-(4) counts.

Exact integer Brent equations (Clause 4):

> For all `i1, j1 in 0..13`, `i2, j2 in 0..14`, `i3, j3 in 0..14` (`210 * 225 * 210 = 9,922,500` equations),
> $$\sum_{q=0}^{1893} U[q, i_1 \cdot 15 + i_2] \, V[q, j_2 \cdot 15 + i_3] \, W[q, j_3 \cdot 14 + j_1] = \delta_{i_1, j_1}\,\delta_{i_2, j_2}\,\delta_{i_3, j_3}$$
> holds over $\mathbb{Z}$ with `0` mismatches.

## 2. Independent Checker Written Before Reading Author's Code

Before reading `verify-it-yourself/check_14x15x15.py`, I wrote an independent exhaustive checker directly from the mathematical definition above using exact 64-bit integer (`numpy.int64`) arithmetic:

1. **Self-tests on positive and negative controls:**
   - **Positive control:** Strassen's `(2, 2, 2)` rank-7 ternary scheme over $\mathbb{Z}$ (`64/64` Brent equations satisfied, `mismatches = 0`, `max_abs = 1`, `zero_terms = 0`).
   - **Negative control 1 (corrupted Brent tensor):** Flipping `W[0, 0]` from `1` to `0` in Strassen's `(2, 2, 2)` scheme is rejected with `mismatches = 4` out of `64`.
   - **Negative control 2 (non-ternary coefficient):** Setting `U[0, 0] = 2` is rejected by the `ZT` check with `max_abs = 2`.
   - **Negative control 3 (all-zero rank-1 factor):** Appending a rank-1 term with `U[q, :] = 0` is rejected with `zero_terms = 1`.
2. **File integrity checks:** Computes exact byte count and SHA-256 digest of `object/14x15x15_m1894_ZT.json` (`944,884` bytes, `sha256: bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb`).
3. **Dense reconstruction and structural checks:** Reconstructs dense `int64` arrays $U \in \mathbb{Z}^{1894 \times 210}$, $V \in \mathbb{Z}^{1894 \times 225}$, and $W \in \mathbb{Z}^{1894 \times 210}$ from `u_sparse`, `v_sparse`, `w_sparse`, verifying bounds, absence of duplicate indices per factor, `max_abs = 1` (all coefficients in $\{-1, 0, 1\}$), `zero_terms = 0`, and naive addition count `(nnz(U) - m) + (nnz(V) - m) + (nnz(W) - 210) = 56959 == complexity`.
4. **Algebraic string cross-check:** Independently formats `u_sparse` and `v_sparse` into Perminov's `m1 .. m1894` polynomial multiplication strings and compares against all `1894` entries of `multiplications` (`0` mismatches), and parses all `210` output expressions `c11 .. c1415` in `elements` into a dense array `W_from_elements` and verifies `np.array_equal(W, W_from_elements) == True`.
5. **Exhaustive exact integer Brent equation check:** Contracts $T[a, b, c] = \sum_{q=0}^{1893} U[q, a] V[q, b] W[q, c]$ in exact `int64` arithmetic for all $210 \times 225 \times 210 = 9,922,500$ index triples $(a, b, c)$ and compares against the exact Kronecker delta tensor $\delta_{i_1, j_1} \delta_{i_2, j_2} \delta_{i_3, j_3}$ (`ones = 3150`, `zeros = 9919350`, `mismatches = 0`).
6. **Direct bilinear matrix multiplication evaluation:** Evaluates the bilinear scheme on `10` deterministic pseudorandom pairs of exact integer matrices $(A, B) \in \mathbb{Z}^{14 \times 15} \times \mathbb{Z}^{15 \times 15}$ with entries in $[-50, 50]$ (seed `20261018`) and verifies $C_{\text{scheme}} = A B$ entrywise over $\mathbb{Z}$ (`10/10` exact matches).
7. **Catalogue baseline checks (`the-record-we-beat/RECORD.md`):** Compares against the Perminov table as of filing (`2026-10-18: ZT 1,905, Z 1,895`, `Q = 1,848`) and `fmm_sota.json` (`rank = 1,848`; note that `1,848` is not the overall best because a rational rank-`1,842` scheme is already merged here in `V3R1T4S`), confirming $1894 < 1895 < 1905$ and $1894 \ge 1848 > 1842$.

## 3. Package Checker Inspection and Execution (`sh verify-it-yourself/run_checks.sh`)

After completing the independent verification, I inspected `verify-it-yourself/check_14x15x15.py` and executed `sh verify-it-yourself/run_checks.sh` twice:

- Run 1 & Run 2 output:
  - `control_positive_strassen_2_2_2: PASS (64/64 equations, mismatches=0)`
  - `control_negative_corrupted_brent: PASS (rejected)`
  - `control_negative_non_zt_coeff: PASS (rejected)`
  - `sha256=bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb`
  - `format=14x15x15 rank=1894 ring=ZT max_abs=1 zero_terms=0`
  - `previous_zt_record=1905 previous_z_record=1895 overall_q_record=1848 delta_zt=-11 delta_z=-1`
  - `total_brent_equations=9922500 mismatches=0`
  - `PASS`

## 4. Re-derivation of the Construction Arithmetic (`HOW_WE_FOUND_IT.md`)

- Base Kronecker product of $s_1 = (7, 5, 5)$ of rank `127` in `ZT` and $s_2 = (2, 3, 3)$ of rank `15` in `ZT` has rank $127 \times 15 = 1905$.
- Replacing `11` disjoint $v$-bud pairs of $s_1$ (each pair originally costing $2 \times 15 = 30$ multiplications) with `11` copies of the conjugated $(4, 3, 3)$ scheme $\pi \cdot s_3$ of rank `29` in `ZT` saves $30 - 29 = 1$ multiplication per pair, giving rank $1905 - 11 = 1894$.
- For any permutation $\pi$ of $\{0, 1, 2, 3\}$, $\delta_{\pi(r), \pi(r')} = \delta_{r, r'}$, so conjugating both $A$-rows and $C$-rows of the $(4, 3, 3)$ scheme by $\pi = (0, 1, 3, 2)$ preserves the exact matrix multiplication tensor while aligning signs so the combined scheme stays in `ZT = {-1, 0, 1}`.

## 5. Summary of Verified Properties

| Property | Expected | Measured | Status |
|---|---|---|---|
| `object/14x15x15_m1894_ZT.json` bytes | `944884` | `944884` | PASS |
| `object/14x15x15_m1894_ZT.json` SHA-256 | `bbdb2461...c2979bb` | `bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb` | PASS |
| Format `n` and rank `m` | `[14, 15, 15]`, `1894` | `(14, 15, 15)`, `1894` | PASS |
| Coefficient ring (`ZT`) | `max_abs = 1`, `zero_terms = 0` | `max_abs = 1`, `zero_terms = 0` | PASS |
| Exact integer Brent equations over $\mathbb{Z}$ | `9,922,500` eqs, `0` mismatches | `9,922,500` eqs (`3,150` ones, `9,919,350` zeros), `0` mismatches | PASS |
| Direct exact integer matrix multiplication | `C_scheme == A @ B` | `10/10` exact integer trials matched | PASS |
| Algebraic strings (`multiplications`, `elements`) | Match `u_sparse, v_sparse, w_sparse` | `1894/1894` and `210/210` exact matches | PASS |
| Bank clauses (1) and (2) as of filing (`2026-10-18`) | `1842 < 1848 <= 1894 < 1895 < 1905` | `1842 < 1848 <= 1894 < 1895 < 1905` | PASS |

pass: true
