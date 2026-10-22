# Frozen protocol

UTC: 2026-10-20T22:28:23.939195+00:00

(1) Explicit adjacency list of a simple undirected graph G on N vertices. (2) Maximum degree <= Delta. (3) G connected with diameter <= D, checked by all-pairs BFS, or by one BFS plus a machine-checked vertex-transitivity proof (explicit Cayley group and generators regenerating exactly the submitted edge set). (4) N STRICTLY GREATER than the (Delta,D) entry of the live Comellas general-graph table at https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html, re-fetched immediately before claiming (the table changes daily). (5) N <= Moore bound; boldface (proven-optimal) entries cannot be beaten, so beating one signals a bug.

null_test: not needed because claims are explicit finite graphs checked deterministically against a live table; no statistical or beats-chance claim is made.

Statistic: N, maximum degree, connectedness, exact all-pairs diameter, strict edge-list parser, and Moore bound. Threshold: N strictly greater than both the live cell and all known trophy/open-submission values; never claim boldface entries. Initially search (14,4) from 8424 and (15,3) from 1620; may test (15,4) from 13365. One object/cell per claim. Search costs and cover failures are heuristic diagnostics, never impossibility. Independent all-roots SciPy checks precede fresh three-skeptic contexts; exact criterion gate and kit checker required. Deadline from start.json is binding.
