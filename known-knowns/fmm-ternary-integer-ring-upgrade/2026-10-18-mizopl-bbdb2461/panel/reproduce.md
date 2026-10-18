# Panelist Report — REPRODUCE

role: REPRODUCE
context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
target: fmm-ternary-integer-ring-upgrade
format: 14x15x15
claimed_rank: 1894
ring: ZT

## 1. Quoted Definition and Bank Criterion (from `claim/CLAIM.md`)

Verbatim bank criterion (`fmm-ternary-integer-ring-upgrade`) quoted from `claim/CLAIM.md`:

> Success means an explicit bilinear scheme for a format `(n,m,p)` with `max(n,m,p) <= 16` and `sorted(n,m,p) != (4,4,4)`, whose coefficients all lie in `{-1,0,1}` (ternary, `ZT`) or all in `Z` (integer), with rank `r` such that:
> 1. `r` is STRICTLY LESS (direction: min) than the `ZT rank` (for a ternary claim) or the `Z rank` (for an integer claim) listed for that format in `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md` re-fetched live immediately before claiming;
> 2. `r` is GREATER THAN OR EQUAL to the minimum over the live `ZT`/`Z`/`Q` columns for that format and to the live `fmm_sota.json` rank, i.e. the scheme does NOT beat the overall best rank (a scheme that does is the catalogue target `fmm-catalogue-small-format-rank`, never both);
> 3. no scheme of rank `<= r` in the same coefficient class already exists in the live `schemes/results/ZT` (or `/Z`) directory of that repository or in `https://github.com/MerlijnW70/fmm-schemes`;
> 4. the Brent equations are verified exactly over `Z` with integer arithmetic (so the scheme is valid over every ring), not merely mod 2. Equalling the format's `Q` rank is the natural goal but any strict `ZT` or `Z` improvement satisfying (1)-(4) counts.

Exact integer Brent equations quoted from `claim/CLAIM.md` (Clause 4):

> For all `i1, j1 in 0..13`, `i2, j2 in 0..14`, `i3, j3 in 0..14` (`210 * 225 * 210 = 9,922,500` equations),
> $$\sum_{q=0}^{1893} U[q, i_1 \cdot 15 + i_2] \, V[q, j_2 \cdot 15 + i_3] \, W[q, j_3 \cdot 14 + j_1] = \delta_{i_1, j_1}\,\delta_{i_2, j_2}\,\delta_{i_3, j_3}$$
> holds over $\mathbb{Z}$ with `0` mismatches.

## 2. Independent Checker Written Before Reading Author's Code

Before reading `claim/author_checker_brent_check.py`, I wrote a standalone exhaustive checker `reproduce_work/indep_brent_check.py` directly from the mathematical definition above. The independent checker performs the following steps using exact 64-bit integer (`numpy.int64`) arithmetic:

1. **Self-tests on positive and negative controls:**
   - **Positive control:** Strassen's `(2, 2, 2)` rank-7 ternary scheme over $\mathbb{Z}$ (`64/64` Brent equations satisfied, `mismatches = 0`, `max_abs = 1`, `zero_terms = 0`).
   - **Negative control 1 (corrupted Brent tensor):** Flipping `W[0, 0]` from `1` to `0` in Strassen's `(2, 2, 2)` scheme is rejected with `mismatches = 4` out of `64`.
   - **Negative control 2 (non-ternary coefficient):** Setting `U[0, 0] = 2` is rejected by the `ZT` check with `max_abs = 2`.
   - **Negative control 3 (all-zero rank-1 factor):** Appending a rank-1 term with `U[q, :] = 0` is rejected with `zero_terms = 1`.
