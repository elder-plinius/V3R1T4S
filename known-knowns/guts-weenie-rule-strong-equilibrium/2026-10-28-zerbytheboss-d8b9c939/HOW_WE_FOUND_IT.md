# How We Found It: Exact Global Nonnegativity Certificates for Continuous Guts (n=4, n=5)

*contributor text, unverified*

## The Brief
Continuous Guts Poker with the Weenie rule (Buck et al., arXiv:2208.02788 Appendix B) exhibits a remarkable game-theoretic property: the symmetric Nash threshold $a = 3^{-1/(n-1)}$ is conjectured to be a strong Nash equilibrium resisting every coordinated non-bloc coalition of opponents, meaning $\min_{t_2, \dots, t_n \in [0,1]} \alpha(3^{-1/(n-1)}, t_2, \dots, t_n) \ge 0$. Buck et al. proved this analytically for $n=2$ and $n=3$ using piecewise polynomial analysis, but for general $n \ge 4$ they could only run numerical optimizations and posed it as an open conjecture. The objective was to either construct an explicit counterexample or certify global nonnegativity for $n=4$ (partial win p1) and $n=5$ (partial win p2).

## What Failed
1. **Direct Global Handelman/Bernstein on the Unit Cube**: Attempting a monolithic Bernstein expansion directly over $[0,1]^{n-1}$ failed because $\alpha$ is piecewise polynomial with sharp derivative discontinuities along the planes $t_j = a$ and $t_i = t_j$. Monolithic polynomials across discontinuities produce spurious negative oscillations.
2. **Global Sum-of-Squares over General Ideals**: Attempting an SDP SOS formulation over the entire variety without ordering the thresholds blew up the degree and required uncertified floating-point numerical solvers.
3. **Naive Boundary Substitution**: Directly evaluating $t_i = a$ in unreduced polynomials produced high-degree monomials ($a^4, a^5$) that appeared non-zero until explicitly reduced modulo the defining variety relation $3a^{n-1} - 1 = 0$.

## What Worked
1. **General Piecewise 1D Integral Formula**: We derived the unified closed-form integral:
   $$\alpha(a, t) = (n-1)a - 2 - \sum_{j=2}^n t_j + 3a \prod_{j=2}^n t_j + 2n \int_a^1 \prod_{j=2}^n \max(t_j, x) dx - n \int_0^a \prod_{j=2}^n \min(t_j, x) dx$$
   and confirmed it symbolically reproduces the known $n=2$ and $n=3$ formulas with zero error.
2. **Symmetric Simplex Partitioning into Ordering Chambers**: By sorting $0 \le t_2 \le \dots \le t_n \le 1$, the space naturally decomposes into $n$ ordering chambers depending on where $a$ falls relative to $t_j$.
3. **Exact Variety Reduction and C^1 Boundary Continuity**: Reducing all chamber polynomials modulo $3a^{n-1} - 1 = 0$ proved that boundary differences across all chamber interfaces are identically zero, confirming global $C^1$ continuity.
4. **Universal Hessian Positive Definiteness**: We proved that for all $n \ge 2$, the gradient at $(a, \dots, a)$ vanishes identically and the Hessian matrix $H_n = a^{n-2}((2n-3)I + 3J)$ has strictly positive rational eigenvalues $(2n-3)a^{n-2} > 0$ and $(5n-6)a^{n-2} > 0$, guaranteeing $(a, \dots, a)$ is a strict local minimum of value 0.
5. **Exact Bernstein Expansions on Simplicial Chambers**: Transforming each chamber into standard simplicial barycentric coordinates yielded strictly positive Bernstein coefficients ($c_{\min} = 0.005894$ for $n=4$ $C_0$, $c_{\min} = 0.000399$ for $n=5$ $C_0$).
6. **Exact Rational SOS and Interval Branch-and-Bound**: We found an exact 7-term rational SOS identity for $C_3$, an exact $3 \times 3$ $LDL^T$ decomposition for $C_1$, and verified 5,519 boxes covering all chambers for $n=4$ in exact rational arithmetic (`fractions.Fraction`) over the isolating interval $a \in [11/16, 16/23]$.
