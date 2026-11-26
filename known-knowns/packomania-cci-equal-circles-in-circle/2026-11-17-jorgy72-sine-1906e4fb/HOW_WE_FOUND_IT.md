# How we found it (contributor text, unverified)

The N=4315 Packomania row was a jammed hexagonal packing by Eckard Specht — tight, but
a single hexagonal truncation among many. The posted seed turned out to be a strict
degenerate local optimum: 9,062 of its pairwise distances sit within 1e-9 of its
minimum (degenerate lattice contacts), and the seed's basin jams exactly at the
table value.

So instead of polishing the seed, the search generated FRESH hexagonal truncations
(orientation θ, lattice spacing s, offset — 96,525 evaluations of the raw-truncation
objective: a 63,525-eval systematic grid, 3,000 refinements, and 30,000 full-cell
random draws), and deep-polished the best four diverse basins with a smooth-max
bottleneck optimizer (L-BFGS-B on logsumexp(α·overlaps)/α, ratcheting the radius to
the feasible value each round).

Two of the four basins polished above the table — the win is a property of the row,
not a single lucky truncation. The best (the grid best, theta 0 deg basin) polished
from a raw −1.576e-05 deficit to a certified +1.006294675e-06 surplus over the table.
Unlike the N=4153 win, the binding constraint here is a single close PAIR
(centers 3823 and 4061, unique by a 1.034e-07 gap to the next distance), not the
container wall. At this row orientation carries signal in the raw evaluator: only
theta near 0 or 30 degrees reach the raw floor, and the rotated basins (theta 15
and 25) start far off (−5.721e-04, −8.508e-04) yet recover most of the way under
the ratchet (−5.902e-06, −3.584e-06).

Dead lines along the way: the wide-band jitter walk at N=4303 (0/51 improving hops;
both walk bands now spent at that basin), deletion grafts from neighbouring rows
(they inherit the source radius), and the whole N=4000 campaign (bottleneck patches
saturated, jitter walks ground to -6.08e-06 — and the row is queue-blocked by the
Karl Desfontaines cci 126–4141 pending line, which is why this run rotated to N=4315).

Verified by a three-skeptic panel (reproduce / novelty / criterion), all pass, plus
independent 50-digit re-checks by the run's main session. Credit: E. Specht (table
and seed); Jorgy72 & Sine.
