# Run it yourself (fresh shell, from this folder)

```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. The script prints the counters' own output above it (counts equal to 530528).

Direct commands:
```sh
cc -O2 -o verify-it-yourself/smcount3 verify-it-yourself/smcount3.c -lm && ./verify-it-yourself/smcount3 enumerate object/instance_n18.txt
```
Expected: `enumerated_ideals: 530528`, `unstable_matchings_found: 0`, `agree: yes`.

The object: `object/instance_n18.txt` (36 list lines: men's lists then women's lists, 1-based, most preferred first), sha256 12429e3eb7c67d315bddabe7ac71edc070cfbaae1760c67f66b8d2fa1e61b488.

How to rebuild the object: see how-we-built-it/COMMANDS.md (search code smclimb.c / smcount3.c; product builder prodGen.py).
