# PREREG.v2 — `reversed-zeckendorf-game-p-positions-a389618`

Recorded at (UTC): `2026-11-08T07:41:00Z` (documenting the Solver 2 structural refinement made during `attempts/evaluator-first/` while keeping all acceptance gates from `PREREG.md` (`2026-11-08T01:18:02Z`) unchanged).

## Refinement to Solver 2 (`attempts/evaluator-first/code/colex_rank_solver.cpp`)
- In `PREREG.md` Section 3 (`Cross-verification gate`), Solver 2 was initially described as an explicit per-$n$ $(h_1, \dots, h_{12})$ suffix-rank forward-reachability BFS + topological piece-count retrograde solver.
- During `attempts/evaluator-first/` (see `attempts/evaluator-first/NOTES.md` H1/H2/H6 and `attempts/evaluator-first/code/verify_invariants.py`), we proved the stronger **Colexicographic Topological Identity**: every legal Split and Combine move strictly decreases the highest modified coordinate $h_{i+1}$ by $1$ while leaving all higher coordinates unchanged. Consequently, the colexicographic rank $r \in \{0, \dots, A003107(n)-1\}$ of $(h_1, \dots, h_{12})$ is itself a strict reverse-topological ordering of $G_n$, with $r = 0$ as the unique terminal state $(n, 0, \dots, 0)$ and $r = A003107(n)-1$ as the initial Zeckendorf state $z(n)$.
- Accordingly, `colex_rank_solver.cpp` uses the partition DP offset table `off_tbl[k][s][c]` to map full partitions $(h_1, \dots, h_{12})$ of a fixed $n$ bijectively to $r \in [0, A003107(n)-1]$ without hash tables or 64-bit packed keys, performing:
  1. **Pass 1 (Bottom-Up Retrograde)**: ascending colex rank $r = 0 \dots A003107(n)-1$ in a 1-bit-per-rank `win_bits` vector.
  2. **Pass 2 (Top-Down Forward Reachability from Zeckendorf Seed)**: descending colex rank $r = A003107(n)-1 \dots 0$ in a 1-bit-per-rank `reach_bits` vector seeded solely at $r = A003107(n)-1$, verifying `reachable_verts == A003107(n)` and `reachable_edges == total_edges` for every $n \in [2, 250]$.
- All acceptance gates (Section 1 `success_criterion` Branch B, Section 2 `p1`, Section 3 calibration/cross-verification/invariant gates, and Section 4 `null_test`) remain identical to `PREREG.md`.
