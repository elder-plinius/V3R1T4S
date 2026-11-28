# Commands used in the run (from this folder)

    gcc -O2 -o pB pB_c/progB.c && ./pB 17 > outputs/progB_17.out    # about 2 s, ~11 MB
    gcc -O2 -o pA pA_c/progA.c && ./pA 17 > outputs/progA_17.out    # 200.8 s on a loaded 8-core box (16-50 s quiet), ~177 MB
    cd self-break && python3 brute_fixtures.py > brute_fixtures.out # third method n <= 12, negative fixture

C and Python standard libraries only. PREREG.md is the run's preregistration, frozen 2026-11-03T21:28:38Z before any
program was written. Output format: one line per n, column 2 = a(n).
