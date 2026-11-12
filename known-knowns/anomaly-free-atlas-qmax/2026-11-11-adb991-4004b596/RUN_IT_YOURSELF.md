# Run it yourself

All commands run in a fresh shell from this package folder. You need a C compiler (gcc), Python 3 (standard library
only), `sha256sum` (or `shasum`) and the usual POSIX tools (`tee`, `mkfifo`, `wc`, `awk`, `sed`, `xargs`, `gzip`).
Nothing large is written to disk: every list is streamed once.

## 1. The check

```sh
sh verify-it-yourself/run_checks.sh                     # default: SM 41 (well under 1 GB of memory)
sh verify-it-yourself/run_checks.sh --rows SM:42
sh verify-it-yourself/run_checks.sh --all               # both rows
```

Expected last line: `PASS` (exit status 0). The real output, with timings, is in `verify-it-yourself/RECEIPTS.md`.
The lines that carry the result in the default run:

```
step 4 calibration SM: Q_max 1..10 = 8 22 82 251 626 1983 3902 7068 14354 23800 = published values: ok
  recount SM Q_max 41: 66526761 = object/counts.txt count: ok
  SM Q_max 41 by acclist: matches object/counts.txt
PASS
```

Options (environment): `PAR` (single-threaded acclist streams run at the same time, default 2), `JOBS` (parallel
counter processes, default 3), `KEEP=1` (keep the scratch folder).

## 2. What it does

1. `verify-it-yourself/rows.py` reads `object/counts.txt`: exactly the rows SM 41 and SM 42, count = lines + 1,
   valid sha256 values, a `checklist:PASS` field, and the count recorded for `mitm.c` equal to the count. A single
   changed digit of a count, a line count or a recorded counter value fails here.
2. Compiles `how-we-built-it/source/mitm.c`, the lister `how-we-built-it/source/acclist.c` and the streaming C
   checker `verify-it-yourself/checklist.c`, and prints the sha256 of every source it uses.
3. Recounts without listing: `mitm` (meet in the middle on the split (Q, L) | (u, d, e), Moebius inversion over
   common factors, Burnside over the overall sign) for Q_max 1..10 of both contents, compared with the twenty
   published Solutions values, and then for each selected row, compared with `object/counts.txt`.
4. Regenerates each selected list (`acclist QMAX 0`) and streams the same bytes into `sha256sum`, `wc -l` and the C
   checker, written from the definition (15 integers per line, all six anomaly conditions, |F| <= Q_max, nonzero,
   each species sorted, the larger of F and -F, gcd 1, lines strictly increasing, so no duplicates). The lister's
   exit status must be 0, the line count and sha256 must equal `object/counts.txt`, and the checker must pass with
   exactly that many valid lines. A list of distinct valid classes whose size equals the independent count is the
   complete list. The Python checker `verify-it-yourself/check_list.py` applies the same rules; it is too slow for
   these lists (set `PYMAX=5000000000` to run it anyway, many hours).

## 3. Rebuilding the object

```sh
gcc -O2 -o acclist how-we-built-it/source/acclist.c
gcc -O3 -o mitm how-we-built-it/source/mitm.c
./acclist 41 0 2>/dev/null | sha256sum   # ad5133b7fcbe5ec91cc5416bda0b5a8629e0b85ba5d2d4c0aa89ef4f4282f6ec
./acclist 42 0 2>/dev/null | sha256sum   # 8d6d0fcd99099ba8b46071ba4a6e1051fa8fcb1fb165f8c55c7f150bcbed6df2
for q in 41 42; do ./mitm SM $q | grep RESULT; done   # inequivalent = 66526761, 79174540
```

Each line of `object/counts.txt` is `content Q_max count lines sha256 lister checklist:PASS mitm.c:count`. More
commands from the run: `how-we-built-it/COMMANDS.md`.
