# Report: Lens 1 — Exact SMT / MILP Counterexample

claim level: solution_claim

## Summary
Using exact SMT constraint synthesis over Z3 and verified with exact rational arithmetic (`fractions.Fraction`), we solved the open Cookson–Shah size-8 key matroid question (arXiv:2608.31121) by discovering a genuine non-negative rational $4 \times 8$ valuation matrix and prescribed agent order $1 \prec 2 \prec 3 \prec 4$ for which **no complete feasible allocation** under the size-8 key matroid is both EF1 and free of envy from each agent toward every later agent.

Every single one of the 864 feasible labeled allocations was generated directly from the group constraints ($G_1=\{1,2,3\}, G_2=\{4,5,6\}, G_3=\{7,8\}$, bundle size 2, group capacity 1) and evaluated against the valuation matrix:
- **828 allocations strictly violate ordered no-envy** ($\exists i < j$ with $v_i(A_i) < v_i(A_j)$).
- **36 allocations strictly violate EF1** ($\exists i > j$ with $v_i(A_i) < \min_{g \in A_j} v_{ig}$).
- **0 allocations are valid**.
- The minimum violation margin across all 864 allocations is strictly $1/100 > 0$.

## Valuation Matrix
Prescribed Agent Ordering: $1 \prec 2 \prec 3 \prec 4$
Cleared Denominator Scale: $100$

| Agent | $g_1$ | $g_2$ | $g_3$ | $g_4$ | $g_5$ | $g_6$ | $g_7$ | $g_8$ | Row Sum |
|---|---|---|---|---|---|---|---|---|---|
| Agent 1 | $1/100$ | $15/100$ | $25/100$ | $7/100$ | $0$ | $12/100$ | $19/100$ | $21/100$ | $1$ |
| Agent 2 | $7/100$ | $23/100$ | $20/100$ | $17/100$ | $0$ | $8/100$ | $13/100$ | $12/100$ | $1$ |
| Agent 3 | $0$ | $12/100$ | $62/100$ | $0$ | $7/100$ | $14/100$ | $1/100$ | $4/100$ | $1$ |
| Agent 4 | $0$ | $78/100$ | $6/100$ | $10/100$ | $3/100$ | $0$ | $1/100$ | $2/100$ | $1$ |

## Artifacts Generated
- `result/valuation_matrix.json`: Machine-readable exact integer and rational representation.
- `result/obstruction_certificate.json`: Comprehensive certification mapping each of the 864 allocations to its exact primary violated inequality, agent pair, and strictly positive margin.
- `REPRODUCE.md`: Deterministic one-line command reproducing the generation and verification.
