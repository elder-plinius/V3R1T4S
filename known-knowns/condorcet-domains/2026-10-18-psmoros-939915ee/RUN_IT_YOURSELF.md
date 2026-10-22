# Run it yourself (fresh shell, from this package folder)

```sh
sh verify-it-yourself/run_checks.sh            # last line: PASS (RECEIPTS.md holds a real run)
```

By hand: `cat object/n15_orders.txt.xz > list.xz; xz -dc list.xz | shasum -a 256` gives 09b0d90e0dbe76a2ad49987339375ff93f18c78ecee325bd75f80356ee5f39b9; `cc -O2 -o check verify-it-yourself/check_condorcet.c; xz -dc list.xz | ./check 15 60956 object/n15_assignment.txt` ends with PASS; `python3 verify-it-yourself/dpcount.py 15 object/n15_assignment.txt 60956 59431` ends with PASS.

Rebuilding the object: how-we-built-it/BUILD.md (time-limited searches; a rerun may end elsewhere). Rebuilding the
list from the assignment is exact: `cc -O3 -o mdom verify-it-yourself/mdom.c && ./mdom enum 15 object/n15_assignment.txt`
prints D(A) in numeric-lexicographic order (sha256 09b0d90e0dbe76a2ad49987339375ff93f18c78ecee325bd75f80356ee5f39b9, the same text as the decompressed list).
