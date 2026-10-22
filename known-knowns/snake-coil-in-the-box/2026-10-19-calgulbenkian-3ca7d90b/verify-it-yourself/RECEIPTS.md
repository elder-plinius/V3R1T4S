# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), by the packager after the integrity guard was added. Elapsed: 0.6 seconds.

```
sha256 matches INDEX.csv (3ca7d90bb6df1a1388eac4b6f6fca628febd8b3611a55f713ec4e60ac29e3ef2)
== check_snake.py: two independent induced-coil tests, length, calibration on published records, class comparison
{"file": "p3_co11_drifted_r0_Q11_740.txt", "n": 11, "kind": "coil", "valid": true, "length": 740, "vertices": 740, "half_period_symmetric_per_table_page_test": false, "table_value": 740, "table_value_source": "minortriad coil column, dimension 11 (page https://www.minortriad.com/snake/, fetched 2026-10-19T04:32:30Z)", "length_minus_table_value": 0, "calibration": [{"id": "minortriad sample co11", "n": 11, "kind": "coil", "table_length": 740, "valid": true, "length": 740, "reproduces_table_length": true, "half_period_symmetric": false}], "calibration_all_reproduce": true, "canonical_class_hash": "a705448579a0df70", "published_classes_compared": 2, "published_classes_with_same_canonical_hash": []}
checker verdict: PASS (valid=True, length=740, calibration reproduces published lengths=True, half-period symmetric=False)
== negative control: one transition changed must NOT be a valid coil
negative control rejected as expected (valid false)
ALL CHECKS PASS
```
