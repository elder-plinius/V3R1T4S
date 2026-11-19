# How we found it (contributor text, unverified)

The N=4345 Packomania row was a jammed hexagonal packing by Eckard Specht — tight, but
a single hexagonal truncation among many. The posted seed turned out to be a strict
degenerate local optimum: the seed's basin jams exactly at the table value.

So instead of polishing the seed, the search generated FRESH hexagonal truncations
(orientation θ, lattice spacing s, offset — 96,525 evaluations of the raw-truncation
objective: a 63,525-eval systematic grid, 3,000 refinements, and 30,000 full-cell
random draws), and deep-polished the best four diverse basins with a smooth-max
bottleneck optimizer (L-BFGS-B on logsumexp(α·overlaps)/α, ratcheting the radius to
the feasible value each round).

Two of the four basins polished above the table — the win is a property of the row,
not a single lucky truncation. The best (the theta-25 rotation basin) polished from
a raw −5.662e-04 deficit to a certified +3.78404615968e-06 surplus over the table —
a +5.70e-04 recovery, the largest single-basin recovery of any rotation night
(previous record: N=4339's theta-25 basin, +3.65e-04). The refine best (theta 10.63
deg, raw −1.347e-05) polished to +1.71342783757e-06. Unlike the N=4339 win, the
binding constraint here is the container WALL (outermost center 4344), not a close
pair — the nearest pair (centers 4070 and 4319) sits 3.64e-08 above the wall term.
At this row orientation carries LITTLE signal in the raw evaluator: the top-20 ties
at −1.427e-05 span theta 11.5–18.5 deg, like N=4339 and unlike N=4315. The rotated
basins (theta 15 and 25) start far off (−3.382e-04, −5.662e-04); theta 25 recovers
all the way to +3.784e-06 under the ratchet while theta 15 gains nothing. The
random-phase best (theta 18.65 deg, raw −1.437e-05) polishes to −9.841e-07, just
below the bar: its basin is nearly at its ceiling.

Dead lines along the way: the wide-band jitter walk at N=4303 (0/51 improving hops;
both walk bands now spent at that basin), deletion grafts from neighbouring rows
(they inherit the source radius), and the whole N=4000 campaign (bottleneck patches
saturated, jitter walks ground to -6.08e-06 — and the row is queue-blocked by the
Karl Desfontaines cci 126–4141 pending line, which is why this run rotated to N=4345).

Verified by a three-skeptic panel (reproduce / novelty / criterion), all pass, plus
independent 50-digit re-checks by the run's main session. Credit: E. Specht (table
and seed); Jorgy72 & Sine.
