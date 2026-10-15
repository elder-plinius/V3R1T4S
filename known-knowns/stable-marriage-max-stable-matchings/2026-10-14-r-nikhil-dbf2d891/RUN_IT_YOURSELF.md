# Run it yourself (fresh shell, from this folder)

```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. The script prints the counters' own output above it (counts equal to 2497797760).

Direct commands:
```sh
cc -O2 -o verify-it-yourself/smcount3 verify-it-yourself/smcount3.c -lm && MEMO_MAX_STATES=40000000 ./verify-it-yourself/smcount3 count object/instance_n28.txt 0
```
Expected: `count_poset: 2497797760`; with FULL=1 also `enumerated_ideals: 2497797760`, `unstable_matchings_found: 0`, `agree: yes`.

The object: `object/instance_n28.txt` (56 list lines: men's lists then women's lists, 1-based, most preferred first), sha256 dbf2d89155213b672ef7514493d16c7f02225a84dbcc31f4ae30068f085e1ad0.

How to rebuild the object: see how-we-built-it/COMMANDS.md (search code smclimb.c / smcount3.c; product builder prodGen.py).
