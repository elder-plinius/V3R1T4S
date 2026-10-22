context: Claude Code subagent, fresh context [Sonnet 5.5]

# novelty report: mixed-z2-r7-g6-n184

Claim: a [2,7;6]-mixed graph (2 in-arcs, 2 out-arcs, 7 edges per vertex) on 184 vertices with no cycle of length 2 to 5 under the forward-arc convention, below the Table 1 upper bound 196 of arXiv:2506.20003. Target cage-upper-bounds, enumerated partial win p2 (a graph strictly beating a live entry of the mixed-cage table; logged as a partial win, never as a cage record).

Read from the package folder: README.md, INDEX.csv, the-record-we-beat/paper_excerpt.txt.

## Common sources (fetched once; the time, HTTP status and sha256 of each fetch are given with its URL)

- Fetch method: plain curl with the honest client string, one request per URL, no retries. Times are UTC. Where a fetch needed a deviation it is stated under unresolved.
- TROPHY_CASE.md: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, 2026-10-19T05:27:03Z, HTTP 200, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1. It lists six result families (degree-diameter graphs, constant-weight codes, matrix multiplication, the Lehmer bound, VNN-COMP counterexamples, a RobustBench attack) plus two cipher commitments. No row for mixed cages.
- known-knowns listing: https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns, 2026-10-19T05:27:03Z, HTTP 200, sha256 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011. Twenty directories; there is no directory for cage-upper-bounds.
- Pull requests: I used a snapshot of all V3R1T4S pull requests (titles and bodies; 473 entries, fetched 2026-10-19T04:30:31Z) instead of the api.github.com pulls pages, and did not fetch the API pulls pages. I read every title and searched every body for the target id and keyword (cage-upper).
- The contributor's review ruling R1: closed pull requests from the 2026-10-14 bulk close by the same contributor (#65-#120) are the author's own earlier filings, not competing values. They are reported, not counted against a cell.

## Primary sources (mixed cages of girth 6)

