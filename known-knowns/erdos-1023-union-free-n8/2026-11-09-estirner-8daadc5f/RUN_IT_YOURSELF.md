# Run it yourself

From this folder, in a fresh shell with Python 3 (standard library only):

    sh verify-it-yourself/run_checks.sh

Expected output (a few seconds):

    0. sha256 8daadc5f6c94a0b0e2364d01cfb9db7931fff7e815d182b329dc4b5cd3293560 matches expected_sha256.txt
    1. calibration a(1..4) by exhaustive search: [1, 2, 4, 7] (expected [1, 2, 4, 7])
    2. 80 members, all distinct sets of distinct elements of {1..8}: True
    3. union-free: maximal-union test True, per-element test True
       size profile: {2: 2, 3: 15, 4: 63}
    4. size 80 >= 80: True
    PASS

A ten-line check of your own: read the 80 lines as sets; for each set S, take the union of all other sets that are
contained in S; it must never equal S.

Rebuild the object (minutes):

    cd how-we-built-it/code && sh run.sh      # writes out/n8_seed*.txt; every n = 8 seed reaches 80
