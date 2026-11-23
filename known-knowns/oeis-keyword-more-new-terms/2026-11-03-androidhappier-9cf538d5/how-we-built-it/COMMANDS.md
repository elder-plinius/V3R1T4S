# Commands used in the run (from this folder)

    gcc -O2 -o pA pA_neck.c && ./pA 1 30                    # outputs/pA_1_30.txt
    (cd pB_go && go build -o ../pB main.go) && ./pB 1 25    # outputs/pB_1_25.txt
    python3 pC_literal.py 1 21                              # outputs/pC_1_21.txt
    python3 pC_neg_fixture.py 1 9                           # outputs/pC_neg_fixture_1_9.txt (negative control)

No third-party packages; Go standard library only (go.mod pins the language version, go 1.21).
PREREG.md is the run's preregistration, frozen 2026-11-03T16:42:32Z before any program was written.
Its disclosure line mentions scratch work on a different sequence (A336131); that does not affect this cell.
