# Independent criterion verdict

Context: fresh headless `opencode run --standalone` (role criterion), isolated independent skeptic. Read only supplied `claim/` material and own instructions/artifacts; did not read the author's checker, parent research, or other verdicts. No subagents, submissions, posts, or pushes; one read-only public table fetch, no retries. `claim/` was not modified.

confirmed_scope: Object SHA256 8331cb2690217f6bc34b22a833f9690d19c87b0fa71db0113b1a12011d47fdb7 has N=8425, maximum degree 14 and diameter 4, exceeding the nonbold live general-graph (14,4) cell value 8303 at https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html fetched on 2026-10-20T22:38:09.928483+00:00.

## Executed evidence

- Exact object: `claim/G_14_4_n8425.edges`, SHA256 `8331cb2690217f6bc34b22a833f9690d19c87b0fa71db0113b1a12011d47fdb7` (matches the claimed hash).
- Independently implemented `check_graph.py` parsed all edges, rejected loops and duplicate unordered edges, checked vertex bounds and sparse-matrix symmetry, and ran unweighted SciPy shortest-path BFS from **every one of 8425 roots**, in batches of 128. No transitivity assumption or sampling. Execution: 6.469 seconds; full results in `graph_evidence.json` and `graph_check.log`.
- 58,971 undirected edges; minimum degree 13, maximum degree 14; connected; every root has eccentricity exactly 4; zero ordered pairs beyond distance 4 and zero unreachable ordered pairs. Vertices 0 and 1 witness distance 4.
- Moore bound: `1 + 14(1 + 13 + 13² + 13³) = 33321`; `8425 <= 33321`.
- `test_checker.py` executed successfully: path with diameter violation, disconnected graph, loop rejection, reversed duplicate rejection, valid triangle. See `test_checker.log`.
- `fetch_table.py` made one request, HTTP 200, started `2026-10-20T22:38:09.268875+00:00`, completed `2026-10-20T22:38:09.928483+00:00`. Saved response `live_table.html`, SHA256 `e155b7ea159c5dd6f43808767b3e31ed386dfaf7c4969bec4e7d07d50c1c17ab`; response headers and timestamps in `fetch_evidence.json`. Server Date: `Tue, 20 Oct 2026 22:38:09 GMT`.
- Table header identifies diameter columns 2, 3, 4, etc.; degree-14 row's third cell links to `desc_g/desc_g4.html#144` and reads `8 303`, with no bold markup or bold inline style. `finish_evidence.py` extracted and asserted this comparison; see `table_cell_evidence.json` and `finish_evidence.log`. Strict improvement is **122**, not equality and not comparison with a special-class table or repository record.
- Literal representation check: the source is an explicit edge list, not adjacency-list syntax. Independently converted its exact undirected edges to the explicit per-vertex adjacency list `verified_adjacency.txt` (8425 rows, `vertex: neighbors`), SHA256 `d76d4e93101af4dde578d22c26b3213f59a099216f21f7f40f9efe5551844a3e`. This supplies the adjacency-list artifact without altering the object.

## Conclusion

All five success conditions hold for this exact object and this fetched table state. The comparison is time-specific, not an optimality claim or a promise about future table updates. This is a deterministic explicit graph; no chance/null test is applicable. Partial-win alternatives are unnecessary.

Reproduce locally using the supplied environment:

```bash
../../../../.venv/bin/python test_checker.py
../../../../.venv/bin/python check_graph.py
../../../../.venv/bin/python finish_evidence.py
```

The final command uses the saved live response; it does not issue another request.

pass: true
