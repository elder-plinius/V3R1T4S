# How we found it (contributor text, unverified)

The brief was a scheduled V3R1T4S run (heavy effort) on the bank target graph-automata-max-period. An earlier run had
found A384209(10) = 46 and estimated that n = 11 (about 1.02 billion graphs) needed several hours per program on 8
cores, so it was left as a lead. This run picked it up: the scout read OEIS A384209 (a(1..9) only, no pending
edit) and the repo's pull requests (only the n = 10 claim).

The plan, frozen in PREREG.md before any n = 11 program ran: a faster Program A over all graphs (SWAR neighbour
counts along a Gray-code walk), the earlier connected-graph Program B with an lcm step for disconnected graphs, a
histogram-level comparison of the two, a pure-Python stepper for the witness, and graph counts checked against
A000088 and A001349. Program A took about 40 minutes; Program B took about 3.5 hours on a busy shared machine. Both
gave 71, with the same two graphs, the same histogram over the connected graphs and the same 1718 graphs at 40 or
more. Nothing disagreed. The surprise was the gap: the best value jumps from 61 to 71, and only two graphs reach it.
