# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), produced while packaging. The time line is from `/usr/bin/time -l`: elapsed seconds real, user, sys; the memory line is the peak resident set size in bytes.

```
sha256 matches INDEX.csv (ad7e599b39b1cb71bd665cc2458ef169ae4da434fdd1e97cfe684053125cac21)
== check_snake.py: two independent induced-snake tests, length, calibration on published records, class comparison
{"file": "p3_sn13_drifted_r0_Q13_2946.txt", "n": 13, "kind": "snake", "valid": true, "length": 2946, "vertices": 2947, "half_period_symmetric_per_table_page_test": false, "table_value": 2946, "table_value_source": "minortriad snake column, dimension 13 (page https://www.minortriad.com/snake/, fetched 2026-10-19T04:32:30Z)", "length_minus_table_value": 0, "calibration": [{"id": "minortriad sample sn13", "n": 13, "kind": "snake", "table_length": 2946, "valid": true, "length": 2946, "reproduces_table_length": true, "half_period_symmetric": false}], "calibration_all_reproduce": true, "canonical_class_hash": "980b7dba160956f6", "published_classes_compared": 2, "published_classes_with_same_canonical_hash": []}
checker verdict: PASS (valid=True, length=2946, calibration reproduces published lengths=True, half-period symmetric=False)
== negative control: one transition changed must NOT be a valid snake
negative control rejected as expected (valid false)
ALL CHECKS PASS
2.48 real         2.22 user         0.12 sys
16498688  maximum resident set size
```
