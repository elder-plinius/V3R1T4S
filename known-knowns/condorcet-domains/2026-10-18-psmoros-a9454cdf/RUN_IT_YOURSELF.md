# Run it yourself (fresh shell, from this package folder)

```sh
sh verify-it-yourself/run_checks.sh            # last line: PASS (RECEIPTS.md holds a real run)
```

By hand: `cat object/n14_orders.txt.xz > list.xz; xz -dc list.xz | shasum -a 256` gives 5df126f0743049408d8e6fcc913afec170efa69998a89e75831908b4e8b5eff3; `cc -O2 -o check verify-it-yourself/check_condorcet.c; xz -dc list.xz | ./check 14 27040 object/n14_assignment.txt` ends with PASS; `python3 verify-it-yourself/dpcount.py 14 object/n14_assignment.txt 27040 27027` ends with PASS.

Rebuilding the object: how-we-built-it/BUILD.md (time-limited searches; a rerun may end elsewhere). Rebuilding the
list from the assignment is exact: `cc -O3 -o mdom verify-it-yourself/mdom.c && ./mdom enum 14 object/n14_assignment.txt`
prints D(A) in numeric-lexicographic order (sha256 5df126f0743049408d8e6fcc913afec170efa69998a89e75831908b4e8b5eff3, the same text as the decompressed list).
