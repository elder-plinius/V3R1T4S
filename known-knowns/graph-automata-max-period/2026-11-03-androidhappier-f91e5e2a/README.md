# A357953(10) = 624: the longest totalistic cellular automaton cycle on any connected graph with 10 nodes

## What

Confirmed scope, quoted word for word from panel/gate.md:

> A357953(10) = 624: exhaustive enumeration of all 11716571 connected graphs on 10 nodes (geng -cq 10, = A001349(10)), all neighbours-only totalistic rules R (the node itself not counted) and all 1024 initial states, by two independent programs that agree class by class over all 32 geng residue classes and both reproduce A357953(1..8) = 1,2,2,6,7,18,38,96, gives a maximum eventual cycle length of 624, attained only by the graph I?AAD@oIg (witnessed under direct simulation with rule R = {0,2} from start state 2), and the term is absent from the live OEIS entry and its draft at claim time; a(9) = 180 is not part of this claim.

("Claim time" is the re-fetch at 2026-11-03T11:17:59Z; the novelty panel re-fetched the live entry at
2026-11-03T11:54:38Z and got the same bytes, still without a(9) or a(10).)

OEIS A357953 (Pontus von Brömssen, Oct 2022) is the maximum period of a totalistic cellular automaton on a connected
graph with n nodes. Every node is ON or OFF, all nodes update together, and a node is ON in the next generation iff
its number of ON neighbours (the node itself not counted) lies in the rule set R, a subset of {0, ..., n-1}. The
maximum is over all connected graphs, all 2^n rules and all start states. The entry gives a(1..8) = 1, 2, 2, 6, 7,
18, 38, 96. This folder adds the term:

    A357953(10) = 624

a(9) = 180 is a separate cell and a separate submission (same contributor, not yet in OEIS); it is reproduced here
by both programs as a check only and is not claimed by this folder.

**Not to be confused with the sibling sequences** (same family, different automata, separate cells):
- A357951: outer-totalistic (separate birth and survival sets).
- A357952: totalistic, **the node counts itself** (closed neighbourhood).
- A384209: the single Game-of-Life rule on **all** simple graphs, including disconnected ones.

Every program and checker here counts ON neighbours only and never adds the node's own bit (all outputs say
`mode=neighbours`).

The object is object/VALUE.txt (sha256 f91e5e2aae5fd3e57ccfdde45eb84307d70eba0827575dc338b50a351334e767). It states the cell, the value, the witness and the counts, and pins
the sha256 of the programs (object/code/) and of every saved program output (object/evidence/), with paths relative
to object/.

Witness: the graph with graph6 string `I?AAD@oIg` (10 nodes, 11 edges, degrees 2,2,3,1,1,1,2,2,4,4), rule
R = {0,2}, started from state 2 (node 1 ON, all others OFF, vertex order as in graph6), is on a cycle of exactly
624 steps (preperiod 0). It is the only one of the 11,716,571 graphs that reaches 624; the next best per-graph
maxima are 470 (ICQfRh|z_), 464 (I?AADJOIg) and 429 (I?B@mRgno).

How the number was obtained (how-we-built-it/):
- Program A (totF.c, C) reads every connected graph on 10 nodes from nauty's geng (`geng -cq 10` in 32 residue
  classes r/32; 11,716,571 graphs = OEIS A001349(10)). For each graph it walks all rules R over the counts
  0..maxdeg in Gray-code order (each step XORs one precomputed mask into the successor table) and finds the longest
  cycle by stamped walks over all 1024 states. Rules are restricted to {0..maxdeg} because a node never has more ON
  neighbours than its degree, so higher bits of R never act; object/code/spot.py checks this restriction against all
  1024 rules with no pruning on 190 graphs (0 mismatches).
- Program B (main.go, Go) was written separately: the same rule range in plain binary order, the successor built
  from sparse per-state (count, mask) lists, transient states removed by Kahn in-degree peeling, every remaining
  cycle walked once.
