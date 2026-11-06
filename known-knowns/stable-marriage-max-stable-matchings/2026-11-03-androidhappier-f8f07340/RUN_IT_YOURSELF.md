# Run it yourself

From this folder, in a fresh shell (Python 3; a C compiler is optional):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected: the last line is `PASS`, with `lattice_count: 412`, `brute_count: 412`, `expected: 412 PASS`, and, if `cc` is present, `n=9 stable_matchings=412` (allperm.c, all 9! = 362880 perfect matchings checked against the definition) and `count_poset: 412` / `count_lattice_verified: 412` (smcount3.c). It takes a few seconds.

Single commands:

```sh
python3 -I verify-it-yourself/count_stable.py --prefs object/instance_n9.txt --brute --expect 412
cc -O2 -o allperm verify-it-yourself/allperm.c && ./allperm object/instance_n9.txt
cc -O2 -o smcount3 verify-it-yourself/smcount3.c -lm && ./smcount3 count object/instance_n9.txt 1
```

The object: `object/instance_n9.txt` has one comment line, then 18 rows of 9 integers. Rows 1-9 are the lists of men 1..9 over women, and rows 10-18 are the lists of women 1..9 over men. Indices are 1-based and the most preferred comes first. sha256 f8f0734081c8c613267257d617d9393d5ad591782b802beaa72c8b1639f35de1.

How to rebuild the object: see how-we-built-it/COMMANDS.md (seed how-we-built-it/seed_ext9.prefs, search code smcount3.c).