2. **File integrity checks:** Computes exact byte counts and SHA-256 digests of `claim/14x15x15_m1894_ZT.json`, `claim/perminov_README.md`, and `claim/fmm_sota.json`.
3. **Dense reconstruction and structural checks:** Reconstructs dense `int64` arrays $U \in \mathbb{Z}^{1894 \times 210}$, $V \in \mathbb{Z}^{1894 \times 225}$, and $W \in \mathbb{Z}^{1894 \times 210}$ from `u_sparse`, `v_sparse`, `w_sparse`, verifying bounds, absence of duplicate indices per factor, `max_abs = 1` (all coefficients in $\{-1, 0, 1\}$), `zero_terms = 0`, and naive addition count `(nnz(U) - m) + (nnz(V) - m) + (nnz(W) - 210) = 56959 == complexity`.
4. **Algebraic string cross-check:** Independently formats `u_sparse` and `v_sparse` into Perminov's `m1 .. m1894` polynomial multiplication strings and compares against all `1894` entries of `multiplications` (`0` mismatches), and parses all `210` output expressions `c11 .. c1415` in `elements` into a dense array `W_from_elements` and verifies `np.array_equal(W, W_from_elements) == True`.
5. **Exhaustive exact integer Brent equation check:** Contracts $T[a, b, c] = \sum_{q=0}^{1893} U[q, a] V[q, b] W[q, c]$ in exact `int64` arithmetic for all $210 \times 225 \times 210 = 9,922,500$ index triples $(a, b, c)$ and compares against the exact Kronecker delta tensor $\delta_{i_1, j_1} \delta_{i_2, j_2} \delta_{i_3, j_3}$ (`ones = 3150`, `zeros = 9919350`, `mismatches = 0`).
6. **Direct bilinear matrix multiplication evaluation:** Evaluates the bilinear scheme on `10` deterministic pseudorandom pairs of exact integer matrices $(A, B) \in \mathbb{Z}^{14 \times 15} \times \mathbb{Z}^{15 \times 15}$ with entries in $[-50, 50]$ (seed `20261018`) and verifies $C_{\text{scheme}} = A B$ entrywise over $\mathbb{Z}$ (`10/10` exact matches).
7. **Saved catalogue baseline checks:** Parses the `14x15x15` rows in `claim/perminov_README.md` (`ZT = 1905`, `Z = 1895`, `Q = 1848`) and the `[14, 15, 15]` entry in `claim/fmm_sota.json` (`rank = 1848`), confirming $1894 < 1905$ (strictly beats live `ZT` by `11`), $1894 < 1895$ (strictly beats live `Z` by `1`), and $1894 \ge 1848$ (does not beat overall best `Q` rank).

## 3. Independent Checker Execution (Run Twice for Determinism)

Running `reproduce_work/indep_brent_check.py` twice in succession produced identical results in `0.599s` (Run 1) and `0.544s` (Run 2):

```text
SELF_TEST: PASS (Strassen (2,2,2) positive: 64/64 eqs, mismatches=0; 3 negative controls rejected)
FILE_CHECK 14x15x15_m1894_ZT.json: bytes=944884 sha256=bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb
FILE_CHECK perminov_README.md: bytes=112671 sha256=7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341
FILE_CHECK fmm_sota.json: bytes=343798 sha256=d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1
SPARSE_STATS: nnz(U)=20861, nnz(V)=17726, nnz(W)=22370, total_nnz=60957, naive_additions=56959, json_complexity=56959
ALGEBRAIC_STRINGS_CHECK: PASS (1894 multiplications and 210 elements strings match u_sparse/v_sparse/w_sparse 100%)
BRENT_EQUATIONS: shape=(14, 15, 15), rank=1894, ring=ZT, max_abs=1, zero_terms=0, total_eqs=9922500, ones=3150, zeros=9919350, mismatches=0
DIRECT_MATMUL_TEST: PASS (10/10 exact integer 14x15 * 15x15 matrix pairs matched A @ B identically)
PERMINOV_README_ROW_1: | `14x15x15` |  1905 (`Z`)   |   [1848](schemes/results/Q/14x15x15_m1848_Q.json) (`Q`)    | **2.801382482** |
PERMINOV_README_ROW_2: | `14x15x15` |  1905 (?)   | 1895 (1905)  | 1848 (1905)  | **2.801382482** |
FMM_SOTA_BEST_RANK: {'format': [14, 15, 15], 'rank': 1848, 'exponent': 2.801382}
INDEP_CHECK_RESULT: PASS (elapsed=0.599s)
--- RUN 2 ---
SELF_TEST: PASS (Strassen (2,2,2) positive: 64/64 eqs, mismatches=0; 3 negative controls rejected)
FILE_CHECK 14x15x15_m1894_ZT.json: bytes=944884 sha256=bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb
FILE_CHECK perminov_README.md: bytes=112671 sha256=7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341
FILE_CHECK fmm_sota.json: bytes=343798 sha256=d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1
SPARSE_STATS: nnz(U)=20861, nnz(V)=17726, nnz(W)=22370, total_nnz=60957, naive_additions=56959, json_complexity=56959
ALGEBRAIC_STRINGS_CHECK: PASS (1894 multiplications and 210 elements strings match u_sparse/v_sparse/w_sparse 100%)
BRENT_EQUATIONS: shape=(14, 15, 15), rank=1894, ring=ZT, max_abs=1, zero_terms=0, total_eqs=9922500, ones=3150, zeros=9919350, mismatches=0
DIRECT_MATMUL_TEST: PASS (10/10 exact integer 14x15 * 15x15 matrix pairs matched A @ B identically)
PERMINOV_README_ROW_1: | `14x15x15` |  1905 (`Z`)   |   [1848](schemes/results/Q/14x15x15_m1848_Q.json) (`Q`)    | **2.801382482** |
PERMINOV_README_ROW_2: | `14x15x15` |  1905 (?)   | 1895 (1905)  | 1848 (1905)  | **2.801382482** |
FMM_SOTA_BEST_RANK: {'format': [14, 15, 15], 'rank': 1848, 'exponent': 2.801382}
INDEP_CHECK_RESULT: PASS (elapsed=0.544s)
```

