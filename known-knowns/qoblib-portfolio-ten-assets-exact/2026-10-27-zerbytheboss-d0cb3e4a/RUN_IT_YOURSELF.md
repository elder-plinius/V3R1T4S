# Run It Yourself

## 1. Fast Python Verification (< 0.6 Seconds)
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
This executes `verify-it-yourself/check_portfolio_opt.py`, which:
1. Downloads the raw QOBLIB instance files (`stock_prices.txt.gz`, `covariance_matrices.txt.gz`) and published canonical schedule (`po_a010_t10_orig_b004_l1e-3.bst.sol`) into a local temporary cache and verifies their compressed and uncompressed SHA-256 checksums.
2. Evaluates the published canonical schedule `po_a010_t10_orig_b004_l1e-3.bst.sol` using exact Zimpl round-half-away-from-zero rational arithmetic, verifying all constraint categories, matching it against `attaining_trajectory` in `object/po_a010_t10_orig_b004_l1e-03_bellman_certificate.json`, and confirming the objective breakdown totaling `-8397`.
3. Recomputes all $10 \times 10,606$ discrete count stage costs from scratch.
4. Verifies all 5 Hasse-diagram Bellman optimality equations and inequalities across all 10,606 states, confirming $\min_{s \in S} V_9(s) = -8397$.
Expected final line: `PASS`.

## 2. Rebuild the Certificate from Source
To re-run the Hasse distance transform solver and export fresh certificates:
```sh
cd how-we-built-it
cargo run --release
```
Execution takes ~140ms on Apple Silicon and generates identical certificate artifacts.
