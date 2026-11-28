# Run it yourself (fresh shell, from this folder)

## 1. Quick check (a few seconds)
    sh verify-it-yourself/run_checks.sh          # last line: PASS

Needs Python 3 (standard library only). With a C compiler on PATH (CC, default cc) step 4 also builds Program B.
Expected key lines:

    sha256: match
    part 1 (nested-tuple definition) a(1..10): 1,1,1,2,3,4,6,12,24,40
    16  1680 trees=235381 sum=9694845 argmax=3 ok
    17  3360 trees=634847 sum=35357670 argmax=1 ok
    a(1..16) equal OEIS DATA
    a(17) = 3360 equals the object (3360)
    control: differs from DATA as expected
    pB a(17) = 3360 identical to object/VALUE.txt
    PASS

## 2. Rerun the authors' programs (needs gcc)
    cd how-we-built-it
    gcc -O2 -o pB pB_c/progB.c && ./pB 17 > B17.out       # seconds; columns: n, max, sum = Catalan(n-1), #trees, #maximizers
    gcc -O2 -o pA pA_c/progA.c && ./pA 17 > A17.out       # brute force over 35357670 ordered trees: about 15 s to 4 min, ~180 MB
    cmp B17.out outputs/progB_17.out && cmp A17.out outputs/progA_17.out   # byte-identical to the saved outputs
    awk '$1==17 {print $2}' A17.out B17.out                # 3360 twice
    (cd self-break && python3 brute_fixtures.py)           # third method n <= 12 and negative fixture (no network needed)

## 3. Rebuild the object
    ./pB 17 | awk '$1==17 {print $2}' > VALUE.txt && sha256sum VALUE.txt
    # ea6ddd47e1fce10db26cc83619ee6f58bbaac89d49bc9fc9c559aa68d54c4456, the same bytes as object/VALUE.txt
