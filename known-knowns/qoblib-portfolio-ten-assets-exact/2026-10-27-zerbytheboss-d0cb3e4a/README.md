# QOBLIB Ten-Asset Portfolio Global Optimality Certificate (`po_a010_t10_orig_b004_l1e-03`)

## What
Globally optimal integer position schedule for QOBLIB instance po_a010_t10_orig_b004_l1e-03 with objective -8397, certified unconditionally by a complete 10,606-state two-pass Hasse-diagram Bellman distance transform matching the -8397 attaining canonical schedule.

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output line: `PASS` (verifies in < 0.6 seconds using pure Python standard library, recomputing all $10 \times 10,606$ stage costs from scratch in exact rational arithmetic, verifying schedule feasibility and exact breakdown, and certifying all 5 Hasse-diagram Bellman inequalities).

## Compared To
- Status Source: `https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/README.md` (Fetched UTC `2026-10-27T16:10:00Z`, SHA-256 `05a6d23392d960fb16028cc1e9ba8d7547aa445a0e3f30c433f5f4acab56c09a`).
- Instance: `po_a010_t10_orig_b004_l1e-03`
- Published Incumbent: `-8397` (Maximilian Schicker, 2025-08-19)
- Literature Lower Bound: `-15342.65126758` (numerical solver continuous relaxation)
- This Work: Unconditionally proves that $-8397$ is the exact integer global optimum, completely closing the 6,945-unit open literature gap with an explicit 10,606-state Bellman optimality certificate.

| Component | Literature Incumbent | This Solution & Certificate | Status |
|---|---|---|---|
| Objective Value | -8,397 | -8,397 | Optimal |
| Lower Bound | -15,342.65 (unproved gap) | -8,397 (certified exact) | Closed |
| Risk | 25,950 | 25,950 | Verified |
| Expected Return | -37,218 | -37,218 | Verified |
| Transaction Cost | 3,831 | 3,831 | Verified |
| Cash Interest | -990 | -990 | Verified |
| Short Cost | 30 | 30 | Verified |
| Liquidation | 0 | 0 | Verified |

## Not Claimed
- We do not claim other instances or parameterizations in QOBLIB class 06; this package specifically proves global optimality for `po_a010_t10_orig_b004_l1e-03`.
- We do not claim a strictly superior objective $< -8397$, as our certificate proves that no schedule with objective $\le -8398$ mathematically exists.

## Credits
- Contributor: `zerbytheboss` (GitHub account `HindsightWise` operated by `zerbytheboss`).
- Thorsten Koch and colleagues at Zuse Institute Berlin (ZIB) for creating and curating the Quantum Optimization Benchmarking Library (QOBLIB).
- Maximilian Schicker for the 2025-08-19 incumbent solution discovery.
