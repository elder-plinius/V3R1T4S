# Commands used in the run (from this folder)

    gcc -O2 -o pA pA_spstats.c && ./pA 0 12                 # outputs/pA_0_12.txt
    (cd pB_go && go build -o ../pB main.go) && ./pB 0 12    # outputs/pB_0_12.txt
    python3 pC_literal.py 0 11                              # outputs/pC_0_11.txt
    python3 pC_neg_fixture.py                               # outputs/pC_neg_fixture.txt (negative controls)

No third-party packages; Go standard library only (go.mod pins the language version, go 1.27.3).
PREREG.md is the run's preregistration, frozen 2026-11-03T16:25:52Z before any program was written.
