# PREREG — `reversed-zeckendorf-game-p-positions-a389618`

Frozen at (UTC): `2026-11-08T01:18:02Z`

## 1. Success criterion (copied verbatim from `repo/bank/targets.json`)
CONFIRMED: either (A) a kernel-checked formal proof (Lean, Rocq or Isabelle; no sorry, admitted goals or axioms beyond the system's standard ones) of Batterman et al. Conjecture 1.2 establishing that for infinitely many starting integers n >= 2, the initial Zeckendorf decomposition of n is a P-position (second-player win) under the Split and Combine rules; OR (B) the exact 1st/2nd-player outcomes of the Reversed Zeckendorf game for every integer n contiguously in 130..250 (yielding one table of outcomes, vertex counts, and edge counts for n = 130..250 that extends OEIS A389618, A389619, and A389617 through n = 250), computed by two independently written solvers using distinct representations that both reproduce every vertex count, edge count, and win/loss outcome in Table A1 of arXiv:2309.12748v2 for all 2 <= n <= 129 and agree on every n in 130..250.

## 2. Partial wins (copied verbatim from `repo/bank/targets.json`)
- `p1`: Determine the exact 1st/2nd-player outcomes (extending OEIS A389618 and A389619) and exact DAG vertex and edge counts (extending OEIS A389617 and Table A1 of arXiv:2309.12748v2) for every integer n contiguously in 130..180, verified by two independent solvers that reproduce Table A1 of arXiv:2309.12748v2 for all 2 <= n <= 129.

## 3. Exact deterministic checker & acceptance threshold
- **Target branch**: Branch (B) (`CONFIRMED_SOLUTION`), computing the exact 1st/2nd-player outcome, DAG vertex count, and DAG edge count for every integer $n$ contiguously in $2 \le n \le 250$ (covering the full calibration baseline $2 \le n \le 129$ and the full open target range $130 \le n \le 250$).
- **Calibration gate**: Both independent solvers must reproduce **all 128 rows** ($2 \le n \le 129$) of Table A1 of `arXiv:2309.12748v2` (`data/table_a1_ground_truth.tsv`, SHA-256 `cea0c77942d3e7c3cc127fb8370da12d4075cc8a6b3dedc71a5ad297ee8361f6`) with **0 discrepancies** in winner, edge count (`A389617`), and vertex count (`A003107`), as well as all 49 published terms of `A389618` and all 79 terms $\ge 2$ of `A389619`.
- **Cross-verification gate**: Solver 1 (`attempts/retrograde-dag/`: universal $h_1$-eliminated induced-subgraph solver stratified by deficit $\Delta(h) = \sum_{i\ge 2}(F_i - 1)h_i$ with 256-bit word-parallel evaluation across all $n \in [2, 250]$) and Solver 2 (`attempts/evaluator-first/`: explicit per-$n$ $(h_1, \dots, h_{12})$ suffix-rank forward-reachability BFS + topological piece-count retrograde solver) must agree **row-for-row on every single integer $n \in [2, 250]$** on `(winner, edges, vertices)`.
- **Analytical invariant gate**: Every row $n \in [2, 250]$ must also satisfy $|V_n| = A003107(n)$, $|E_n| = \sum_{i\ge 2}(A003107(n - F_i) + A003107(n - 2 F_i))$, and Winner $= 1$ whenever $n = F_{i+1} + F_{i-2}$ (Theorem 1.1 of Batterman et al.).

## 4. Null design
null_test: not needed because the claim is an exact deterministic combinatorial game evaluation (exact 1st/2nd-player normal-play outcomes, DAG vertex counts, and DAG edge counts for $n = 2..250$) verified by two independent exact algorithms and a literal-definition checker against Table A1 of arXiv:2309.12748v2 and OEIS A389617/A389618/A389619.
