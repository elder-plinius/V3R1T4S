# Run it yourself (fresh shell, from this package folder)

```sh
sh verify-it-yourself/run_checks.sh            # last line: PASS (RECEIPTS.md holds a real run)
```

By hand: `cat object/n19_orders.txt.xz > list.xz; xz -dc list.xz | shasum -a 256` gives c8a2048ff9b15a23f27a4d2213f4ecba2f65e59f76f0c766f1cc6dbf5e8d733d; `cc -O2 -o check verify-it-yourself/check_condorcet.c; xz -dc list.xz | ./check 19 1497276 object/n19_assignment.txt` ends with PASS; `python3 verify-it-yourself/dpcount.py 19 object/n19_assignment.txt 1497276 1432837` ends with PASS.

Rebuilding the object: how-we-built-it/BUILD.md (time-limited searches; a rerun may end elsewhere). Rebuilding the
list from the assignment is exact: `cc -O3 -o mdom verify-it-yourself/mdom.c && ./mdom enum 19 object/n19_assignment.txt`
prints D(A) in numeric-lexicographic order (sha256 c8a2048ff9b15a23f27a4d2213f4ecba2f65e59f76f0c766f1cc6dbf5e8d733d, the same text as the decompressed list).
