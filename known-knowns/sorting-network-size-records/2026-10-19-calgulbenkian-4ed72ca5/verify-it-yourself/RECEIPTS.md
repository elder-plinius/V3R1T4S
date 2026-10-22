# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), produced while packaging. The time line is from `/usr/bin/time -l`: elapsed seconds real, user, sys; the memory line is the peak resident set size in bytes.

```
sha256 matches INDEX.csv (4ed72ca5cb966a3d915e0769777a0750e0a2b98aa5109f5efe81db821e374a12)
== check_sorter.py: exact 0-1 principle check, depth, comparison with the listed pairs
{"file": "N53_S422_D19.txt", "n": 53, "size": 422, "header_size": 422, "depth": 19, "max_states_tracked": 6232, "final_states": 54, "SORTS": true, "matches_stated_n_size_depth": true, "listed_pairs": [[411, 22], [412, 21], [414, 20], [423, 19]], "listed_pairs_that_weakly_dominate_this_pair": [], "listed_pairs_that_this_pair_weakly_dominates": [[423, 19]], "not_dominated_by_any_listed_pair": true, "smaller_size_than_every_listed_pair": false, "smaller_depth_than_every_listed_pair": false}
checker verdict: PASS (SORTS=True, n/size/depth match=True, not dominated by a listed pair=True)
== negative control: the middle comparator deleted must NOT sort
negative control rejected as expected (SORTS false)
ALL CHECKS PASS
0.45 real         0.28 user         0.11 sys
16007168  maximum resident set size
```
