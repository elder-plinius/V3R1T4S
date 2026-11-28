# Run it yourself (fresh shell, from this folder)

## 1. Quick check (under 1 s)
    sh verify-it-yourself/run_checks.sh          # last line: PASS

Needs Python 3 (standard library only). With a C compiler on PATH (CC, default cc) step 4 also builds Program B.
Expected key lines:

    sha256: match
    6 len=132 sum=10395 head: 720,360,360,360,360,360,240,240,240,240,180,180
    indices 0..65 equal OEIS DATA (66 terms)
    row 6 (132 values, flattened indices 65..196) equals object/ROW6.txt
    index 66 = T(6,2) = 360 equals object/VALUE.txt
    control: differs from DATA as expected
    pB row 6 identical to object/ROW6.txt
    PASS

## 2. Rerun the authors' programs (needs Python 3 and gcc)
    cd how-we-built-it
    python3 pA_py/progA.py 7 > A7.out                     # "index value" lines, offset 0 (well under 1 s)
    gcc -O2 -o pB pB_c/progB.c && ./pB 7 > B7.out          # identical lines (about 0.1 s; NMAX <= 8)
    cmp A7.out B7.out && cmp A7.out outputs/progA_7.out    # byte-identical to the saved outputs
    # self-break/fixtures.py (Lang's row-5 class grouping, negative fixtures) reads the OEIS b-file:
    # curl -s -o self-break/preclaim_b131449.txt https://oeis.org/A131449/b131449.txt && (cd self-break && python3 fixtures.py)

## 3. Rebuild the objects
    ./pB 6 2>/dev/null | awk '$1>=65 {print $2}' | paste -sd, - > ROW6.txt && sha256sum ROW6.txt
    # c3661e45bbff1f5a2fb05098c2940739a0d096689e593c1095142858cb66f120, the same bytes as object/ROW6.txt
    ./pB 6 2>/dev/null | awk '$1==66 {print $2}' > VALUE.txt   # 360, the same bytes as object/VALUE.txt
