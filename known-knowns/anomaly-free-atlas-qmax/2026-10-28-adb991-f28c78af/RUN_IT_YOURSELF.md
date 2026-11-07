# Run it yourself

All commands run in a fresh shell from this package folder. You need a C compiler (gcc; OpenMP for the SMnuR 19
lister), Python 3 (standard library only), `sha256sum` (or `shasum`) and the usual POSIX tools (`tee`, `mkfifo`,
`wc`, `awk`, `sed`, `xargs`, `gzip`). Nothing large is written to disk: every list is streamed once.

## 1. The check

```sh
sh verify-it-yourself/run_checks.sh                     # default: SM 32 and 33 (well under 1 GB of memory)
sh verify-it-yourself/run_checks.sh --rows "SM:34 SM:35"
sh verify-it-yourself/run_checks.sh --rows SMnuR:19     # about 90 minutes on 3 threads, about 4.4 GB of memory
sh verify-it-yourself/run_checks.sh --all               # all five rows
```

Expected last line: `PASS` (exit status 0). The real output, with timings, is in `verify-it-yourself/RECEIPTS.md`
(a 4-core machine pinned to 3 cores). The lines that carry the result in the default run:

```
step 4 calibration SM: Q_max 1..10 = 8 22 82 251 626 1983 3902 7068 14354 23800 = published values: ok
step 4 calibration SMnuR: Q_max 1..10 = 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 = published values: ok
  recount SM Q_max 32: 15866882 = object/counts.txt count: ok
  recount SM Q_max 33: 19550225 = object/counts.txt count: ok
  SM Q_max 32 by acclist: matches object/counts.txt
  SM Q_max 33 by acclist: matches object/counts.txt
PASS
```

Options (environment): `PAR` (single-threaded acclist streams run at the same time, default 2), `THREADS` (csenum2
threads, default 3), `JOBS` (parallel counter processes, default 3), `KEEP=1` (keep the scratch folder).

## 2. What it does

1. `verify-it-yourself/rows.py` reads `object/counts.txt`: exactly the rows SMnuR 19 and SM 32..35, count = lines + 1,
   valid sha256 values, checker column `checklist:PASS`, and the count recorded for the independent counter equal to
   the count. A single changed digit of a count, a line count or a recorded counter value fails here.
2. Compiles `how-we-built-it/source/mitm.c`, the listers named in `object/counts.txt` (`acclist.c`, and
   `csenum2.c` with OpenMP) and the streaming C checker `verify-it-yourself/checklist.c`, and prints the sha256 of
   every source it uses.
3. Recounts without listing: `mitm` (meet in the middle on the split (Q, L, nu) | (u, d, e), Moebius inversion over
   common factors, Burnside over the overall sign) for Q_max 1..10 of both contents, compared with the twenty
   published Solutions values, and then for each selected row, compared with `object/counts.txt`.
4. Regenerates each selected list (`acclist QMAX 0` for the SM, `csenum2 19 1 40 3` for SMnuR 19) and streams the
   same bytes into `sha256sum`, `wc -l` and the C checker, written from the definition (15 or 18 integers per line,
   all six anomaly conditions, |F| <= Q_max, nonzero, each species sorted, the larger of F and -F, gcd 1, lines
   strictly increasing, so no duplicates). The lister's exit status must be 0 (the same guard as `set -o
   pipefail`), the line count and sha256 must equal `object/counts.txt`, and the checker must pass with exactly that
   many valid lines. A list of distinct valid classes whose size equals the independent count is the complete
   list. The Python checker `verify-it-yourself/check_list.py` applies the same rules; it is too slow for these lists
   (set `PYMAX=5000000000` to run it anyway, many hours).

## 3. Rebuilding the object

```sh
gcc -O2 -o acclist how-we-built-it/source/acclist.c
gcc -O2 -fopenmp -o csenum2 how-we-built-it/source/csenum2.c
gcc -O3 -o mitm how-we-built-it/source/mitm.c
./acclist 32 0 | sha256sum       # 3a5d7d1695cd98e6aa70ecc3c0ff9121f9312a11f0123ec6e6cec7a8ad408a07
./acclist 33 0 | sha256sum       # fab3aded0a00e3dfeedf3c45386728a3d9bd3f6bf22f748c58c0dcea7f1ee86c
./acclist 34 0 | sha256sum       # e22875f7b3ded06eeb05e00464da98b943e60db7afac2d673357e1da1e72c74b
./acclist 35 0 | sha256sum       # f3a6b7ff8fd4abe877c3d3f867877a811a27eb0fe3317495978f6c631a02fa9f
./csenum2 19 1 40 3 | sha256sum  # 0fc9e8b841f69b7825c4de8c8ff1b987f29a2314edce997157069e0b48216f81
./mitm SMnuR 19 | grep RESULT    # RESULT SMnuR Qmax 19: inequivalent = 4247050205
for q in 32 33 34 35; do ./mitm SM $q | grep RESULT; done
```

Each line of `object/counts.txt` is then `content Q_max count lines sha256 lister checklist:PASS mitm.c:count`. The run
used 40 passes and 3 threads for `csenum2` at Q_max 19 (`object/receipts/SMnuR19.enum.log`). More commands from the run:
`how-we-built-it/COMMANDS.md`.
