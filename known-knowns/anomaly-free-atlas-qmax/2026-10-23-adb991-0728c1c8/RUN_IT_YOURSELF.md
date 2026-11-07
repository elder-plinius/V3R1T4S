# Run it yourself

All commands run in a fresh shell from this package folder. You need a C compiler with OpenMP (gcc), Python 3
(standard library only), `sha256sum` (or `shasum`) and the usual POSIX tools (`tee`, `mkfifo`, `wc`, `awk`, `sed`,
`xargs`, `gzip`). About 4.5 GB of free memory; nothing large is written to disk (the two lists, roughly 100 GB and
160 GB as text, are streamed once each).

## 1. The check

```sh
sh verify-it-yourself/run_checks.sh                    # both rows (the default: no row is small)
sh verify-it-yourself/run_checks.sh --rows SMnuR:17    # one row
```

Expected last line: `PASS` (exit status 0). The real output, with timings, is in `verify-it-yourself/RECEIPTS.md`
(a 4-core machine pinned to 3 cores). The lines that carry the result:

```
step 4 calibration SMnuR: Q_max 1..10 = 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 = published values: ok
  recount SMnuR Q_max 17: 1643386480 = object/counts.txt count: ok
  recount SMnuR Q_max 18: 2720672222 = object/counts.txt count: ok
  SMnuR Q_max 17 by csenum2: matches object/counts.txt
  SMnuR Q_max 18 by csenum2: matches object/counts.txt
PASS
```

Options: `THREADS` (lister threads, default 3), `JOBS` (parallel counter processes, default 3; the counter at
Q_max 17 and 18 takes about 25 minutes per bound on one core, so three jobs finish the recount in about the time of
the slowest bound).

## 2. What it does

1. `verify-it-yourself/rows.py` reads `object/counts.txt`: exactly the rows SMnuR 17 and 18, count = lines + 1, valid
   sha256 values, checker column `checklist:PASS`, and the count recorded for the independent counters equal to the
   count.
2. Compiles `how-we-built-it/source/csenum2.c` (OpenMP), `count.c` and the streaming C checker
   `verify-it-yourself/checklist.c`, and prints the sha256 of every source it uses.
3. Recounts without listing: `count` for every Q_max up to 18, then `conventions.py`; checks the twenty published
   Solutions values (Q_max 1..10, both contents) and then the two claimed counts.
4. Regenerates each list with `csenum2` (16 passes at Q_max 17, 25 at 18, as in the run) and streams the same bytes
   into `sha256sum`, `wc -l` and the C checker, written from the definition (18 integers per line, all six anomaly
   conditions, |F| <= Q_max, nonzero, each species sorted, the larger of F and -F, gcd 1, lines strictly increasing,
   so no duplicates). The lister's exit status must be 0, the line count and sha256 must equal `object/counts.txt`,
   and the checker must pass with exactly that many valid lines. A list of distinct valid classes whose size equals
   the independent count is the complete list. The Python checker `verify-it-yourself/check_list.py` applies the
   same rules; it is too slow for these lists (set `PYMAX=3000000000` to run it anyway, many hours).

## 3. Rebuilding the object

```sh
gcc -O2 -fopenmp -o csenum2 how-we-built-it/source/csenum2.c
./csenum2 17 1 16 3 | sha256sum    # 385eb5abe1adb8107c6d678374555095202c3c7fcae17316f8334730d5e61023
./csenum2 18 1 25 3 | sha256sum    # ba766218c78ca20f29c48f2bb677bca4a31235f398638ba317315b7bf8994d3c
```

The output bytes do not depend on the number of passes or threads (the panel regenerated Q_max 17 with 20 passes:
same hash). More commands from the run: `how-we-built-it/COMMANDS.md`.
