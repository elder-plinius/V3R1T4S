# Run it yourself

From this folder, in a fresh shell (Python 3 standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (the exhaustive pass takes a few minutes with 4 processes):

```
object consistent: A389690(23) = 3570, 4194304 sets, 673 distinct periods, maximising set(s) recomputed
exhaustive pass over all 4194304 sets (4 processes): histogram identical, maximum 3570
PASS
```

`python3 verify-it-yourself/check_term.py object/A389690_23.txt --quick` checks only the object's consistency and the
maximising set (under a second). To recompute the maximiser with the OEIS entry's own program, download it from
https://oeis.org/A389690/a389690_2.txt, delete its last lines (the demo loop after "# If you want to do the first few terms") and call its
sg_eventual_period(set(S), 23) with S = {2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23}: the period is 3570.

To rebuild the object with the fast programs, see how-we-built-it/BUILD.md.
