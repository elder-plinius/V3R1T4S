# Independent skeptic verdict

Context: fresh headless `opencode run --standalone` (role reproduce). Only `claim/` and the supplied instructions were read as input; no author checker was consulted and `claim/` was not modified.

Object: `claim/G_14_4_n8425.edges`, SHA-256 `8331cb2690217f6bc34b22a833f9690d19c87b0fa71db0113b1a12011d47fdb7`.

The graph definition was quoted in `definition.md` before writing the independent checker. `skeptic_check.py` completed successfully; `evidence.json` records strict ASCII edge-record parsing (whole-line `#` comments allowed), endpoint-range checks, loop and duplicate rejection, connectivity, 8,425 vertices, 58,971 edges, minimum degree 13, maximum degree 14, and exact diameter 4. Every one of 8,425 roots has eccentricity 4. All 70,980,625 ordered pairs including self were checked. Ordered-pair distance counts: 0: 8,425; 1: 117,942; 2: 1,381,794; 3: 14,372,414; 4: 55,100,050. The Moore bound is 1 + 14(1 + 13 + 169 + 2197) = 33,321, above 8,425.

Executed negative controls rejected malformed records, blank records, out-of-range vertices, loops, reversed duplicate edges, excessive degree, disconnected graphs and a four-vertex path exceeding diameter bound 2. A positive path control verified exact diameter 3. The first distance engine used SciPy unweighted shortest paths; the separate `bfs_check.py` directly invokes breadth-first traversal from every root and compares the full distance histogram.

`bfs_check.py` completed all 8,425 actual breadth-first traversals; `bfs_evidence.json` exactly matches the independently computed shortest-path histogram above. Its four-vertex path control also produced diameter 3, rejecting bound 2. No root sampling or transitivity assumption was used.

The live general-graph table was fetched read-only once, immediately during verification, with HTTP 200 at 2026-10-20 22:45:08 UTC. `table_fetch.json` records the response and timestamps. Saved response `live_table.html` has SHA-256 `e155b7ea159c5dd6f43808767b3e31ed386dfaf7c4969bec4e7d07d50c1c17ab`. Its degree-14 row and diameter-4 column, linking to `desc_g/desc_g4.html#144`, show 8,303 without boldface. Thus 8,425 strictly exceeds the live entry by 122; no proven-optimal entry is contradicted. The claim's separate pinned value 8,424 is smaller by one, but its repository provenance was not independently authenticated and is not needed for the live-table success criterion.

Executed commands (all shell executions used background mode):

```bash
../../../../.venv/bin/python skeptic_check.py > checker.log 2>&1
../../../../.venv/bin/python bfs_check.py > bfs.log 2>&1
../../../../.venv/bin/python fetch_table.py > fetch.log 2>&1
../../../../.venv/bin/python compare_inputs.py > comparison.log 2>&1
```

`compare_inputs.py` completed successfully. `comparison.json` confirms that the explicit adjacency list `claim/verified_adjacency.txt` has exactly vertices 0 through 8424, no repeated neighbors, reciprocal adjacency, and precisely the submitted edge set. Its SHA-256 is `d76d4e93101af4dde578d22c26b3213f59a099216f21f7f40f9efe5551844a3e`. The same executed check locates the live table cell by row and column, verifies its link and non-bold formatting, and confirms the 122-vertex improvement.

Conclusion: all five stated success criteria are satisfied for the supplied object against the freshly fetched table. This verifies the candidate, not optimality or independent publication priority. No posts, submissions, pushes, or other outward changes were made.

pass: true
