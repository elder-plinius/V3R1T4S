# Run it yourself (fresh shell, from this package folder)

```sh
sh verify-it-yourself/run_checks.sh            # last line: PASS (RECEIPTS.md holds a real run)
```

By hand: `cat object/n16_orders.txt.xz > list.xz; xz -dc list.xz | shasum -a 256` gives b71a77f8646e026818398933e44c2a88d901298041bb2097d0f59560a5cb9c2e; `cc -O2 -o check verify-it-yourself/check_condorcet.c; xz -dc list.xz | ./check 16 135072 object/n16_assignment.txt` ends with PASS; `python3 verify-it-yourself/dpcount.py 16 object/n16_assignment.txt 135072 131537` ends with PASS.

Rebuilding the object: how-we-built-it/BUILD.md (time-limited searches; a rerun may end elsewhere). Rebuilding the
list from the assignment is exact: `cc -O3 -o mdom verify-it-yourself/mdom.c && ./mdom enum 16 object/n16_assignment.txt`
prints D(A) in numeric-lexicographic order (sha256 b71a77f8646e026818398933e44c2a88d901298041bb2097d0f59560a5cb9c2e, the same text as the decompressed list).
