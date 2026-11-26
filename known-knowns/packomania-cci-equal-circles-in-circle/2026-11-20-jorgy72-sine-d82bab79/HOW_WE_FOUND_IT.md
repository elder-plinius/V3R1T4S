# How we found it (contributor text, unverified)

The N=4357 Packomania row was a jammed hexagonal packing by Eckard Specht — tight, but
a single hexagonal truncation among many. The posted seed turned out to be a strict
degenerate local optimum: the seed's basin jams exactly at the table value.

So instead of polishing the seed, the search generated FRESH hexagonal truncations
(orientation θ, lattice spacing s, offset — 96,525 evaluations of the raw-truncation
objective: a 63,525-eval systematic grid, 3,000 refinements, and 30,000 full-cell
random draws), and deep-polished the best four diverse basins with a smooth-max
bottleneck optimizer (L-BFGS-B on logsumexp(α·overlaps)/α, ratcheting the radius to
the feasible value each round).

One of the four basins polished above the table — the win is the random-phase basin,
not the grid best. The random best (theta 1.09 deg, raw −1.609e-05) polished to a
certified +4.93845300182e-06 surplus over the table, a +2.10e-05 recovery. The refine
best (theta 7.75 deg, raw −1.568e-05) polished to −2.348e-07, just below the bar.
Unlike the N=4339 win, the binding constraint here is the container WALL (outermost
center 4347), not a close pair — the nearest pair (centers 4109 and 4347) sits
3.05e-07 above the wall term, like the N=4345 win. At this row orientation carries
LITTLE signal in the raw evaluator: the top-20 ties at −1.568e-05 span theta
7.75–22.25 deg, like N=4339 and N=4345 and unlike N=4315. The rotated basins
(theta 15 and 25) start far off (−8.256e-04, −1.114e-03); theta 15 recovers
+8.19e-04 under the ratchet to −6.908e-06 — the largest single-basin recovery of
any rotation night (previous record: N=4345's theta-25 basin, +5.70e-04) — while
theta 25 gains nothing.

Dead lines along the way: the wide-band jitter walk at N=4303 (0/51 improving hops;
both walk bands now spent at that basin), deletion grafts from neighbouring rows
(they inherit the source radius), and the whole N=4000 campaign (bottleneck patches
saturated, jitter walks ground to -6.08e-06 — and the row is queue-blocked by the
Karl Desfontaines cci 126–4141 pending line, which is why this run rotated to N=4357).

Verified by a three-skeptic panel (reproduce / novelty / criterion), all pass, plus
independent 50-digit re-checks by the run's main session. Credit: E. Specht (table
and seed); Jorgy72 & Sine.
