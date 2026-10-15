# Run it yourself (fresh shell, from this folder)

```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. The script prints the counters' own output above it (counts equal to 12277568).

Direct commands:
```sh
cc -O2 -o verify-it-yourself/smcount3 verify-it-yourself/smcount3.c -lm && ./verify-it-yourself/smcount3 enumerate object/instance_n22.txt
```
Expected: `enumerated_ideals: 12277568`, `unstable_matchings_found: 0`, `agree: yes`.

The object: `object/instance_n22.txt` (44 list lines: men's lists then women's lists, 1-based, most preferred first), sha256 213b4ac73bfb4218a4295514410d0d53b6a87f48e8f1462d61382579efdd5b37.

How to rebuild the object: see how-we-built-it/COMMANDS.md (search code smclimb.c / smcount3.c; product builder prodGen.py).
