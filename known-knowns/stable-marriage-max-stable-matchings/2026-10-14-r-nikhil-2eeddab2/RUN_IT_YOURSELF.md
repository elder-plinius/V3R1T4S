# Run it yourself (fresh shell, from this folder)

```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. The script prints the counters' own output above it (counts equal to 24992).

Direct commands:
```sh
python3 -I verify-it-yourself/count_stable.py --prefs object/instance_n14.txt --brute --expect 24992
```
Expected: `expected: 24992 PASS` with `lattice_count: 24992` and `brute_count: 24992`.

The object: `object/instance_n14.txt` (28 list lines: men's lists then women's lists, 1-based, most preferred first), sha256 2eeddab210507ca8fecf7cb18e88a27245dd861ab7497acfc0d023766cf76965.

How to rebuild the object: see how-we-built-it/COMMANDS.md (search code smclimb.c / smcount3.c; product builder prodGen.py).
