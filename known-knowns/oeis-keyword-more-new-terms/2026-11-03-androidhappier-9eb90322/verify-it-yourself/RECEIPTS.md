# Receipts: real output of verify-it-yourself/run_checks.sh

Run from the package folder on the build machine, 2026-11-03T21:57Z (Python 3, cc available), wall time under 1 s:

    == 1. sha256 of object/ROW6.txt
    got  9eb90322eeb05dd9fd023d19ae3dc7142c591b06e70bbe00db1e7ece89b706b5
    want 9eb90322eeb05dd9fd023d19ae3dc7142c591b06e70bbe00db1e7ece89b706b5
    sha256: match
    == 2. independent count from the definition (n = 1..6)
    1 sum=1 wsum=1 row: 1
    2 sum=2 wsum=2 row: 2
    3 sum=5 wsum=7 row: 3,2
    4 sum=14 wsum=35 row: 4,2,6,1,1
    5 sum=42 wsum=226 row: 5,2,6,9,1,4,4,4,2,1,2,2
    6 sum=132 wsum=1787 row: 6,2,6,9,11,4,4,4,2,15,8,2,0,6,12,0,0,1,4,6,0,4,4,0,8,4,0,0,0,4,0,0,0,1,2,0,0,2,0,0,0,1
    rows 1..5 equal OEIS DATA (21 terms)
    row 6 (42 values) equals object/ROW6.txt; A(6,1) = 6
    pairs file equals row 6 (k, A(6,k)) for k = 1..42
    %e n = 3 drawing counts (multiset): [1, 1, 1, 2, 2] ok
    == 3. negative control: deletion sequences instead of distinct tree chains
    control (deletion sequences) rows 1..5: [1, 1, 1, 1, 1, 2, 0, 0, 1, 1, 1, 2, 2, 0, 2, 0, 2, 0, 0, 0, 3]
    control: differs from DATA as expected
    == 4. Program B (C) row 6
    pB row 6 identical to object/ROW6.txt
    summary: A155520 row 6 = 6,2,6,9,11,4,4,4,2,15,8,2,0,6,12,0,0,1,4,6,0,4,4,0,8,4,0,0,0,4,0,0,0,1,2,0,0,2,0,0,0,1; A(6,1) = 6
    PASS
