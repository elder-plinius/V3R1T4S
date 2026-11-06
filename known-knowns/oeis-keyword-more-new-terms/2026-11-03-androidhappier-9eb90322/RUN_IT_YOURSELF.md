# Run it yourself (fresh shell, from this folder)

## 1. Quick check (under 1 s)
    sh verify-it-yourself/run_checks.sh          # last line: PASS

Needs Python 3 (standard library only). With a C compiler on PATH (CC, default cc) step 4 also builds Program B.
Expected key lines:

    sha256: match
    5 sum=42 wsum=226 row: 5,2,6,9,1,4,4,4,2,1,2,2
    6 sum=132 wsum=1787 row: 6,2,6,9,11,4,4,4,2,15,8,2,0,6,12,0,0,1,4,6,0,4,4,0,8,4,0,0,0,4,0,0,0,1,2,0,0,2,0,0,0,1
    rows 1..5 equal OEIS DATA (21 terms)
    row 6 (42 values) equals object/ROW6.txt; A(6,1) = 6
    pairs file equals row 6 (k, A(6,k)) for k = 1..42
    control: differs from DATA as expected
    pB row 6 identical to object/ROW6.txt
    PASS

## 2. Rerun the authors' programs (needs Python 3 and gcc)
    cd how-we-built-it
    python3 pA_py/progA.py 8                              # lines "n sum= wsum= row: ..." (about 0.03 s)
    gcc -O2 -o pB pB_c/progB.c && ./pB 8                  # identical lines (under 0.01 s; NMAX <= 12)
    python3 self-break/fixtures.py outputs/progA_8.out outputs/progB_8.out   # DATA check, %e cases, negative fixture

Saved outputs from the run: outputs/progA_8.out, outputs/progB_8.out (byte-identical), self-break/fixtures.out.

## 3. Rebuild the object
    ./pB 6 | awk '$1=="6" {sub(/.*row: /,""); print}' > ROW6.txt && sha256sum ROW6.txt
    # 9eb90322eeb05dd9fd023d19ae3dc7142c591b06e70bbe00db1e7ece89b706b5, the same bytes as object/ROW6.txt
