# How we found it (contributor text, unverified)

The brief was a scheduled V3R1T4S run (heavy effort) on the bank target triangular-peg-solitaire-shortest-11-12.
The scout found the live OEIS A127500 entry and Bell's 2007 page both at 19 <= a(11) <= 28 and 21 <= a(12) <= 29,
with no pending OEIS edit and no V3R1T4S pull request on the cell. Bell's 28-move Triangle(11) solution was built
by hand around one long final sweep. Before any search ran, PREREG.md froze the checker, the thresholds (claim T11
only at 27 moves or fewer) and the rule of no lower-bound claim from a capped search.

Two simulators came first (a Python one and a C one in cube coordinates), both tested on Bell's published T9-T12
solutions and two corrupted orders. The search that worked was a move-layered beam (beam3.c): each child is a full
jump chain of one peg, boards are deduplicated under the six symmetries of the triangle, and boards are ranked by
pegs left plus a weight times the number of fully filled Merson regions. It reached 24 moves at beam width 20000
(11 s) and 22 at 100000; widths up to 1000000, other weights and seeds all stalled at 22. On small boards the same
beam finds the optimum for T6-T8 and is one move off for T9 and T10, so it is close to optimal but not exact.

What failed: reordering the jumps of Bell's 28 and 29 move solutions (and of the 22) never shortened them; a
stronger region lower bound gave only 17 on T11; an exhaustive 19-move search for a lower bound was not attempted.
For Triangle(12) the beam reached 25 moves; that cell is handled separately and is not part of this package.
