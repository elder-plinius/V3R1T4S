# How the certificates were built

Orders 18 to 20: the p1 package (pull request #917, runs 2026-11-03-0818). Orders 21 and 22: the p2 package (#945,
run 2026-11-03-2244). Orders 23 to 25: run 2026-11-04-1135, described here. The search code is byte-identical across
all eight orders (sem_direct.c, alpha_sem.c; caterpillar_sem.py differs only in its import-path line). `PREREG.md` is
the run's pre-registration as written, with its two dated addenda; each addendum was written before the output it
governs existed.

## Null test: waived, and why
`null_test: not needed because each claim is an explicit object (a labeling per tree) checked by deterministic
checkers against the definition, with coverage checked against A000055.` In its place the independent checker was
calibrated on known positives and injected negatives in run 2026-11-03-2244 (13/13) and replayed on the known orders.

## Machine and limits
The contributor's desktop (32 threads, 30 GB, Ubuntu 24.04), at most 16 (n = 23) and 28 (n = 24, 25) worker processes,
each under `nice -n 19 ionice -c3` and `ulimit -v 500000`. Trees from nauty 2.8.9 `gentreeg` in res/mod chunks.

## Build and run
- nauty 2.8.9 for `gentreeg`; `cc -O2 -o alpha_sem alpha_sem.c` and `cc -O2 -o sem_direct sem_direct.c`; python3.
- A folder `$V3_HOME` with `bin/` (gentreeg, the two binaries, the scripts in `code/`, `check_sem.py`,
  `verify_sem_coverage.py`, `verify_cert.py`, the OEIS b-file `b000055.txt`) and `runs/`.

      V3_HOME=/path DEEP_SEC=900  bin/run.sh 23 4096 16     # then the residue retry, PREREG addendum 1
      V3_HOME=/path INDEP_CHECK=verify-it-yourself/indep_check.py P=28 bin/drive_one.sh 24 8192
      V3_HOME=/path INDEP_CHECK=verify-it-yourself/indep_check.py P=28 bin/drive_one.sh 25 16384            # stopped after search; bin/finish25.sh per addendum 2

`chunk.sh n i M`: `gentreeg -q -p n i/M | awk -f p2e.awk`, then `alpha_sem 300 200`, `sem_direct 300 100000` on trees
without an alpha-labeling, `caterpillar_sem.py`, and `sem_direct 2000 10000000` under the deep-stage timeout (900 s at
n = 23, 3600 s at 24 and 25). `assemble_chunk.py` keeps per tree the first labeling that passes `check_sem.check` and
writes the rest to a residue file. `drive_one.sh` runs an order, retries the residue (sem_direct 2000, up to 10^9
attempts, 16 parts, 3 h each), merges and runs both checkers; `finish25.sh` adds the n = 25 second pass (28 parts,
12 h each) on residue the first retry did not reach, found by set difference.

| n | search | residue | retry | both checkers on merged file |
|---|---|---|---|---|
| 23 | 8 h 38 min, 16 workers | 301 | all labelled | PASS |
| 24 | 23 h, 28 workers | 1,012 | all labelled | PASS |
| 25 | 3 d 13 h, 28 workers | 23,458 | 21,987 in step 1, 1,471 in pass 2 | PASS (11.4 GB per checker) |

`leftovers/leftover_trees_n2X.txt.xz`: the residue trees, one `n;edges` line each. Their labelings are in the
certificates. The searches are randomised; a rebuild gives different, equally valid labelings.
