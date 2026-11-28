# Commands used in the run (from this folder)

    python3 pA_py/progA.py 7 > outputs/progA_7.out        # well under 1 s; stderr: row lengths and sums
    gcc -O2 -o pB pB_c/progB.c && ./pB 7 > outputs/progB_7.out   # about 0.1 s; byte-identical to progA_7.out
    # self-break (needs the OEIS b-file next to the script, saved as preclaim_b131449.txt):
    cd self-break && python3 fixtures.py > fixtures.out

Python and C standard libraries only. PREREG.md is the run's preregistration, frozen 2026-11-03T21:54:14Z before any
program was written. Output format: one "index value" line per term, offset 0 (index 66 = T(6,2)).
