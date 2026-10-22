# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder on 2026-10-19 (python3, standard library only), by the packager after the integrity guard was added. Elapsed: 1.1 seconds.

```
sha256 matches INDEX.csv (13f82b2e8ef05882c7d78fe1511df710fa3754f9debec76c2ac83aa3ecd60c54)
== check_snake.py: two independent induced-snake tests, length, calibration on published records, class comparison
{"file": "p3_sn11_drifted_r0_Q11_750.txt", "n": 11, "kind": "snake", "valid": true, "length": 750, "vertices": 751, "half_period_symmetric_per_table_page_test": false, "table_value": 750, "table_value_source": "minortriad snake column, dimension 11 (page https://www.minortriad.com/snake/, fetched 2026-10-19T04:32:30Z)", "length_minus_table_value": 0, "calibration": [{"id": "minortriad sample sn11", "n": 11, "kind": "snake", "table_length": 750, "valid": true, "length": 750, "reproduces_table_length": true, "half_period_symmetric": false}], "calibration_all_reproduce": true, "canonical_class_hash": "09e8fd82251c383a", "published_classes_compared": 2, "published_classes_with_same_canonical_hash": []}
checker verdict: PASS (valid=True, length=750, calibration reproduces published lengths=True, half-period symmetric=False)
== negative control: one transition changed must NOT be a valid snake
negative control rejected as expected (valid false)
ALL CHECKS PASS
```
