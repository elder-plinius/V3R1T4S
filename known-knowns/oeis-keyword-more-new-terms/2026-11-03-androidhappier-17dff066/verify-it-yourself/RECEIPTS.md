# Receipts: real output of verify-it-yourself/run_checks.sh

Run from the package folder on the build machine, 2026-11-03T21:26Z (Python 3, cc available), wall time about 5 s, peak RAM about 300 MB:

    == 1. sha256 of object/VALUE.txt
    got  17dff06626c3c02e2d547f5d180ce2ec5f658153433a495413f4f62c8d21683f
    want 17dff06626c3c02e2d547f5d180ce2ec5f658153433a495413f4f62c8d21683f
    sha256: match
    == 2. independent exhaustive count from the definition (n = 1..21)
    1 1
    2 1
    3 2
    4 4
    5 8
    6 17
    7 37
    8 83
    9 191
    10 450
    11 1076
    12 2610
    13 6404
    14 15875
    15 39676
    16 99880
    17 253016
    18 644524
    19 1649918
    20 4242226
    21 10950456
    literal Mathematica transcription equals the fast count for n = 1..11
    a(1..20) equal OEIS DATA
    computed a(21) = 10950456; object says 10950456
    == 3. negative control: no local disjointness
    nodisj control a(1..16): [1, 1, 2, 4, 8, 18, 41, 98, 237, 591, 1488, 3805, 9820, 25593, 67184, 177604]
    control: differs from DATA as expected
    == 4. Program A (C) for n = 1..21
    pA 21 output identical to the checker's a(1..21): 21 10950456
    summary: A331783(21) = 10950456
    PASS
