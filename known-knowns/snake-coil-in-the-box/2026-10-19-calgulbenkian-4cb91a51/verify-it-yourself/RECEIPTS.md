# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), produced while packaging. The time line is from `/usr/bin/time -l`: elapsed seconds real, user, sys; the memory line is the peak resident set size in bytes.

```
sha256 matches INDEX.csv (4cb91a51274083a86d9f3edca2dc46358757d9990d246755f6756b989ff6fbda)
== check_snake.py: two independent induced-coil tests, length, calibration on published records, class comparison
{"file": "best_sym13_from2882_Q13_2886.txt", "n": 13, "kind": "coil", "valid": true, "length": 2886, "vertices": 2886, "half_period_symmetric_per_table_page_test": true, "table_value": 2830, "table_value_source": "minortriad symmetric-coil column, dimension 13 (page https://www.minortriad.com/snake/, fetched 2026-10-19T04:32:30Z)", "length_minus_table_value": 56, "calibration": [{"id": "minortriad sample sc13", "n": 13, "kind": "coil", "table_length": 2830, "valid": true, "length": 2830, "reproduces_table_length": true, "half_period_symmetric": true}], "calibration_all_reproduce": true, "canonical_class_hash": "ee70083e8016dbc6", "published_classes_compared": 1, "published_classes_with_same_canonical_hash": []}
checker verdict: PASS (valid=True, length=2886, calibration reproduces published lengths=True, half-period symmetric=True)
== negative control: one transition changed must NOT be a valid coil
negative control rejected as expected (valid false)
ALL CHECKS PASS
3.41 real         3.04 user         0.07 sys
16351232  maximum resident set size
```
