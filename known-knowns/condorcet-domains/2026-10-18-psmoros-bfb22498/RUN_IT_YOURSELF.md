# Run it yourself (fresh shell, from this package folder)

```sh
sh verify-it-yourself/run_checks.sh            # last line: PASS (RECEIPTS.md holds a real run)
FULL=1 sh verify-it-yourself/run_checks.sh   # also enumerates all of D(A) and checks every order
```

By hand: `python3 verify-it-yourself/dpcount.py 24 object/n24_assignment.txt 81912986 73279873` ends with PASS (|D(A)| = 81912986).

Rebuilding the object: how-we-built-it/BUILD.md (time-limited searches; a rerun may end elsewhere). Rebuilding the
list from the assignment is exact: `cc -O3 -o mdom verify-it-yourself/mdom.c && ./mdom enum 24 object/n24_assignment.txt`
prints D(A) in numeric-lexicographic order (sha256 54baf18b85aecce8a420ce8c1b7350f86b3bf27590741ba9b23193ca0e4a0605).
