# Preregistration: `game-of-sloanes-complex-line-packings`

- Date: 2026-10-30T06:25:00Z
- Target ID: `game-of-sloanes-complex-line-packings`
- Frozen Success Criterion:
  Success means n unit vectors in C^d, 3 <= d <= 7, for a (d,n) row of the live leaderboard (https://github.com/gnikylime/GameofSloanes README table, re-fetched live immediately before claiming) whose coherence mu = max_{j<k} |<phi_j,phi_k>|, computed in mpmath at 40 digits after normalising each vector, is STRICTLY LOWER (direction: min) than the listed 'Best Coherence' by at least 1e-8 (the table's resolution and the maintainers' stated acceptance threshold), the row is not marked provably optimal, mu is at least the listed lower bound (a value below it means a bug), and the vectors are given to >= 16 significant digits in the repository's file format (real parts of all vectors vector-by-vector, then imaginary parts).
- Exact Checker:
  mpmath 40 decimal digits precision evaluator computing pairwise Hermitian inner products $|\langle \phi_j, \phi_k \rangle| = \left|\sum_{m=1}^d \overline{\phi_{j, m}} \phi_{k, m}\right|$ after Euclidean vector normalization $\|\phi_j\|_2 = 1$.
- Decision Threshold:
  $\mu_{\text{candidate}} \le \mu_{\text{leaderboard}} - 10^{-8}$ and $\mu_{\text{candidate}} \ge \mu_{\text{lower\_bound}}$.
- Null Design:
  null_test: not needed because deterministic geometric optimization verified by exact mpmath 40-digit coherence calculation against table value.
