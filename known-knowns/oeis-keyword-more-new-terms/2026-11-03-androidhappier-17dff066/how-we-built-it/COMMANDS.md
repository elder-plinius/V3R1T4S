# Commands used in the run (from this folder)

    gcc -O2 -o pA pA_c/progA.c && ./pA 21                   # outputs/progA_21.out (0.29 s, 186 MB)
    ./pA 16 nodisj                                          # outputs/progA_nodisj_16.out (negative fixture)
    (cd pB_go && go build -o ../pB .) && ./pB 21            # outputs/progB_21.out (4.3 s, 0.99 GB)
    ./pB 16 nodisj                                          # outputs/progB_nodisj_16.out (negative fixture)
    python3 pC_py/progC.py 11                               # outputs/progC_11.out (needs sympy; columns n, A000081, A331783)

C and Go standard libraries only (go.mod: go 1.21). Program C needs sympy (any recent version; prime, primepi, factorint).
PREREG.md is the run's preregistration, frozen 2026-11-03T20:05:19Z before any program was written.
