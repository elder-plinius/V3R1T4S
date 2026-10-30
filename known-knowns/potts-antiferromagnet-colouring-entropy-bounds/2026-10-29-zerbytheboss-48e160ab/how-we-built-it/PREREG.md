# PREREG: potts-antiferromagnet-colouring-entropy-bounds

Date: 2026-10-29T15:07:30Z

## Frozen Success Criterion
Success means a rigorous bound strictly improving one of the eight published bounds above (upper smaller or lower larger), by at least 1e-9 for W_sq(4) or W_sq(5) and at least 1e-6 for W_c(3) or W_c(4), with the transfer-matrix definition and a nonnegative test vector whose Collatz-Wielandt ratios (or the exact eigenvalue inequality used by Lundow and Markstrom, cited by equation) a skeptic recomputes in exact or outward-rounded arithmetic, AND an arXiv/Google Scholar search re-run immediately before claiming that finds no published bound at least as good.

## Partial Win Criteria
- p1: At least 15 decimals of W_sq(4) (or W_sq(5)) by two independent non-rigorous methods (corner transfer matrix or VUMPS, and strip transfer matrices with extrapolation), lying inside the Lundow-Markstrom bracket and agreeing with the series value 2.336056641 within 1e-9.
- p2: An independent reproduction of Lundow and Markstrom's eigenvalue table for 4-colourings of the square grid up to their largest width, with exact or multiprecision eigenvalues released as data.

## Statistical and Numerical Estimators
1. **Lens 1: S_q x Aut(G) Compressed Transfer Matrix**:
   - Construct state space of set partitions of boundary graph $G$ with $\le q$ blocks.
   - Quotient by spatial automorphisms $\text{Aut}(P_k) = \mathbb{Z}_2$, $\text{Aut}(C_k) = D_k$, or $\text{Aut}(C_k \times C_l) = D_k \times D_l \rtimes \mathbb{Z}_2$.
   - Form compressed transfer matrix $T_{i, j} = \sum_{\sigma \in \text{orbit}(j)} \mathbb{I}(\text{proper transition from } \tau_i \text{ to } \sigma)$.
   - Evaluate spectral radius $\lambda_0(T)$ via power iteration / Arnoldi iteration.
   - Match Table 2, Table 3, Table 4, Table 6, Table 9, Table 11 of Lundow & Markström (2008) to all published digits.
2. **Lens 2: Dual 60-Digit High-Precision Estimators (p1)**:
   - Method 1: Baxter Symmetric Corner Transfer Matrix Renormalization Group (CTMRG) on Interaction-Round-a-Face (IRF) colouring face tensor, bond dimension $\chi \in [24, 64]$, 80-digit mpmath precision.
   - Method 2: Strip sequence extrapolation of $w_k = \lambda(C_{2k})^{1/(2k)}$ for $2k \in [4, 18]$ via Wynn's $\epsilon$-algorithm in $1/k^2$.
   - Acceptance: Agreement between Method 1 and Method 2 to $\ge 20$ decimal places, lying strictly inside $[2.336056640723116, 2.33606820555777]$ for $q=4$ and $[3.2504049231640764, 3.250407145038276]$ for $q=5$.
3. **Lens 2: Collatz-Wielandt Rigorous Bound Improvement (CONFIRMED_SOLUTION)**:
   - Construct strictly positive test vector $v > 0$.
   - Compute matrix-vector product $w = T v$.
   - In exact / outward-rounded interval arithmetic, compute:
     $$\overline{\lambda} = \max_i \frac{w_i}{v_i}, \quad \underline{\lambda} = \min_i \frac{w_i}{v_i}$$
   - Apply upper bound inequality $W \le \overline{\lambda}^{1/(2k)}$ on cylinder $C_{2k}$ (or $\overline{\lambda}^{1/(4rt)}$ on torus $C_{2r} \times C_{2t}$).
   - Target improvement: $\Delta \ge 10^{-9}$ on square lattice (e.g. $C_{18}$ upper bound $\le 2.336061...$ vs published $2.33606820555777$, improvement $\approx 7 \times 10^{-6}$), or $\Delta \ge 10^{-6}$ on cubic lattice.

null_test: not needed because transfer matrix construction, Collatz-Wielandt min-max bounds, and CTMRG evaluations are deterministic mathematical computations verified against exact algebraic theorems and published ground-truth tables
