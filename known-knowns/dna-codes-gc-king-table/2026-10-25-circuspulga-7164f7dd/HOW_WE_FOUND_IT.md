# How we found it (contributor text, unverified)
A scheduled CPU run on King's GC table picked the n=15 'v' cells. King 2003 Theorem 4 showed (15,12)=15 is already optimal, so the secondary cell (15,11)=34 became the focus.
Far import: the 3-dimensional GF(4) code on 15 points of PG(2,4) (punctured), with a per-column letter map searched to maximise a constant-GC slice, gave 40 words with distance >= 11.
A min-conflicts search (gcmc.c) warm-started from that slice added one word (41), then another (42). 43 was not found in 5 x 1600 s.
What failed: cold min-conflicts (weak), simulated annealing on letter maps (38), the same slice at (18,13) and (16,12) (below table).
400 random greedy maximal codes reach at most 26.
