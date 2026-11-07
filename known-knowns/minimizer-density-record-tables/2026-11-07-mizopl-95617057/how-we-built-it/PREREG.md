# Pre-Registration (`minimizer-density-record-tables` — `(w = 12, k = 4)` Direct 4-Ary DNA Order)

- `target_id`: `minimizer-density-record-tables`
- `frozen_utc`: `2026-11-07T15:00:00Z`
- `micro_bet_id`: `L-MDRT-001` (`mdrt_minimizers_best_orders_gap_search`)
- `cell`: `w = 12, k = 4` ($\sigma = 4$ DNA alphabet, $4^4 = 256$ 4-mers)
- `statistic`: Exact expected DNA gamechanger density over all $4^{w+k} = 4^{16} = 4,294,967,296$ equiprobable DNA windows of length $w + k = 16$ under leftmost tie-breaking.
- `baseline_to_beat`: `574,313,157 / 2^32 = 0.1337177020` (`OrensteinLab/Minimizers` `lowest-density/binary/best-orders.csv` / `k4-w12.txt` `[3, 16, 2, 16, 16, 4, 1, 0, 16, 16, 16, 16, 16, 16, 5, 6]`, extended to DNA) and `584,312,429 / 2^32 = 0.1360458389` (`OrensteinLab/10-minimizers` `w12_k4.gm`).
- `success_threshold`: Relative reduction $\ge 0.5\%$ below `0.1337177020`, i.e., exact DNA density $\le 0.1330491135$ ($\le 571,441,591 / 2^{32}$ gamechanger contexts).
- `method`: Direct 4-ary DNA permutation hill-climbing (`how-we-built-it/opt_4ary_dna.cpp`, `rng_seed = 42`) initialized from the binary-projected order `[15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5]`.
- `null_test`: `required` (400 uniformly random 256-entry 4-ary permutations evaluated with the identical exact 4-ary de Bruijn transfer-matrix DP, `seed = 20261107`).
