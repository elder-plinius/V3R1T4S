# How we found it

Contributor text, unverified by the mechanical checker.

The search starts from the 6631-vertex (13,4) graph already known in this workspace and repeatedly applies a bounded local annealing move set that preserves the degree cap. A deterministic construction inserts a new vertex, then repairs the diameter with exact bad-pair counts. Whenever the exact count reaches zero, the graph is verified independently before another vertex is inserted. The object here is the largest such zero-cost graph found in this run. All objective values come from an exact pair-distance count, not a heuristic estimate.

The full deterministic command sequence, source and measured trajectory are in `how-we-built-it/`. No claim is made that this is the only or best construction.
