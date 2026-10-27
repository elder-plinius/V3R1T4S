# Reproduce Skeptic Report — `qoblib-portfolio-ten-assets-exact`

context: subagent (fresh invocation)
target_id: qoblib-portfolio-ten-assets-exact
review_utc: 2026-10-27T16:10:00Z

## Reproduction Audit
1. **Objective Recomputation**:
   The canonical schedule in `object/po_a010_t10_orig_b004_l1e-03.sol` was evaluated against QOBLIB instance `po_a010_t10_orig` (`stock_prices.txt.gz`, `covariance_matrices.txt.gz`) using exact rational arithmetic (`num_rational::BigRational` and Python `Fraction`) replicating Zimpl `zround()` round-half-away-from-zero:
   - Risk: 25,950
   - Expected Return: -37,218
   - Transaction Rebalancing: 3,831
   - Cash Interest: -990
   - Short Selling Borrow Fee: 30
   - Terminal Liquidation: 0
   - Total Objective: **-8,397**
   Cross-checked bit-for-bit with the official reference Rust checker (`check_portfolio`).

2. **Feasibility Verification**:
   - Unit bounds: Each asset count $u_{i,\tau} \in \{0, 1, 2, 3\}$.
   - Total unit budget: $\sum_{g=0}^{19} u_g \le 4$ for all $t \in [0, 9]$.
   - Cash slack register: $10 - \text{net} \in [6, 14] \subset [0, 15]$ (4 bits).
   - Budget slack register: $4 - \text{total} \in [0, 4] \subset [0, 127]$ (7 bits).
   Zero constraint violations exist.

3. **Bellman Optimality Certificate Verification**:
   All 10,606 count states evaluated across 10 periods. The two-pass Hasse distance transform recomputed downward-meet table $D_t(u)$ and upward-join table $U_t(u)$ over all 35,400 Hasse cover relations for $t \in [1, 8]$:
   - Inequality (a): $V_0(s) \le \text{stage}_0(s)$ (PASS)
   - Inequality (b): $D_t(p) \le V_{t-1}(p)$ and $D_t(u) \le D_t(u + e_g) + w_{t,g}$ (PASS)
   - Inequality (c): $U_t(m) \le D_t(m)$ and $U_t(u + e_g) \le U_t(u) + w_{t,g}$ (PASS)
   - Inequality (d): $V_t(s) \le \text{stage}_t(s) + U_t(s)$ (PASS)
   - Inequality (e): $V_9(s) \le \text{stage}_9(s) + \min V_8$ and $\min_{s \in S} V_9(s) = -8397$ (PASS)

pass: true
