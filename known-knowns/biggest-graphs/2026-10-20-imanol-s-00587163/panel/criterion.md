# Criterion verdict

Context: fresh headless opencode run --standalone (role criterion).

Object: `claim/object/G_13_4_n6637.edges`; exact SHA-256: `00587163283c37fbb2d5d83ebd2c533e010af603f5e27d59a01c55a527185059`.

## Reproduced finite-object checks

Independent code `check.cpp`, compiled and executed through `run.py`, parses the actual two-column encoding, rejects extra tokens, loops, repeated undirected edges and out-of-range labels, and builds symmetric adjacency. All labels 0 through 6636 occur. Results: 6637 vertices, 43140 distinct undirected edges, minimum degree 12, maximum degree 13, connected, diameter exactly 4. BFS was run independently from every one of the 6637 vertices, without quotient, transitivity or construction assumptions. Ordered distance counts for distances 0 through 4: 6637, 86280, 1032870, 10869336, 32054646. The Moore bound is 1 + 13 + 156 + 1872 + 22464 = 24506, greater than 6637. Compilation and checking both exited 0; check runtime was 0.723 seconds. `receipt.json` records commands, elapsed times, UTC timestamps and hash.

## Binding comparison

One honest GET of the live primary general-graph table, with no retry, returned HTTP 200 at 2026-10-20T21:28:07Z. Saved bytes: `live-table.html`; SHA-256 `e155b7ea159c5dd6f43808767b3e31ed386dfaf7c4969bec4e7d07d50c1c17ab`. Source: https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html . The header explicitly orders diameter columns starting 2, 3, 4; row 13's third data cell is `6 615` linking to `desc_g/desc_g4.html#134`. This cell has no bold markup; its inline border is not boldface, and the table stylesheet only removes link decoration and inherits colour. The page identifies bold entries as optimal. Thus 6637 strictly exceeds the live entry by 22; no proven-optimal entry is being beaten.

The earlier 6631 object is not counted as a new result. Separate live read-only GitHub requests covered all three pages of open PRs (284 entries); the only degree-diameter matches were #598, claiming 6631 for (13,4), and #457 for a different cell (14,3). No subsuming (13,4) claim was found there. This candidate exceeds the already submitted 6631 record by 6, and the supplied pinned trophy's 6630 by 7. Raw responses are `live-open-prs.json`, `live-open-prs-2.json` and `live-open-prs-3.json`; timestamped request receipts and matching bodies are `novelty-receipt.json` and `remaining-receipt.json`, produced by `novelty.py` and `remaining.py`. These comparisons establish non-subsumption against the live primary table and inspected submissions, not a universal literature novelty proof. This is one object for one cell, not a claim for every degree/diameter pair, optimality, heuristic exclusion or a special graph class. No partial-win criterion or null control is needed for the demonstrated full finite-object criterion.

confirmed_scope: The explicit graph with SHA-256 `00587163283c37fbb2d5d83ebd2c533e010af603f5e27d59a01c55a527185059` has 6637 vertices, maximum degree 13 and diameter 4, exceeding the (13,4) value 6615 in the live Comellas general-graph table at https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html fetched on 2026-10-20T21:28:07Z.

pass: true
