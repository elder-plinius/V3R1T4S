# Run it yourself (fresh shell, from this folder)

## 1. Quick check (about 5 s, about 300 MB RAM)
    sh verify-it-yourself/run_checks.sh          # last line: PASS

Needs Python 3 (standard library only). With a C compiler on PATH (CC, default cc) step 4 also builds Program A.
Expected key lines:

    sha256: match
    20 4242226
    21 10950456
    literal Mathematica transcription equals the fast count for n = 1..11
    a(1..20) equal OEIS DATA
    computed a(21) = 10950456; object says 10950456
    control: differs from DATA as expected
    pA 21 output identical to the checker's a(1..21): 21 10950456
    PASS

## 2. Rerun the authors' programs (needs gcc, Go >= 1.21, Python 3 with sympy for Program C; RAM < 1.1 GB for B, < 200 MB for A)
    cd how-we-built-it
    gcc -O2 -o pA pA_c/progA.c && ./pA 21                    # lines "n a(n)"; last line: 21 10950456 (under 1 s)
    (cd pB_go && go build -o ../pB .) && ./pB 21             # same lines (a few seconds)
    python3 pC_py/progC.py 11                                # columns n, A000081(n), A331783(n) for n <= 11
    ./pA 16 nodisj ; ./pB 16 nodisj                          # negative fixture: 1,1,2,4,8,18,41,... (not DATA)

Saved outputs from the run: outputs/progA_21.out, outputs/progB_21.out, outputs/progC_11.out,
outputs/progA_nodisj_16.out, outputs/progB_nodisj_16.out.

## 3. Rebuild the object
    ./pA 21 | awk '$1=="21" {print "A331783(" $1 ") = " $2}' > VALUE.txt && sha256sum VALUE.txt
    # 17dff06626c3c02e2d547f5d180ce2ec5f658153433a495413f4f62c8d21683f, the same bytes as object/VALUE.txt
