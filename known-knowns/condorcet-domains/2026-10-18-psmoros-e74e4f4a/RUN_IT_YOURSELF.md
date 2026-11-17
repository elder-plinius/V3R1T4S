# Run it yourself (fresh shell, from this package folder)

```sh
sh verify-it-yourself/run_checks.sh            # last line: PASS (RECEIPTS.md holds a real run)
FULL=1 sh verify-it-yourself/run_checks.sh   # also enumerates all of D(A) and checks every order
```

By hand: `python3 verify-it-yourself/dpcount.py 25 object/n25_assignment.txt 178950728 160316047` ends with PASS (|D(A)| = 178950728).

Rebuilding the object: how-we-built-it/BUILD.md (time-limited searches; a rerun may end elsewhere). Rebuilding the
list from the assignment is exact: `cc -O3 -o mdom verify-it-yourself/mdom.c && ./mdom enum 25 object/n25_assignment.txt`
prints D(A) in numeric-lexicographic order (sha256 2ac0df90378e94892f7af7dc8df27581428be20fb21e90edfc751fee5246bd38).
