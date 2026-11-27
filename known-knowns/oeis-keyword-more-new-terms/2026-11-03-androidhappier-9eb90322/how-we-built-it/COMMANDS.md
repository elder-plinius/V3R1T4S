# Commands used in the run (from this folder)

    python3 pA_py/progA.py 8                         # outputs/progA_8.out (about 0.03 s)
    gcc -O2 -o pB pB_c/progB.c && ./pB 8             # outputs/progB_8.out (under 0.01 s), byte-identical to progA_8.out
    python3 self-break/fixtures.py outputs/progA_8.out outputs/progB_8.out   # self-break/fixtures.out

Python and C standard libraries only. PREREG.md is the run's preregistration, frozen 2026-11-03T21:47:04Z before any
program was written. self-break/fixtures.out was produced in the run folder, so its first two lines show the run's
relative paths to the same two output files.
