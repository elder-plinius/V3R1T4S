# Run it yourself

All commands run in a fresh shell from this package folder. You need a C compiler with OpenMP (gcc), Python 3
(standard library only), `sha256sum` (or `shasum`) and the usual POSIX tools (`tee`, `mkfifo`, `wc`, `awk`, `sed`,
`xargs`, `gzip`). About 3 GB of free memory for the default subset; nothing large is written to disk.

## 1. The check

```sh
sh verify-it-yourself/run_checks.sh            # default subset: SMnuR 12, 13 and SM 12..20 (11 of 25 rows)
sh verify-it-yourself/run_checks.sh --all      # all 25 rows: adds SMnuR 14..16 and SM 21..31
sh verify-it-yourself/run_checks.sh --rows "SMnuR:16 SM:31"   # chosen rows
```

Expected last line: `PASS` (exit status 0). The real output of the default subset, with timings, is in
`verify-it-yourself/RECEIPTS.md`. `--all` was not run for this package; from the run's own timings it takes roughly
2 to 3 hours on 3 cores (SMnuR 16 alone streamed in 1020 s, SM 21..31 took about 21 minutes in total, and the counter
at SM Q_max 27..31 took several minutes per bound) and about 3 GB of memory. Each row ends with a line
`SMnuR Q_max 13 by csenum: matches object/counts.txt`; the run ends with `rows checked: 11 of 25 (default)`
(or `25 of 25 (all)`) and `PASS`.

Options: `THREADS` (lister threads, default 3), `JOBS` (parallel counter processes, default 3), `PYMAX` (the Python
checker also reads every list of at most this many lines, default 2000000), `--both` (also run the second lister
where `object/counts.txt` records two, for example `--rows SMnuR:12 --both`).

## 2. What it does

1. `verify-it-yourself/rows.py` reads `object/counts.txt`: exactly the 25 claimed rows, count = lines + 1, valid
   sha256 values, at least one lister recorded per row, and the recorded independent count equal to the count.
2. Compiles `how-we-built-it/source/acclist.c`, `csenum.c` (OpenMP), `count.c` and the streaming C checker
   `verify-it-yourself/checklist.c`, and prints the sha256 of every source it uses.
3. Recounts without listing: `count` for every Q_max up to the largest selected row, then `conventions.py`; checks
   the twenty published Solutions values (Q_max 1..10, both contents) and then each selected row's count.
4. Regenerates each selected row's list (SM rows with `acclist`, SMnuR rows with `csenum`, as recorded in
   `object/counts.txt`) and streams the same bytes into `sha256sum`, `wc -l` and the C checker, and into the Python
   checker `verify-it-yourself/check_list.py` for lists of up to `PYMAX` lines. Both checkers were written from the
   definition: 15 or 18 integers per line, all six anomaly conditions, |F| <= Q_max, nonzero, each species sorted,
   the larger of F and -F, gcd 1, lines strictly increasing (so no duplicates). Line count and sha256 must equal
   `object/counts.txt` and the checker must pass with exactly that many valid lines. A list of distinct valid
   classes whose size equals the independent count is the complete list.

## 3. Rebuilding the object

`object/counts.txt` is the record of these runs. Any row's list is rebuilt with, for example,

```sh
gcc -O2 -o acclist how-we-built-it/source/acclist.c
gcc -O2 -fopenmp -o csenum how-we-built-it/source/csenum.c
./acclist 31 0 | sha256sum          # ace3ca282d91c147d56d61370c945daee94d7c5982222052606578aa69bf134e (SM 31)
./csenum 16 1 26 3 | sha256sum      # 15bc1ed7dada71acf9bba04cc85734710259f75d9e4f1b9a94c6745f74d632d2 (SMnuR 16)
```

More commands from the run: `how-we-built-it/COMMANDS.md`.
