# A 6637-vertex graph with maximum degree 13 and diameter 4

## What

The explicit graph with SHA-256 `00587163283c37fbb2d5d83ebd2c533e010af603f5e27d59a01c55a527185059` has 6637 vertices, maximum degree 13 and diameter 4, exceeding the (13,4) value 6615 in the live Comellas general-graph table at https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html fetched on 2026-10-20T21:28:07Z.

The object is `object/best_n6637_s3108_c0.edges`: a two-column undirected edge list with labels 0 through 6636. The skeptic contexts received the identical bytes under their own `claim/` directory; the scope sentence is quoted unchanged, and this package stores the same bytes at `object/best_n6637_s3108_c0.edges`. It is an explicit graph, not a probabilistic or asymptotic construction.

## Check It Yourself

From this package directory:

```
sh verify-it-yourself/run_checks.sh
```

Expected terminal line: `PASS`. The script checks the object SHA-256, compiles the included C++17 checker and runs all-pairs BFS.

## Compared To

The live Comellas general-graph table showed 6615 vertices for (13,4) when this record was frozen (fetched 2026-10-20T21:28:07Z, page SHA-256 `e155b7ea159c5dd6f43808767b3e31ed386dfaf7c4969bec4e7d07d50c1c17ab`). This graph has 6637, so it is 22 more vertices.

The known independent bar also included a 6631-vertex graph in an existing pull request, and the pinned repository trophy at 6630 vertices. Neither is re-claimed here.

## Not Claimed

- Not claimed optimal. The Moore bound for degree 13 and diameter 4 is 24506, so a much larger graph may exist.
- No claim that the search is exhaustive, or that any construction family is impossible.
- No claim about unpublished work, later table updates, special-class tables, or other cells.
- No probabilistic or beats-chance claim; the object is checked deterministically.

## Credits

Target and table: Francesc Comellas and the degree-diameter table contributors. Research run under the V3R1T4S rules. Skeptic verdicts are in `panel/`.
