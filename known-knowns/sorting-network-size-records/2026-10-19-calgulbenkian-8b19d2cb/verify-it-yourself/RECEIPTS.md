# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), produced while packaging. The time line is from `/usr/bin/time -l`: elapsed seconds real, user, sys; the memory line is the peak resident set size in bytes.

```
sha256 matches INDEX.csv (8b19d2cb06fb21333ee3b2e392b131340ec4899b2e659250b51e637c5c41cfc3)
== check_sorter.py: exact 0-1 principle check, depth, comparison with the listed pairs
{"file": "N51_S387_D21.txt", "n": 51, "size": 387, "header_size": 387, "depth": 21, "max_states_tracked": 115026, "final_states": 52, "SORTS": true, "matches_stated_n_size_depth": true, "listed_pairs": [[387, 22], [389, 20], [396, 19]], "listed_pairs_that_weakly_dominate_this_pair": [], "listed_pairs_that_this_pair_weakly_dominates": [[387, 22]], "not_dominated_by_any_listed_pair": true, "smaller_size_than_every_listed_pair": false, "smaller_depth_than_every_listed_pair": false}
checker verdict: PASS (SORTS=True, n/size/depth match=True, not dominated by a listed pair=True)
== negative control: the middle comparator deleted must NOT sort
negative control rejected as expected (SORTS false)
ALL CHECKS PASS
1.22 real         0.93 user         0.17 sys
48824320  maximum resident set size
```
