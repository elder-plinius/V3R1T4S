# Receipts: real output of the standard-library checker

Run 2026-11-19 10:21:59 ET (America/New_York, UTC-5) on the object RLE, python3 3.13.5:

```
gen0: population 65, 13 components, all gliders
rewind T=2880: ok
rewind T=4012: ok
forward: exact repeat from generation 1786, period 1, population 26
final object: matches xs26_8kk69ba952zw3453 exactly, nothing else live
cost: 13 gliders < table cost 32
result: {'ok': True, 'target': 'xs26_8kk69ba952zw3453', 'n_gliders': 13, 'rewind_ok': True, 'periodic_from': 1786, 'period': 1, 'final_population': 26, 'final_matches_target': True, 'table_cost': 32}
PASS
```

Controls (same life_check.py, --controls --controls-skip-rewind --control-positive xs27_g88ehmkia4z0178a6):

```
gen0: population 65, 13 components, all gliders
rewind T=2880: ok
rewind T=4012: ok
forward: exact repeat from generation 1786, period 1, population 26
final object: matches xs26_8kk69ba952zw3453 exactly, nothing else live
cost: 13 gliders < table cost 32
result: {'ok': True, 'target': 'xs26_8kk69ba952zw3453', 'n_gliders': 13, 'rewind_ok': True, 'periodic_from': 1786, 'period': 1, 'final_population': 26, 'final_matches_target': True, 'table_cost': 32}
control drop glider  0 at (0, 717): target built? False; builds xs27_g88ehmkia4z0178a6 (positive control)
control drop glider  1 at (155, 538): target built? False
control drop glider  2 at (162, 2): target built? False
control drop glider  3 at (172, 540): target built? False
control drop glider  4 at (310, 124): target built? False
control drop glider  5 at (312, 118): target built? False
control drop glider  6 at (453, 258): target built? False
control drop glider  7 at (473, 274): target built? False
control drop glider  8 at (587, 129): target built? False
control drop glider  9 at (589, 408): target built? False
control drop glider 10 at (591, 120): target built? False
control drop glider 11 at (595, 408): target built? False
control drop glider 12 at (694, 1): target built? False
positive controls found: 1
PASS
```
