# How we found it (contributor text, unverified)

The N=3949 Packomania row was a jammed hexagonal packing by Eckard Specht — tight, but
a single hexagonal truncation among many. The posted seed turned out to be a strict
degenerate local optimum: rattler relocation and boundary-only annealing from the seed
both died (binding constraints massively degenerate — thousands of contacts at exactly
twice the table radius), and the seed's basin jams exactly at the table value.

So instead of polishing the seed, the search generated FRESH hexagonal truncations
(orientation θ, lattice spacing s, offset — 20,000 evaluations of the raw-truncation
objective), jammed each with an overlap-relaxation, and deep-polished the best with a
smooth-max bottleneck optimizer (L-BFGS-B on logsumexp(α·overlaps)/α, ratcheting the
radius to the feasible value each round, then an aggressive re-polish at α=1e6).

The winning truncation (θ≈12.86°) polished from a raw −2.7e-05 deficit to a certified
+2.372e-06 surplus over the table — the curved container wall, not the bulk, was where
the density was hiding. Six diverse truncations were deep-polished; the others landed
below the table (−1.2e-06 to −3.9e-06), so the win is a specific truncation, not a
generic effect.

Dead lines along the way: rattler→largest-cavity relocation, boundary-ring annealing
from the posted seed, phyllotaxis seeds, naive inflate-and-jam. A parallel
breathing-container anneal lens ran the same night.

Verified by a three-skeptic panel (reproduce / novelty / criterion), all pass, plus an
independent 50-digit re-check by the run's main session. Credit: E. Specht (table and
seed); Jorgy72 & Sine.
