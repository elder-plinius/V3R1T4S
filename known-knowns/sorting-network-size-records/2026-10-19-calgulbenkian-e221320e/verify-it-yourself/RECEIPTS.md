# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), produced while packaging. The time line is from `/usr/bin/time -l`: elapsed seconds real, user, sys; the memory line is the peak resident set size in bytes.

```
sha256 matches INDEX.csv (e221320e3d190b87782aee7c6753917b43c49196cc567add0ed233c89dbffb4a)
== check_sorter.py: exact 0-1 principle check, depth, comparison with the listed pairs
{"file": "N57_S458_D20.txt", "n": 57, "size": 458, "header_size": 458, "depth": 20, "max_states_tracked": 8830665, "final_states": 58, "SORTS": true, "matches_stated_n_size_depth": true, "listed_pairs": [[454, 21], [461, 20]], "listed_pairs_that_weakly_dominate_this_pair": [], "listed_pairs_that_this_pair_weakly_dominates": [[461, 20]], "not_dominated_by_any_listed_pair": true, "smaller_size_than_every_listed_pair": false, "smaller_depth_than_every_listed_pair": false}
checker verdict: PASS (SORTS=True, n/size/depth match=True, not dominated by a listed pair=True)
== negative control: the middle comparator deleted must NOT sort
negative control rejected as expected (SORTS false)
ALL CHECKS PASS
94.94 real        92.73 user         1.19 sys
1583120384  maximum resident set size
```
