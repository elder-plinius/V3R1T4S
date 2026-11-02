# How we found it (contributor text, unverified)

The brief was a scheduled V3R1T4S run (heavy effort). The workspace's open lead (a benzel tiling term) needed more
memory than the machine had free that night, so the run took a fresh bank target, graph-automata-max-period. The
scout read OEIS A384209: a(1..9) known, no a(10), no pending edit, and no V3R1T4S pull request or paper with a(10).

The plan, frozen in PREREG.md before any program ran: exhaust all graphs on 10 vertices with one program, get the
same number by a different route with a second, simulate the witness with a third small stepper, and check graph
counts against A000088 and A001349. Program A finished n = 10 in about 2.5 minutes on 8 cores and gave 46. Program
B (connected graphs plus the lcm of component periods) gave 46 too, with the same two graphs. Both reproduced the
published a(1..9), and Program A found the published optimal graphs. Nothing failed along the way. The only
surprise was that the n = 10 optimum is not unique.

A timing sample suggests A384209(11) (about 1.02 billion graphs) needs about 5 hours per program on 8 cores with
this code. It was left as a lead.