- Table 1 of arXiv:2506.20003 "New upper bounds on the order of mixed cages of girth 6": https://arxiv.org/html/2506.20003, fetched 2026-10-19T05:27:04Z, HTTP 200, sha256 1b1cc422cd10a41255b96a03e4a544a5d337ddbfa0aa3759907e1be647f02537 (same sha256 as the triage fetch). I parsed Table 1 (columns Arcs, Edges, Girth, Lower bound, Exact, Upper bound). Rows used: Arcs 2, Edges 7: lower 123*, upper 196 [6]; Arcs 2, Edges 8: lower 155*, upper 252; Arcs 2, Edges 9: lower 191*, upper 320; Arcs 2, Edges 11: lower 275*, upper 480. The star means conditional on a conjecture.
- Source paper of the 196 entry: arXiv:2401.14768 "On Mixed Cages of Girth 6" (https://arxiv.org/html/2401.14768, 2026-10-19T05:33:30Z, HTTP 200, sha256 8d5d16e124ebdb0718bc00afe9615a95f19ac18c40a4f9b1d1e92bd50ed36975).
- Newer literature: arXiv API query 4 of 4 (mixed graphs and girth, newest first, 2026-10-19T05:32:39Z, HTTP 200, sha256 a237665ab66c31009e88a61c109990d47b130275316637f18364106d7ac5c1ea). The newest paper is 2610.14110 "New mixed cages, bounds and computational results" (2026-10-09; https://arxiv.org/html/2610.14110 fetched 2026-10-19T05:32:54Z, HTTP 200, sha256 1f5753e7a09b688e0c6bb329d67d8d5a461f6c9bbc03e55304b81ea9adb7972d). It treats girth 3 and 4 exactly and gives computational tables for small parameters; I searched its text for the order 184 and for girth 6 entries with 2 arcs and 7 edges and found none. Other results: 2503.17152 (girth 5), 2401.14768, 2506.20003.
- Pull requests on this target: the contributor's closed #102 ([2,7;6] 184) (R1: own earlier filing; the claim states the same graph). No other contributor has a pull request on cage-upper-bounds in the snapshot; no merged package exists for this target.

## Cycle convention (first open question), settled from the table itself

The table cannot be using the direction-blind convention (every arc treated as an undirected adjacency). Evidence in the table I fetched: the row Arcs 1, Edges 2, Girth 6 has Exact 18 (citing a published mixed cage). A vertex of a [1,2;6] graph has 1 in-arc, 1 out-arc and 2 edges, i.e. 4 neighbours. A 4-regular graph of girth 6 needs at least 2(1 + 3 + 9) = 26 vertices (Moore bound for girth 6, degree 4), so an exact value 18 is impossible under the direction-blind convention. Likewise Arcs 2, Edges 2 has upper bound 27, while a 6-regular girth-6 graph needs at least 2(1 + 5 + 25) = 62. So the table's entries are forward-arc entries: a cycle may use an edge in either direction but an arc only from tail to head. The papers say the same in their proofs: 2401.14768 argues that a mixed 4-cycle "requires two arcs, one leaving B_q ... and one entering it", and builds its lower bound from a directed circulant of directed girth g, to which "adding any new arc ... creates a directed cycle". The object's girth 4 under the direction-blind convention (reported in README.md) therefore does not matter for comparability with the table; the forward-arc girth is the right one. Whether the object has forward-arc girth 6 is for the reproduce role.

## This cell

Table entry compared: [2,7;6], lower bound 123*, upper bound 196 [6] (live Table 1 as fetched). Claimed order: 184, which is 12 below the upper bound and above the lower bound.

Newer sources: none with girth 6, 2 arcs and 7 edges (see arXiv:2610.14110 above). Open and merged pull requests by others: none. Earlier own filing: #102, the same graph (R1, reported, not competing).

Propagation (PR #350 rule): monotonicity or edge/arc deletion from other table rows cannot give this value, because every other table row with at least 2 arcs and at least 7 edges has an upper bound above 184 (480, 484, 672, ... for the larger ones) and deleting a perfect matching of edges from a bigger graph does not reduce the order. A smaller-parameter row does not bound a [2,7;6] graph from above. The value is a construction result.

## Open questions for the panel, as far as they concern novelty

1. Cycle convention: the table uses the forward-arc convention (evidence under the cycle-convention heading above, from the table's own Exact 18 entry against the Moore bound 26 and from the source paper's proofs). The direction-blind girth 4 of the object is therefore not a conflict with the table. The paper's Preliminaries do not state it outright, as README.md says; the inference from the table and proofs is what I rely on.
2. Does a smaller order with an explicit graph meet p2 ("strictly beating a live entry ... verified exactly against that table's own definition")? For novelty: 184 is strictly below the live entry 196 under the same convention, so it beats the entry. Whether the exact verification meets p2 is for the criterion and reproduce roles.
3. The conditional lower bound 123* is below the claim and consistent with it; it is not relevant to whether the upper bound is beaten. It is marked as depending on a conjecture, so it proves nothing against the claim in either direction.
4. The author's own lower-bound table disagreeing with the live Table 1: I used only the live row for [2,7;6] and quote it above, so the disagreement does not affect this comparison.
5. Reviewing the generator construction itself is for the reproduce and criterion roles; the closed #102 used the same construction.

unresolved: Google Scholar was not searched; only the four arXiv queries of the group budget were used (query 4 covers mixed graphs and girth, and the newest paper found does not contain these parameters). The Dynamic Cage Survey and the combinatorics journal were not fetched; Table 1 of the 2025 paper is the table the claim names. Whether the object has forward-arc girth 6 and the stated degrees is for the reproduce role.

novelty verdict: the order 184 is strictly below the live Table 1 entry 196 for [2,7;6], no newer source or pending value is below it, and it does not follow from other table rows.

pass: true
