# REPRODUCE skeptic: A357953(9) = 180

context: subagent (reproduce skeptic, isolated claim copy)

## Definition used (quoted from claim.md / data/A357953.txt, sha256 e217d9de...4754c re-checked)
"Maximum period of a totalistic cellular automaton on a connected graph with n nodes (not counting the state of the
updated node itself). Each node can be in one of two states, ON or OFF. The automaton is totalistic, meaning that the
state of a node in the next generation depends only on the number of ON-nodes among its neighbors. ... a(n) is the
maximum of the length of that cycle, over all connected graphs with n nodes, all totalistic updating rules, and all
initial states."
Rule convention (OEIS examples): set R of neighbour counts; node ON next iff its ON-neighbour count is in R; for n nodes
all 2^n subsets of {0..n-1}.

## Own checker (written before opening code/totA.c or code/totB.c)
C program (kept outside panel/), different method from the author's:
- parses graph6 itself (upper triangle column order, 6-bit big-endian) and checks each graph is connected (BFS on bitmasks);
- per graph precomputes M[s][c] = set of nodes with exactly c ON neighbours in state s; successor under rule R is
  OR over c in R of M[s][c], built incrementally over all 2^n rules (R from R minus its top bit);
- exact cycle lengths by a full functional-graph traversal of all 2^n states for each rule (every state visited once,
  each newly closed cycle measured by position difference). No sampling, no hashing, no Brent/Floyd.
- records overall max + witness and a histogram of per-graph max (over rules and starts).
Independent witness stepper in Python (own graph6 parser, dict-based cycle detection).

## Results
- n=1..8 (tools/geng -cq n): graph counts 1,1,2,6,21,112,853,11117; maxima 1,2,2,6,7,18,38,96 = OEIS DATA. OK.
- n=9, run 1 (geng -cq 9 r/8, r=0..7, 8 parallel): part counts 44686,35236,38391,18939,20847,12060,56096,34825,
  sum 261080 = A001349(9). All graphs connected. Max = 180, witness H?`DBbS rule mask 5 = {0,2}, cycle state 175.
- n=9, run 2 (single unsplit geng -cq 9 stream): 261080 graphs, max 180, same witness; per-graph-max histogram identical
  to the split run. No duplicate graph6 strings among the 261080 (sort | uniq -d empty).
- n=9, run 3 (split again): per-part output and histograms byte-identical to run 1. Deterministic.
- My per-graph-max histogram (n=9) equals result/A_n9_merged.txt graphs_by_max_period_over_rules exactly, and each
  per-part histogram equals the `hist` lines in result/A_n9_part{0..7}.txt. Per-part max/witness lines also identical.
- Witness by direct simulation (own Python): H?`DBbS (9 nodes, 11 edges, degrees [3,3,2,2,1,2,2,3,4]), rule {0,2},
  start 175: preperiod 0, period 180. Program B's witness state 2 (same graph/rule) also lies on a 180-cycle.
  code/tstepper.py gives cycle_length=180, matching result/witness_simulation.txt.

## Author programs (opened only after the above)
- Compiled code/totA.c and code/totB.c (gcc -O2); n=1..8 both print 1,2,2,6,7,18,38,96 with counts as OEIS/A001349.
- Re-ran both at n=9 (8 parts each): outputs identical to saved result/A_n9_part*.txt and result/B_n9_part*.txt except
  that each saved file carries an extra trailing line "exit 0" (wrapper exit-status record); no content difference.
- A and B saved results agree: both merged files report 261080 graphs and max 180 at H?`DBbS, rule {0,2}; per-part
  graph counts and maxima agree between A and B for all 8 parts.

## Caveat
Graph completeness relies on nauty geng (tools/geng, sha256 75d1bf01...e91f450 re-checked): verified count 261080 =
A001349(9), all connected, no repeated strings; pairwise non-isomorphism was not independently re-proved (standard
reliance on geng, as in the criterion). Did not check novelty/live OEIS status (not this role).

pass: true
