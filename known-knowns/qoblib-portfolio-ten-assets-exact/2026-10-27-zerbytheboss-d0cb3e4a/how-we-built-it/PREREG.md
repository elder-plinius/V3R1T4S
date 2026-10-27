# Preregistered Evaluation Bar (`qoblib-portfolio-ten-assets-exact`)

frozen_utc: 2026-10-27T16:10:00Z
target_id: qoblib-portfolio-ten-assets-exact
category: optimization-benchmarks
null_test: not needed because deterministic checker evaluates exact integer arithmetic on explicit object

## 1. Verbatim Target Bank Criteria
> Give a globally optimal feasible position schedule for this exact instance, its integer objective v <= -8397, and an independently checkable matching lower-bound certificate. A solution equal to -8397 is a full win only with an exact global optimality certificate. Certificates may be a complete dynamic-programming/Bellman certificate or an exact rational branch-and-bound proof for the published BQP; a solver status or floating-point gap alone does not qualify.
> Partial Win p1: An explicit feasible canonical schedule with recomputed integer objective at most -8398, strictly improving the published -8397 incumbent, even without proving optimality.

## 2. Evaluation Metric & Thresholds
- Target instance: `po_a010_t10_orig_b004_l1e-03`
- Objective: Exact Zimpl integer rounding round-half-away-from-zero matching `bqp_u3_c10.zpl` and `check_portfolio`.
- Decision variables: 10 assets, $T=10$ periods, integer unit counts $u_{i, \tau} \in \{0, 1, 2, 3\}$, total units $\sum_{i, \tau} u_{i, \tau} \le 4$.
- Success bar:
  - Global Optimality Certificate for $v = -8397$ (proving no feasible schedule has $v < -8397$ via Bellman values $V_t(s)$) -> CONFIRMED_SOLUTION
  - Feasible schedule with $v \le -8398$ -> Partial Win p1 / CONFIRMED_SOLUTION.
