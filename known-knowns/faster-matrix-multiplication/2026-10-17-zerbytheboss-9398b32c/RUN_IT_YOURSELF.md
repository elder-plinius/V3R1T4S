# Run It Yourself

## 1. Verify the `4x5x5` Rank-76 `cr=280` SLP in 0.2 Seconds
From this package root:
```sh
sh verify-it-yourself/run_checks.sh
```
This runs `verify-it-yourself/check_slp.py` using only the Python 3 standard library. It verifies:
1. Exact SHA-256 match of `object/4x5x5_m76_cr280_ZT_reduced.json` against `INDEX.csv`.
2. Strict DAG acyclicity (`u_fresh`, `v_fresh`, `w_fresh` reference only already-defined variables with no cross-factor sharing).
3. Every expanded linear form entry of `U`, `V`, `W` is strictly in `{-1, 0, 1}`.
4. Exact satisfaction of all `20 * 25 * 20 = 10,000` integer Brent equations over `Z` (`0` errors) and 20 random integer matrix products `A * B = C`.
5. Exact reduced addition count: `U = 75`, `V = 84`, `W = 121`, total `cr = 280`.
