# QOBLIB Ten-Asset Portfolio Global Optimality Certificate (`po_a010_t10_orig_b004_l1e-03`)

## What
Globally optimal integer position schedule for QOBLIB instance po_a010_t10_orig_b004_l1e-03 with objective -8397, certified by a complete 10,606-state two-pass Hasse-diagram Bellman distance transform matching the published -8397 schedule.

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output line: `PASS` (verifies in < 0.6 seconds using pure Python standard library, downloading and verifying the SHA-256 checksums of the published QOBLIB instance and solution files, recomputing all $10 \times 10,606$ stage costs from scratch in exact rational arithmetic with Zimpl `round()` half-away-from-zero, verifying schedule feasibility and exact breakdown, and certifying all 5 Hasse-diagram Bellman equations and inequalities).

### Published QOBLIB Source Files & SHA-256 Checksums
- **Published `-8397` Canonical Schedule (`po_a010_t10_orig_b004_l1e-3.bst.sol`)**:
  - URL: `https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3.bst.sol`
  - SHA-256 (`388` bytes): `d0cb3e4a86d01ac2b2884e3275df8219bb1d38dae908830784417b0d4e4b30ea`
- **Instance Stock Prices (`06-portfolio/instances/po_a010_t10_orig/stock_prices.txt.gz`)**:
  - URL: `https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/instances/po_a010_t10_orig/stock_prices.txt.gz`
  - Compressed (`.gz`) SHA-256: `80a583a0ccd63b9432b94ae3b8012df9661ab8bb5e6faf26df121f43adc588f3`
  - Uncompressed (`stock_prices.txt`) SHA-256: `d553472d20c40270416ff3011008f8a776957cd7c5f8dd51f2a8c55823c0d391`
- **Instance Covariance Matrices (`06-portfolio/instances/po_a010_t10_orig/covariance_matrices.txt.gz`)**:
  - URL: `https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/instances/po_a010_t10_orig/covariance_matrices.txt.gz`
  - Compressed (`.gz`) SHA-256: `41dab1816d7a8f9f50dc07fe60816d435f9dc085eaaee034d8ecc3721ee5c202`
  - Uncompressed (`covariance_matrices.txt`) SHA-256: `7b58ef8e869c35b60799e6dce1da39ca6e3eaea55dc6b124d5cbda16100bdd73`
- **Reference Zimpl Model (`06-portfolio/models/binary_quadratic_programming/bqp_u3_c10.zpl`)**:
  - URL: `https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/models/binary_quadratic_programming/bqp_u3_c10.zpl`
  - SHA-256: `8962c6a83db1eed11557c8d68dae229d39e14eb31e59b8a16579fc577697513d`

### Note on Period 8-to-9 Transition in `bqp_u3_c10.zpl` (Bellman Inequality (e))
In the reference Zimpl model [`bqp_u3_c10.zpl`](https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/models/binary_quadratic_programming/bqp_u3_c10.zpl), the inter-period rebalancing transaction-cost sum
```zimpl
+ sum <t> in TX \ { t_beg, t_end } : (
   - sum <i,m,tau> in SX : (
      round(tau * (p[i,t+1] - p[i,t])) * x[i,m,tau,t]  # return
      - round(delta * p[i,t]) * (x[i,m,tau,t-1] + x[i,m,tau,t]
                          - 2 * x[i,m,tau,t-1] * x[i,m,tau,t])  # transaction cost
   )
)
```
ranges strictly over `t in TX \ { t_beg, t_end } = {1, ..., 8}`, whereas the terminal period `t_end = 9` contributes only the terminal liquidation sum `+ sum <i,m,tau> in SX : round(delta * p[i,t_end]) * x[i,m,tau,t_end]`. Consequently, the published BQP model has **no transaction-cost term coupling period `8` (`t_end - 1`) and period `9` (`t_end`)**, so the period-9 Bellman relation reduces to $V_9(s) \le \text{stage}_9(s) + \min_{p \in S} V_8(p)$ (inequality (e)).

