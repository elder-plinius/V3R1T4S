# Criterion report: mixed-z2-r8-g6-n234

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

Method. I read the package folder and the saved paper excerpt, wrote my own checker (Python for the degree and simplicity tests, a C program for exhaustive short-cycle search), and fetched once the live paper page https://arxiv.org/html/2506.20003 (2026-10-19T05:28:03Z, HTTP 200, sha256 1b1cc422cd10a41255b96a03e4a544a5d337ddbfa0aa3759907e1be647f02537, identical to the folder's hash) to quote definitions in full. Its output is not shipped in this package.

Target and win text. Target cage-upper-bounds, partial win p2: 'A graph strictly beating a live entry of the separate girth-diameter cage table (arXiv 2511.21144) or the mixed-cage table (arXiv 2506.20003), verified exactly against that table's own definition; logged as a partial win, never as a cage record.' The main criterion explicitly says mixed cages do not count, so only p2 can apply.

Which cycle convention is the table's? I decided on the forward-arc convention, for these reasons.
- Definition quoted from the paper: 'We represent walks, paths, and cycles as sequences of the form (v_0, v_1, ..., v_n), where each consecutive pair v_i and v_{i+1} is either edge- or arc-adjacent', and 'Two vertices u and v are said to be edge-adjacent (respectively, arc-adjacent) if there exists an edge (respectively, an arc) between them.' Read alone this is ambiguous: 'arc-adjacent' does not say whether the arc must point from v_i to v_{i+1}.
- The paper's own usage settles it. Lemma 2 speaks of 'directed girth 6' of the circulants and Lemma 3 proves 'no mixed cycle of length 4' by checking arc directions: 'there is no arc from (x', ...) to (x, y) by construction'. That argument is only needed if an arc may be used only forward. The paper also states that the circulant digraph C_q(1,...,z) with q = z(g-1)+1 is a [z,0;g]-mixed graph; for z = 2, g = 6 that is the circulant on 11 vertices with jumps 1 and 2, which has directed girth 6 but, read direction-blind, has triangles (0,1,2).
- The table's own numbers cannot satisfy the direction-blind reading. In the direction-blind reading a [z,r;g] graph is a (2z+r)-regular graph of girth g. For [1,2;6] that is a 4-regular girth-6 graph, which needs at least 26 vertices (the (4,6)-cage), yet Table 1 lists 18 as exact. For [2,8;6] the direction-blind reading is a 12-regular girth-6 graph, whose Moore bound is 266; the listed upper bound 252 is below that, which is impossible for a direction-blind graph, so the table cannot be using that reading.
So the forward-arc convention is the table's own definition, and the claim's statement of it is correct. Under it the object must have no cycle of length 2 to 5.

Clauses, checked:
1. Valid [2,8;6]-mixed graph on 234 vertices: MET. Every vertex has 8 edges, 2 in-arcs and 2 out-arcs (exact degree counts); no loops, no parallel edges, no parallel or antiparallel arcs, no arc and edge on the same pair; the underlying graph is connected.
2. No cycle of length 2, 3, 4 or 5 under the forward-arc convention: MET. Exhaustive search of all simple closed walks of length up to 6 from every start vertex (edges both ways, arcs forward only) finds none of length 2 to 5 and finds cycles of length 6 (so the girth is exactly 6). See my checker's output (not shipped).
3. Direction-blind check (for completeness): shortest cycle 4 for this object, as the claim itself states; this reading does not apply.
4. Strictly below the live entry: MET. The live Table 1 row for [2,8;6] has lower bound 155 (marked as conditional on a conjecture) and upper bound 252, listed without an earlier citation (the paper's own construction). 234 < 252, and 234 > 155.
5. p2 'logged as a partial win, never as a cage record': accepted as the only claim made. This is not a (k,g)-cage record for a regular undirected graph.

Hidden quantifiers and null models. The comparison is to the table's own listed upper bound for one row, not to any cage table. The object is a constructive upper bound; the conditional lower bound does not constrain it. No requirement of exact girth beyond 6 is hidden. I did not check whether a newer source improves the row (novelty role).

Open questions in the claim record (not shipped) that concern this role.
- Which cycle convention does the table use? Answer: forward-arc, as argued above, with the quotes.
- Does a smaller upper bound with an explicit graph meet p2 ('strictly beating a live entry ... verified exactly against that table's own definition')? Answer: yes; it is an explicit graph, verified exactly under the table's definition, smaller than the listed entry.
- Is the conjectural lower bound 155* relevant? Answer: no. It is a lower bound conditional on a conjecture about directed cages; the object lies above it and it does not affect an upper-bound entry.
- Inconsistencies in the author's own lower-bound table? Answer: not used here; only the row for [2,8;6] of the live table is used, and I read that row from the saved excerpt.
- Review the construction as well as the lists? Answer: not needed for the criterion; the explicit lists are the object and were verified exactly.

confirmed_scope: Under the forward-arc cycle convention that the source paper's table uses, the object is a connected [2,8;6]-mixed graph on 234 vertices (every vertex 8 edges, 2 in-arcs, 2 out-arcs, girth exactly 6), which is a partial win p2 against the listed upper bound 252 for [2,8;6] in arXiv 2506.20003 Table 1, and not a cage record.

pass: true
