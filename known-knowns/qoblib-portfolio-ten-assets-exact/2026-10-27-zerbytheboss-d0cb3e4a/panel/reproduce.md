# Reproduce Report — `qoblib-portfolio-ten-assets-exact`

- Context: Independent reproduction verification of `object/po_a010_t10_orig_b004_l1e-03_bellman_certificate.json` against the published QOBLIB instance and solution files
- Target ID: `qoblib-portfolio-ten-assets-exact`

## Reproduction Audit
1. **Objective Recomputation**:
   QOBLIB's published canonical schedule `06-portfolio/solutions/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3.bst.sol` (`https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3.bst.sol`, SHA-256 `d0cb3e4a86d01ac2b2884e3275df8219bb1d38dae908830784417b0d4e4b30ea`) and the matching `attaining_trajectory` in `object/po_a010_t10_orig_b004_l1e-03_bellman_certificate.json` were evaluated against QOBLIB instance `po_a010_t10_orig` (`stock_prices.txt.gz` compressed SHA-256 `80a583a0ccd63b9432b94ae3b8012df9661ab8bb5e6faf26df121f43adc588f3`, uncompressed SHA-256 `d553472d20c40270416ff3011008f8a776957cd7c5f8dd51f2a8c55823c0d391`; `covariance_matrices.txt.gz` compressed SHA-256 `41dab1816d7a8f9f50dc07fe60816d435f9dc085eaaee034d8ecc3721ee5c202`, uncompressed SHA-256 `7b58ef8e869c35b60799e6dce1da39ca6e3eaea55dc6b124d5cbda16100bdd73`) using exact rational arithmetic (`num_rational::BigRational` and Python `Fraction`) replicating Zimpl `round()` round-half-away-from-zero:
   - Risk: `25,950`
   - Expected Return: `-37,218`
   - Transaction Rebalancing: `3,831`
   - Cash Interest: `-990`
   - Short Selling Borrow Fee: `30`
   - Terminal Liquidation: `0`
   - Total Objective: **`-8,397`**
   In our contributor run, we also compiled and ran QOBLIB's official Rust checker (`06-portfolio/check`, `./target/release/check_portfolio instances/po_a010_t10_orig solutions/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3.bst.sol`), which printed the identical breakdown and `Objective value = -8397`, `Solution successfully verified`.

2. **Feasibility Verification**:
   - Unit bounds: Each asset count $u_{i,\tau} \in \{0, 1, 2, 3\}$.
   - Total unit budget: $\sum_{g=0}^{19} u_g \le 4$ for all $t \in [0, 9]$.
   - Cash slack register: $10 - \text{net} \in [6, 14] \subset [0, 15]$ (4 bits).
   - Budget slack register: $4 - \text{total} \in [0, 4] \subset [0, 127]$ (7 bits).
   Zero constraint violations exist.

3. **Bellman Optimality Certificate Verification**:
   All 10,606 count states were evaluated across all 10 periods. The two-pass Hasse distance transform recomputed downward-meet table $D_t(u)$ and upward-join table $U_t(u)$ over all 35,400 Hasse cover relations for $t \in [1, 8]$:
   - Inequality (a): $V_0(s) \le \text{stage}_0(s)$ (PASS)
   - Inequality (b): $D_t(p) \le V_{t-1}(p)$ and $D_t(u) \le D_t(u + e_g) + w_{t,g}$ (PASS)
   - Inequality (c): $U_t(m) \le D_t(m)$ and $U_t(u + e_g) \le U_t(u) + w_{t,g}$ (PASS)
   - Inequality (d): $V_t(s) \le \text{stage}_t(s) + U_t(s)$ (PASS)
   - Inequality (e): $V_9(s) \le \text{stage}_9(s) + \min V_8$ and $\min_{s \in S} V_9(s) = -8397$ (PASS; in `bqp_u3_c10.zpl` there is no transaction-cost term between periods 8 and 9).

pass: true
