# How we found it (contributor text, unverified)

The brief was a scheduled V3R1T4S heavy run on the bank target triangular-peg-solitaire-shortest-11-12, with two
cells: Triangle(11) (published bound 28) and Triangle(12) (published bound 29, Bell 2007). One cell per claim; this
folder is the Triangle(12) cell. The scout read OEIS A127500 and Bell's pages (bounds unchanged since 2007, no
pending OEIS draft, no V3R1T4S pull request on the target). The plan, frozen in how-we-built-it/PREREG.md before
any attack program ran: a simulator written from the definition, tested on Bell's published solutions and on
corrupted ones, plus a second independent simulator that must agree before any claim.

What failed: polishing Bell's 29-move solution by reordering jumps stayed at 29. A move-layered beam search ranked
only by Merson regions and peg count (B = 100000, W = 2, no dead-peg penalty) ran into boards with two isolated pegs
and did not solve Triangle(12) within 45 moves (how-we-built-it/logs/T12_B100000_W2_V0.*).

What worked: the same beam (how-we-built-it/beam3.c), where each child is every jump chain by one peg and boards are
merged under the six symmetries of the triangle, plus a penalty for isolated pegs (BEAM_V=2), beam 200000 and
weight 3. It reached one peg after 25 moves, from vacancy a3 to j12, in a few minutes on one core (a rebuild took 3 min 52 s). Two runs with
random tie-break seeds (21, 22) also gave 25 moves, with different solutions. None gave fewer than 25. The beam is
capped, so this says nothing about a lower bound.
