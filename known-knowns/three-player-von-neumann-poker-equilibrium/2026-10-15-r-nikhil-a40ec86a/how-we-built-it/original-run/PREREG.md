timestamp: 2026-10-15T08:29:45.681217+00:00

For b = 2 in the game exactly as defined in arXiv:2407.16155 Section 4 (II and III decide without observing each other's decision), EITHER (A) a proof, by exact symbolic computation verified by an independent checker or by a machine-checked proof, that the profile (A, B, C) defined by the paper's Eq. A-C (with A, B, C given as exact real algebraic numbers, isolating intervals included) is a Nash equilibrium: for every hand value, each player's prescribed action is a best response against the other two, over ALL measurable deviations; OR (B) a refutation: an explicit hand interval and deviation for one player that strictly improves that player's payoff against the other two players' profile, certified in exact or interval arithmetic. Direction: settle, either way. In case (A) the exact game value at b = 2 must be stated as an algebraic number matching 0.122557074714865 to the digits given.

Scope frozen: one claim only, b=2, branch A exact equilibrium verification (or branch B if a certified profitable interval is found). No claim about uniqueness or the optimum bet.

Statistic/checker: exact polynomial identities for all action-payoff differences; rational isolation of A, B, C and the value; exact sign certificates on every breakpoint interval covering [0,1]. Acceptance requires prescribed actions to maximize payoff pointwise, with ties allowed, and an explicit argument covering arbitrary measurable randomized deviations. A floating sample or a finite-deck result alone cannot pass. Reject any nonzero regret interval.

Calibration: exact two-player b=2 cutoffs and value 1/9; three-player finite deck n=4, b=1 published profile and values 1/24,-1/48,-1/48, plus a deliberately exploitable profile.

null_test: not needed because the proposed result is an explicit deterministic algebraic proof certificate checked over the entire hand domain, not a statistical or search-based beats-chance claim. Numerical and finite-grid diagnostics cannot establish success. Mutation tests are checker tests, not a null-model novelty claim.

Resource plan: two lenses, certifier and adversary. At most four CPU threads, low-priority capped long jobs, under 7 GB RAM and 6 GB new disk. Light budget about 60 minutes; no new research line after 48 minutes.
