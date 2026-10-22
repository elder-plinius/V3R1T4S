# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), by the packager after the integrity guard was added. Elapsed: 0.4 seconds.

```
sha256 matches INDEX.csv (80851a336fbc159e2b27b2fa0b862285a7e099b81a57dcd283b21284eb67ab2d)
== check_snake.py: two independent induced-coil tests, length, calibration on published records, class comparison
{"file": "p3_co10_drifted_r0_Q10_374.txt", "n": 10, "kind": "coil", "valid": true, "length": 374, "vertices": 374, "half_period_symmetric_per_table_page_test": false, "table_value": 374, "table_value_source": "minortriad coil column, dimension 10 (page https://www.minortriad.com/snake/, fetched 2026-10-19T04:32:30Z)", "length_minus_table_value": 0, "calibration": [{"id": "minortriad sample co10", "n": 10, "kind": "coil", "table_length": 374, "valid": true, "length": 374, "reproduces_table_length": true, "half_period_symmetric": false}], "calibration_all_reproduce": true, "canonical_class_hash": "f2ddf6e1f06e26fd", "published_classes_compared": 14, "published_classes_with_same_canonical_hash": []}
checker verdict: PASS (valid=True, length=374, calibration reproduces published lengths=True, half-period symmetric=False)
== negative control: one transition changed must NOT be a valid coil
negative control rejected as expected (valid false)
ALL CHECKS PASS
```
