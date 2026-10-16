# PREREG (frozen before any attack output of this run is scored)
frozen_at (date -u): see first line written by command below
Thu Oct 15 13:14:30 UTC 2026

## Criterion (verbatim from bank, three-player-von-neumann-poker-equilibrium)
For b = 2 in the game exactly as defined in arXiv:2407.16155 Section 4 (II and III decide without observing each other's decision), EITHER (A) a proof, by exact symbolic computation verified by an independent checker or by a machine-checked proof, that the profile (A, B, C) defined by the paper's Eq. A-C (with A, B, C given as exact real algebraic numbers, isolating intervals included) is a Nash equilibrium: for every hand value, each player's prescribed action is a best response against the other two, over ALL measurable deviations; OR (B) a refutation: an explicit hand interval and deviation for one player that strictly improves that player's payoff against the other two players' profile, certified in exact or interval arithmetic. Direction: settle, either way. In case (A) the exact game value at b = 2 must be stated as an algebraic number matching 0.122557074714865 to the digits given.

Partial win p1 (verbatim): Settle the same question for every b > 0 (or for every b in a stated interval containing 2): a symbolic proof that the threshold profile from Eq. A-C is (or, for a certified explicit b, is not) a Nash equilibrium.

## What this run scores and how
1. Panel of lane X2's frozen claim (copied byte for byte into claim/, MANIFEST.json sha256s verified): three fresh
   Opus subagents (REPRODUCE, NOVELTY, CRITERION), each seeing only claim/. Gate per kit/RUN.md step 7.
2. Own lenses: statistic = sign of each player's action advantage (prescribed minus alternative) as an exact
   function of own hand, against the fixed other two. Equilibrium holds iff advantage >= 0 for almost every hand,
   for each player (pointwise optimality a.e. is equivalent to optimality over all measurable deviations because
   payoffs are linear in the behavioural strategy and the hand density is product-uniform).
   Thresholds: exact (sympy rational / algebraic, Sturm or root isolation); any float result is NUMERICAL only.
3. Literal digit clause: the exact b=2 value, rounded to 15 decimals, must equal 0.122557074714865 for case (A).
   Decided by exact interval arithmetic, no tolerance.
4. A refutation (case B) needs an explicit interval and deviation with strictly positive gain, certified exactly.

null_test: not needed because every claim here is an explicit mathematical object (algebraic thresholds and
polynomial sign certificates) checked by deterministic exact checkers, not a search or statistical score.