### Official QOBLIB Rust Checker (`check_portfolio`) Execution Report (Contributor Run)
We also compiled and ran QOBLIB's official Rust solution checker (`06-portfolio/check`, `cargo build --release`) against `po_a010_t10_orig` and `po_a010_t10_orig_b004_l1e-3.bst.sol`:
```text
$ ./target/release/check_portfolio instances/po_a010_t10_orig solutions/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3.bst.sol
Instance: po_a010_t10_orig (10 assets, 10 periods)
Model:    B=4, lambda=0.001, ub=3, C=10, slack bits 4+7
t= 0: net=   0 total=   2 cash_slack=  10 count_slack=   2  ok
t= 1: net=  -1 total=   3 cash_slack=  11 count_slack=   1  ok
t= 2: net=   0 total=   2 cash_slack=  10 count_slack=   2  ok
t= 3: net=  -2 total=   4 cash_slack=  12 count_slack=   0  ok
t= 4: net=   1 total=   1 cash_slack=   9 count_slack=   3  ok
t= 5: net=   0 total=   4 cash_slack=  10 count_slack=   0  ok
t= 6: net=   0 total=   0 cash_slack=  10 count_slack=   4  ok
t= 7: net=   1 total=   3 cash_slack=   9 count_slack=   1  ok
t= 8: net=   2 total=   4 cash_slack=   8 count_slack=   0  ok
t= 9: net=   0 total=   0 cash_slack=  10 count_slack=   4  ok
Objective breakdown:
  risk                       25950
  return                    -37218
  transaction                 3831
  cash interest               -990
  short cost                    30
  liquidation                    0
Objective value = -8397
Claimed objective matches.
Solution successfully verified
```

## Compared To
- Status Source: `https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/README.md` (Fetched UTC `2026-10-27T16:10:00Z`, SHA-256 `05a6d23392d960fb16028cc1e9ba8d7547aa445a0e3f30c433f5f4acab56c09a`).
- Instance: `po_a010_t10_orig_b004_l1e-03`
- Published Incumbent: `-8397` (`06-portfolio/solutions/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3.bst.sol`, Maximilian Schicker, 2025-08-19)
- Literature Lower Bound: `-15342.65126758` (Gurobi's numerical MIP bound after `3600.03 s` in `06-portfolio/submissions/20250819_MIP_Schicker/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3/README.md`)
- This Work: Establishes that `-8397` is the exact integer global optimum by providing an explicit 10,606-state Bellman optimality certificate (`min_{s in S} V_9(s) = -8397`), closing the `6945.65`-unit gap between the `-8397` incumbent and Gurobi's `-15342.65126758` numerical MIP bound.

| Component | Literature Incumbent | This Certificate (`object/`) | Status |
|---|---|---|---|
| Objective Value | -8,397 | -8,397 | Optimal |
| Lower Bound | -15,342.65126758 (Gurobi MIP bound after 3600.03 s) | -8,397 (exact Bellman certificate) | Closed |
| Risk | 25,950 | 25,950 | Verified |
| Expected Return | -37,218 | -37,218 | Verified |
| Transaction Cost | 3,831 | 3,831 | Verified |
| Cash Interest | -990 | -990 | Verified |
| Short Cost | 30 | 30 | Verified |
| Liquidation | 0 | 0 | Verified |

## Not Claimed
- We do not claim other instances or parameterizations in QOBLIB class 06; this package specifically certifies global optimality for `po_a010_t10_orig_b004_l1e-03`.
- We do not claim a schedule with objective `< -8397`; the Bellman certificate establishes that no feasible schedule with objective `<= -8398` exists and that QOBLIB's published `po_a010_t10_orig_b004_l1e-3.bst.sol` (`-8397`) is globally optimal.

## Credits
- Contributor: `@HindsightWise` (`Zerbytheboss`).
- Thorsten Koch and colleagues at Zuse Institute Berlin (ZIB) for creating and curating the Quantum Optimization Benchmarking Library (QOBLIB).
- Maximilian Schicker for the 2025-08-19 incumbent solution (`06-portfolio/solutions/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3.bst.sol`) and reference portfolio checker (`06-portfolio/check`).
