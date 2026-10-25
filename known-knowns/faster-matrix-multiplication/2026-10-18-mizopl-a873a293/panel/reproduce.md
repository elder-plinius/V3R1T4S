# Panelist Report: REPRODUCE

role: REPRODUCE
context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
target: fmm-ternary-integer-ring-upgrade
claimed_object: object/9x12x14_m954_ZT.json

## 1. Quoted Mathematical Definition and Bank Criterion

Quoting the verbatim `fmm-ternary-integer-ring-upgrade` criterion and the Brent (1970) bilinear matrix multiplication equations:

"Success means an explicit bilinear scheme for a format `(n,m,p)` with `max(n,m,p)` at most `16` and `sorted(n,m,p) != (4,4,4)`, whose coefficients all lie in `{-1,0,1}` (ternary, `ZT`) or all in `Z` (integer), with rank `r` such that:
1. `r` is STRICTLY LESS (direction: min) than the `ZT rank` (for a ternary claim) or the `Z rank` (for an integer claim) listed for that format in `dronperminov/FastMatrixMultiplication` `README.md` re-fetched live immediately before claiming;
2. `r` is GREATER THAN OR EQUAL to the minimum over the live `ZT`/`Z`/`Q` columns for that format and to the live `fmm_sota.json` rank, i.e. the scheme does NOT beat the overall best rank (a scheme that does is the catalogue target `fmm-catalogue-small-format-rank`, never both);
3. no scheme of rank at most `r` in the same coefficient class already exists in the live `schemes/results/ZT` (or `/Z`) directory of that repository or in `MerlijnW70/fmm-schemes`;
4. the Brent equations are verified exactly over `Z` with integer arithmetic (so the scheme is valid over every ring), not merely mod 2."

For matrix multiplication of $A \in \mathbb{Z}^{n_1 \times n_2}$ and $B \in \mathbb{Z}^{n_2 \times n_3}$ into $C = A B \in \mathbb{Z}^{n_1 \times n_3}$ (represented in trace form $\operatorname{Tr}(A B C^T)$ with $U \in \mathbb{Z}^{m \times (n_1 n_2)}$, $V \in \mathbb{Z}^{m \times (n_2 n_3)}$, $W \in \mathbb{Z}^{m \times (n_3 n_1)}$), the exact integer Brent equations require that for all $i_1, j_1 \in \{0, \dots, n_1 - 1\}$, $i_2, j_2 \in \{0, \dots, n_2 - 1\}$, and $i_3, j_3 \in \{0, \dots, n_3 - 1\}$:
$$\sum_{q=0}^{m-1} U[q, i_1 n_2 + i_2] \, V[q, j_2 n_3 + i_3] \, W[q, j_3 n_1 + j_1] = \delta_{i_1, j_1} \, \delta_{i_2, j_2} \, \delta_{i_3, j_3}.$$

## 2. Independent Checker Written Before Reading Author Code

Before viewing `verify-it-yourself/check_9x12x14.py`, I wrote an independent exhaustive verifier directly from the mathematical definition above using `numpy` `int64` exact integer arithmetic.

