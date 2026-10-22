context: Claude Code subagent, fresh context [Claude Sonnet 5.5]
# Reproduce report, mixed-z2-r7-g6-n184

Folder integrity: ran the hash list from inside the package folder (the paths in that list are relative to the package folder); every listed file reported OK. I then worked only on a private copy of the package. No network was used.

## Definition (quoted)
Claim: "object/mixed_z2_r7_g6_N184.json describes a [2,7;6]-mixed graph on 184 vertices (every vertex has 2 in-arcs, 2 out-arcs and 7 edges), with no cycle of length 2, 3, 4 or 5 when cycles follow edges in either direction and arcs only forward (the forward-arc cycle convention), which is below the upper bound 196 listed for [2,7;6] in Table 1 of arXiv:2506.20003."
Source paper definitions (the-record-we-beat/paper_excerpt.txt, quoted): "We represent walks, paths, and cycles as sequences of the form (v_0, v_1, ..., v_n), where each consecutive pair v_i and v_{i+1} is either edge- or arc-adjacent. The girth of the graph is defined as the length of its shortest cycle. ... A mixed graph is called regular if each vertex has exactly z incoming arcs, z outgoing arcs, and r undirected edges."
The excerpt does not say outright whether an arc may be traversed against its direction. The cell's claim states the forward-arc convention (an edge in either direction, an arc only from tail to head).

## My checker (written before opening verify-it-yourself/)
- My own checker (written from scratch, not shipped in this package): loads the stored edge list and arc list only (it does not rebuild from generators), checks indices in range, no loops, no repeated edge or arc, each vertex has exactly r edges, z=2 in-arcs and 2 out-arcs, no vertex pair joined twice (edge plus arc, or two arcs), and computes the direction-blind girth (every edge and arc as one undirected link, BFS from every vertex).
- A second program in C (compiled with cc -O2; its input made by a small dump script; neither is shipped in this package): exhaustive depth-first search from every vertex over the forward digraph (each edge usable both ways, each arc only tail to head), counting every simple closed walk of length 2 to 6, excluding only the trivial use of the same edge back and forth. Counts for lengths 2..5 must be zero; length 6 must be positive.
Real output of these two programs:
== mixed-z2-r7-g6-n184
N 184 edges 644 arcs 368
no loops True
edges distinct (no repeats) True
arcs distinct True
edge deg all r True in all z True out all z True
max adjacencies per vertex pair 1 pairs with >1: 0
direction-blind girth 4
forward-arc convention, simple cycles up to length 6:
len 2: 0 (closed cycles counted from each start vertex)
len 3: 0 (closed cycles counted from each start vertex)
len 4: 0 (closed cycles counted from each start vertex)
len 5: 0 (closed cycles counted from each start vertex)
len 6: 761760 (closed cycles counted from each start vertex)
(The length-6 count is per start vertex, so each cycle is counted six times; all that matters is zero for 2..5 and positive for 6.)

## Both conventions
- Forward-arc convention (the one the claim states): no cycle of length 2, 3, 4 or 5; cycles of length 6 exist; so the girth is exactly 6. Reproduces.
- Direction-blind convention: girth 4, as printed above. So the claim reproduces ONLY under the forward-arc convention; I report that plainly.
- Which convention the source table uses, from checks on the saved data alone: if arcs were read as undirected links, this graph would have underlying degree 7 edges + 2 in-arcs + 2 out-arcs = 11 (it is a simple graph, no pair joined twice), and a graph of degree 11 with girth 6 needs at least the Moore bound 2(1 + 10 + 10^2) = 222 vertices. The saved Table 1 upper bound for this row is 196. That is below the Moore bound, so under the direction-blind reading no [2,7;6] mixed graph of order 184 (or of the listed order 196) could exist; the claimed order and the table entry are only possible if cycles are forward-arc cycles.
  Row [1,2;6] (exact value 18 in the saved table): underlying degree 1+1+2 = 4, Moore bound for girth 6 is 26 > 18, so the table's exact value 18 is impossible under the direction-blind reading. Together these indicate that the saved table counts forward-arc cycles. This is my own inference from the saved excerpt, not a statement of the paper.

## Cell values
Order N = 184; saved upper bound for [2,7;6] = 196; N < 196: True. Parameters in the file: N = 184, edges, arcs counts above match N*r/2 edges and 2N arcs.

## Author's checker (run only after mine)
sha256 matches INDEX.csv (fc561db7e3e7b50619bb4b6e8673994ad0192d582bab9c29a40ba7b2769cd00b)
checker verdict: PASS (valid under the forward-arc convention=True, N=184, table upper bound 196; direction-blind girth=4)
== negative control: one arc head changed must NOT be valid
negative control rejected as expected
ALL CHECKS PASS
It also reports stored lists equal to the graph rebuilt from the generators; agrees with my results (forward girth 6, direction-blind girth 4).

## Verdict
Regularity, simplicity, absence of forward-convention cycles of length 2..5 and presence of length 6 reproduce exactly by exhaustive search (not sampling). Under the direction-blind convention the girth is 4. The claim as written (forward-arc convention) reproduces; whether that convention is the table's is a criterion matter, with the Moore-bound inference above as supporting evidence.

pass: true
