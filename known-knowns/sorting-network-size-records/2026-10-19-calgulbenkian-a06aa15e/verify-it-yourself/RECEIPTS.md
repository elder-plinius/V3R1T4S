# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), produced while packaging. The time line is from `/usr/bin/time -l`: elapsed seconds real, user, sys; the memory line is the peak resident set size in bytes.

```
sha256 matches INDEX.csv (a06aa15e8bce7af1bc7b6c18dd33b4230b8cad01d8be921c32b8180aa0a84fa0)
== check_sorter.py: exact 0-1 principle check, depth, comparison with the listed pairs
{"file": "N54_S434_D19.txt", "n": 54, "size": 434, "header_size": 434, "depth": 19, "max_states_tracked": 7216, "final_states": 55, "SORTS": true, "matches_stated_n_size_depth": true, "listed_pairs": [[421, 20], [435, 19]], "listed_pairs_that_weakly_dominate_this_pair": [], "listed_pairs_that_this_pair_weakly_dominates": [[435, 19]], "not_dominated_by_any_listed_pair": true, "smaller_size_than_every_listed_pair": false, "smaller_depth_than_every_listed_pair": false}
checker verdict: PASS (SORTS=True, n/size/depth match=True, not dominated by a listed pair=True)
== negative control: the middle comparator deleted must NOT sort
negative control rejected as expected (SORTS false)
ALL CHECKS PASS
0.48 real         0.29 user         0.11 sys
16318464  maximum resident set size
```
