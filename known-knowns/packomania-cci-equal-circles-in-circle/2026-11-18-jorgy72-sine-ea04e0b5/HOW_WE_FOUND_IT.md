# How we found it (contributor text, unverified)

The N=4339 Packomania row was a jammed hexagonal packing by Eckard Specht — tight, but
a single hexagonal truncation among many. The posted seed turned out to be a strict
degenerate local optimum: its two smallest pair distances agree to 8.4e-32
(degenerate lattice contacts), and the seed's basin jams exactly at the
table value.

So instead of polishing the seed, the search generated FRESH hexagonal truncations
(orientation θ, lattice spacing s, offset — 96,525 evaluations of the raw-truncation
objective: a 63,525-eval systematic grid, 3,000 refinements, and 30,000 full-cell
random draws), and deep-polished the best four diverse basins with a smooth-max
bottleneck optimizer (L-BFGS-B on logsumexp(α·overlaps)/α, ratcheting the radius to
the feasible value each round).

Two of the four basins polished above the table — the win is a property of the row,
not a single lucky truncation. The best (the grid best, theta 29.25 deg basin)
polished from a raw −1.285e-05 deficit to a certified +1.014393041e-05 surplus over
the table. Unlike the N=4153 win, the binding constraint here is a single close PAIR
(centers 3861 and 4096, unique by a 2.698e-07 gap to the next distance), not the
container wall. At this row orientation carries LITTLE signal in the raw evaluator:
the top-20 ties at −1.285e-05 span theta 0–29.25 deg, unlike N=4315 where only
theta near 0 or 30 reached the raw floor. The rotated basins (theta 15 and 25)
start far off (−1.002e-03, −3.570e-04); theta 25 recovers all the way to
+8.345e-06 under the ratchet — the largest single-basin recovery of any rotation
night (+3.65e-04) — while theta 15 gains nothing. The random-phase best
(theta 0.24 deg, raw −1.209e-05, the best raw floor of any rotation night) also
gains nothing under the ratchet: its basin is already at its ceiling.

Dead lines along the way: the wide-band jitter walk at N=4303 (0/51 improving hops;
both walk bands now spent at that basin), deletion grafts from neighbouring rows
(they inherit the source radius), and the whole N=4000 campaign (bottleneck patches
saturated, jitter walks ground to -6.08e-06 — and the row is queue-blocked by the
Karl Desfontaines cci 126–4141 pending line, which is why this run rotated to N=4339).

Verified by a three-skeptic panel (reproduce / novelty / criterion), all pass, plus
independent 50-digit re-checks by the run's main session. Credit: E. Specht (table
and seed); Jorgy72 & Sine.
