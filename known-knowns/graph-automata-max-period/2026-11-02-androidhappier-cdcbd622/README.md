# A357952(9) = 200: the longest self-counting totalistic cellular automaton cycle on any connected graph with 9 nodes

## What

Confirmed scope, quoted word for word from panel/gate.md:

> Exhaustive enumeration of all 261080 connected 9-node graphs (geng -cq 9), all 1024 self-counting totalistic rules R ⊆ {0..9} and all 512 states, by two separately written programs that agree graph by graph and reproduce A357952(1..8), gives A357952(9) = 200, uniquely attained on graph H?o|]|~, with witness rule {1,3,5} from start state 1 directly simulated to a 200-cycle, and the term was absent from the live OEIS entry as of 2026-11-02 21:35Z.

(21:35Z is the claim-time re-fetch; the novelty panel re-fetched the live entry at 2026-11-02T21:50:44Z and got the
same bytes, still without a(9).)

OEIS A357952 (Pontus von Brömssen, Oct 2022) is the maximum period of a totalistic cellular automaton on a connected
graph with n nodes, **counting the state of the updated node itself**. Every node is ON or OFF, all nodes update
together, and a node is ON in the next generation iff the number of ON nodes among its neighbours *and itself* (its
closed neighbourhood) lies in the rule set R, a subset of {0, ..., n}; so there are 2^(n+1) rules (1024 at n = 9).
The maximum is over all connected graphs, all rules and all start states. The entry gives a(1..8) = 2, 2, 4, 6, 8,
18, 42, 112. This folder adds the next term:

    A357952(9) = 200

**Not to be confused with A357953**, the neighbours-only sibling, where the node itself is not counted, R ⊆ {0..n-1}
and A357953(9) = 180 has a different witness. The two are different automata on the same graphs; the programs here
run in the self-counting mode (totA's `self` argument adds the node's own bit, totB's closed-neighbourhood masks
include the node), and every checker in verify-it-yourself/ counts the node itself.

The object is object/VALUE.txt (sha256 cdcbd62283fd8901256f0c29257a5c5e97280c04dab1947d2254cf9804d8e8f6). It states
the value, the witness and the counts, and pins the sha256 of the programs (object/code/) and of every saved program
output (object/evidence/), with paths relative to object/.

Witness: the graph with graph6 string `H?o|]|~` (9 nodes, 22 edges, degrees 3,3,3,3,6,6,6,7,7), rule {1,3,5}
(ON next iff 1, 3 or 5 nodes of the closed neighbourhood are ON), started from state 1 (node 0 ON, all others OFF,
vertex order as in graph6), is on a cycle of exactly 200 steps (preperiod 0). Rule {1,3,5,9} gives the same cycle,
since no closed neighbourhood here has 9 nodes. It is the only one of the 261,080 graphs that reaches 200; the next
best is 198 (HEjfayn).

How the number was obtained (how-we-built-it/):
- Program A (totA.c, run as `totA self`; totA_pg.c adds a per-graph output line) reads every connected graph on 9
  nodes from nauty's geng (`geng -cq 9`, 261,080 graphs = OEIS A001349(9)), precomputes closed-neighbourhood counts
  for every node and state, builds the successor map for each of the 1024 rules, and takes the longest cycle by
  stamped walks over all 512 states.
- Program B (totB.go) was written separately in Go: its own graph6 parser, closed-neighbourhood bit masks, the
  successor map for every rule, transient states removed by in-degree peeling, every remaining cycle walked once.
- Both reproduce A357952(1..8) with graph counts equal to A001349(1..8). At n = 9 they print the same maximum for
  every one of the 261,080 graphs (diff_AB.py), the same histogram and the same witness in each of the 8 geng
  residue classes.

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: a few seconds. Requirements: Python 3 (standard library only), plus
a C compiler and Go for the compiled part of step 5 (skipped without them). The script checks the hash of
object/VALUE.txt against INDEX.csv and every pinned file. It checks the saved graph counts, the published terms
a(1..8) and the graph-by-graph agreement of both programs at n = 9. It simulates the witness from the definition,
checks that no rule or start on the witness graph beats 200, and recomputes a(1..6) from all labelled graphs with no
nauty. It runs pure Python and both compiled programs on the saved optimal graphs for n = 1..8, the OEIS examples
for n = 7 and 8, and the witness. To recompute a(1..9) itself (about 16 minutes on 8 cores), put nauty's geng on
PATH (or set GENG) and run `FULL=1 sh verify-it-yourself/run_checks.sh`; the fresh outputs must be byte-identical to
the saved ones. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A357952 (revision #12, Oct 23 2022), DATA and draft | a(9) | absent (DATA ends at a(8) = 112; draft: no pending changes) | 200 | 2026-11-02T21:05:02Z (scout); 2026-11-02T21:35:11Z (claim-time re-fetch); 2026-11-02T21:50:44Z (novelty panel); gate review 2026-11-02T21:56:04Z |

URL: https://oeis.org/A357952 (text form https://oeis.org/search?q=id:A357952&fmt=text). The fetch record is in
the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only one cell, A357952(9). A357952(10) and the related sequences A357951, A357953 and A384209 are not claimed
  here (A357953(9) and A384209(10) are separate submissions and separate cells).
- This is an exact computer enumeration, not a proof by hand. It rests on two programs, written separately in the
  same run, that agree graph by graph (and on a third checker by the reproduce skeptic, panel/reproduce.md). All of
  them take their graphs from the same nauty geng binary (version 2.8.8). The count matches A001349(9) and the run's
  self-break check found 261,080 distinct canonical forms, but no second graph generator was used.
- The geng executable the run used is pinned in object/VALUE.txt (tools/geng) but not shipped here, since it is a
  third-party binary; a stranger builds nauty 2.8.8 from its source instead.
- Uniqueness means: one graph (up to isomorphism) reaches 200. On that graph two rules reach it, {1,3,5} and
  {1,3,5,9}, which act identically there.
- panel/ holds the panel files as written, except that one machine-local scratch path in panel/reproduce.md was
  replaced. panel/REDACTIONS.md lists the change and the original files' sha256.

## Credits

- Pontus von Brömssen: the sequence A357952, its terms a(1..8) and the example optima, https://oeis.org/A357952,
  and the related sequences https://oeis.org/A357951, https://oeis.org/A357953, https://oeis.org/A384209.
- The OEIS Foundation, https://oeis.org, and the count A001349 (https://oeis.org/A001349) used as a completeness control.
- Brendan McKay and Adolfo Piperno: nauty and its graph generator geng (https://pallini.di.uniroma1.it/), used to
  enumerate the graphs.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: credited through the GitHub account that submits this folder.
