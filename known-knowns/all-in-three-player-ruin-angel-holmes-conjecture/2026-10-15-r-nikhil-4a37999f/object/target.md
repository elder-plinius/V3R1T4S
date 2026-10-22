id: all-in-three-player-ruin-angel-holmes-conjecture

Success criterion (verbatim):
Settle Angel-Holmes Conjecture 9 as stated in arXiv:2410.15329 Section 5.3 (direction: settle, either way), for the game exactly as defined in that paper's abstract and Section 1. EITHER (A) COUNTEREXAMPLE: explicit positive rationals x < y and z with f(x, y, z) <= f(y, y, z), proved by rigorous enclosures: f(s) lies in [h_n(s), h_n(s) + 2^-n] where h_n(s) is the exact (rational) probability that player 1 is eliminated first within n rounds, so it suffices to exhibit n with h_n(x, y, z) + 2^-n <= h_n(y, y, z), computed in exact rational arithmetic (or interval arithmetic with directed rounding) by a checker that shares no code with the search. OR (B) PROOF: a machine-checked proof (Lean, Coq or Isabelle, no sorry/axioms) or a computer-assisted proof whose certificate (region partition plus the bounds used in each region, in exact arithmetic) is verified by an independent checker, that f(x, y, z) > f(y, y, z) for ALL real x, y, z > 0 with x < y.

Partial p1 (verbatim):
A certified computer-assisted proof of Conjecture 9 on one of the three orderings of z separately, with an independently verified certificate: z >= y (player 3 is the chip leader), or z <= x (player 3 is the shortest), or x < z < y. All three together are the full win (B).