### Self-Test Controls
1. **Positive control A (Naive `(2,2,2)` rank 8):** Verified `m = 8`, `max_abs = 1`, `zero_terms = 0`, all `64` Brent equations over $\mathbb{Z}$ (`mismatches = 0`), and `20` random exact integer matrix multiplication trials $C = A B$ and $\operatorname{Tr}(A B C')$.
2. **Positive control B (Strassen `(2,2,2)` rank 7):** Verified `m = 7`, `max_abs = 1`, `zero_terms = 0`, all `64` Brent equations over $\mathbb{Z}$ (`mismatches = 0`), and `20` random exact integer matrix multiplication trials.
3. **Negative control A (Corrupted Brent entry):** Setting `U[0][0] = 0` in Strassen `(2,2,2)` is caught and rejected (`ValueError: Brent equations failed`).
4. **Negative control B (Non-ternary entry):** Setting `U[0][0] = 2` is caught and rejected under `require_zt=True` (`ValueError: Coefficient out of ZT = {-1, 0, 1} range: max_abs = 2`).
5. **Negative control C (Degenerate all-zero rank-1 term):** Appending an all-zero row to `U` is caught and rejected (`ValueError: Found 1 degenerate rank-1 terms`).

### Independent Verification of `object/9x12x14_m954_ZT.json` (Two Runs for Determinism)

- **Run 1 output:**
  `INDEP_SELF_TEST: PASS (2 positive controls: naive 2x2x2 rank 8, Strassen 2x2x2 rank 7; 3 negative controls: corrupted entry, non-ZT entry=2, zero row)`
  `INDEP_CHECK PASS: file=9x12x14_m954_ZT.json bytes=915296 sha256=a873a293abc4e1b7c659250591e544062ad26ca556af28f29b25e63998355b02 n=(9, 12, 14) m=954 max_abs=1 zero_terms=0 nnz=(5936, 7599, 5124) complexity=16625 strings_verified=True brent_eqs=2286144 ones=1512 zeros=2284632 mismatches=0 bilinear_trials=20 verify_time=2.3537s total_time=2.4046s`
- **Run 2 output:**
  `INDEP_SELF_TEST: PASS (2 positive controls: naive 2x2x2 rank 8, Strassen 2x2x2 rank 7; 3 negative controls: corrupted entry, non-ZT entry=2, zero row)`
  `INDEP_CHECK PASS: file=9x12x14_m954_ZT.json bytes=915296 sha256=a873a293abc4e1b7c659250591e544062ad26ca556af28f29b25e63998355b02 n=(9, 12, 14) m=954 max_abs=1 zero_terms=0 nnz=(5936, 7599, 5124) complexity=16625 strings_verified=True brent_eqs=2286144 ones=1512 zeros=2284632 mismatches=0 bilinear_trials=20 verify_time=2.4238s total_time=2.4555s`

### Exhaustive Property Checklist Verified
- **Object file integrity:** `object/9x12x14_m954_ZT.json` has exact size `915,296` bytes and SHA-256 `a873a293abc4e1b7c659250591e544062ad26ca556af28f29b25e63998355b02`, matching `README.md` and `RUN_IT_YOURSELF.md`.
- **Format and rank:** `n = [9, 12, 14]` (`max(9, 12, 14) = 14`, which is at most `16`, and `sorted(9, 12, 14) != (4, 4, 4)`), rank `m = 954`, array shapes `U: (954, 108)`, `V: (954, 168)`, `W: (954, 126)`.
- **Ternary ring (`ZT`):** Every entry of `U`, `V`, and `W` is a Python `int` in `{-1, 0, 1}` (`unique(U) = unique(V) = unique(W) = [-1, 0, 1]`, `max_abs = 1`), with `zero_terms = 0` degenerate rank-1 terms.
- **Support and naive additive complexity:** `nnz(U) = 5936`, `nnz(V) = 7599`, `nnz(W) = 5124`, giving naive additive complexity `(5936 - 954) + (7599 - 954) + (5124 - 126) = 16625`, matching `"complexity": 16625` and `"z2": false`.
- **Algebraic string consistency:** All `954` strings in `"multiplications"` and all `126` strings in `"elements"` match the linear forms regenerated from `U`, `V`, `W` character-for-character (`strings_verified = True`).
- **Exhaustive Brent equations over $\mathbb{Z}$:** All `108 * 168 * 126 = 2,286,144` equations hold in exact `int64` arithmetic with `mismatches = 0` (`1,512` ones on the Kronecker-delta support $9 \times 12 \times 14 = 1512$ and `2,284,632` zeros elsewhere).
- **Direct bilinear and trilinear evaluation:** Across `20` seeded random `int64` matrix triples $(A, B, C')$ with entries in `[-1000, 1000]`, the scheme reproduces $C = A B$ and $\operatorname{Tr}(A B C')$ with zero error.
- **Construction decomposition:** The `954` rank-1 terms decompose into `52 * 15 = 780` unpaired product terms plus `6 * 29 = 174` bud-paired terms (`780 + 174 = 954`), saving `6` multiplications over the `64 * 15 = 960` Kronecker product baseline while remaining strictly inside `ZT = {-1, 0, 1}`.
- **Benchmark records (`the-record-we-beat/RECORD.md`):**
  - Perminov `README.md` / `docs/ranks.md` as listed on 2026-10-18 (`ZT 960, Z 960`, `Q 940`), confirming `954 < 960` (Clause 1) and `954 >= 940` (Clause 2).
  - Sedoglavic `fmm_sota.json` (`sha256: d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1`) lists `{"format": [9, 12, 14], "rank": 940, "exponent": 2.805233}`, confirming `954 >= 940` (Clause 2).

## 3. Inspection and Execution of Package Checker (`sh verify-it-yourself/run_checks.sh`)

After completing the independent verification above, I read `verify-it-yourself/check_9x12x14.py` and ran `sh verify-it-yourself/run_checks.sh` twice:

- **Run 1 & Run 2 output:**
  `control_positive_strassen_2_2_2: PASS (64/64 equations, mismatches=0)`
  `control_negative_corrupted_brent: PASS (rejected)`
  `control_negative_non_zt_coeff: PASS (rejected)`
  `sha256=a873a293abc4e1b7c659250591e544062ad26ca556af28f29b25e63998355b02`
  `format=9x12x14 rank=954 ring=ZT max_abs=1 zero_terms=0`
  `previous_zt_record=960 previous_z_record=960 overall_q_record=940 delta_zt=-6`
  `total_brent_equations=2286144 mismatches=0`
  `PASS`

Both the independent checker and the package checker pass deterministically with zero mismatches across all `2,286,144` exact integer Brent equations.

pass: true
