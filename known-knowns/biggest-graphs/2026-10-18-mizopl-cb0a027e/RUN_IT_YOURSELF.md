# Run it yourself

## 1. Check the shipped object

From a fresh shell in this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. A real run is recorded in `verify-it-yourself/RECEIPTS.md`. To run the checker alone:

```sh
python3 verify-it-yourself/check_dd.py object/G_14_3_N1118.edges --delta 14 --diameter 3 --expect-n 1118 --record 1117
```

It reads the 0-indexed edge list (`7,809` lines), checks that there are no loops, no repeated edges, and no unused vertex numbers (`0..1117`), and verifies that the maximum degree is at most 14 (`34` vertices of degree 13 and `1,084` of degree 14). It then runs a breadth-first search from every one of the 1,118 vertices and reports the exact diameter (`3`), along with the Moore bound (`2,563`). The run script also checks the sha256 against `INDEX.csv` and verifies that a corrupted copy with vertex 0's edges removed is rejected.

## 2. How the object was built

`how-we-built-it/` holds the compiled bit-parallel BFS + simulated annealing optimizer (`sa2_opt.c`) and its pre-registration (`PREREG.md`). Starting from the 1,117-vertex graph `G_14_3_N1117.edges` (V3R1T4S PR #143), which has 68 vertices of degree 13 (and 84 unused degree slots after pruning 8 redundant seed edges):

```sh
cc -O3 -o sa2_opt how-we-built-it/sa2_opt.c -lm
./sa2_opt G_14_3_N1117.edges 14 3 1 G_14_3 50000 10 1
```

Restart 8 (seed 1) reduced bad vertex pairs (`dist > 3`) from 49 down to 13, and multi-temperature polish rounds (`T = 0.35 / 0.18 / 0.08 -> 0.015`, with new-vertex screen inclusion) reached 0 bad pairs on polish round 9, writing `G_14_3_N1118.edges`.
