# Run it yourself

All commands run in a fresh shell from this package folder. You need a C compiler (gcc; OpenMP for the SMnuR 20
lister), Python 3 (standard library only), `sha256sum` (or `shasum`) and the usual POSIX tools (`tee`, `mkfifo`,
`wc`, `awk`, `sed`, `xargs`, `gzip`). Nothing large is written to disk: every list is streamed once.

## 1. The check

```sh
sh verify-it-yourself/run_checks.sh                     # default: SM 36 (well under 1 GB of memory)
sh verify-it-yourself/run_checks.sh --rows "SM:37 SM:38"
sh verify-it-yourself/run_checks.sh --rows SMnuR:20     # about 2 hours on 3 threads, about 4.7 GB of memory
sh verify-it-yourself/run_checks.sh --all               # all four rows
```

Expected last line: `PASS` (exit status 0). The real output, with timings, is in `verify-it-yourself/RECEIPTS.md`
(a 4-core machine; the run was pinned to one core). The lines that carry the result in the default run:

```
step 4 calibration SM: Q_max 1..10 = 8 22 82 251 626 1983 3902 7068 14354 23800 = published values: ok
step 4 calibration SMnuR: Q_max 1..10 = 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 = published values: ok
  recount SM Q_max 36: 32457211 = object/counts.txt count: ok
  SM Q_max 36 by acclist: matches object/counts.txt
PASS
```

Options (environment): `PAR` (single-threaded acclist streams run at the same time, default 2), `THREADS` (csenum2
threads, default 3), `JOBS` (parallel counter processes, default 3), `KEEP=1` (keep the scratch folder).

## 2. What it does

1. `verify-it-yourself/rows.py` reads `object/counts.txt`: exactly the rows SMnuR 20 and SM 36..38, count = lines + 1,
   valid sha256 values, a `checklist:PASS` field, and the count recorded for `mitm.c` equal to the count. A single changed digit of a count, a line count or a recorded counter value fails here.
2. Compiles `how-we-built-it/source/mitm.c`, the listers named in `object/counts.txt` (`acclist.c`, and
   `csenum2.c` with OpenMP) and the streaming C checker `verify-it-yourself/checklist.c`, and prints the sha256 of
   every source it uses.
3. Recounts without listing: `mitm` (meet in the middle on the split (Q, L, nu) | (u, d, e), Moebius inversion over
   common factors, Burnside over the overall sign) for Q_max 1..10 of both contents, compared with the twenty
   published Solutions values, and then for each selected row, compared with `object/counts.txt`.
4. Regenerates each selected list (`acclist QMAX 0` for the SM, `csenum2 20 1 80 3` for SMnuR 20) and streams the
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
./acclist 36 0 | sha256sum       # 7fd525fd695292d2991dbc051bf7ddf10a35b91d3e85a7a22a165e9183e52b4f
./acclist 37 0 | sha256sum       # 06de08d7c30a9ffd285529c826037f9cd90a1afb1932c243e2a82a3ba26ae5bc
./acclist 38 0 | sha256sum       # bf99b850233b5ef48594174f48779bbe1b3bded3efaf7e854153a62ab7632393
./csenum2 20 1 80 3 | sha256sum  # 4919f760902d647f6406a801bf463a9fdafdbf8189f549093f00826ed3a327cf
./mitm SMnuR 20 | grep RESULT    # RESULT SMnuR Qmax 20: inequivalent = 6465226975
for q in 36 37 38; do ./mitm SM $q | grep RESULT; done
```

Each line of `object/counts.txt` is `content Q_max count lines sha256 lister checklist:PASS mitm.c:count` (the SMnuR row
names the lister as `csenum2(NPASS 80)`; the SM 36 row adds a count.c value from an earlier run, not receipted here).
The run used 80 passes and 3 threads for `csenum2` at Q_max 20 (`object/receipts/SMnuR20.enum.log`; peak resident
memory 4.66 GB, `object/receipts/SMnuR20.rss.txt`). With 40 passes the lister needs more than 7 GB. More commands from the run:
`how-we-built-it/COMMANDS.md`.
