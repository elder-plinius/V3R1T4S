# PREREG — Milestone W7-M4B

- Frozen UTC time: 2026-10-29T03:00:00Z
- null_test: not needed because deterministic game-theoretic equilibrium and graph computation

## Hypotheses & Targets
1. **Lens 1: GSP PoA Analysis**:
   - Hypothesis 1 (Calibrations): Exact rational verification of $n=2$ instance gives $5/4$, and Caragiannis et al. 3-bidder instance gives ratio $\ge 1.259133$.
   - Hypothesis 2 (p2 Certification): For $n=4$, all 24 rankings in $S_4$ satisfy $PoA_4(\pi) \le 1.259134$ under per-bidder no overbidding ($b_i \le v_i$).
   - Hypothesis 3 (Pure NE Search $n=4..8$): Bilinear/LP optimization over permutations for $n=4..8$ searches for pure Nash equilibria with ratio $> 1.259134$.
   - Hypothesis 4 (p1 CCE Construction): Linear programming over finite-support bid profile distributions enables constructing an exact rational CCE with $OPT / \mathbb{E}[SW] > 1.259134$.
2. **Lens 2: Shapley Network Design PoS**:
   - Hypothesis 1 (p1 Calibration): Disser et al. 5-vertex instance has unique pure Nash equilibrium with cost 1769, optimum cost 1126, and exact ratio $1769/1126 \approx 1.571048$.
   - Hypothesis 2 (p1 Potential-Optimal Family): 4-vertex family with parameter $\epsilon$ has unique potential minimum with ratio approaching $286/175 \approx 1.634286$ as $\epsilon \to 0$.
   - Hypothesis 3 (CONFIRMED_SOLUTION): Exact rational edge-cost LP optimization on 5-8 vertex topologies yields an explicit 3-player instance whose Price of Stability strictly exceeds $1769/1126$.

## Decision Rules
- GSP:
  - If a pure NE is found with $OPT/SW > 1.259134$, claim `solution_claim`.
  - If pure NE is certified $\le 1.259134$ for $n=4$ across all 24 rankings and CCE $> 1.259134$ is constructed, claim `partial_win_claim` for p1/p2.
- Shapley:
  - If an explicit instance is verified with $PoS > 1769/1126$ via exhaustive path/profile/deviation checking by two independent checkers, claim `solution_claim`.
