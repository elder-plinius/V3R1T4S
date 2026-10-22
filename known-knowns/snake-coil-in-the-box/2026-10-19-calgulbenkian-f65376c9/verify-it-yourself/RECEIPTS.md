# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), produced while packaging. The time line is from `/usr/bin/time -l`: elapsed seconds real, user, sys; the memory line is the peak resident set size in bytes.

```
sha256 matches INDEX.csv (f65376c952a341360326ffffc366447cce2b4ee96be4e6335d62fa0ceadf9cb2)
== check_snake.py: two independent induced-coil tests, length, calibration on published records, class comparison
{"file": "best_sym12_Q12_1454.txt", "n": 12, "kind": "coil", "valid": true, "length": 1454, "vertices": 1454, "half_period_symmetric_per_table_page_test": true, "table_value": 1434, "table_value_source": "minortriad symmetric-coil column, dimension 12 (page https://www.minortriad.com/snake/, fetched 2026-10-19T04:32:30Z)", "length_minus_table_value": 20, "calibration": [{"id": "minortriad sample sc12", "n": 12, "kind": "coil", "table_length": 1434, "valid": true, "length": 1434, "reproduces_table_length": true, "half_period_symmetric": true}], "calibration_all_reproduce": true, "canonical_class_hash": "4b4273abb595433e", "published_classes_compared": 1, "published_classes_with_same_canonical_hash": []}
checker verdict: PASS (valid=True, length=1454, calibration reproduces published lengths=True, half-period symmetric=True)
== negative control: one transition changed must NOT be a valid coil
negative control rejected as expected (valid false)
ALL CHECKS PASS
1.20 real         0.99 user         0.13 sys
16105472  maximum resident set size
```
