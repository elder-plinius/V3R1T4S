# Run it yourself (fresh shell, from this folder)

```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. The script prints the counters' own output above it (counts equal to 30362).

Direct commands:
```sh
python3 -I verify-it-yourself/count_stable.py --prefs object/instance_n15.txt --brute --expect 30362
```
Expected: `expected: 30362 PASS` with `lattice_count: 30362` and `brute_count: 30362`.

The object: `object/instance_n15.txt` (30 list lines: men's lists then women's lists, 1-based, most preferred first), sha256 ed5147118033557c8331a5b2b9ec7b08ee67139ee00f417b951f58ac24983fef.

How to rebuild the object: see how-we-built-it/COMMANDS.md (search code smclimb.c / smcount3.c; product builder prodGen.py).
