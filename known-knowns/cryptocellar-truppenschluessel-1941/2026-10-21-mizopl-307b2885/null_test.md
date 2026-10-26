# Null Model Control Test (`cryptocellar-truppenschluessel-1941`, Partial Win `p1`)

controls: 400
best_control: 54395
real: 417578
command: python3 claim/author_checker_ts1941.py
real_beats_all_controls: yes

## Summary of 200-Shuffle and 400-Shuffle Ciphertext Null Controls

- **Number of independent shuffled-ciphertext controls**: `400` (`s = 0..399` in `work/run_400_null.c`, extending the `200` controls in `claim/p1_blind_garble_solver.c` and `claim/p1_benchmark_certificate.json`)
- **Generator & Pipeline**: Random Fisher-Yates permutations of all `116` ciphertext bigrams (`232` cipher letters across the 3 messages of lengths `80, 76, 76`) optimized through the exact same `climb_with_unmix` (`5,120`-move row-pair subset unmixer + rectangle local search) and scored with the pure 25-letter 1941 *Heeresgruppe Nord* conditional 4-gram language model (`T4_COND`, `crib_exact_w_g = 0`)
- **200-shuffle null distribution (`claim/p1_benchmark_certificate.json`)**:
  - `null_mean`: `-106,514.29` (`null_sd = 56,548.45`)
  - `null_min`: `-269,946`
  - `best_control` (`null_max`): `54,395`
  - Separation of `real = 417,578`: **`+9.27 SD` above mean**, **`+6.42 SD` above `best_control`** (`>= 5.0 SD PASS`)
- **400-shuffle null distribution (`work/run_400_null.c`)**:
  - `null_mean`: `-103,210.6` (`null_sd = 55,257.8`)
  - `best_control` (`null_max`): `54,395`
  - Separation of `real = 417,578`: **`+9.42 SD` above mean**, **`+6.57 SD` above `best_control`** (`>= 5.0 SD PASS`, `400 / 400` controls beaten)
