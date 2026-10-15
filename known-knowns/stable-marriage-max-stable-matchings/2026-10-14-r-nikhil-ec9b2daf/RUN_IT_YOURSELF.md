# Run it yourself (fresh shell, from this folder)

```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. The script prints the counters' own output above it (counts equal to 7698).

Direct commands:
```sh
python3 -I verify-it-yourself/count_stable.py --prefs object/instance_n13.txt --brute --expect 7698
```
Expected: `expected: 7698 PASS` with `lattice_count: 7698` and `brute_count: 7698`.

The object: `object/instance_n13.txt` (26 list lines: men's lists then women's lists, 1-based, most preferred first), sha256 ec9b2daf4bafd04fb7118987cc88ae424471d1bb49f6e3632fb0367c9e3acc69.

How to rebuild the object: see how-we-built-it/COMMANDS.md (search code smclimb.c / smcount3.c; product builder prodGen.py).
