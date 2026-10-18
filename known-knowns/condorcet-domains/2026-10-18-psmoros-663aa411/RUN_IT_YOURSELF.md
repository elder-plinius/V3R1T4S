# Run it yourself (fresh shell, from this package folder)

```sh
sh verify-it-yourself/run_checks.sh            # last line: PASS (RECEIPTS.md holds a real run)
FULL=1 sh verify-it-yourself/run_checks.sh   # also enumerates all of D(A) and checks every order
```

By hand: `python3 verify-it-yourself/dpcount.py 23 object/n23_assignment.txt 36894088 33162137` ends with PASS (|D(A)| = 36894088).

Rebuilding the object: how-we-built-it/BUILD.md (time-limited searches; a rerun may end elsewhere). Rebuilding the
list from the assignment is exact: `cc -O3 -o mdom verify-it-yourself/mdom.c && ./mdom enum 23 object/n23_assignment.txt`
prints D(A) in numeric-lexicographic order (sha256 7a5a7d8ca65a2668c6f8c4bba680f6275019f94d5189a0728febeecd3da633ff).
