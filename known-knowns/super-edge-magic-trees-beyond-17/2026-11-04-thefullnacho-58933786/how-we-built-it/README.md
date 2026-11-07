# How the certificates were built

Orders 18 to 20 are the certificates of the p1 package (pull request #917, Zenodo 10.5281/zenodo.23918679); see that
package's how-we-built-it/. This folder covers orders 21 and 22, built in run 2026-11-03-2244. `PREREG.md` is that
run's pre-registration, copied as written (2026-11-03T22:44:50Z, before any attack output of the run).

## Null test: waived, and why

`PREREG.md` says `null_test: not needed because each claim is an explicit object (a labeling per tree) checked by a
deterministic checker against the definition, with coverage checked against A000055.` Each labeling satisfies the
definition or not, and coverage is a count compared with OEIS A000055, so a shuffled-input control has nothing to
beat. In its place the independent checker was calibrated on known positives and injected negatives (Otter counts,
exhaustive Pruefer enumeration at n = 7, 8, and seven injected defect classes, all rejected) and replayed on the known
orders 18 to 20 before it was used on 21 and 22.

## Machine and limits

One Linux desktop (32 threads, 30 GB, Ubuntu 24.04), a dedicated user, at most 16 worker processes, each under
`nice -n 19 ionice -c3` and `ulimit -v 500000` (500 MB virtual). Trees from nauty 2.8.9 `gentreeg`.

## Requirements and build

- nauty 2.8.9 for `gentreeg` (https://pallini.di.uniroma1.it); a C compiler: `cc -O2 -o alpha_sem alpha_sem.c` and
  `cc -O2 -o sem_direct sem_direct.c` (the run's exact compile line was not logged); python3 (standard library) for
  `caterpillar_sem.py` and `assemble_chunk.py`, and `check_sem.py` from `../verify-it-yourself/`.
- Layout: a folder `$V3_HOME` with `bin/` holding gentreeg, the two binaries, the scripts here, `check_sem.py`,
  `verify_sem_coverage.py`, `verify_cert.py` and the OEIS b-file `b000055.txt`, and a Python at `$V3_HOME/venv/bin/python`.
  The only change from the files that ran is that the worker's home folder, hard-coded as `H=` in `run.sh` and
  `chunk.sh`, is now taken from `$V3_HOME`.

## Steps

    V3_HOME=/path/to/worker nohup setsid nice -n 19 ionice -c3 $V3_HOME/bin/run.sh 21 1024 16 > n21.log 2>&1 &
    V3_HOME=/path/to/worker nohup setsid nice -n 19 ionice -c3 $V3_HOME/bin/run.sh 22 2048 16 > n22.log 2>&1 &

`run.sh n M P` runs chunks 0..M-1 with P parallel workers through `chunk.sh n i M`, which pipes `gentreeg -q -p n i/M`
through `p2e.awk` (parent arrays to edge lists) and then: `alpha_sem 300 200` (node cap, attempts); `sem_direct 300
100000` on trees without an alpha-labeling; `caterpillar_sem.py` on what is left; `sem_direct 2000 10000000` under
`timeout 900` on any remainder. `assemble_chunk.py` keeps, per tree, the first labeling that passes
`check_sem.check` and writes anything unlabelled to a residue file. When every chunk is done, `run.sh` concatenates
the chunks, runs `verify_sem_coverage.py`, and compresses and hashes the certificate.

Recorded runs: n = 21 started 17:47:29 EST, all 1024 chunks done 18:23:17, coverage PASS, residue 0. n = 22 started
18:49:24 EST and was relaunched at 19:41:02 with the same n and M (done chunks skipped); all 2048 chunks done
21:19:53, coverage PASS, residue 0. At n = 21 the alpha stage labelled about 27% of trees and sem_direct most of the
rest.

The searches are randomised; rerunning gives different, equally valid labelings. Rebuilding is not needed to check
the claim: the certificates are checked directly.
