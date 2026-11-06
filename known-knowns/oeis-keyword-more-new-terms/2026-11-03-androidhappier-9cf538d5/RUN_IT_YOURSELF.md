# Run it yourself (fresh shell, from this folder)

## 1. Quick check (well under a minute)
    sh verify-it-yourself/run_checks.sh          # last line: PASS

Needs Python 3 (standard library only). With a C compiler on PATH (CC, default cc) step 4 also builds Program A.
Expected key lines:

    sha256: match
    21 93725
    a(1..20) equal OEIS DATA
    computed a(21) = 93725
    control: differs from DATA as expected
    pA 1 21 identical to the checker's a(1..21): 21 93725
    PASS

## 2. Rerun the authors' programs (needs gcc, Go >= 1.21, Python 3; RAM < 50 MB)
    cd how-we-built-it
    gcc -O2 -o pA pA_neck.c && ./pA 1 21                     # n a(n), last line: 21 93725 (well under a second)
    (cd pB_go && go build -o ../pB main.go) && ./pB 1 21     # same 21 lines (a few seconds)
    python3 pC_literal.py 1 21                               # same 21 lines (about 20 s)
    python3 pC_neg_fixture.py 1 9                            # control: 1 1 3 4 11 ... (fails DATA at n = 3)

Saved outputs from the run: outputs/pA_1_30.txt, outputs/pB_1_25.txt, outputs/pC_1_21.txt, outputs/pC_neg_fixture_1_9.txt
(timing lines included as printed).

## 3. Rebuild the object
    ./pA 21 21 | awk '{print "A325786(" $1 ") = " $2}' > VALUE.txt && sha256sum VALUE.txt
    # 9cf538d5a41058aa72a6ce79df5852e594cd1d0c0ff8c68b3354332ec38125c5, the same bytes as object/VALUE.txt
