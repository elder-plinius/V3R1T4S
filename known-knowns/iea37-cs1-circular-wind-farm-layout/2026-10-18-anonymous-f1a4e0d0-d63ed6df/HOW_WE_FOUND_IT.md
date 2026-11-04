# How we found it (contributor text, unverified)
We reimplemented the official evaluator in vectorised numpy with an analytic gradient (matching the official code to
5e-6 MWh on all 39 published layouts). Re-scoring the official results folder showed that participant 12's layouts
(posted after the 2019 paper) are the best in every size but sit slightly outside the boundary (4.1 mm for 64
turbines, from 6-significant-figure rounding). What failed: 400 random starts with wake-expansion continuation and
SLSQP (best 1519355, 2 of 400 above the paper's winner); ring + hexagonal-lattice constructions (best 1501627).
What worked: repairing participant 12 into strict feasibility and polishing it (1527532), then a ruin-and-recreate
large-neighbourhood search imported from vehicle routing: remove 1-6 turbines (random, lowest-producing or a spatial
cluster), re-insert each at the best point of a 50 m grid plus a dense boundary ring, polish with SLSQP, keep if
better (later with annealed acceptance). It reached 1539277.7, and a low-temperature annealed run from there reached
1539447.1 in two seeds independently. The same search started from random-start optima (never seeing participant 12)
reached 1533259 and 1528741, both above participant 12.
