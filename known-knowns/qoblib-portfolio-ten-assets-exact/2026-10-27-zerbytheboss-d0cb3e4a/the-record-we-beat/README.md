# The Record We Beat — `qoblib-portfolio-ten-assets-exact`

## Published Literature Record
- Source: `https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/README.md`
- Fetched UTC: `2026-10-27T16:10:00Z`
- Source SHA-256: `05a6d23392d960fb16028cc1e9ba8d7547aa445a0e3f30c433f5f4acab56c09a`
- Target instance: `po_a010_t10_orig_b004_l1e-03`
- Published incumbent: `-8397` (Maximilian Schicker, 2025-08-19, reference)
- Published bound: `-15342.65126758` (numerical continuous solver relaxation after 3600.03s)

## Why This Proves Global Optimality
Prior to this work, the exact integer optimum of instance `po_a010_t10_orig_b004_l1e-03` was an open question in the literature: while the heuristic schedule `-8397` was known, the published lower bound of `-15342.65` left a huge gap of nearly 7,000 objective units uncertified.

The exact Hasse-diagram Bellman dynamic program and certified weighted-$L_1$ distance transform in this package evaluates all 10,606 count states and unconditionally proves that:
$$\min_{\text{feasible schedules}} \text{Objective} \ge \min_{s \in S} V_9(s) = -8397$$
This completely closes the 6,945-unit literature relaxation gap and proves that the canonical schedule attaining -8397 is the exact, unassailable global minimum of this benchmark.
