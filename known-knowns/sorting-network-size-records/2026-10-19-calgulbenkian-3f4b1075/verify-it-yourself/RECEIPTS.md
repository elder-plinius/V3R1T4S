# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), produced while packaging. The time line is from `/usr/bin/time -l`: elapsed seconds real, user, sys; the memory line is the peak resident set size in bytes.

```
sha256 matches INDEX.csv (3f4b1075834d34c5903360bee8e064386f0aafb1aabd2130e1cee6eba350e382)
== check_sorter.py: exact 0-1 principle check, depth, comparison with the listed pairs
{"file": "N60_S488_D20.txt", "n": 60, "size": 488, "header_size": 488, "depth": 20, "max_states_tracked": 12952800, "final_states": 61, "SORTS": true, "matches_stated_n_size_depth": true, "listed_pairs": [[483, 21], [489, 20]], "listed_pairs_that_weakly_dominate_this_pair": [], "listed_pairs_that_this_pair_weakly_dominates": [[489, 20]], "not_dominated_by_any_listed_pair": true, "smaller_size_than_every_listed_pair": false, "smaller_depth_than_every_listed_pair": false}
checker verdict: PASS (SORTS=True, n/size/depth match=True, not dominated by a listed pair=True)
== negative control: the middle comparator deleted must NOT sort
negative control rejected as expected (SORTS false)
ALL CHECKS PASS
136.05 real       135.57 user         0.45 sys
2090287104  maximum resident set size
```
