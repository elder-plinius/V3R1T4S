# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), by the packager after the integrity guard was added. Elapsed: 2.8 seconds.

```
sha256 matches INDEX.csv (4c4bc79e20aa730e2e8feb4c2d90d6f3cc493060cd9965dc9d252b184abe710c)
== check_snake.py: two independent induced-coil tests, length, calibration on published records, class comparison
{"file": "p3_co12_drifted_r0_Q12_1468.txt", "n": 12, "kind": "coil", "valid": true, "length": 1468, "vertices": 1468, "half_period_symmetric_per_table_page_test": false, "table_value": 1468, "table_value_source": "minortriad coil column, dimension 12 (page https://www.minortriad.com/snake/, fetched 2026-10-19T04:32:30Z)", "length_minus_table_value": 0, "calibration": [{"id": "minortriad sample co12", "n": 12, "kind": "coil", "table_length": 1468, "valid": true, "length": 1468, "reproduces_table_length": true, "half_period_symmetric": false}], "calibration_all_reproduce": true, "canonical_class_hash": "8b60333e45552c4e", "published_classes_compared": 2, "published_classes_with_same_canonical_hash": []}
checker verdict: PASS (valid=True, length=1468, calibration reproduces published lengths=True, half-period symmetric=False)
== negative control: one transition changed must NOT be a valid coil
negative control rejected as expected (valid false)
ALL CHECKS PASS
```
