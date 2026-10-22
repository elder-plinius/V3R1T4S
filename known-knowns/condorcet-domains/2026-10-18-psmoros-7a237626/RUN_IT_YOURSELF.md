# Run it yourself (fresh shell, from this package folder)

```sh
sh verify-it-yourself/run_checks.sh            # last line: PASS (RECEIPTS.md holds a real run)
```

By hand: `cat object/n18_orders.txt.xz > list.xz; xz -dc list.xz | shasum -a 256` gives a5cdc42ee46244c890c092806e91a6b59bd5220679e5a5a2da19ba8691d414b5; `cc -O2 -o check verify-it-yourself/check_condorcet.c; xz -dc list.xz | ./check 18 675512 object/n18_assignment.txt` ends with PASS; `python3 verify-it-yourself/dpcount.py 18 object/n18_assignment.txt 675512 649080` ends with PASS.

Rebuilding the object: how-we-built-it/BUILD.md (time-limited searches; a rerun may end elsewhere). Rebuilding the
list from the assignment is exact: `cc -O3 -o mdom verify-it-yourself/mdom.c && ./mdom enum 18 object/n18_assignment.txt`
prints D(A) in numeric-lexicographic order (sha256 a5cdc42ee46244c890c092806e91a6b59bd5220679e5a5a2da19ba8691d414b5, the same text as the decompressed list).
