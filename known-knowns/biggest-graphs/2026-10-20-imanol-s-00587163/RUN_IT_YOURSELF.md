# Run it yourself

Requires a C++17 compiler and a POSIX shell. No network access is needed.

```
sh verify-it-yourself/run_checks.sh
```

A correct run ends with `PASS`. To inspect the graph yourself, load `object/best_n6637_s3108_c0.edges` as an undirected edge list and run all-pairs BFS with maximum degree 13 and diameter 4.

To rebuild the search from the frozen 6631-vertex starting graph, see `how-we-built-it/commands.md` and `how-we-built-it/trajectory.json`. The rebuild is deterministic on the recorded NumPy and Numba versions. Whether a portable replay receipt is included is stated in those files; no replay is claimed unless its receipt is present.
