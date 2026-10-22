# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), produced while packaging. The time line is from `/usr/bin/time -l`: elapsed seconds real, user, sys; the memory line is the peak resident set size in bytes.

```
sha256 matches INDEX.csv (e4ef45f9dda97a64c70c380dc0508ecb86e21b0654d8fa4248d58e30b3628f09)
== check_sorter.py: exact 0-1 principle check, depth, comparison with the listed pairs
{"file": "N38_S253_D16.txt", "n": 38, "size": 253, "header_size": 253, "depth": 16, "max_states_tracked": 68228, "final_states": 39, "SORTS": true, "matches_stated_n_size_depth": true, "listed_pairs": [[250, 17], [254, 16]], "listed_pairs_that_weakly_dominate_this_pair": [], "listed_pairs_that_this_pair_weakly_dominates": [[254, 16]], "not_dominated_by_any_listed_pair": true, "smaller_size_than_every_listed_pair": false, "smaller_depth_than_every_listed_pair": false}
checker verdict: PASS (SORTS=True, n/size/depth match=True, not dominated by a listed pair=True)
== negative control: the middle comparator deleted must NOT sort
negative control rejected as expected (SORTS false)
ALL CHECKS PASS
0.89 real         0.54 user         0.09 sys
32096256  maximum resident set size
```
