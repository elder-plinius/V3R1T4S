# Run it yourself

Fresh shell, from this package folder. Requirements: python3 (standard library only) and, for the C programs, gcc or
clang with OpenMP (`-fopenmp`) on a 64-bit machine.

## 1. Verify the package (about 1 minute)

    sh verify-it-yourself/run_checks.sh

What it does, in order:
1. `check_value.py pins`: the sha256 of object/VALUE.txt must equal the one in INDEX.csv. Every `pin` line in
   VALUE.txt (221 files: the run's saved outputs in object/evidence/ and the four programs in verify-it-yourself/)
   must match. The `run A` and `run B` lines must state the value with exit 0 and overflow 0.
2. `check_value.py evidence`: the saved n = 20 outputs of Program A (object/evidence/A_final/) and Program B
   (object/evidence/B_final/) must both equal the value, with exit=0 and an overflow-0 log. Run A's log must show the
   declared resume at t=210, after the declared SIGTERM stop of its first segment. Every saved published-term run
   (A_repro: benzZQ.c, A364416 n=3..20 and A364417 n=3..19; B_repro: benzB128.c, n=3..18), the checkpoint-resume
   test and the saved indep_check.py outputs must equal the published terms listed in VALUE.txt.
3. `indep_check.py 11 3`: counts A364416 and A364417 for n = 3..11 fresh, straight from Propp's complex-plane
   definition, by memoized exact cover with no transfer matrix. The results are compared with the published terms.
4. Compiles benzZQ.c and benzB64.c (the two programs that produced the n = 20 value) and runs both on A364416(n)
   and A364417(n) for n = 3..NMAX (default 14), requiring overflow 0 and exact equality with the published terms.

Expected output ends with:

    summary: A364417(20) = 225354012176304818 (two independent programs, saved runs verified; published terms reproduced fresh)
    PASS

The full real output is in verify-it-yourself/RECEIPTS.md. `NMAX=16 sh verify-it-yourself/run_checks.sh` takes
about 2 minutes more.

## 2. Single commands

    gcc -O3 -fopenmp -o benzZQ verify-it-yourself/benzZQ.c
    gcc -O3 -fopenmp -o benzB64 verify-it-yourself/benzB64.c
    BENZ_M=5 ./benzZQ 14 25 3      # A364417(14) = 149124688482 (stderr ends "... overflow=0")
    ./benzB64 14 25 3 5            # 149124688482 (stderr ends "max states ... overflow 0")
    python3 verify-it-yourself/indep_check.py 8 3

Usage: `benzZQ a b K [nodelimit]` (K = rows checked ahead by the feasibility search; the environment variable BENZ_M
sets how often it runs) and `benzB64 a b Z every [limit]`. A364416(n) uses b = 2n-4 and A364417(n) uses b = 2n-3.

## 3. Recompute the new term (about 40 minutes and 3.5 GB per program; run them one at a time)

    BENZ_M=5 OMP_NUM_THREADS=7 ./benzZQ 20 37 3     # stdout 225354012176304818; stderr ends with overflow=0
    OMP_NUM_THREADS=7 ./benzB64 20 37 3 5           # stdout 225354012176304818; stderr ends "max states 50055349 overflow 0"

Optional checkpointing for Program A: set `BENZ_CKPT` to a file name and `BENZ_CKPT_SEC` to a period in seconds.
Rerunning the same command with the same `BENZ_CKPT` resumes (the log says "resumed t=..."). The saved run A used
this once (object/evidence/A_final/: *.seg1.* is the stopped segment, and A364417_n20.* is the resumed run).

## 4. Rebuild the object

object/VALUE.txt is a plain text file. Its value and run lines repeat the program outputs above. Its published lines
are the OEIS DATA as fetched (the-record-we-beat/TABLE_SNAPSHOT.md). Its `pin` lines are `sha256sum` of the listed
files with the prefix `pin`, in the order of a sorted walk of object/evidence/ followed by the four programs:

    sha256sum $(find object/evidence -type f | LC_ALL=C sort) verify-it-yourself/benzZQ.c verify-it-yourself/benzB64.c verify-it-yourself/benzB128.c verify-it-yourself/indep_check.py

(The pin order in VALUE.txt follows Python's os.walk: the files of a folder come before its subfolders.) The
evidence files were written by how-we-built-it/timed.sh around the commands in how-we-built-it/BUILD.md.
verify-it-yourself/check_value.py and run_checks.sh were written at packaging time and are covered by SHA256SUMS,
not by VALUE.txt.
