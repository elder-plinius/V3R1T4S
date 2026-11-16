# Pre-Registration: bivariate-bicycle-exact-distance-360-756

frozen_utc: 2026-11-15T16:12:45Z
target_id: bivariate-bicycle-exact-distance-360-756
null_test: not needed because exact algebraic/circuit certificate

## Exact Acceptance Rules Frozen Before Solver Execution
1. **Matrix & Rank Invariants (`GF(2)`)**:
   - Construct `H_X = [A | B]` and `H_Z = [B^T | A^T]` over `Z_l x Z_m` (`N = l * m`, `n = 2N`) from the exact polynomials specified in Bravyi et al. (`2308.07915`) and Symons-Rajput-Browne (`2511.13560`).
   - Verify `H_X * H_Z^T == 0 (mod 2)` and `k = n - rank(H_X) - rank(H_Z)` equals `12` (`n = 288, 360, 432, 504`) or `16` (`n = 756`).
2. **Partial Win `p1` Acceptance**:
   - An explicit binary vector `u` of length `n` satisfying `H_X u = 0 (mod 2)`, `rank([H_Z; u]) == rank(H_Z) + 1` over `GF(2)` (strictly outside the stabilizer row space), and Hamming weight strictly below the published upper bound (`wt(u) <= 23` for `n = 360` or `432`, `wt(u) <= 29` for `n = 504`, or `wt(u) <= 33` for `n = 756`).
3. **Lower-Bound / Exact-Distance Rule**:
   - No heuristic or budget-stopped run may be claimed as a lower bound; any lower bound (`p3` or main criterion) requires a complete, unbudgeted exhaustive certificate corroborated by an independent second method or DRAT/LRAT proof.
