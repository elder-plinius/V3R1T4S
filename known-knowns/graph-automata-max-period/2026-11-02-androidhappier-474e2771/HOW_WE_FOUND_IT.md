# How we found it (contributor text, unverified)

The brief was a scheduled V3R1T4S run (heavy effort) on the bank target graph-automata-max-period. An earlier run
that day had packaged A384209(10), so this run took the sibling sequence A357953. The scout read the OEIS entry:
a(1..8) known, no a(9), no pending edit, and no V3R1T4S pull request, code or paper with a(9).

The plan, frozen in PREREG.md before any program ran: exhaust all 261,080 connected 9-node graphs from geng with
one program, get the same number by a different route with a second, simulate the witness with a small pure-Python
stepper, and check graph counts against A001349. Program A took about 2 minutes on 8 cores and Program B about 4;
both gave 180 on the same single graph, H?`DBbS with rule {0,2}. A separate self-break checker written from the
definition gave the same 180 and the same per-shard maxima. The run was interrupted before its panel and was
picked up later the same day, when the three skeptics and the honesty gate passed it.

Nothing failed along the way. One side observation: the OEIS example graph listed for n = 8 seems to be the
complement of an optimal graph (it reaches only 10 with the listed rule; its complement reaches 96).
