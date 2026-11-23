# Receipts: real output of the standard-library checker

Run 2026-11-19 10:21:59 ET (America/New_York, UTC-5) on the object RLE, python3 3.13.5:

```
gen0: population 145, 29 components, all gliders
rewind T=4920: ok
rewind T=6284: ok
forward: exact repeat from generation 2810, period 1, population 27
final object: matches xs27_08e1ugmicz651346 exactly, nothing else live
cost: 29 gliders < table cost 62
result: {'ok': True, 'target': 'xs27_08e1ugmicz651346', 'n_gliders': 29, 'rewind_ok': True, 'periodic_from': 2810, 'period': 1, 'final_population': 27, 'final_matches_target': True, 'table_cost': 62}
PASS
```

Controls (same life_check.py, --controls --controls-skip-rewind --control-positive xs27_caar4kl3z330343):

```
gen0: population 145, 29 components, all gliders
rewind T=4920: ok
rewind T=6284: ok
forward: exact repeat from generation 2810, period 1, population 27
final object: matches xs27_08e1ugmicz651346 exactly, nothing else live
cost: 29 gliders < table cost 62
result: {'ok': True, 'target': 'xs27_08e1ugmicz651346', 'n_gliders': 29, 'rewind_ok': True, 'periodic_from': 2810, 'period': 1, 'final_population': 27, 'final_matches_target': True, 'table_cost': 62}
control drop glider  0 at (0, 2): target built? False; builds xs27_caar4kl3z330343 (positive control)
control drop glider  1 at (177, 172): target built? False
control drop glider  2 at (183, 175): target built? False
control drop glider  3 at (314, 303): target built? False
control drop glider  4 at (428, 975): target built? False
control drop glider  5 at (431, 437): target built? False
control drop glider  6 at (434, 968): target built? False
control drop glider  7 at (437, 424): target built? False
control drop glider  8 at (552, 847): target built? False
control drop glider  9 at (556, 556): target built? False
control drop glider 10 at (559, 548): target built? False
control drop glider 11 at (566, 560): target built? False
control drop glider 12 at (688, 691): target built? False
control drop glider 13 at (704, 727): target built? False
control drop glider 14 at (720, 707): target built? False
control drop glider 15 at (728, 693): target built? False
control drop glider 16 at (736, 695): target built? False
control drop glider 17 at (841, 556): target built? False
control drop glider 18 at (846, 561): target built? False
control drop glider 19 at (848, 551): target built? False
control drop glider 20 at (855, 554): target built? False
control drop glider 21 at (975, 428): target built? False
control drop glider 22 at (977, 422): target built? False
control drop glider 23 at (980, 432): target built? False
control drop glider 24 at (986, 434): target built? False
control drop glider 25 at (986, 972): target built? False
control drop glider 26 at (1101, 306): target built? False
control drop glider 27 at (1102, 300): target built? False
control drop glider 28 at (1227, 176): target built? False
positive controls found: 1
PASS
```
