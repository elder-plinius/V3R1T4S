# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), produced while packaging. The time line is from `/usr/bin/time -l`: elapsed seconds real, user, sys; the memory line is the peak resident set size in bytes.

```
sha256 matches INDEX.csv (f9d89cde03cfc8905aecdd3fb1d2096f67c5490f666e2645791b86fdb524b350)
== check_sorter.py: exact 0-1 principle check, depth, comparison with the listed pairs
{"file": "N58_S469_D20.txt", "n": 58, "size": 469, "header_size": 469, "depth": 20, "max_states_tracked": 11613473, "final_states": 59, "SORTS": true, "matches_stated_n_size_depth": true, "listed_pairs": [[465, 21], [471, 20]], "listed_pairs_that_weakly_dominate_this_pair": [], "listed_pairs_that_this_pair_weakly_dominates": [[471, 20]], "not_dominated_by_any_listed_pair": true, "smaller_size_than_every_listed_pair": false, "smaller_depth_than_every_listed_pair": false}
checker verdict: PASS (SORTS=True, n/size/depth match=True, not dominated by a listed pair=True)
== negative control: the middle comparator deleted must NOT sort
negative control rejected as expected (SORTS false)
ALL CHECKS PASS
121.07 real       120.20 user         0.70 sys
2103279616  maximum resident set size
```