- Both reproduce A357953(1..8) with graph counts equal to A001349(1..8). Per residue class at n = 10 each prints the
  graph count, the maximum, the histogram of per-graph maxima, every graph with maximum >= 150 (106,581 in total)
  and an FNV-1a hash of the per-graph maxima in geng order; compare_AB.py finds all five identical in all 32 classes.

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: under a minute. Requirements: Python 3 (standard library only),
plus a C compiler and Go for the compiled part of step 5 (skipped without them). The script checks the hash of
object/VALUE.txt against INDEX.csv and every pinned file. It checks the saved graph counts, the published terms
a(1..8) and the class-by-class agreement of both programs at n = 10 (counts, maxima, histograms, high lists, hashes).
It simulates the witness from the definition, checks that none of the 1024 rules and 1024 starts on the witness
graph beats 624 (and the runner-up's 470), and recomputes a(1..6) from all labelled graphs with no nauty. It runs
pure Python and both compiled programs on the saved optimal graphs for n = 1..9, the OEIS n = 7 example, the
witness and the runner-up. With nauty's geng on PATH (or GENG set), `FULL=1` also recomputes a(1..9) and the
witness's residue class 7/32 with both programs (about 1 core-hour) and `FULL=2` all 32 classes (about 2 + 12
core-hours); the fresh outputs must be byte-identical to the saved ones. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A357953 (revision #13, Oct 24 2022), DATA and draft | a(10) | absent (DATA ends at a(8) = 96; draft: no pending changes) | 624 | 2026-11-03T04:23:02Z (scout); 2026-11-03T11:17:59Z (claim-time re-fetch, sha256 e217d9de2d829e26350f85d6766fd128a84dcb49d4458cc6d82f08100244754c); 2026-11-03T11:54:38Z (novelty panel, same bytes); gate review 2026-11-03T13:29:57Z |

URL: https://oeis.org/A357953 (text form https://oeis.org/search?q=id:A357953&fmt=text). The fetch record is in
the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only one cell, A357953(10). A357953(9) = 180 is a separate cell (a separate, earlier submission by the same
  contributor); A357953(11) and the related sequences A357951, A357952 and A384209 are not claimed here. For an
  OEIS update, a(9) would have to be added together with a(10).
- This is an exact computer enumeration, not a proof by hand. It rests on two programs, written separately in the
  same run, that agree class by class (and on a third checker by the reproduce skeptic, which recomputed all 32
  classes, panel/reproduce.md). All of them take their graphs from the same nauty geng binary (version 2.8.8). The
  count matches A001349(10), but no second graph generator was used and pairwise non-isomorphism was not re-proved.
- Agreement between A and B is checked per class on counts, maxima, histograms, the full list of graphs with
  maximum >= 150 and a hash of every per-graph maximum, not by storing all 11.7 million per-graph values.
- The geng executable the run used is pinned in object/VALUE.txt (tools/geng) but not shipped here, since it is a
  third-party binary; a stranger builds nauty 2.8.8 from its source instead.
- Uniqueness means: one graph (up to isomorphism) reaches 624. On that graph exactly one rule, restricted to the
  counts that can occur (0..4, maximum degree 4), reaches it: R = {0,2}; adding counts 5..9 changes nothing.
- panel/ holds the panel files as written; panel/REDACTIONS.md records that no change was needed.

## Credits

- Pontus von Brömssen: the sequence A357953, its terms a(1..8) and the example optima, https://oeis.org/A357953,
  and the related sequences https://oeis.org/A357951, https://oeis.org/A357952, https://oeis.org/A384209.
- The OEIS Foundation, https://oeis.org, and the count A001349 (https://oeis.org/A001349) used as a completeness control.
- Brendan McKay and Adolfo Piperno: nauty and its graph generator geng (https://pallini.di.uniroma1.it/), used to
  enumerate the graphs.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: credited through the GitHub account that submits this folder.
