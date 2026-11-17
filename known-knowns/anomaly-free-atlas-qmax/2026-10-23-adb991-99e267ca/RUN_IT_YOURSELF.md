# Run it yourself

All commands run in a fresh shell from this package folder. You need a C compiler (gcc; OpenMP is not needed for
this package), Python 3 (standard library only), `sha256sum` (or `shasum`) and the usual POSIX tools (`tee`,
`mkfifo`, `wc`, `awk`, `sed`, `xargs`, `gzip`). About 3 GB of free memory; nothing large is written to disk.

## 1. The check

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (exit status 0). The real output, with timings, is in `verify-it-yourself/RECEIPTS.md`.
The lines that carry the result:

```
step 1 counts file: 2 rows, count = lines + 1 in every row: ok
  stored list object/SM_q11.txt.gz (SM Q_max 11): matches object/counts.txt
step 4 calibration SM: Q_max 1..10 = 8 22 82 251 626 1983 3902 7068 14354 23800 = published values: ok
  recount SM Q_max 11: 37006 = object/counts.txt count: ok
step 4 calibration SMnuR: Q_max 1..10 = 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 = published values: ok
  recount SMnuR Q_max 11: 45378378 = object/counts.txt count: ok
  SM Q_max 11 by acclist: matches object/counts.txt
  SMnuR Q_max 11 by acclist: matches object/counts.txt
PASS
```

Options: `THREADS`, `JOBS` (parallel counter processes, default 3), `PYMAX` (the Python checker also reads every
list of at most this many lines; `PYMAX=50000000` makes it read the SMnuR list too, about 15 minutes more),
`--rows SM:11` (one row). `sh verify-it-yourself/run_checks.sh --help` prints the header.

## 2. What it does

1. `verify-it-yourself/rows.py` reads `object/counts.txt`: exactly the rows SM 11 and SMnuR 11, count = lines + 1,
   valid sha256 values, and the stored list it names exists.
2. Compiles `how-we-built-it/source/acclist.c`, `how-we-built-it/source/count.c` and the streaming C checker
   `verify-it-yourself/checklist.c`, and prints the sha256 of every source it uses.
3. Decompresses `object/SM_q11.txt.gz` once and feeds the same bytes to `sha256sum`, `wc -l`, the C checker and the
   Python checker `verify-it-yourself/check_list.py` (both written from the definition: 15 or 18 integers per line,
   all six anomaly conditions, |F| <= Q_max, nonzero, each species sorted, the larger of F and -F, gcd 1, lines
   strictly increasing, so no duplicates).
4. Recounts without listing: `count` for every Q_max up to 11, then `conventions.py`; checks the twenty published
   Solutions values (Q_max 1..10, both contents) and then the claimed counts.
5. Regenerates both lists with `acclist` and streams each into `sha256sum`, `wc -l` and the C checker (and the
   Python checker for the SM list) at once. Line count and sha256 must equal `object/counts.txt`; the checker must
   pass with exactly that many valid lines. A list of distinct valid classes whose size equals the independent count
   is the complete list.

## 3. Rebuilding the object

`object/counts.txt` is the record of these runs; the lists are rebuilt with

```sh
gcc -O2 -o acclist how-we-built-it/source/acclist.c
./acclist 11 0 | gzip -1 > SM_q11.txt.gz      # gzip -dc SM_q11.txt.gz | sha256sum -> 723e21fb...0667d68
./acclist 11 1 | sha256sum                     # f4e16ec8613a78ef6437fde6c43e56320fbb6bc901fa072c0889667d96dbdaf4
```

The `.gz` bytes depend on the gzip build; compare the uncompressed stream. More commands from the run:
`how-we-built-it/COMMANDS.md`.
