# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), produced while packaging. The time line is from `/usr/bin/time -l`: elapsed seconds real, user, sys; the memory line is the peak resident set size in bytes.

```
sha256 matches INDEX.csv (4528989d7ce26b1f97c9c4566a34daecccaa3834fcc67502369638016309fda5)
== check_snake.py: two independent induced-snake tests, length, calibration on published records, class comparison
{"file": "p3_sn12_drifted_r0_Q12_1480.txt", "n": 12, "kind": "snake", "valid": true, "length": 1480, "vertices": 1481, "half_period_symmetric_per_table_page_test": false, "table_value": 1480, "table_value_source": "minortriad snake column, dimension 12 (page https://www.minortriad.com/snake/, fetched 2026-10-19T04:32:30Z)", "length_minus_table_value": 0, "calibration": [{"id": "minortriad sample sn12", "n": 12, "kind": "snake", "table_length": 1480, "valid": true, "length": 1480, "reproduces_table_length": true, "half_period_symmetric": false}], "calibration_all_reproduce": true, "canonical_class_hash": "dd9f75020311847a", "published_classes_compared": 2, "published_classes_with_same_canonical_hash": []}
checker verdict: PASS (valid=True, length=1480, calibration reproduces published lengths=True, half-period symmetric=False)
== negative control: one transition changed must NOT be a valid snake
negative control rejected as expected (valid false)
ALL CHECKS PASS
1.01 real         0.76 user         0.13 sys
16154624  maximum resident set size
```
