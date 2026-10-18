# Run it yourself (fresh shell, from this package folder)

```sh
sh verify-it-yourself/run_checks.sh            # last line: PASS (RECEIPTS.md holds a real run)
```

By hand: `cat object/n17_orders.txt.xz > list.xz; xz -dc list.xz | shasum -a 256` gives c281d6301f9db7d703141016322ca314a5118636b62bd4d9efed49c0b0c21470; `cc -O2 -o check verify-it-yourself/check_condorcet.c; xz -dc list.xz | ./check 17 300388 object/n17_assignment.txt` ends with PASS; `python3 verify-it-yourself/dpcount.py 17 object/n17_assignment.txt 300388 292016` ends with PASS.

Rebuilding the object: how-we-built-it/BUILD.md (time-limited searches; a rerun may end elsewhere). Rebuilding the
list from the assignment is exact: `cc -O3 -o mdom verify-it-yourself/mdom.c && ./mdom enum 17 object/n17_assignment.txt`
prints D(A) in numeric-lexicographic order (sha256 c281d6301f9db7d703141016322ca314a5118636b62bd4d9efed49c0b0c21470, the same text as the decompressed list).
