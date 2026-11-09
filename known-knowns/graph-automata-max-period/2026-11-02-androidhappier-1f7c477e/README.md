# A384209(10) = 46: the longest Game of Life cycle on any simple graph with 10 vertices

## What

Confirmed scope, quoted word for word from panel/gate.md:

> Exhaustive enumeration of all 12005168 simple graphs on 10 vertices and all 1024 states, by two independent programs that both reproduce a(1..9), shows that A384209(10) = 46 (a term absent from the live OEIS entry on 2026-11-02), with witness graph6 I?zUvYujw, Life rule B3/S23, start state 62, whose directly simulated cycle length is 46.

OEIS A384209 (Pontus von Brömssen, May 2025) is the maximum period of Conway's Game of Life run on the vertices of
a simple graph with n vertices: a live vertex stays alive with 2 or 3 live neighbours, a dead vertex comes alive
with exactly 3, all vertices update together. The entry gives a(1..9) = 1, 1, 1, 1, 2, 4, 8, 14, 27. This folder
adds the next term:

    A384209(10) = 46

The object is object/VALUE.txt (sha256 1f7c477e32f0448ba5fda0a9361b2392e6f3f4421155e632364c7166b61015bb). It states the value, the witness and the counts, and pins the sha256 of
every saved program output (object/evidence/) and of the programs.

Witness: the graph with graph6 string `I?zUvYujw` (10 vertices, 27 edges), started from state 62 (vertices 1-5 alive,
vertex v alive when bit v of 62 is set, vertex order as in graph6), returns to its start after exactly 46 steps.
A second graph, `IEhffT{^w` (28 edges, start 842), also reaches 46. Unlike n = 5..9, the optimum is not unique.

How the number was obtained (how-we-built-it/):
- Program A (lifeA.c) reads every one of the 12,005,168 non-isomorphic graphs on 10 vertices from nauty's geng
  (OEIS A000088(10)), builds the Life successor map on all 1024 states, and takes the longest cycle.
- Program B (lifeB.c, merge_parts.py, combine.py) was written separately and takes another route. It reads only
  the connected graphs (11,716,571 = A001349(10)) and records every achievable cycle length per order, with a
  bit-sliced successor map and in-degree peeling. It then gets a(n) as the best lcm over the ways to split n into
  connected components. A disjoint union evolves component by component, so this covers every disconnected graph.
  At n = 10 the best disconnected value is 27 (9 + 1).
- Both programs reproduce a(1..9). Program A also finds exactly the five published optimal graphs for n = 5..9.

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: about 10 seconds. Requirements: Python 3 (standard library only),
plus a C compiler for step 5 (skipped without one). The script checks the hash of object/VALUE.txt against
INDEX.csv and every pinned file. It checks the saved graph counts, the published terms and the agreement of both
programs. It simulates the two period-46 witnesses from the definition, and recomputes a(1..6) over all labelled
graphs with no nauty. It runs both C programs on the published optimal graphs and on the witnesses.
To recompute a(10) itself (about 3 minutes on 8 cores), put nauty's geng on PATH and run
`FULL=1 sh verify-it-yourself/run_checks.sh`. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A384209 (revision #8, May 22 2025), DATA and draft | a(10) | absent (DATA ends at a(9) = 27; draft: no pending changes) | 46 | 2026-11-02T09:21:21Z (scout); 2026-11-02T09:29:55Z (novelty panel); 2026-11-02T09:43:11Z (gate) |

URL: https://oeis.org/A384209 (text form https://oeis.org/search?q=id:A384209&fmt=text). The fetch record is in
the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only one cell, A384209(10). A384209(11) and the related sequences A357951, A357952 and A357953 are not claimed.
- This is an exact computer enumeration, not a proof by hand. It rests on two programs, written separately in
  the same run, that agree. Both take their graphs from the same nauty geng binary (version 2.8.8). The graph
  counts match A000088 and A001349 at every n, but no second graph generator was used.
- Program B was not rerun on order 10 by the panel. The reproduce skeptic reran Program A twice, and ran its own
  exhaustive checker over all 12,005,168 graphs. All of them agree (panel/reproduce.md).
- A fitted formula in LODA (a(n) = floor((2^(n-1)+C(n-1,3))/12)+1) matches a(1..9) and would give 50 at n = 10. It
  has no witness and is not a computed value. The exhaustive runs show no graph on 10 vertices exceeds 46.

## Credits

- Pontus von Brömssen: the sequence A384209, its terms a(1..9) and the optimal graphs, https://oeis.org/A384209,
  and the related sequences https://oeis.org/A357951, https://oeis.org/A357952, https://oeis.org/A357953.
- The OEIS Foundation, https://oeis.org, and the counts A000088 and A001349 used as completeness controls.
- Brendan McKay and Adolfo Piperno: nauty and its graph generator geng (https://pallini.di.uniroma1.it/), used to
  enumerate the graphs.
- John H. Conway: the Game of Life rule.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: credited through the GitHub account that submits this folder.
