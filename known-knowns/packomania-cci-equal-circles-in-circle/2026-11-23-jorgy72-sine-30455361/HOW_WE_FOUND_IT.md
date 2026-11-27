# How we found it (contributor text, unverified)

The N=4405 Packomania row was a jammed hexagonal packing by Eckard Specht — tight, but
a single hexagonal truncation among many. The posted seed turned out to be a strict
degenerate local optimum: the seed's basin jams exactly at the table value.

So instead of polishing the seed, the search generated FRESH hexagonal truncations
(orientation θ, lattice spacing s, offset — 96,525 evaluations of the raw-truncation
objective: a 63,525-eval systematic grid, 3,000 refinements, and 30,000 full-cell
random draws), and deep-polished the best four diverse basins with a smooth-max
bottleneck optimizer (L-BFGS-B on logsumexp(α·overlaps)/α, ratcheting the radius to
the feasible value each round).

Two of the four basins polished above the table — the win is the random-phase basin,
not the grid best. The random best (theta 13.09 deg, raw −1.554e-05) polished to a
certified +3.607125049e-06 surplus over the table, a +1.915e-05 recovery — the
largest single gain of any rotation night. The refine best (theta 0.00 deg, raw
−1.419e-05) polished to −2.221e-06, below the bar. Unlike the N=4357 win, the
binding constraint here is a close PAIR (centers 4130 and 4394), not the container
wall — the wall term sits 2.24e-06 above the pair term, like the N=4339 win.
At this row orientation carries NO signal in the raw evaluator: the top-20 ties at
−1.419e-05 span theta 0.00–4.75 deg (the raw floor is spacing-limited, F = s/2
for every orientation). The rotated basins (theta 15 and 25) start at the same
spacing-limited floor (−1.419e-05); theta 15 polishes to −4.862e-06 while theta 25
polishes to +2.038e-06 — a second above-bar file, banked, not bundled.

Dead lines along the way: the wide-band jitter walk at N=4381 (0/46 improving hops
across two attempts; both walk bands now spent at that basin), deletion grafts from
neighbouring rows (they inherit the source radius), and the whole N=4000 campaign
(bottleneck patches saturated, jitter walks ground to -6.08e-06 — and the row is
queue-blocked by the Karl Desfontaines cci 126–4141 pending line, which is why
this run rotated to N=4405).

Verified by a three-skeptic panel (reproduce / novelty / criterion), all pass, plus
independent 50-digit re-checks by the run's main session. Credit: E. Specht (table
and seed); Jorgy72 & Sine.
