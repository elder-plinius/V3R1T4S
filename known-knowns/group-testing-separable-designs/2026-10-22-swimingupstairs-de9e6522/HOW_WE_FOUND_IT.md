# How we found it (contributor text, unverified)
A V3R1T4S run on pooled-testing designs targeted A054961 at n=16 and 17. Earlier min-conflicts searches with unrestricted
vectors reached 92 at n=16. The published 91-families are mostly weight 5 and 6, so this run restricted random vectors
and moves to weight 4. A ladder that tries one more vector each step (alternating random starts and warm starts from the
previous family) reached 93..100 within about 20 minutes, then 101 from a random start and 102 warm-started from that
101. Three tries at 103 stopped at 3 colliding pairs, and a later run's tries at 103 stopped at 1. An exhaustive add-one
search on the 102 found no vector to add and no 1-out-2-in swap.
