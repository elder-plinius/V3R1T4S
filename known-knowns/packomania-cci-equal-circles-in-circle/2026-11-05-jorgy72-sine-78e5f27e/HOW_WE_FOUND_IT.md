# How we found it (contributor text, unverified)

The N=4153 Packomania row was a jammed hexagonal packing by Eckard Specht — tight, but
a single hexagonal truncation among many. The posted seed turned out to be a strict
degenerate local optimum: its five smallest pairwise distances are all exactly
0.02919284 (degenerate lattice contacts), and the seed's basin jams exactly at the
table value.

So instead of polishing the seed, the search generated FRESH hexagonal truncations
(orientation θ, lattice spacing s, offset — 96,525 evaluations of the raw-truncation
objective: a 63,525-eval systematic grid, 3,000 refinements, and 30,000 full-cell
random draws), and deep-polished the best four diverse basins with a smooth-max
bottleneck optimizer (L-BFGS-B on logsumexp(α·overlaps)/α, ratcheting the radius to
the feasible value each round).

All four basins polished above the table — the win is a property of the row, not a
single lucky truncation. The best (theta 9.51 deg basin) polished from a raw
−2.042e-05 deficit to a certified +2.706e-06 surplus over the table — the curved
container wall, not the bulk, was where the density was hiding: the binding
constraint is the outermost center, not a close pair.

Dead lines along the way: boundary-rule variants (worse than plain truncation at
neighbouring rows), deletion grafts from neighbouring rows (they inherit the source
radius), and the whole N=4000 campaign (bottleneck patches saturated, jitter walks
ground to -6.08e-06 — and the row is queue-blocked by the Karl Desfontaines cci
126–4141 pending line, which is why the run rotated to N=4153).

Verified by a three-skeptic panel (reproduce / novelty / criterion), all pass, plus
independent 50-digit re-checks by the run's main session. Credit: E. Specht (table
and seed); Jorgy72 & Sine.
