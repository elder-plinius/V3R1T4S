# Null-Model Control Test (`minimizer-density-record-tables` — `(w = 12, k = 4)`)

- `controls`: `400`
- `best_control`: `0.1498304838 (643517028 / 4294967296)`
- `real`: `0.1327703733 (570244411 / 4294967296)`
- `real_beats_all_controls`: `yes`
- `command`: `sh verify-it-yourself/run_checks.sh`

## Summary Statistics Across 400 Uniformly Random 256-Entry 4-Ary DNA Permutations (`seed = 20261107`)

- **Control sample size:** `400` uniformly random permutations of `0..255`
- **Control mean gamechanger count:** `660,668,696.60 / 2^32` (`0.1538239179`)
- **Control standard deviation:** `7,175,783.35 / 2^32` (`0.0016707423`)
- **Best (minimum) control across 400 trials:** `643,517,028 / 2^32` (`0.1498304838`)
- **Worst (maximum) control across 400 trials:** `694,059,891 / 2^32` (`0.1615984112`)
- **Claimed order (`object/w12_k4_4ary.gm`):** `570,244,411 / 2^32` (`0.1327703733`)
- **Z-score vs. random 4-ary permutation ensemble:** `z = -12.6013` (`0 / 400` random controls reach or beat `570,244,411`, which is `73,272,617` windows below the best of 400 controls).
