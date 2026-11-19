# Receipts: real output of sh verify-it-yourself/run_checks.sh

Run 2026-11-06T16:37:02Z (date -u) from this package folder, python3 3.13.5:

```
gen0: population 160, 32 components, all gliders
rewind T=8004: ok
rewind T=10916: ok
forward: exact repeat from generation 4332, period 1, population 27
final object: matches xs27_0ca1ugmicz651346 exactly, nothing else live
cost: 32 gliders < table cost 66
result: {'ok': True, 'target': 'xs27_0ca1ugmicz651346', 'n_gliders': 32, 'rewind_ok': True, 'periodic_from': 4332, 'period': 1, 'final_population': 27, 'final_matches_target': True, 'table_cost': 66}
PASS
PASS
```

Controls run (attempts/indep-sim of the packaging run, same life_check.py):

```
control drop glider  0 at (0, 1998): target built? False; builds xs27_8ehf8bbgz6430321 (positive control)
control drop glider  1 at (168, 1816): target built? False
control drop glider  2 at (169, 1): target built? False
control drop glider  3 at (172, 1813): target built? False
control drop glider  4 at (299, 1687): target built? False
control drop glider  5 at (299, 1692): target built? False
control drop glider  6 at (441, 1568): target built? False
control drop glider  7 at (564, 1439): target built? False
control drop glider  8 at (683, 1335): target built? False
control drop glider  9 at (689, 530): target built? False
control drop glider 10 at (937, 1046): target built? False
control drop glider 11 at (940, 768): target built? False
control drop glider 12 at (946, 766): target built? False
control drop glider 13 at (1069, 897): target built? False
control drop glider 14 at (1073, 924): target built? False
control drop glider 15 at (1076, 917): target built? False
control drop glider 16 at (1096, 918): target built? False
control drop glider 17 at (1096, 924): target built? False
control drop glider 18 at (1222, 1037): target built? False
control drop glider 19 at (1228, 1045): target built? False
control drop glider 20 at (1356, 1170): target built? False
control drop glider 21 at (1356, 1175): target built? False
control drop glider 22 at (1357, 638): target built? False
control drop glider 23 at (1477, 1314): target built? False
control drop glider 24 at (1485, 1313): target built? False
control drop glider 25 at (1489, 517): target built? False
control drop glider 26 at (1501, 497): target built? False
control drop glider 27 at (1503, 502): target built? False
control drop glider 28 at (1505, 1318): target built? False
control drop glider 29 at (1608, 396): target built? False
control drop glider 30 at (1738, 267): target built? False
control drop glider 31 at (1852, 1697): target built? False
positive controls found: 1
PASS
```
