# Commands used in the run (from this folder)

    gcc -O2 -o pA pA_progA.c && ./pA 21           # outputs/pA_21.txt
    ./pA 26                                       # outputs/pA_26.txt (by-products a(22..26), not claimed)
    ./pA 16 nodisj                                # outputs/pA_nodisj_16.txt (negative fixture: A004111)
    (cd pB_go && go build -o ../pB .) && ./pB 21  # outputs/pB_21.txt
    ./pB 16 nodisj                                # outputs/pB_nodisj_16.txt (negative fixture: A004111)
    python3 pC_progC.py 11                        # outputs/pC_11.txt (columns n, A000081(n), A316471(n))

Requirements: gcc; Go >= 1.21 (go.mod says go 1.21; standard library only); Python 3 with sympy for Program C
(pin: sympy==1.14.0, the version the reproduce skeptic used). Programs A and B have no third-party dependencies.
PREREG.md is the run's preregistration, frozen 2026-11-03T20:01:18Z before any program was written.
