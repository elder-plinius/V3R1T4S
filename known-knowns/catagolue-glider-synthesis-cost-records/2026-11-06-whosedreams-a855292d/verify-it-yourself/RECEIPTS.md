# Receipts: real output of sh verify-it-yourself/run_checks.sh

Run 2026-11-06T16:14:05Z (date -u) from this package folder, python3 3.13.5:

```
gen0: population 60, 12 components, all gliders
rewind T=2860: ok
rewind T=4040: ok
forward: exact repeat from generation 1774, period 1, population 26
final object: matches xs26_08ehmkk8z6a87066 exactly, nothing else live
cost: 12 gliders < table cost 58
result: {'ok': True, 'target': 'xs26_08ehmkk8z6a87066', 'n_gliders': 12, 'rewind_ok': True, 'periodic_from': 1774, 'period': 1, 'final_population': 26, 'final_matches_target': True, 'table_cost': 58}
PASS
PASS
```

Controls run (attempts/indep-sim of the packaging run, same life_check.py):

```
control drop glider  0 at (0, 0): target built? False
control drop glider  1 at (0, 534): target built? False
control drop glider  2 at (130, 117): target built? False
control drop glider  3 at (131, 124): target built? False
control drop glider  4 at (132, 400): target built? False
control drop glider  5 at (248, 244): target built? False
control drop glider  6 at (252, 249): target built? False
control drop glider  7 at (282, 251): target built? False
control drop glider  8 at (282, 271): target built? False
control drop glider  9 at (291, 243): target built? False
control drop glider 10 at (534, 534): target built? False
control drop glider 11 at (712, 709): target built? False; builds xs28_651ugmmz69706221 (positive control)
positive controls found: 1
PASS
```
