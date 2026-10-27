# Criterion Skeptic Report — `qoblib-portfolio-ten-assets-exact`

context: subagent (fresh invocation)
target_id: qoblib-portfolio-ten-assets-exact
review_utc: 2026-10-27T16:10:00Z

## Verbatim Success Criterion Audit

1. **Bank Success Criterion**:
   > *"Give a globally optimal feasible position schedule for this exact instance, its integer objective v <= -8397, and an independently checkable matching lower-bound certificate. A solution equal to -8397 is a full win only with an exact global optimality certificate. Certificates may be a complete dynamic-programming/Bellman certificate or an exact rational branch-and-bound proof for the published BQP; a solver status or floating-point gap alone does not qualify."*

2. **Compliance Verification**:
   - Explicit feasible canonical position schedule provided: `object/po_a010_t10_orig_b004_l1e-03.sol`.
   - Integer objective: Recomputed objective is $v = -8397 \le -8397$ in exact rational decimal arithmetic matching Zimpl `zround()` at every model site.
   - Complete dynamic-programming/Bellman certificate provided: `object/po_a010_t10_orig_b004_l1e-03_bellman_certificate.json` (with exact Bellman value function $V_t(s)$ for all 10 periods and 10,606 count states) and verified Hasse-diagram distance transform tables $D_t(u)$ and $U_t(u)$.
   - Independently checkable matching lower-bound certificate: The 5 Hasse-diagram inequalities unconditionally certify that for all feasible schedules, the objective is at least $\min_{s \in S} V_9(s) = -8397$, matching the attaining canonical schedule.
   - The criterion for a full win (`CONFIRMED_SOLUTION`) is satisfied in full with zero compromises.

pass: true
