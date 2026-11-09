# The Record We Beat — `qoblib-portfolio-ten-assets-exact`

## Published Literature Record
- Source: `https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/README.md`
- Fetched UTC: `2026-10-27T16:10:00Z`
- Source SHA-256: `05a6d23392d960fb16028cc1e9ba8d7547aa445a0e3f30c433f5f4acab56c09a`
- Target instance: `po_a010_t10_orig_b004_l1e-03`
- Published incumbent: `-8397` (`06-portfolio/solutions/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3.bst.sol`, SHA-256 `d0cb3e4a86d01ac2b2884e3275df8219bb1d38dae908830784417b0d4e4b30ea`, Maximilian Schicker, 2025-08-19)
- Published bound: `-15342.65126758` (Gurobi's numerical MIP bound after `3600.03 s` in `06-portfolio/submissions/20250819_MIP_Schicker/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3/README.md`)

## How This Certificate Closes the Optimality Gap
Prior to this work, the exact integer optimum of instance `po_a010_t10_orig_b004_l1e-03` was listed as `best known` (`-8397`) rather than `optimal` in the QOBLIB table, because Gurobi's numerical MIP bound after `3600.03 s` was `-15342.65126758`.

The exact Hasse-diagram Bellman dynamic program and weighted-$L_1$ distance transform in `object/` evaluates all 10,606 count states across all 10 periods and establishes that:
$$\min_{\text{feasible schedules}} \text{Objective} \ge \min_{s \in S} V_9(s) = -8397$$
closing the gap between `-8397` and `-15342.65126758` and certifying that the published schedule `06-portfolio/solutions/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3.bst.sol` (`-8397`) is the exact global minimum of this benchmark.
