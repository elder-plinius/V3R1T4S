# Run it yourself (fresh shell, from this folder)

## 1. Quick check (a few seconds)
    sh verify-it-yourself/run_checks.sh          # last line: PASS

Needs Python 3 (standard library only). With a C compiler on PATH (CC, default cc) step 4 also builds Program A.
Expected key lines:

    sha256: match
    11 61987
    a(0..10) equal OEIS DATA
    computed a(11) = 61987
    control: differs from DATA as expected
    pA 0 11 A326335 column identical to the checker's a(0..11): 11 61987
    PASS

## 2. Rerun the authors' programs (needs gcc, Go (go.mod says go 1.27.3; edit it for an older toolchain), Python 3; RAM < 20 MB)
    cd how-we-built-it
    gcc -O2 -o pA pA_spstats.c && ./pA 0 11                  # columns: n A326245 A326246 A326249 A326335 A326336
                                                             # last line: 11 23096 596688 24744 61987 70472
    (cd pB_go && go build -o ../pB main.go) && ./pB 0 11     # same table
    python3 pC_literal.py 0 11                               # same table (minutes)
    python3 pC_neg_fixture.py                                # control: any-pairs nesting fails DATA

The A326335 column is the fifth. Saved outputs from the run: outputs/pA_0_12.txt, outputs/pB_0_12.txt,
outputs/pC_0_11.txt, outputs/pC_neg_fixture.txt (timing lines included as printed).

## 3. Rebuild the object
    ./pA 11 11 | awk '$1=="11" {print "A326335(" $1 ") = " $5}' > VALUE.txt && sha256sum VALUE.txt
    # 1726275264dcaacd920d82809a0363b4c5b93c894297cf7f8d2166e9a80350bc, the same bytes as object/VALUE.txt
