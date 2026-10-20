# RUN_IT_YOURSELF

From this package folder, in a fresh shell:

```
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`, about 20-30 s on one laptop core. Full expected output:

```
VALID n=6631 maxdeg=13 diameter=4 edges=43099
PASS
```

What it does: `verify-it-yourself/check_graph.py` reads `object/G_13_4_n6631.edges` (one
`u v` pair per line, 0-based, one `#` header line), rejects loops, multi-edges and labels out of
range, checks that every vertex lies in `0..6630` and no vertex is isolated, asserts maximum
degree <= 13, runs an all-pairs BFS from every one of the 6 631 vertices (so a disconnected graph
or a diameter above 4 fails), and prints the counted n, max degree, diameter and edge count.

Optional cross-check with scipy, if your Python has it: `check_graph.py` plus
`python3 -c "import scipy"` is enough; the panel's REPRODUCE file records the scipy check it ran
(`shortest_path`, diameter 4, max degree 13).

## Rebuild

The object was found by search, not by a formula: the construction code is in `how-we-built-it/`
and the exact sequence of commands is in `HOW_WE_FOUND_IT.md`. Re-running it is not deterministic
(the annealer is seeded but the run that produced the object needed several seeds), so the
package ships the finished edge list as the object of record.

## Provenance

- `object/G_13_4_n6631.edges` sha256 `391f09bb6f72f16ca5b867694b96d1d1ca31569c8974ba0f0ef00099c6cd5cbe`.
- The table snapshot, URL, fetch time and page sha256 are in `the-record-we-beat/cell.json`.
- `SHA256SUMS` hashes every other file in this package.
