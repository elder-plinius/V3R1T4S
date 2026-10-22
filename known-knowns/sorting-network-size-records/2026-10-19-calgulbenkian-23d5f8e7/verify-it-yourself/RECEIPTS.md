# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), produced while packaging. The time line is from `/usr/bin/time -l`: elapsed seconds real, user, sys; the memory line is the peak resident set size in bytes.

```
sha256 matches INDEX.csv (23d5f8e799b3be5d5195fbcfff00d0b23f03ef57264bb9120b24b613ec335922)
== check_sorter.py: exact 0-1 principle check, depth, comparison with the listed pairs
{"file": "N53_S413_D20.txt", "n": 53, "size": 413, "header_size": 413, "depth": 20, "max_states_tracked": 207535, "final_states": 54, "SORTS": true, "matches_stated_n_size_depth": true, "listed_pairs": [[411, 22], [412, 21], [414, 20], [423, 19]], "listed_pairs_that_weakly_dominate_this_pair": [], "listed_pairs_that_this_pair_weakly_dominates": [[414, 20]], "not_dominated_by_any_listed_pair": true, "smaller_size_than_every_listed_pair": false, "smaller_depth_than_every_listed_pair": false}
checker verdict: PASS (SORTS=True, n/size/depth match=True, not dominated by a listed pair=True)
== negative control: the middle comparator deleted must NOT sort
negative control rejected as expected (SORTS false)
ALL CHECKS PASS
1.76 real         1.25 user         0.08 sys
56164352  maximum resident set size
```
