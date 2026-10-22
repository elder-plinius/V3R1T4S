# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), produced while packaging. The time line is from `/usr/bin/time -l`: elapsed seconds real, user, sys; the memory line is the peak resident set size in bytes.

```
sha256 matches INDEX.csv (82c812aff15882e17177fd6fd63b1746bc2b6af01dc7601ccddb76eec2c7e181)
== check_snake.py: two independent induced-coil tests, length, calibration on published records, class comparison
{"file": "p3_co13_drifted_r0_Q13_2930.txt", "n": 13, "kind": "coil", "valid": true, "length": 2930, "vertices": 2930, "half_period_symmetric_per_table_page_test": false, "table_value": 2930, "table_value_source": "minortriad coil column, dimension 13 (page https://www.minortriad.com/snake/, fetched 2026-10-19T04:32:30Z)", "length_minus_table_value": 0, "calibration": [{"id": "minortriad sample co13", "n": 13, "kind": "coil", "table_length": 2930, "valid": true, "length": 2930, "reproduces_table_length": true, "half_period_symmetric": false}], "calibration_all_reproduce": true, "canonical_class_hash": "1fd11788688a82c3", "published_classes_compared": 2, "published_classes_with_same_canonical_hash": []}
checker verdict: PASS (valid=True, length=2930, calibration reproduces published lengths=True, half-period symmetric=False)
== negative control: one transition changed must NOT be a valid coil
negative control rejected as expected (valid false)
ALL CHECKS PASS
3.72 real         3.32 user         0.21 sys
16842752  maximum resident set size
```
