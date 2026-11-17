# How it was built

- code/anneal_own.py: simulated annealing over families of subsets of {1..n}. For each member S it keeps
  cov[S] = OR of the members properly inside S, and calls S bad when cov[S] = S. The energy is -|F| + 2 * #bad. Moves
  toggle one set of size 2..n-2; geometric cooling from T = 1.5 to 0.05. The best bad-free family is re-validated
  from scratch before it is written.
- code/run.sh: six seeds x 100 s at n = 8 (and three x 200 s at n = 9). outputs/anneal_own_run.txt: n = 8 gives 80
  on all six seeds, never more; the object is the seed-1 family.
- code/scan_unionfree_probe.py and code/scan_probe_replay.py: a second, independently written search (incremental
  per-element cover counters, three seed modes), from the bank scan's deep check of 2026-11-09. Rerun here:
  outputs/scan_probe_replay.txt (n = 8: 80 from the middle-layer seed, 79 from the others).
- PREREG.md: the checker and bar, frozen before the searches of this run.
Python 3 standard library only.
