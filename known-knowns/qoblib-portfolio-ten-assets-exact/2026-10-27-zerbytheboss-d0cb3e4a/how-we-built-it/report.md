# Lens 3 Report: Certified Hasse-Diagram Bellman Distance Transform & Optimality Export

target_id: qoblib-portfolio-ten-assets-exact
run_id: 2026-10-27-1610
attempt: attempts/lens3_certified_hasse_bellman_export/
claim level: solution_claim

## Executive Summary
Lens 3 designed, implemented, and executed a certified two-pass Hasse-diagram weighted-$L_1$ distance transform dynamic program over all 10,606 count states and exported the complete Bellman optimality certificate for QOBLIB portfolio instance `po_a010_t10_orig_b004_l1e-03`.

1. **Exact Mathematical Certificate Verification**:
   - Enumerated all 10,606 count states $S = \{u \in \{0,1,2,3\}^{20} : \sum_g u_g \le 4\}$.
   - Precomputed exact stage costs $\text{stage}_t(s)$ using Zimpl round-half-away-from-zero `zround(x)` in exact rational arithmetic.
   - Recomputed downward-meet table $D_t(u)$ and upward-join table $U_t(u)$ across all 35,400 Hasse cover relations per period ($t \in 1..8$).
   - Verified all 5 Hasse-diagram Bellman optimality inequalities:
     (a) $V_0(s) \le \text{stage}_0(s)$ across all 10,606 states (PASS).
     (b) $D_t(p) \le V_{t-1}(p)$ and $D_t(u) \le D_t(u + e_g) + w_{t,g}$ across all states and cover relations (PASS).
     (c) $U_t(m) \le D_t(m)$ and $U_t(u + e_g) \le U_t(u) + w_{t,g}$ across all states and cover relations (PASS).
     (d) $V_t(s) \le \text{stage}_t(s) + U_t(s)$ for all $t \in 1..8, s \in 0..10605$ (PASS).
     (e) $V_9(s) \le \text{stage}_9(s) + \min_{p \in S} V_8(p)$ and $\min_{s \in S} V_9(s) = -8397$ (PASS).

2. **Global Optimality Proof**:
   - The verified certificate unconditionally establishes that:
     $$\min_{\text{feasible schedules}} \text{Objective} \ge \min_{s \in S} V_9(s) = -8397.$$
   - The canonical schedule achieves exactly $-8397$ with exact breakdown:
     $\text{risk} = 25950$, $\text{return} = -37218$, $\text{transaction} = 3831$, $\text{cash\_interest} = -990$, $\text{short\_cost} = 30$, $\text{liquidation} = 0$, $\text{total} = -8397$.
   - Thus $-8397$ is proved to be the exact global minimum.

3. **Exported Certificate Objects**:
   - `object/po_a010_t10_orig_b004_l1e-03_bellman_certificate.json` (594,500 bytes, < 1MB)
   - `object/po_a010_t10_orig_b004_l1e-03_downward_meet_tables.json` (471,942 bytes, < 1MB)
   - `object/po_a010_t10_orig_b004_l1e-03_upward_join_tables.json` (489,825 bytes, < 1MB)
   - `object/po_a010_t10_orig_b004_l1e-03.sol` (388 bytes)
