# Pre-Registration: qrac-n-to-1-shared-randomness-optimality

- **Frozen UTC**: `2026-11-15T14:10:42Z`
- **Target ID**: `qrac-n-to-1-shared-randomness-optimality`
- `null_test: not needed because exact mathematical certificate (rigorous outward-rounded interval branch-and-bound proof over a complete dyadic cover of the parameter domain, deterministically checked in arbitrary-precision interval arithmetic)`

## Verbatim Success Criterion and Partial Wins

- **Full win**: Success means EITHER (a) a rigorous, independently re-checkable proof that the optimal n-to-1 QRAC with SR for n = 4 has p <= 0.741481 + 1e-6, i.e. that max over unit vectors v_1..v_4 in R^3 of S/(4*2^5) + 1/2 does not exceed that value (interval-arithmetic branch-and-bound with a posted cover of the parameter domain, an exact SOS certificate, or a machine-checked proof); OR (b) n unit vectors in R^3 for some n in 4..9 whose p, computed in mpmath at 40 digits from the formula above, is STRICTLY GREATER (direction: max) than the arXiv:0810.2937 Table 2 value for that n by at least 1e-6 (re-fetch Tan-Jafar arXiv:2607.10414 and search arXiv before claiming, in case a newer value or proof exists).
- **Partial win p1**: A rigorous certified upper bound p(4) <= 0.745 for the 4-to-1 QRAC with SR (strictly below the proven 0.75), re-checkable as in (a).
- **Partial win p2**: A rigorous optimality proof, as in (a), for n = 5 (0.713578) or n = 6 (0.694046) within 1e-6.

## Exact Mathematical Quantity and Thresholds Frozen Before Execution

For `n` unit vectors `v_1, ..., v_n in S^2 subset R^3`, define

$$S(v_1, \dots, v_n) = \sum_{x \in \{-1, +1\}^n} \left\| \sum_{i=1}^n x_i v_i \right\|_2, \qquad p(v_1, \dots, v_n) = \frac{1}{2} + \frac{S(v_1, \dots, v_n)}{n \cdot 2^{n+1}}.$$

- **Calibration checks required first**:
  1. For `n = 2` and orthogonal unit vectors `v_1 = (1, 0, 0), v_2 = (0, 1, 0)`, `p(v_1, v_2) = 1/2 + sqrt(2)/4 = 0.8535533905932737622...` (matches `0.853553`).
  2. For `n = 4` and the Ambainis et al. disphenoid/rectangular configuration, `p = 1/2 + (1 + sqrt(3)) / (8 * sqrt(2)) = 0.7414814565722670904...` (matches `0.741481`).
  3. Negative calibration check: in `R^4`, four orthonormal vectors give `p = 0.75 > 0.741482`, confirming a valid `R^3` checker must reject bounds exceeding the threshold or incomplete domain covers.

- **Certification threshold for full win (a)**:
  - Strict certified upper bound `U_cert <= 0.741481 + 1e-6 = 0.741482` (specifically targeting `U_cert <= 0.7414816 < 0.741482`) across an exact, gap-free dyadic partition of the symmetry-reduced fundamental domain of `(S^2)^4`, verified independently by a standalone Python `mpmath.iv` checker at `>= 100` bits of working precision.
  - Every file in `object/` must be plain machine-readable text strictly under `1,000,000` bytes (`< 1 MB`), and corrupting any digit in the certificate must cause `verify-it-yourself/run_checks.sh` to exit nonzero and print `FAIL`.

- **Secondary threshold for partial win p2 (if attempted after full win (a))**:
  - Strict certified upper bound `U_cert(5) <= 0.713578 + 1e-6 = 0.713579` across an exact dyadic cover of the symmetry-reduced fundamental domain of `(S^2)^5`.

## Baseline Reproduction Note

Not an empirical benchmark on a dataset (`kit/RUN.md` step 3c: an explicit mathematical certificate checked by a deterministic arbitrary-precision interval checker against an exact mathematical threshold needs no dataset baseline). Calibration against the analytical values `n = 2` (`0.853553...`) and `n = 4` (`0.7414814565...`) from `arXiv:0810.2937` is built directly into the standalone verifier.
