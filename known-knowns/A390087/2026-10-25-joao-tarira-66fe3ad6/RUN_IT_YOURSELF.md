# Run it yourself

From this folder:

```
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. A few seconds. Exit status 0. Python 3, standard library only.

The command checks `object/terms.json`: both witnesses are irreducible odd zero-sum sets of the claimed lengths and largest absolute values, and the A390085 row from index 31 through 48 is the attested row (eight 7s, nine 8s, then 9).

It does not re-run the exhaustive search. To do that, compile `how-we-built-it/vf2.c` or `how-we-built-it/verify_fixed.cpp` and repeat the magnitude and length ranges named in `panel/reproduce.md`. That is the historical run, on the order of an hour for the longest lengths, not the one-command check.
