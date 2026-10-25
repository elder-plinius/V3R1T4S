# Run it yourself (fresh shell, from this package folder)

```sh
sh verify-it-yourself/run_checks.sh            # last line: PASS (RECEIPTS.md holds a real run)
```

By hand: `cat object/n22_orders.txt.xz.part_aa object/n22_orders.txt.xz.part_ab object/n22_orders.txt.xz.part_ac object/n22_orders.txt.xz.part_ad object/n22_orders.txt.xz.part_ae object/n22_orders.txt.xz.part_af > list.xz; xz -dc list.xz | shasum -a 256` gives 19175ef6e0109ea0642f2c8dbad1ba4f2bdeb483905cc6853f460f1bcd75e123; `cc -O2 -o check verify-it-yourself/check_condorcet.c; xz -dc list.xz | ./check 22 16571072 object/n22_assignment.txt` ends with PASS; `python3 verify-it-yourself/dpcount.py 22 object/n22_assignment.txt 16571072 15037179` ends with PASS.

Rebuilding the object: how-we-built-it/BUILD.md (time-limited searches; a rerun may end elsewhere). Rebuilding the
list from the assignment is exact: `cc -O3 -o mdom verify-it-yourself/mdom.c && ./mdom enum 22 object/n22_assignment.txt`
prints D(A) in numeric-lexicographic order (sha256 19175ef6e0109ea0642f2c8dbad1ba4f2bdeb483905cc6853f460f1bcd75e123, the same text as the decompressed list).
