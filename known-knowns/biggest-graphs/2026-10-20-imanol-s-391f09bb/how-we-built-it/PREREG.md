# PREREG - degree-diameter-table

Written 2026-10-20T18:42Z, before any attack output was produced this run.

## Criterion (verbatim from bank/targets.json)

(1) Explicit adjacency list of a simple undirected graph G on N vertices. (2) Maximum degree <= Delta. (3) G connected with diameter <= D, checked by all-pairs BFS, or by one BFS plus a machine-checked vertex-transitivity proof (explicit Cayley group and generators regenerating exactly the submitted edge set). (4) N STRICTLY GREATER than the (Delta,D) entry of the live Comellas general-graph table at https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html, re-fetched immediately before claiming (the table changes daily). (5) N <= Moore bound; boldface (proven-optimal) entries cannot be beaten, so beating one signals a bug.

## Statistic and checker

- Statistic: N, the number of vertices of one explicit edge list, with max degree and diameter
  recomputed from the edge list alone by two independent implementations:
  (a) `attempts/evaluator/code/ddcheck.py` - pure standard library, all-pairs BFS;
  (b) `attempts/evaluator/code/verify_scipy.py` - scipy.sparse.csgraph.shortest_path.
- Thresholds: N strictly greater than the live cell AND strictly greater than the shipped trophy
  N for the same cell. Targets: (15,4) >= 13366; (13,4) >= 6631; (15,3) >= 1621; (14,4) >= 8425;
  (13,6) >= 535496; (15,6) >= 1424897.
- One graph, one cell, one claim. Equal N is a tie, not a win.
- The live table is re-fetched at claim time; if it has moved to or above the candidate, the
  claim is dead.

## Null design

null_test: not needed because the claim is one explicit graph checked by a deterministic,
exhaustive all-pairs checker against a table value; there is no search or statistical claim
being scored.

## Search budget and stopping rule

- Attack window: 2026-10-20T18:42Z to about 20:45Z; background jobs under `nice` with a hard time
  cap, checkpoints on disk, PIDs recorded.
- Stop a cell when one valid graph at or above its target exists; keep the program output that
  produced it. No threshold changes after results.
