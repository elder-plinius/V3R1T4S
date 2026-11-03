# Receipts: real output of verify-it-yourself/run_checks.sh

Run from the package folder on the build machine, 2026-11-03T21:31:02Z (Python 3.13.5, cc = gcc 14.2.0), wall time about 1.4 s:

    == 1. sha256 of object/VALUE.txt
    got  7eb8fe00ca9ad3d0cd9e416451bb86b10febf6b4551078a0034854cc7191ecd9
    want 7eb8fe00ca9ad3d0cd9e416451bb86b10febf6b4551078a0034854cc7191ecd9
    sha256: match
    == 2. independent exhaustive enumeration from the definition (n = 1..21)
    1 1
    2 1
    3 1
    4 2
    5 3
    6 6
    7 11
    8 21
    9 43
    10 89
    11 185
    12 391
    13 840
    14 1822
    15 3975
    16 8727
    17 19280
    18 42841
    19 95661
    20 214490
    21 482706
    a(1..20) equal OEIS DATA
    computed a(21) = 482706; object says 482706
    == 3. negative control: no locally-disjoint test
    control (no disjointness) a(1..16): [1, 1, 1, 2, 3, 6, 12, 25, 52, 113, 247, 548, 1226, 2770, 6299, 14426]
    control equals A004111: True
    control equals A316471 DATA: False
    control: differs from DATA as expected
    == 4. Program A (C) for n = 1..21
    pA 21 output identical to the checker's a(1..21): 21 482706
    summary: A316471(21) = 482706
    PASS
