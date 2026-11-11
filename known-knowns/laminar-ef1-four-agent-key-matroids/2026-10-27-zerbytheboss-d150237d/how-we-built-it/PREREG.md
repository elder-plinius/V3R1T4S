# Preregistered Evaluation Bar (`laminar-ef1-four-agent-key-matroids`)

frozen_utc: 2026-10-28T00:35:00Z
target_id: laminar-ef1-four-agent-key-matroids
category: graphs-games-automata
null_test: not needed because deterministic checker evaluates exact rational arithmetic on explicit object

## 1. Verbatim Target Bank Criteria
> EITHER a nonnegative rational 4x8 or 4x12 valuation matrix and an agent order for which no complete feasible allocation under the corresponding key matroid is both EF1 and free of envy from each agent towards every later agent, with a complete exact obstruction certificate; OR an existence certificate for BOTH key matroids covering every nonnegative additive valuation matrix and every agent order: either a kernel-checked formal proof (Lean, Coq or Isabelle, no sorry, admit or extra axioms), or a finite partition of the normalised valuation space into rational polyhedra, each with a named allocation and exact linear-arithmetic (Farkas) certificates of coverage and of every EF1 and ordered-no-envy inequality, re-checked by an independent exact checker. A counterexample refutes the stronger key-matroid property the authors' reduction needs, not EF1 existence for laminar matroids.

## 2. Partial Wins (Verbatim)
- **p1:** An existence certificate of the same standard for exactly one of the two key matroids, covering arbitrary nonnegative additive values and any prescribed agent order.

## 3. Evaluation Metric & Thresholds
- For a counterexample on the size-8 key matroid:
  - Valuation matrix $V \in \mathbb{Q}_{\ge 0}^{4 \times 8}$ with non-trivial rows.
  - Enumeration of all 864 complete feasible labeled allocations generated directly from group constraints $G_1=\{1,2,3\}, G_2=\{4,5,6\}, G_3=\{7,8\}$ with bundle size 2 and at most 1 good per group.
  - Verification: For every one of the 864 allocations $A = (A_1, A_2, A_3, A_4)$, verify that either:
    1. $\exists i < j$ with $v_i(A_i) < v_i(A_j)$ (ordered envy violation), OR
    2. $\exists i > j$ with $v_i(A_i) < \min_{g \in A_j} v_{ig}$ (EF1 violation).
  - Residual / margin: Exact rational inequality checks in Python `fractions.Fraction` or Z3 rational model with strictly zero error tolerance.
