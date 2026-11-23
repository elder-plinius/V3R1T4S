# Receipts: real output of the standard-library checker

Run 2026-11-19 10:21:59 ET (America/New_York, UTC-5) on the object RLE, python3 3.13.5:

```
gen0: population 55, 11 components, all gliders
rewind T=2816: ok
rewind T=3980: ok
forward: exact repeat from generation 1752, period 1, population 26
final object: matches xs26_oo0o4qabqiczx321 exactly, nothing else live
cost: 11 gliders < table cost 35
result: {'ok': True, 'target': 'xs26_oo0o4qabqiczx321', 'n_gliders': 11, 'rewind_ok': True, 'periodic_from': 1752, 'period': 1, 'final_population': 26, 'final_matches_target': True, 'table_cost': 35}
PASS
```

Controls (same life_check.py, --controls --controls-skip-rewind --control-positive xs27_3lkmz01iu1u8zw1221):

```
gen0: population 55, 11 components, all gliders
rewind T=2816: ok
rewind T=3980: ok
forward: exact repeat from generation 1752, period 1, population 26
final object: matches xs26_oo0o4qabqiczx321 exactly, nothing else live
cost: 11 gliders < table cost 35
result: {'ok': True, 'target': 'xs26_oo0o4qabqiczx321', 'n_gliders': 11, 'rewind_ok': True, 'periodic_from': 1752, 'period': 1, 'final_population': 26, 'final_matches_target': True, 'table_cost': 35}
control drop glider  0 at (0, 0): target built? False
control drop glider  1 at (250, 274): target built? False
control drop glider  2 at (258, 272): target built? False
control drop glider  3 at (262, 269): target built? False
control drop glider  4 at (262, 280): target built? False
control drop glider  5 at (270, 274): target built? False
control drop glider  6 at (389, 131): target built? False
control drop glider  7 at (392, 126): target built? False
control drop glider  8 at (392, 390): target built? False
control drop glider  9 at (516, 1): target built? False
control drop glider 10 at (701, 699): target built? False; builds xs27_3lkmz01iu1u8zw1221 (positive control)
positive controls found: 1
PASS
```
