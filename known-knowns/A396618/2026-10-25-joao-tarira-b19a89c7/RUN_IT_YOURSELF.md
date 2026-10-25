# Run it yourself

From this folder, in a new shell, with Python 3 and gcc (or another C compiler
that accepts the same flags) on the path:

```
sh verify-it-yourself/run_checks.sh
```

Expected: one OK line for each of a(2) through a(19), a line saying a(20)
through a(25) match the attested list, and the last line `PASS`. About one
minute. Exit status 0.

What that command recomputes: a(2) through a(19), by compiling
`verify-it-yourself/count.c` and counting every k with 10^(n-1) <= k^2 < 10^n.
A proper suffix of k^2 that is a square, including 0, rejects k. a(1) is the
given value 4 and is only checked for equality.

What it does not recompute: a(22) through a(25). To re-enumerate those, compile
the counters in `how-we-built-it/` and split the range into parts, as in
`how-we-built-it/COMMANDS.md`. The saved half-totals that add to the four new
terms are quoted in `panel/reproduce.md`.

Rebuilding the object: `object/terms.json` is the list. a(1) through a(21) are
the published b-file. a(22) through a(25) are the totals of the saved counts.
