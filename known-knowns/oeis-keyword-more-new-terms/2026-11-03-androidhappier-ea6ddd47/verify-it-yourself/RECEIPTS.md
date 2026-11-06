# Receipts: real output of verify-it-yourself/run_checks.sh

Run from a clean copy of the package folder on the build machine, 2026-11-03T22:28Z (Python 3, cc available), wall time about 2 s:

    == 1. sha256 of object/VALUE.txt
    got  ea6ddd47e1fce10db26cc83619ee6f58bbaac89d49bc9fc9c559aa68d54c4456
    want ea6ddd47e1fce10db26cc83619ee6f58bbaac89d49bc9fc9c559aa68d54c4456
    sha256: match
    == 2. independent count from the definition (n = 1..17)
    part 1 (nested-tuple definition) a(1..10): 1,1,1,2,3,4,6,12,24,40
     1     1 trees=1 sum=1 argmax=1 ok
     2     1 trees=1 sum=1 argmax=1 ok
     3     1 trees=2 sum=2 argmax=2 ok
     4     2 trees=4 sum=5 argmax=1 ok
     5     3 trees=9 sum=14 argmax=1 ok
     6     4 trees=20 sum=42 argmax=2 ok
     7     6 trees=48 sum=132 argmax=5 ok
     8    12 trees=115 sum=429 argmax=3 ok
     9    24 trees=286 sum=1430 argmax=1 ok
    10    40 trees=719 sum=4862 argmax=1 ok
    11    60 trees=1842 sum=16796 argmax=6 ok
    12   120 trees=4766 sum=58786 argmax=4 ok
    13   240 trees=12486 sum=208012 argmax=2 ok
    14   420 trees=32973 sum=742900 argmax=3 ok
    15   840 trees=87811 sum=2674440 argmax=3 ok
    16  1680 trees=235381 sum=9694845 argmax=3 ok
    17  3360 trees=634847 sum=35357670 argmax=1 ok
    a(1..16) equal OEIS DATA
    a(17) = 3360 equals the object (3360)
    == 3. negative control: no multiplicity division
    control a(1..12): 1,1,2,6,24,120,720,5040,40320,362880,3628800,39916800
    control: differs from DATA as expected
    == 4. Program B (C) a(17)
    pB a(17) = 3360 identical to object/VALUE.txt
    pB output identical to how-we-built-it/outputs/progB_17.out
    summary: A214570(17) = 3360
    PASS
