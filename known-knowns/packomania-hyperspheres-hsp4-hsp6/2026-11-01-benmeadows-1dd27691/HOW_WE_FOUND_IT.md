# How we found it (contributor text, unverified)

The brief: one search lane over hsp4 N = 211..300, four cores, about 3.75 hours, with the 2026-10-31 snapshot of
radius.txt as the target values. Packomania's posted coordinates were not available offline, so no search started
from them. Points are kept in the unit ball and the minimum distance D is maximised; the ball radius is D / (2 + D).

What failed: single round-1 runs per cell (two-shell, D4-lattice-cut and random seeds, penalty compression by L-BFGS,
monotonic basin hopping, sequential-LP polish) ended 2e-4 to 2e-3 below the table for N >= 220; most chain seeds for
N = 217 and 218 ended 1e-5 to 1.4e-4 short.

What worked: an extended round-1 run at N = 213, then a chain: take the best N - 1 packing, insert one ball at the
largest probed hole, run 1100 s of basin hopping and polish. This gave N = 214, 215, 216 and 217 (217 after 14 runs).
This package is N = 213.
