# PREREG: binary-action-games-max-nash-equilibria

- **Frozen timestamp (UTC)**: 2026-10-29T04:42:30Z
- **Target ID**: binary-action-games-max-nash-equilibria

## Criterion Verbatim
CONFIRMED by an explicit game with rational payoffs (for each of the n players a payoff table over the 2^n pure profiles) that is generic in the sense that every equilibrium is regular (for each equilibrium the indifference system of the players who mix has a nonsingular Jacobian there, and every pure-strategy best-response comparison at the equilibrium is strict) and that has (a) at least 39 Nash equilibria for n = 4, refuting Conjecture 4.5, or (b) at least 189 Nash equilibria for n = 5, exceeding both the formula value 185 and the printed 187. The full equilibrium list must be produced by exact support enumeration (all 3^n combinations of 'plays 0', 'plays 1', 'mixes' per player), each support's polynomial system solved exactly (Gröbner basis or resultants with certified real-root isolation), every candidate checked against all best-response inequalities in exact arithmetic, and the count reproduced by a second, independently written enumerator (for example one using a different computer algebra system). Since generic counts are odd, an even count signals an error. Alternatively, (c) a kernel-checked formal proof (Lean, Rocq/Coq or Isabelle, with no sorry, admit or extra axioms, and an axiom audit) that mu(4) <= 63 is also a full win; a written or computer-assisted upper-bound argument whose analytic steps are not formalised does not count. For the equilibrium-count constructions, also beat any higher count from later published games or valid compositions of published games with the same total player count. Disclose whether the game is a composition and cite its components. Unmerged submissions are not bars.

Partial win p1 verbatim:
An explicit generic 4-player binary-action game with rational payoffs and exactly 37 equilibria, every equilibrium listed with exact algebraic coordinates and certified as in the success criterion. The published lower bound is proved by a deformation argument; an explicit certified example makes it checkable by anyone and gives the search a verified starting point.

## Exact Statistic and Checker
The statistic is the exact integer count $N_{eq}$ of regular Nash equilibria of a generic rational binary-action game across all $3^4 = 81$ supports.
Every claimed equilibrium $x^* \in [0, 1]^4$ must satisfy:
1. Exact indifference for mixing players: $\Delta^i(x^*_{-i}) = 0$ for all $i$ with $x^*_i \in (0, 1)$.
2. Strict best-response for pure players: $\Delta^i(x^*_{-i}) < 0$ for $x^*_i = 0$, and $\Delta^i(x^*_{-i}) > 0$ for $x^*_i = 1$.
3. Regularity: $\det(J) \neq 0$ where $J = [\partial \Delta^i / \partial x_j]_{i, j \in S_M(x^*)}$.
4. Exact algebraic / rational coordinates: certified by exact rational arithmetic or root isolating intervals.
5. Verification by two independently implemented support enumeration solvers.

## Thresholds
- $N_{eq} \ge 37$ regular equilibria: satisfies partial win p1.
- $N_{eq} \ge 39$ regular equilibria: satisfies full win (CONFIRMED_SOLUTION).
- Any even count $N_{eq} \equiv 0 \pmod 2$: immediate invalidation / bug detection.

## Null Design
null_test: not needed because an explicit algebraic game checked by two independent deterministic support-enumeration solvers against exact rational payoff tables and published theorems is verified deterministically without statistical inference.
