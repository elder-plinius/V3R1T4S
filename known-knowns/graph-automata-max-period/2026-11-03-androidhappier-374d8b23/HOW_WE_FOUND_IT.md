# How we found it (contributor text, unverified)

The brief was a scheduled V3R1T4S run (heavy effort) on the bank target graph-automata-max-period. Earlier runs had
packaged A384209(10), A357953(9) and A357952(9), so this run took the remaining named cell, A357951(8), the
outer-totalistic sibling (separate birth and survival sets). The scout read the OEIS entry: a(1..7) known, no a(8),
no pending edit, and no V3R1T4S pull request, code or paper with a(8).

The plan, frozen in PREREG.md before any program ran: exhaust all 11,117 connected 8-node graphs from geng with
Program A (a new C program walking all 65,536 (B,S) rules in Gray-code order with no pruning), get the same numbers
with a separately written Go Program B (rules restricted to the counts a graph can actually produce, with the
completeness argument in its header), diff the two graph by graph, simulate the witness with a small pure-Python
stepper, and check graph counts against A001349. Program A took about a minute and a half on 8 cores and Program B
about five; both gave 150 on the same single graph, GCQfBg with B={0,2}, S={1,3,4}, and agreed on the maximum of
every one of the 11,117 graphs. The next best graph reaches 124 (G?rfUw).

What failed: an attempt to predict or bound the answer by linear algebra (the GF(2)-affine rule family reaches only
30 at n = 8), and reusing the optimal rules of smaller n as a guess (the n = 8 optimum uses a different rule). A
self-break pass (numpy re-check of 26 graphs plus the witness over all rules, a fresh rebuild giving byte-identical
outputs, random relabelings of the top graphs, a canonical-form completeness check of the graph list) found nothing.
Three skeptics and the honesty gate then passed it. The OEIS n = 7 example (FBjng) reaches the listed 66.
