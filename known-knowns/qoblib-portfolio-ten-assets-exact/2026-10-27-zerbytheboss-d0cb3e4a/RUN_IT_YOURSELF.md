# Run It Yourself

## 1. Fast Python Verification (< 0.6 Seconds)
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
This executes `verify-it-yourself/check_portfolio_opt.py`, which:
1. Downloads the raw QOBLIB instance files (`stock_prices.txt.gz`, `covariance_matrices.txt.gz`) into a local temporary cache and verifies their sha256 checksums.
2. Evaluates the canonical schedule `object/po_a010_t10_orig_b004_l1e-03.sol` using exact Zimpl round-half-away-from-zero rational arithmetic, verifying all 6 constraint categories and the exact objective breakdown totaling -8397.
3. Recomputes all $10 \times 10,606$ discrete count stage costs from scratch.
4. Verifies all 5 Hasse-diagram Bellman optimality inequalities across all 10,606 states, certifying global optimality.
Expected final line: `PASS`.

## 2. Rebuild the Certificate from Source
To re-run the certified Hasse distance transform solver and export fresh certificates:
```sh
cd how-we-built-it
cargo run --release
```
Execution takes ~140ms on Apple Silicon and generates identical certificate artifacts.
