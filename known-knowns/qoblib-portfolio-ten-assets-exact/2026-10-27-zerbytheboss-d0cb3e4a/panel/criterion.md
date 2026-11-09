# Criterion Report — `qoblib-portfolio-ten-assets-exact`

- Context: Target criterion verification for `qoblib-portfolio-ten-assets-exact`
- Target ID: `qoblib-portfolio-ten-assets-exact`

## Verbatim Success Criterion Audit

1. **Bank Success Criterion**:
   > *"Give a globally optimal feasible position schedule for this exact instance, its integer objective v <= -8397, and an independently checkable matching lower-bound certificate. A solution equal to -8397 is a full win only with an exact global optimality certificate. Certificates may be a complete dynamic-programming/Bellman certificate or an exact rational branch-and-bound proof for the published BQP; a solver status or floating-point gap alone does not qualify."*

2. **Compliance Verification**:
   - Attaining feasible canonical position schedule: QOBLIB's published `06-portfolio/solutions/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3.bst.sol` (`https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3.bst.sol`, SHA-256 `d0cb3e4a86d01ac2b2884e3275df8219bb1d38dae908830784417b0d4e4b30ea`), recorded as `attaining_trajectory` in `object/po_a010_t10_orig_b004_l1e-03_bellman_certificate.json`.
   - Integer objective: Recomputed objective is $v = -8397 \le -8397$ in exact rational decimal arithmetic matching Zimpl `round()` at every model site in `bqp_u3_c10.zpl`.
   - Complete dynamic-programming/Bellman certificate provided: `object/po_a010_t10_orig_b004_l1e-03_bellman_certificate.json` (with exact Bellman value function $V_t(s)$ for all 10 periods and 10,606 count states) and Hasse-diagram distance transform tables $D_t(u)$ (`object/po_a010_t10_orig_b004_l1e-03_downward_meet_tables.json`) and $U_t(u)$ (`object/po_a010_t10_orig_b004_l1e-03_upward_join_tables.json`).
   - Independently checkable matching lower-bound certificate: The 5 Hasse-diagram inequalities certify that for all feasible schedules, the objective is at least $\min_{s \in S} V_9(s) = -8397$, matching the attaining `-8397` canonical schedule.

pass: true