## 4. Author's Checker Inspection and Reproduction (`claim/REPRODUCE.md`)

After completing the independent verification, I inspected `claim/author_checker_brent_check.py` (`209` lines, `7012` bytes) and executed the reproduction command from `claim/REPRODUCE.md` twice:

- Run 1 completed in `0.400s`:
  - Self-test (`Strassen (2,2,2)` positive + 2 negative controls): `PASS`
  - `PASS 14x15x15_m1894_ZT.json: shape=(14, 15, 15), rank=1894, ring=ZT (max_abs=1), brent_equations=9922500 (mismatches=0), sha256=bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb, time=0.400s`
  - `BRENT_CHECK: PASS`
- Run 2 completed in `0.414s` with identical output.

## 5. Re-derivation of the Construction Arithmetic in `claim/CLAIM.md`

- Base Kronecker product of $s_1 = (7, 5, 5)$ of rank `127` in `ZT` and $s_2 = (2, 3, 3)$ of rank `15` in `ZT` has rank $127 \times 15 = 1905$.
- Replacing `11` disjoint $v$-bud pairs of $s_1$ (each pair originally costing $2 \times 15 = 30$ multiplications) with `11` copies of the conjugated $(4, 3, 3)$ scheme $\pi \cdot s_3$ of rank `29` in `ZT` saves $30 - 29 = 1$ multiplication per pair, giving rank $1905 - 11 = 1894$.
- For any permutation $\pi$ of $\{0, 1, 2, 3\}$, $\delta_{\pi(r), \pi(r')} = \delta_{r, r'}$, so conjugating both $A$-rows and $C$-rows of the $(4, 3, 3)$ scheme by $\pi = (0, 1, 3, 2)$ preserves the exact matrix multiplication tensor while aligning signs so the combined scheme stays in `ZT = {-1, 0, 1}`.

## 6. Summary of Verified Properties

| Property | Expected | Measured | Status |
|---|---|---|---|
| `claim/14x15x15_m1894_ZT.json` bytes | `944884` | `944884` | PASS |
| `claim/14x15x15_m1894_ZT.json` SHA-256 | `bbdb2461...c2979bb` | `bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb` | PASS |
| `claim/perminov_README.md` bytes & SHA-256 | `112671`, `7b0761ec...7e78341` | `112671`, `7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341` | PASS |
| `claim/fmm_sota.json` bytes & SHA-256 | `343798`, `d0da2c36...bd244c1` | `343798`, `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1` | PASS |
| Format `n` and rank `m` | `[14, 15, 15]`, `1894` | `(14, 15, 15)`, `1894` | PASS |
| Coefficient ring (`ZT`) | `max_abs = 1`, `zero_terms = 0` | `max_abs = 1`, `zero_terms = 0` | PASS |
| Exact integer Brent equations over $\mathbb{Z}$ | `9,922,500` eqs, `0` mismatches | `9,922,500` eqs (`3,150` ones, `9,919,350` zeros), `0` mismatches | PASS |
| Direct exact integer matrix multiplication | `C_scheme == A @ B` | `10/10` exact integer trials matched | PASS |
| Algebraic strings (`multiplications`, `elements`) | Match `u_sparse, v_sparse, w_sparse` | `1894/1894` and `210/210` exact matches | PASS |
| Bank clauses (1) and (2) vs saved files | `1848 <= 1894 < 1905` | `1848 <= 1894 < 1895 < 1905` | PASS |

pass: true
