# How we found it (contributor text, unverified)

The brief was a scheduled V3R1T4S run (heavy effort) on the bank target graph-automata-max-period. Earlier runs that
day had packaged A384209(10) and A357953(9), so this run took the sibling sequence A357952, where the node counts
itself. The scout read the OEIS entry: a(1..8) known, no a(9), no pending edit, and no V3R1T4S pull request, code or
paper with a(9).

The plan, frozen in PREREG.md before any program ran: exhaust all 261,080 connected 9-node graphs from geng with
Program A (the C program from the A357953 run, in its `self` mode), get the same numbers with a separately written
Go Program B, diff the two graph by graph, simulate the witness with a small pure-Python stepper, and check graph
counts against A001349. Program A took about 10 minutes on 8 cores and Program B about 14; both gave 200 on the
same single graph, H?o|]|~ with rule {1,3,5}, and agreed on the maximum of every one of the 261,080 graphs. The next
best graph reaches 198. A self-break pass (Python re-check of 120 graphs, canonical-form completeness check of the
graph list, a rerun of B with a different worker count) found nothing. Three skeptics and the honesty gate then
passed it.

Nothing failed along the way. Both OEIS examples (n = 7: F@Unw, n = 8: G?Dlvw) reach the listed values.
