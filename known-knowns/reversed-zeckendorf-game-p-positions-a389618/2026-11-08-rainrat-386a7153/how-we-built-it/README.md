# How We Built It (`how-we-built-it/`)

This folder contains the two independent C++17 solvers and the preregistration records (`PREREG.md` and `PREREG.v2.md`) used to produce `object/reversed_zeckendorf_n2_250.tsv`.

## Files
- `universal_delta_solver.cpp` — **Solver 1 (Lens 1: Deficit-Stratified Universal DAG + 256-Bit Word-Parallel Retrograde Evaluation, `PROVED-HERE`)**. Eliminates $h_1 = n - \sum_{i=2}^{12} h_i F_i$, embeds every game DAG $G_n$ ($2 \le n \le 250$) as the induced subgraph $V_n = \{h : m(h) \le n\}$ of a single universal state space of $21,890,964$ tuples $(h_2, \dots, h_{12})$ packed into 45-bit keys, stratifies states by the deficit invariant $\Delta(h) = \sum_{i=2}^{12}(F_i - 1)h_i$, and evaluates all $n \in [2, 250]$ simultaneously in 256-bit word-parallel bitvectors.
- `colex_rank_solver.cpp` — **Solver 2 (Lens 2: Colexicographic Rank Bijection + Top-Down Reachability Verification, `PROVED-HERE`)**. Evaluates each integer $n \in [2, 250]$ independently without hash tables or 64-bit packed keys by mapping each full partition $(h_1, \dots, h_{12})$ of $n$ bijectively to its colexicographic rank $r \in [0, A003107(n)-1]$ via a partition DP offset table. Exploits the fact that every legal Split and Combine move strictly decreases the highest modified coordinate $h_{i+1}$ by $1$ (making colex rank $r$ a strict reverse-topological order), and verifies via a top-down reachability pass from the Zeckendorf starting state $r = A003107(n) - 1$ that all $A003107(n)$ partitions and all directed transitions are reachable.
- `PREREG.md` — Initial preregistration frozen prior to running the search (`2026-11-08T01:18:02Z`).
- `PREREG.v2.md` — Recorded refinement (`2026-11-08T07:41:00Z`) documenting the replacement of suffix-rank forward BFS in Solver 2 with the colexicographic rank bijection and top-down reachability pass while preserving all acceptance gates unchanged.

## Prerequisites & Compilation
Requires a C++17 compiler with OpenMP support (`g++`) and Python $\ge 3.9$:
```sh
g++ -O3 -std=c++17 how-we-built-it/universal_delta_solver.cpp -o universal_delta_solver
./universal_delta_solver out_solver1.tsv

g++ -O3 -fopenmp -std=c++17 how-we-built-it/colex_rank_solver.cpp -o colex_rank_solver
./colex_rank_solver out_solver2.tsv

diff -u out_solver1.tsv out_solver2.tsv
diff -u out_solver1.tsv object/reversed_zeckendorf_n2_250.tsv
```
