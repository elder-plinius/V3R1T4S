# How we found it (contributor text, unverified)

The brief: Packomania's four-dimensional "hyperspheres in a hypersphere" table is a single-author table (247 of 299 rows
from one program, last touched July 2025) that no other group had worked on. The plan was patience plus an honest
evaluator: write the 50-digit checker first, prove it on the posted packings (all 299 rows reproduce their table value),
then polish the posted coordinates with a different optimiser and look for nearby better basins.

What failed: the rows credited to classical constructions (N = 2..25, 121) gained nothing; a sibling lens showed that the
rows for N = 9..20, 23..25 and 38 are exactly D4-lattice fragments, and lattice fragments alone were below the table for
almost every other N up to 117.

What worked: a trust-region sequential-linear-programming maximiser of the feasible radius (linearised pair and wall
constraints, LP by HiGHS, true radius re-evaluated after every step), followed by basin hopping that displaces the few
loosest balls and re-polishes. Within four minutes per row on a laptop this beat the posted value on 15 of the 51 rows it
reached between N = 26 and 76. N = 66 had the largest margin (7.9e-6) and is the one cell packaged here; the others are
recorded in the contributor's workspace and will be panelled separately.
