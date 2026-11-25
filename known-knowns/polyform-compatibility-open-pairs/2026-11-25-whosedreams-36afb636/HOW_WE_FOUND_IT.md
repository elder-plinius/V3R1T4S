# How we found it (contributor text, unverified)

Brief: the V3R1T4S bank target polyform-compatibility-open-pairs notes that Sicherman's heptiamond table (last
revised 2012) still has 21 '?' cells in the unrestricted table, and suggests a joint SAT model. Our run kit
(how-we-built-it/code/) encodes, for a pair (P, Q) and a tile count k, a figure F of 7k triangles inside a
rectangle-like board plus exact tilings of F by k copies of P and by k copies of Q, and asks CaDiCaL. A SAT
answer would have been a candidate figure (re-checked by an independent checker); an UNSAT answer is re-solved
with a DRAT proof and checked with drat-trim.

What happened: on the contributor's PC the run went through all 21 '?' pairs for k = 2..8 (work/run_unrestricted,
about 2 minutes for M-X) and then k = 9..20 (work/run_k9_20, about 25 minutes for M-X). No pair produced a figure.
For M-X every k was UNSAT with a verified proof. Some other pairs needed reruns because of a 300 s drat-trim
time limit and memory pressure with many workers; M-X was not affected. The proofs for M-X (the smallest set,
about 1 GB of DRAT) were bundled into one archive and uploaded to Zenodo as the pilot for archiving the rest.

What this is not: a proof of incompatibility. The board for each k is fixed by a formula, and a common figure, if
one exists, may be larger than k = 20 or may not fit in that board. It narrows where such a figure can be.
