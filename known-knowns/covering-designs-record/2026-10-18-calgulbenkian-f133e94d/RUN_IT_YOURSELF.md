# Run it yourself

## 1. Check the shipped design

From a fresh shell in this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Needs python3 3.8 or later, standard library only. Rough laptop time: about a second. The last line is `ALL CHECKS PASS`. The checkers alone:

```sh
python3 verify-it-yourself/check_covering.py object/C_57_14_3_b108.json
python3 verify-it-yourself/schonheim.py object/C_57_14_3_b108.json
```

Expected: a line starting `C(57,14,3) b=108 blocks_ok=True covered=29260/29260 PASS` and the line `Schonheim L(57,14,3) = 90; blocks b = 108; b >= L: True; parameters within v<=99,k<=25,t<=8: True`. The first asserts that each of the 108 blocks has exactly 14 distinct points in 1..57 and enumerates all 29260 3-subsets to confirm each lies in some block. The run script also removes one block and requires the checker to fail.

## 2. Rebuild the design

See `how-we-built-it/README.md`. The program and its start file are included, but the iteration count and thread count of the original run are not recorded, so a rerun may not reach 108 blocks.
