# Receipts

Command run from the package root:

```
sh verify-it-yourself/run_checks.sh
```

The checker compiles the included C++17 source, verifies the object SHA-256, then parses the edge list and runs BFS from every vertex.

Expected terminal line: `PASS`.

## Independent scipy check made while building this record

```
{"n": 6637, "edges": 43140, "max_degree": 13, "connected": true, "diameter": 4, "bad_pairs": 0, "valid": true, "sha256": "00587163283c37fbb2d5d83ebd2c533e010af603f5e27d59a01c55a527185059", "seconds": 4.223385625053197}
```

The three skeptics wrote their own checkers and their complete verdicts are in `../panel/`. Their reported runs are transcribed there, not reworded here.

## Table state when this record was frozen

Live general-graph table: https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html

Fetched: 2026-10-20T21:28:07Z

Page SHA-256: `e155b7ea159c5dd6f43808767b3e31ed386dfaf7c4969bec4e7d07d50c1c17ab`

Cell (13,4), general graphs, non-bold: 6615 vertices.

This package does not reproduce the table; it records the URL, UTC fetch time, hash and observed cell so a reader can check the live page.
