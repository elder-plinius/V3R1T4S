# Run it yourself (fresh shell, from this folder)

## 1. Quick check (a few seconds)
    sh verify-it-yourself/run_checks.sh          # last line: PASS

Needs Python 3 (standard library only). With a C compiler on PATH (CC, default cc) step 4 also builds Program A.
Expected key lines:

    sha256: match
    20 214490
    21 482706
    a(1..20) equal OEIS DATA
    computed a(21) = 482706; object says 482706
    control: differs from DATA as expected
    pA 21 output identical to the checker's a(1..21): 21 482706
    PASS

## 2. Rerun the authors' programs (needs gcc, Go >= 1.21, Python 3 with sympy for Program C; RAM < 300 MB)
    cd how-we-built-it
    gcc -O2 -o pA pA_progA.c && ./pA 21                      # lines "n a(n)", last line: 21 482706
    (cd pB_go && go build -o ../pB .) && ./pB 21             # same lines (about 2 s, ~230 MB)
    ./pA 16 nodisj ; ./pB 16 nodisj                          # control: A004111, not A316471
    python3 pC_progC.py 11                                   # columns n A000081(n) A316471(n), n <= 11 (needs sympy)

Saved outputs from the run: outputs/pA_21.txt, outputs/pA_26.txt, outputs/pA_nodisj_16.txt, outputs/pB_21.txt,
outputs/pB_nodisj_16.txt, outputs/pC_11.txt.

## 3. Rebuild the object
    ./pA 21 | awk '$1=="21" {print "A316471(" $1 ") = " $2}' > VALUE.txt && sha256sum VALUE.txt
    # 7eb8fe00ca9ad3d0cd9e416451bb86b10febf6b4551078a0034854cc7191ecd9, the same bytes as object/VALUE.txt
