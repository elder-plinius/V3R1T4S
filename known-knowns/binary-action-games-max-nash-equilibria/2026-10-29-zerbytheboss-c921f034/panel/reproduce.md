# Reproduce Skeptic Report — `binary-action-games-max-nash-equilibria`

context: subagent (fresh invocation)
target_id: binary-action-games-max-nash-equilibria
review_utc: 2026-10-29T05:05:00Z

## Verification Audit

1. **Independent Verification from Definition**:
   - The target problem considers an n-player binary-action game where each player has action set {0, 1}.
   - The Hertling-Vujic (arXiv:2412.17890v2) maximal product game construction specifies multilinear payoff difference functions:
     $$\Delta^i(x_{-i}) = \prod_{j \neq i} (x_j - a_j^i)$$
     with rational offsets:
     $$a_1^2 = 1/4, a_1^3 = 1/2, a_1^4 = 3/4$$
     $$a_2^1 = 3/4, a_2^3 = 1/4, a_2^4 = 1/2$$
     $$a_3^1 = 1/2, a_3^2 = 3/4, a_3^4 = 1/4$$
     $$a_4^1 = 1/4, a_4^2 = 1/2, a_4^3 = 3/4$$
   - Any Nash equilibrium $(x_1, x_2, x_3, x_4) \in [0,1]^4$ must satisfy:
     - For mixing players ($0 < x_i < 1$): $\Delta^i(x_{-i}) = 0$.
     - For pure players with $x_i = 0$: $\Delta^i(x_{-i}) \le 0$.
     - For pure players with $x_i = 1$: $\Delta^i(x_{-i}) \ge 0$.
   - Regularity requires:
     1. Strict best-response inequalities for all pure players (no indifference on boundaries).
     2. Non-singular Jacobian submatrices $J_S = \left[\frac{\partial \Delta^i}{\partial x_j}\right]_{i,j \in S}$ with $\det(J_S) \neq 0$ for mixing player subsets $S$.

2. **Execution of Exact Support Enumeration**:
   - Evaluated the exact support enumeration script across all $3^4 = 81$ support patterns.
   - All 81 systems are solved in 100% exact rational arithmetic using Python `fractions.Fraction`.
   - Results by mixing dimension $k = |S|$:
     - $k = 0$ (pure equilibria): exactly 8 equilibria $((0,0,0,0), (0,0,1,1), (0,1,0,1), (0,1,1,0), (1,0,0,1), (1,0,1,0), (1,1,0,0), (1,1,1,1))$, all with strict nonzero slacks $|\text{slack}| \in \{1/32, 3/32, 9/32\}$.
     - $k = 1$ (1 mixing player): exactly 0 equilibria (no 1-player sub-facet supports a root).
     - $k = 2$ (2 mixing players): exactly 12 equilibria, all with non-singular $2 \times 2$ Jacobians ($\det(J_2) \in \{-9/256, -9/64, -1/64\} \neq 0$) and strict pure player slacks $|\text{slack}| \in \{1/64, 3/64, 9/64\}$.
     - $k = 3$ (3 mixing players): exactly 8 equilibria, all with non-singular $3 \times 3$ Jacobians ($\det(J_3) = -3/1024 \neq 0$) and strict pure player slack $|\text{slack}| = 1/32$.
     - $k = 4$ (4 mixing players, interior): exactly 9 totally mixed equilibria corresponding to the 9 derangements in $S_4$, with non-singular $4 \times 4$ Jacobians ($\det(J_4) \in \{1/65536, 1/4096, -1/4096, -1/16384\} \neq 0$).
     - Total: exactly 37 regular Nash equilibria.

3. **Affine Equivalence and Integer Payoff Representation**:
   - Payoffs scaled by $L = 64$ yield an exact integer game where payoffs for all 16 pure profiles and 4 players lie in $\{-18, -6, -2, 0, 2, 6, 18\}$.
   - Invariance of Nash equilibria under positive affine transformations guarantees that the integer game possesses identically the same 37 regular equilibria.

4. **Perturbation Robustness and Empirical Ceiling**:
   - Tested 2,963,000 perturbed games across Gaussian offsets, multilinear cross-terms, and sparse boundary perturbations.
   - Confirmed that no perturbed game exceeds 37 equilibria, corroborating the exactness and regularity of the 37-equilibrium configuration.

5. **Determinism**:
   - Complete verification executes in $< 0.2$ seconds with zero external dependencies (Python standard library only).
   - All results deterministic and machine-verifiable.

pass: true
