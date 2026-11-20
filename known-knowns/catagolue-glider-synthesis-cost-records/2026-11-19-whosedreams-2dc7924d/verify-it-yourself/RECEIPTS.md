# Receipts: real output of the standard-library checker

Run 2026-11-19 10:21:59 ET (America/New_York, UTC-5) on the object RLE, python3 3.13.5:

```
gen0: population 105, 21 components, all gliders
rewind T=7016: ok
rewind T=9892: ok
forward: exact repeat from generation 3840, period 1, population 25
final object: matches xs25_69ar1mkiczx643 exactly, nothing else live
cost: 21 gliders < table cost 49
result: {'ok': True, 'target': 'xs25_69ar1mkiczx643', 'n_gliders': 21, 'rewind_ok': True, 'periodic_from': 3840, 'period': 1, 'final_population': 25, 'final_matches_target': True, 'table_cost': 49}
PASS
```

Controls (same life_check.py, --controls --controls-skip-rewind --control-positive xs27_cikm1da4ozxd8711):

```
gen0: population 105, 21 components, all gliders
rewind T=7016: ok
rewind T=9892: ok
forward: exact repeat from generation 3840, period 1, population 25
final object: matches xs25_69ar1mkiczx643 exactly, nothing else live
cost: 21 gliders < table cost 49
result: {'ok': True, 'target': 'xs25_69ar1mkiczx643', 'n_gliders': 21, 'rewind_ok': True, 'periodic_from': 3840, 'period': 1, 'final_population': 25, 'final_matches_target': True, 'table_cost': 49}
control drop glider  0 at (0, 1752): target built? False; builds xs27_cikm1da4ozxd8711 (positive control)
control drop glider  1 at (174, 3): target built? False
control drop glider  2 at (313, 132): target built? False
control drop glider  3 at (437, 1302): target built? False
control drop glider  4 at (438, 258): target built? False
control drop glider  5 at (556, 1186): target built? False
control drop glider  6 at (561, 1178): target built? False
control drop glider  7 at (562, 389): target built? False
control drop glider  8 at (568, 385): target built? False
control drop glider  9 at (692, 1043): target built? False
control drop glider 10 at (827, 937): target built? False
control drop glider 11 at (930, 772): target built? False
control drop glider 12 at (936, 773): target built? False
control drop glider 13 at (952, 807): target built? False
control drop glider 14 at (957, 798): target built? False
control drop glider 15 at (973, 778): target built? False
control drop glider 16 at (979, 770): target built? False
control drop glider 17 at (1359, 387): target built? False
control drop glider 18 at (1615, 130): target built? False
control drop glider 19 at (1730, 1): target built? False
control drop glider 20 at (1739, 1): target built? False
positive controls found: 1
PASS
```
