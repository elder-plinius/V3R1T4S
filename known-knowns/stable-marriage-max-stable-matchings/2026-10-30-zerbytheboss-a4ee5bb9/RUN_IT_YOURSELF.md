# Run it yourself (fresh shell, from this folder)

```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Both counters print their exact counts of 206,728 stable matchings.

Direct commands:
```sh
# Method 1 (Python, standard library):
python3 -I verify-it-yourself/count_stable.py --prefs object/instance_n17.txt --expect 206728

# Method 2 (C):
cc -O3 -o verify-it-yourself/smcount3 verify-it-yourself/smcount3.c -lm
./verify-it-yourself/smcount3 count object/instance_n17.txt 1
```

The object: `object/instance_n17.txt` (34 lines: 17 men's lists followed by 17 women's lists, 1-based permutations of 1..17), sha256 `a4ee5bb91e8b1422d460df2330349a9e04140ebb017714b2bbb25398f60bd1c0`.

How to rebuild the object: see `how-we-built-it/` (seeded local search using `smcount3.c` initialized from Thurber's G17 matrix).
