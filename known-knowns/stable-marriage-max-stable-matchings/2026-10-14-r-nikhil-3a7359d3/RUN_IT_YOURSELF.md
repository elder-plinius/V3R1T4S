# Run it yourself (fresh shell, from this folder)

```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. The script prints the counters' own output above it (counts equal to 27510).

Direct commands:
```sh
python3 -I verify-it-yourself/count_stable.py --prefs object/instance_n15.txt --brute --expect 27510
```
Expected: `expected: 27510 PASS` with `lattice_count: 27510` and `brute_count: 27510`.

The object: `object/instance_n15.txt` (30 list lines: men's lists then women's lists, 1-based, most preferred first), sha256 3a7359d3db2f878cae106c2f527763c6abf150c0788b943de38661076ab539a8.

How to rebuild the object: see how-we-built-it/COMMANDS.md (search code smclimb.c / smcount3.c; product builder prodGen.py).
