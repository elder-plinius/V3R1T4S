# Receipts: real output of verify-it-yourself/run_checks.sh

Run from the package folder on the build machine, 2026-11-03T20:4xZ (Python 3, cc available), wall time about 4 s:

    == 1. sha256 of object/VALUE.txt
    got  9459f487d861a49adae0c14a4e752a63813fbc1c13ac85ac585ee216278e8dcf
    want 9459f487d861a49adae0c14a4e752a63813fbc1c13ac85ac585ee216278e8dcf
    sha256: match
    == 2. independent exhaustive count from the definition (n = 0..11)
    fast capture test equals the literal any-pair test on every block pair, n <= 8
    0 1
    1 1
    2 1
    3 1
    4 2
    5 7
    6 24
    7 100
    8 458
    9 2279
    10 12270
    11 70472
    a(0..10) equal OEIS DATA
    computed a(11) = 70472; object says 70472
    == 3. negative control: crossing edges instead of capturing
    crossing control a(0..9): [1, 1, 1, 1, 2, 6, 21, 85, 385, 1907]
    control: differs from DATA as expected
    == 4. Program A (C) for n = 0..11
    pA 0 11 A326336 column identical to the checker's a(0..11): 11 70472
    summary: A326336(11) = 70472
    PASS
