# Run it yourself

From this folder:

```
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Under a second. Exit status 0. Python 3, standard library only.

The command reads `object/rulers.json` and checks both witnesses directly: sorted distinct marks, 0 at the left end, the claimed diameter at the right end, and at most five copies of each positive difference.

To repeat the minimality search, compile the C files in `how-we-built-it/` and run the diameter loop described in `panel/reproduce.md`. That is the historical run, not this command. a(20) is about 45 minutes on one core. a(21), diameter 61, is about 3.5 hours on two cores.
