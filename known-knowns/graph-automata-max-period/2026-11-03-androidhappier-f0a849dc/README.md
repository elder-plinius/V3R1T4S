# A384209(11) = 71: the longest Game of Life cycle on any simple graph with 11 vertices

## What

Confirmed scope, quoted word for word from panel/gate.md:

> A384209(11) = 71: exhaustive enumeration of all 1018997864 simple graphs on 11 vertices (geng -q 11, = A000088(11), disconnected included) and all 2048 initial states under the Game of Life rule B3/S23, by two independent programs that agree (Program A over all graphs; Program B over all 1006700565 connected graphs plus the lcm over connected components) and reproduce a(1..9) = 1,1,1,1,2,4,8,14,27, gives a maximum eventual cycle length of 71, attained by exactly two graphs, J?qrdjivb}_ (witnessed under direct simulation from start state 752) and JCpbdo}ttv_ (start 1728), and the term is absent from the live OEIS entry and its draft at claim time; a(10) = 46 is not part of this claim.

OEIS A384209 (Pontus von Brömssen, May 2025) is the maximum period of Conway's Game of Life run on the vertices of
a simple graph with n vertices: a live vertex stays alive with 2 or 3 live neighbours, a dead vertex comes alive
with exactly 3, all vertices update together. The maximum is over all simple graphs on n vertices, disconnected ones
included, and all 2^n start states. The live entry gives a(1..9) = 1, 1, 1, 1, 2, 4, 8, 14, 27. This folder gives

    A384209(11) = 71

The object is object/VALUE.txt (sha256 f0a849dcadf9018aaa648246a287cf769fdb914bf642668b3bde7b754bf0a451). It states the cell, the value, the
witnesses and the counts, and pins the sha256 of the programs (object/code/) and of every saved program output
(object/evidence/), with paths relative to object/.

Witness: the graph with graph6 string `J?qrdjivb}_` (11 vertices, 31 edges, connected), started from state 752
(bit v of 752 set = vertex v alive, vertex order as in graph6), returns to its start after exactly 71 steps
(preperiod 0). A second, non-isomorphic graph, `JCpbdo}ttv_` (31 edges, start 1728), also reaches 71. These are the
only two of the 1,018,997,864 graphs that do; the next best per-graph maxima are 61 (`JCpbbqkVt^_`,
`JCRbd\]ms~_`) and 60. No disconnected 11-vertex graph exceeds 46.

How the number was obtained (how-we-built-it/):
- Program A (lifeA11.c) reads every one of the 1,018,997,864 non-isomorphic graphs on 11 vertices from nauty's
  geng (`geng -q 11` in 64 residue classes; total = OEIS A000088(11)), builds the Life successor of all 2048 states
  along a Gray-code walk with packed 4-bit neighbour counts, and finds every cycle with epoch-stamped walks. It keeps
  per-graph-maximum histograms for all graphs and for the connected ones, and lists every graph with maximum >= 40.
- Program B (lifeB2.c, merge_orders.py, combine.py) was written separately and takes another route. It reads only
  the connected graphs (`geng -cq k`, k = 1..11; 1,006,700,565 = A001349(11) at k = 11), builds the successor map
  bit-sliced over all states at once, removes transient states by in-degree peeling and records every achievable
  cycle length per order. It then gets a(n) as the best lcm over the ways to split n into connected components; a
  disjoint union evolves component by component, so this covers every disconnected graph.
- compare_AB.py: A's connected-graph histogram equals B's exactly, the 1718 connected graphs with maximum >= 40 are
  the same set, and A's all-graph maximum 71 equals B's combined a(11). Both programs reproduce a(1..9) (and both
  give a(10) = 46, which is not part of this claim). stepper.py, a pure-Python stepper from the definition,
  simulates both witnesses to cycle length 71.

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: a few seconds. Requirements: Python 3 (standard library only), plus
a C compiler with x86-64 BMI2 support for step 5 (skipped without one). The script checks the hash of
object/VALUE.txt against INDEX.csv and every pinned file. It checks the saved graph counts against A000088 and
A001349, the published terms, the 64 residue outputs of both programs, re-merges B's parts, recomputes B's
component-lcm step, and checks that A and B agree at n = 11. It simulates both period-71 witnesses from the
definition, checks that no start on either witness graph (or on the 61 runner-up) beats its value, and recomputes
a(1..6) over all labelled graphs with no nauty. It runs both C programs on the published optimal graphs for
n = 5..9 and on the witnesses. To recompute a(11) itself with Program A (about 40 minutes on 8 cores), put nauty's
geng on PATH (or set GENG) and run `FULL=1 sh verify-it-yourself/run_checks.sh`; the fresh outputs are compared
byte by byte with the saved ones. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A384209 (revision #8, May 22 2025), DATA and draft | a(11) | absent (DATA ends at a(9) = 27; no a(10); draft: no pending changes) | 71 | 2026-11-03T03:24:38Z (scout); 2026-11-03T07:36:52Z (claim time); 2026-11-03T07:53:58Z (novelty panel, sha256 a2d2fe9c9ff2aab776502142000c0bd3bc4d5b2e120022d1679f0990a8c84247); gate review 2026-11-03T09:56:51Z |

URL: https://oeis.org/A384209 (text form https://oeis.org/search?q=id:A384209&fmt=text). The fetch record is in
the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only one cell, A384209(11). A384209(10) = 46 is reproduced by both programs here but is a separate, earlier
  submission (open PR #904) and gets no credit from this folder. A384209(12) and the related sequences A357951,
  A357952 and A357953 are not claimed.
- This is an exact computer enumeration, not a proof by hand. It rests on two programs, written separately by the
  same contributor, that agree, and on a third exhaustive checker written by the reproduce skeptic
  (panel/reproduce.md), which recomputed all 64 residue classes of n = 11 and matched Program A's histograms
  residue by residue. All of them take their graphs from the same nauty geng binary (version 2.8.8); the graph counts
  match A000088 and A001349 at every n, but no second graph generator was used.
- Program B's coverage of disconnected graphs is derived (lcm over connected components), not enumerated graph by
  graph; Program A and the reproduce checker enumerate disconnected graphs directly.
- Program B was not rerun on order 11 by the panel; its saved outputs are consistent with the reproduce checker's
  connected subset.

## Credits

- Pontus von Brömssen: the sequence A384209, its terms a(1..9) and the optimal graphs, https://oeis.org/A384209.
- The OEIS Foundation, https://oeis.org, and the counts A000088 and A001349 used as completeness controls.
- Brendan McKay and Adolfo Piperno: nauty and its graph generator geng (https://pallini.di.uniroma1.it/), used to
  enumerate the graphs.
- John H. Conway: the Game of Life rule.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: credited through the GitHub account that submits this folder.
