# A357951(8) = 150: the longest outer-totalistic cellular automaton cycle on any connected graph with 8 nodes

## What

Confirmed scope, quoted word for word from panel/gate.md:

> A357951(8) = 150: exhaustive enumeration of all 11117 connected 8-node graphs (geng -cq 8), all 65536 outer-totalistic (B,S) rules and all 256 initial states, by two independent programs that agree graph by graph and reproduce a(1..7) = 2,2,4,6,16,26,66, gives a maximum eventual cycle length of 150, attained uniquely by the graph GCQfBg (witnessed under direct simulation by rule B={0,2}, S={1,3,4} from start state 1), and the term is absent from the live OEIS entry and its draft at claim time.

("Claim time" is the re-fetch at 2026-11-03T02:50:41Z; the novelty panel re-fetched the live entry at
2026-11-03T04:15:37Z and got the same bytes, still without a(8).)

OEIS A357951 (Pontus von Brömssen, Oct 2022) is the maximum period of an **outer-totalistic** cellular automaton on
a connected graph with n nodes. Every node is ON or OFF and all nodes update together. With c = the number of ON
neighbours of a node (the node itself is not counted), an OFF node turns ON iff c is in the birth set B, and an ON
node stays ON iff c is in the survival set S; B and S are any subsets of {0, ..., n-1}, so there are 2^(2n) rules
(65,536 at n = 8). The maximum is over all connected graphs, all rules and all start states. The entry gives
a(1..7) = 2, 2, 4, 6, 16, 26, 66. This folder adds the next term:

    A357951(8) = 150

**Not to be confused with the sibling sequences** (same graphs, different automata, separate cells):
- A357952: totalistic, **the node counts itself**: one rule set R ⊆ {0..n}, applied to the number of ON nodes in the
  closed neighbourhood. A357952(9) = 200 is a separate submission.
- A357953: totalistic, **neighbours only**: one rule set R ⊆ {0..n-1} for the number of ON neighbours, whatever the
  node's own state (that is B = S). A357953(9) = 180 is a separate submission.
- A384209: the single Game-of-Life rule (B={3}, S={2,3}) on **all** simple graphs, including disconnected ones.
  A384209(10) = 46 is a separate submission.

Both totalistic classes are special cases of outer-totalistic rules, so A357951(n) is at least A357952(n) and
A357953(n); the value here says nothing exact about either of them. The programs here keep B and S separate, never
add the node's own bit to the count, and every checker in verify-it-yourself/ does the same.

The object is object/VALUE.txt (sha256 374d8b230aee9f8089d4cb72ee49a554910d364f50811c49cf46ff23264007fa). It states
the cell, the value, the witness and the counts, and pins the sha256 of the programs (object/code/) and of every
saved program output (object/evidence/), with paths relative to object/.

Witness: the graph with graph6 string `GCQfBg` (8 nodes, 11 edges, degrees 1,2,3,3,3,3,3,4), rule B={0,2},
S={1,3,4}, started from state 1 (node 0 ON, all others OFF, vertex order as in graph6), is on a cycle of exactly 150
steps (transient 0). Program A's raw rule also has 7 in B, which no node of this graph (maximum degree 4) can see,
so the dynamics are the same. It is the only one of the 11,117 graphs that reaches 150; the next best is 124
(G?rfUw).

How the number was obtained (how-we-built-it/):
- Program A (otA.c) reads every connected graph on 8 nodes from nauty's geng (`geng -cq 8`, 11,117 graphs = OEIS
  A001349(8)), walks all 65,536 (B,S) rules in Gray-code order (each step XORs one precomputed change into the
  successor table, no pruning) and takes the longest cycle by stamped walks over all 256 states.
- Program B (otB.go) was written separately in Go: its own graph6 parser, rules over counts 0..maxdeg only (complete,
  since a node never has more ON neighbours than its degree; the argument is in its header), the successor map built
  directly per rule, transient states removed by in-degree peeling, every remaining cycle walked once.
- Both reproduce A357951(1..7) with graph counts equal to A001349(1..7). At n = 8 they print the same maximum for
  every one of the 11,117 graphs (diff_AB.py), the same histogram and the same best graph in each of the 8 geng
  residue classes.

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: a few seconds. Requirements: Python 3 (standard library only), plus
a C compiler and Go for the compiled part of step 5 (skipped without them). The script checks the hash of
object/VALUE.txt against INDEX.csv and every pinned file. It checks the saved graph counts, the published terms
a(1..7) and the graph-by-graph agreement of both programs at n = 8. It simulates the witness from the definition,
checks that none of the 65,536 rules and 256 starts on the witness graph beats 150, and recomputes a(1..6) from all
labelled graphs with no nauty. It runs pure Python and both compiled programs on the saved optimal graphs for
n = 1..7, the OEIS n = 7 example, the witness and the runner-up. To recompute a(1..8) itself (a few minutes on 8
cores), put nauty's geng on PATH (or set GENG) and run `FULL=1 sh verify-it-yourself/run_checks.sh`; the fresh
outputs must be byte-identical to the saved ones. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A357951 (revision #11, Oct 23 2022), DATA and draft | a(8) | absent (DATA ends at a(7) = 66; draft: no pending changes) | 150 | 2026-11-03T02:36:55Z (scout); 2026-11-03T02:50:41Z (claim-time re-fetch); 2026-11-03T04:15:37Z (novelty panel, sha256 e8e8bfa7c8a4953334164e23d561e02541c275663e8a984b7640e62d5578b302); gate review 2026-11-03T04:29:37Z |

URL: https://oeis.org/A357951 (text form https://oeis.org/search?q=id:A357951&fmt=text). The fetch record is in
the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only one cell, A357951(8). A357951(9) and the related sequences A357952, A357953 and A384209 are not claimed
  here (A357952(9), A357953(9) and A384209(10) are separate submissions and separate cells).
- This is an exact computer enumeration, not a proof by hand. It rests on two programs, written separately in the
  same run, that agree graph by graph (and on a third checker by the reproduce skeptic, panel/reproduce.md). All of
  them take their graphs from the same nauty geng binary (version 2.8.8). The count matches A001349(8) and both the
  run (labelg) and the reproduce skeptic (its own canonical form) found 11,117 distinct graphs, but no second graph
  generator was used.
- The geng executable the run used is pinned in object/VALUE.txt (tools/geng) but not shipped here, since it is a
  third-party binary; a stranger builds nauty 2.8.8 from its source instead.
- Uniqueness means: one graph (up to isomorphism) reaches 150. On that graph one rule, restricted to the counts that
  can occur (0..4), reaches it: B={0,2}, S={1,3,4}; adding counts 5..7 to B or S changes nothing there.
- panel/ holds the panel files as written, except that the temporary-folder prefix of two skeptics' scratch copies
  was replaced. panel/REDACTIONS.md lists the changes and the original files' sha256.

## Credits

- Pontus von Brömssen: the sequence A357951, its terms a(1..7) and the example optima, https://oeis.org/A357951,
  and the related sequences https://oeis.org/A357952, https://oeis.org/A357953, https://oeis.org/A384209.
- The OEIS Foundation, https://oeis.org, and the count A001349 (https://oeis.org/A001349) used as a completeness control.
- Brendan McKay and Adolfo Piperno: nauty and its graph generator geng (https://pallini.di.uniroma1.it/), used to
  enumerate the graphs.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: credited through the GitHub account that submits this folder.
