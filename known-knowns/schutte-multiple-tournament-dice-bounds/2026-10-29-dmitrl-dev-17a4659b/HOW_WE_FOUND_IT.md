# How we found it (contributor text, unverified)

AI-assisted work for DmitrL-dev (2026-10-28). The bank target asks for an S_5 set of two tournaments on at most 13
vertices or an S_6 set of three tournaments on at most 12, below the Proposition 2.3 compositions of arXiv:2604.08790
(Figure 7: 14 and 13); its partial win p1 asks instead for an exact value proved by an UNSAT certificate checked by a
formally verified checker.

What did not work. Pairs of circulant tournaments on Z13 (all 2080 pairs of the 64 connection sets): the best leaves 1131
of the 1287 5-sets undominated; a regular tournament on 13 vertices dominates only 13*6 five-sets, so far-from-regular
out-degrees are needed. Simulated annealing on edge flips: it finds S_6 triples on 13 vertices at once (the iterated
composition 3 + 3 + 7) but stalls at 27 undominated 6-sets on 12 vertices, and it does not even rediscover the 14-vertex
(2,5) composition, so it was dropped for (2,5). The plain CNF (no symmetry breaking) needs 98 s already for the starred
cell (2,4,9) and did not finish the target cells.

What worked. First we reproduced every starred cell of Figure 7 with m < k+1 (SAT at f(m,k), UNSAT at f(m,k) - 1, every
model checked). Then we broke symmetry with a vertex of maximum out-degree, first as eight separate cubes (all UNSAT for
13 vertices, about 12 minutes), then as one CNF ('global', UNSAT in 583 s), and finally with nested initial-segment
constraints ('global3', how-we-built-it/SOUNDNESS.md): CaDiCaL proves the 13-vertex CNF UNSAT in about 150 s and its
372 MB LRAT proof passes cake_lpr in about 17 s. The 'global' proof (1.24 GB) passed cake_lpr as well. A second encoding
written separately (how-we-built-it/encode_alt.py: all ordered pairs as variables, totalizer degree comparison) is UNSAT
under kissat 4.0.4, and the added clauses were tested by random relabelling (how-we-built-it/sb_audit.py).

Not finished. The same encoding for three tournaments on 12 vertices is UNSAT according to CaDiCaL (7089 s), but its
LRAT proof has about 62.6 million clause ids and exhausted cake_lpr's heap at 1500 and 2600 MB on this laptop, so there
is no verified certificate for f(3,6) = 13 yet and it is not claimed here.
