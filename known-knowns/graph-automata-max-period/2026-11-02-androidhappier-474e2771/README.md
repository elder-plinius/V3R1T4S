# A357953(9) = 180: the longest totalistic cellular automaton cycle on any connected graph with 9 nodes

## What

Confirmed scope, quoted word for word from panel/gate.md:

> Exhaustive enumeration of all 261080 connected 9-node graphs (nauty geng -c), all 2^9 neighbours-only totalistic rules and all 2^9 start states, by two differently-built programs that agree and reproduce A357953(1..8), gives A357953(9) = 180, with witness H?`DBbS, rule {0,2}, start 175 confirmed by direct simulation; the term is absent from the OEIS entry snapshot fetched 2026-11-02 04:58 EST.

(04:58 EST is 2026-11-02T09:58:53Z, the scout fetch; the novelty panel re-fetched the live entry at
2026-11-02T20:50:20Z and found the same revision, still without a(9).)

OEIS A357953 (Pontus von Brömssen, Oct 2022) is the maximum period of a totalistic cellular automaton on a connected
graph with n nodes. Every node is ON or OFF, all nodes update together, and a node is ON in the next generation iff
its number of ON neighbours (the node itself not counted) lies in the rule set R, a subset of {0, ..., n-1}. The
maximum is over all connected graphs, all 2^n rules and all start states. The entry gives a(1..8) = 1, 2, 2, 6, 7,
18, 38, 96. This folder adds the next term:

    A357953(9) = 180

The object is object/VALUE.txt (sha256 474e2771c5ee7d80d0d71427747d4731c56fad594bf3da1bcd7ee56e80dfd76b). It states
the value, the witness and the counts, and pins the sha256 of the programs (object/code/) and of every saved program
output (object/evidence/), with paths relative to object/.

Witness: the graph with graph6 string `H?`DBbS` (9 nodes, 11 edges, degrees 3,3,2,2,1,2,2,3,4), rule {0,2}, started
from state 175 (node v ON when bit v of 175 is set, vertex order as in graph6), is on a cycle of exactly 180 steps
(preperiod 0). It is the only one of the 261,080 graphs that reaches 180; the next best is 142.

How the number was obtained (how-we-built-it/):
- Program A (totA.c) reads every connected graph on 9 nodes from nauty's geng (`geng -cq 9`, 261,080 graphs =
  OEIS A001349(9)), precomputes neighbour counts for every node and state, builds the successor map for each of
  the 512 rules, and takes the longest cycle by stamped walks over all 512 states.
- Program B (totB.c) was written separately and takes another route: bit-sliced neighbour-count masks over all
  states, the successor table as an OR of equality masks over the counts in R, transient states removed by
  in-degree peeling, every remaining cycle walked once.
- Both reproduce A357953(1..8) with graph counts equal to A001349(1..8), and they agree on every one of the 8
  geng residue classes at n = 9 (same graph counts, same maxima, same witness graph and rule).

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: a few seconds. Requirements: Python 3 (standard library only), plus a
C compiler for the C part of step 5 (skipped without one). The script checks the hash of object/VALUE.txt against
INDEX.csv and every pinned file. It checks the saved graph counts, the published terms a(1..8) and the agreement of
both programs at n = 9. It simulates the witness from the definition, checks that no rule or start on the witness
graph beats 180, and recomputes a(1..6) from all labelled graphs with no nauty. It runs both C programs on the saved
optimal graphs for n = 1..8 and on the witness. To recompute a(9) itself (about 6 minutes in total on 8 cores), put
nauty's geng on PATH (or set GENG) and run `FULL=1 sh verify-it-yourself/run_checks.sh`; the fresh outputs must be
byte-identical to the saved ones. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A357953 (revision #13, Oct 24 2022), DATA and draft | a(9) | absent (DATA ends at a(8) = 96; draft: no pending changes) | 180 | 2026-11-02T09:58:53Z (scout); 2026-11-02T20:50:20Z (novelty panel); gate review 2026-11-02T21:03:30Z |

URL: https://oeis.org/A357953 (text form https://oeis.org/search?q=id:A357953&fmt=text). The fetch record is in
the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only one cell, A357953(9). A357953(10) and the related sequences A357951, A357952 and A384209 are not claimed.
- This is an exact computer enumeration, not a proof by hand. It rests on two programs, written separately in the
  same run, that agree (and on a third checker by the reproduce skeptic, panel/reproduce.md). All of them take
  their graphs from the same nauty geng binary (version 2.8.8). The count matches A001349(9) and no graph6 string
  repeats, but no second graph generator was used and pairwise non-isomorphism was not re-proved.
- The geng executable the run used is pinned in object/VALUE.txt (tools/geng) but not shipped here, since it is a
  third-party binary; a stranger builds nauty 2.8.8 from its source instead.
- The OEIS example for n = 8 (graph6 G?CidW, rule {0,2,4}) reaches only 10 in this run's checks; its complement,
  isomorphic to the saved optimum GCz^nw, reaches 96. This is reported as an observation about the entry, not a
  claim, and does not affect a(8) = 96.

## Credits

- Pontus von Brömssen: the sequence A357953, its terms a(1..8) and the example optima, https://oeis.org/A357953,
  and the related sequences https://oeis.org/A357951, https://oeis.org/A357952, https://oeis.org/A384209.
- The OEIS Foundation, https://oeis.org, and the count A001349 (https://oeis.org/A001349) used as a completeness control.
- Brendan McKay and Adolfo Piperno: nauty and its graph generator geng (https://pallini.di.uniroma1.it/), used to
  enumerate the graphs.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: credited through the GitHub account that submits this folder.
