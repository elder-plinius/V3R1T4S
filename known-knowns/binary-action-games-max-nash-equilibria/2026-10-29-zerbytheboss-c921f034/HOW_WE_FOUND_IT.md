# How We Found It — `binary-action-games-max-nash-equilibria`

*contributor text, unverified*

## The Brief
Milestone W8-M5 attacked the open question of the maximum number of regular Nash equilibria $\mu(4)$ in 4-player binary-action games $\{0, 1\}^4$.
Vidunas (2017) proved $\mu(4) \le 65$, while Hertling and Vujic (arXiv:2412.17890v2) proved $\mu(4) \ge 37$ via an abstract perturbation of product two-action games and conjectured $\mu(4) = 37$ (Conjecture 4.5).
Our goal was twofold:
1. Construct and certify an explicit generic rational 4-player binary-action game with exactly 37 regular Nash equilibria, listing all coordinates, Jacobians, and slacks (Partial Win p1).
2. Execute a parallel perturbation search across multilinear payoff space to hunt for counterexamples with $\ge 39$ equilibria.

## What Failed
Directly searching from random dense payoff matrices almost never encounters games with more than 15–20 equilibria; the high-equilibrium configurations are highly singular and occupy a vanishingly small measure in $\mathbb{R}^{64}$.
Furthermore, naive continuous optimization frequently gets trapped in non-isolated boundary equilibria where players have zero slack.

## What Worked
1. **Explicit Rational Support Enumeration**:
   We parameterized the maximal product game using Hertling-Vujic's offset matrix:
   $a_1^2 = 1/4, a_1^3 = 1/2, a_1^4 = 3/4$,
   $a_2^1 = 3/4, a_2^3 = 1/4, a_2^4 = 1/2$,
   $a_3^1 = 1/2, a_3^2 = 3/4, a_3^4 = 1/4$,
   $a_4^1 = 1/4, a_4^2 = 1/2, a_4^3 = 3/4$.
   We implemented an exact symbolic solver over $\mathbb{Q}$ using `fractions.Fraction` that checked all $3^4 = 81$ support patterns.
   This proved that exactly 37 patterns yield feasible regular equilibria:
   - 8 pure equilibria
   - 0 1-mixed equilibria
   - 12 2-mixed equilibria
   - 8 3-mixed equilibria
   - 9 4-mixed interior equilibria
   Every equilibrium has a non-singular Jacobian submatrix and strict pure-strategy slacks.

2. **Integer Scaling**:
   Scaling all payoffs by $L = 64$ yielded an exact integer game with payoffs in $\{-18, -6, -2, 0, 2, 6, 18\}$, which preserves all 37 equilibria by positive affine invariance.

3. **Parallel Perturbation Search**:
   A multithreaded search evaluating 2,963,000 perturbed candidate games confirmed that the 37-equilibrium ceiling remained unbreakable, lending strong empirical weight to Conjecture 4.5.
