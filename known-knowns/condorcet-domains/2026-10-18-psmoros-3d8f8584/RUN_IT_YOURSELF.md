# Run it yourself (fresh shell, from this package folder)

```sh
sh verify-it-yourself/run_checks.sh            # last line: PASS (RECEIPTS.md holds a real run)
```

By hand: `cat object/n20_orders.txt.xz.part_aa object/n20_orders.txt.xz.part_ab > list.xz; xz -dc list.xz | shasum -a 256` gives fcd38f16f2a6c954eb2adfe79f5e9b9420180dfa6ec306bf5388dff9b9023930; `cc -O2 -o check verify-it-yourself/check_condorcet.c; xz -dc list.xz | ./check 20 3336208 object/n20_assignment.txt` ends with PASS; `python3 verify-it-yourself/dpcount.py 20 object/n20_assignment.txt 3336208 3155367` ends with PASS.

Rebuilding the object: how-we-built-it/BUILD.md (time-limited searches; a rerun may end elsewhere). Rebuilding the
list from the assignment is exact: `cc -O3 -o mdom verify-it-yourself/mdom.c && ./mdom enum 20 object/n20_assignment.txt`
prints D(A) in numeric-lexicographic order (sha256 fcd38f16f2a6c954eb2adfe79f5e9b9420180dfa6ec306bf5388dff9b9023930, the same text as the decompressed list).
