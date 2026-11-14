# Pre-Registration (`magic-state-stabilizer-rank-exponents`)

- `target_id`: `magic-state-stabilizer-rank-exponents`
- `frozen_utc`: `2026-11-09T09:05:00Z`
- `null_test`: `not needed because magic-state-stabilizer-rank-exponents is an exact algebraic stabilizer-rank decomposition and lower-bound problem verified by deterministic exact arithmetic in Z[i] and Z[omega_3]`
- `primary_criterion`: Exact computational-basis stabilizer state equality (`0` integer residual in $\mathbb{Z}[i]$ and $\mathbb{Z}[i, \sqrt{3}]$ across all $2^m$ bitstrings) for constructive decompositions, and exhaustive symmetry-reduced $D_3$ / $D_4$ slice-cover and Galois-quotient enumeration for lower-bound and subspace obstruction certificates (`p2`, `p3`).
- `planned_lenses`:
  1. `Lens 1 (Galois-Quotient & 135-Tableau Pauli-Fiber Slice Exhaustion)`: Exact $2$-dimensional Galois splitting over $\mathbb{Q}(i) \oplus \sqrt{2}\,\mathbb{Q}(i)$, $\mathbb{Q}(i) \oplus \sqrt{3}\,\mathbb{Q}(i)$, and $\mathbb{Q}(\omega_3) \oplus \sqrt{3}\,\mathbb{Q}(\omega_3)$, coupled with the 135-fiber bitwise-XOR slice homomorphism on $D_3$ (`1,080` states).
  2. `Lens 2 (Face-Cat Contraction, Multi-Block Symmetry & Tetrahedral/Tau-Invariant MILP)`: Exact Gaussian-rational contraction of even-parity face-cat states $|\text{cat}_{2k}(F)\rangle \in \mathbb{Z}[i]^{2^{2k}}$, block-symmetric `QlAb` LNS search, tetrahedral $A_4^\Delta$ word-algebra MILP, and $\tau$-invariant real MILP for qutrit magic states.
