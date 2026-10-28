# Run it yourself

From this folder, in a fresh shell. Needs python3 (3.9 or newer, standard library only) and gzip. About 20 s.

    sh verify-it-yourself/run_checks.sh

Expected output (the real run is in verify-it-yourself/RECEIPTS.md):

    ALL_PASS
    compare_values: ALL_EQUAL
    ALL_PASS
    my_verify summary: 30 passed, 0 failed, of 30 certificates
    reproduced_known_knowns_16_30: ALL_EQUAL
    15 certificates n=31..45 verified; 15 calibration certificates n=1..15 equal published terms; repository terms n=16..30 reproduced; second verifier agrees
    PASS

What it does:
1. Unpacks object/n31.json.gz and reassembles/unpacks object/n32.json.gz.part* through n45.json.gz.part* in verify-it-yourself/_work/.
2. verify-it-yourself/ros_cert_check.py (written from the definition, exact fractions) checks every certificate n = 31..45:
   every position (a, b, c) with 0 <= b < n, 0 <= c < n, 0 <= a < n - b listed exactly once (n^2(n+1)/2 rows), forced
   toss at a = 0, P(a, b, c) = max(continue, stop) at a >= 1 with continue = (1/2)(1 - P(0, c, b)) + (1/2) P(a+1, b, c),
   stop = 1 - P(0, c, a + b), P = 1 when a + b >= n, and the claimed action attains the max. It prints P(0, 0, 0).
3. verify-it-yourself/compare_values.py confirms those P(0, 0, 0) equal the 15 claimed terms in object/values.txt.
4. The same checker, with --oeis verify-it-yourself/published_terms, confirms the calibration certificates n = 1..15
   satisfy all Bellman equations and equal the published terms of A387261/A387262 exactly.
5. verify-it-yourself/my_verify.py, a second verifier written independently (integer cross-multiplication, no Fraction, coprimality checking),
   re-checks all 30 certificates (15 calibration + 15 claim).
6. Compares object/values.txt lines 16..30 against verify-it-yourself/published_terms/values_16_30.txt to confirm exact reproduction of repository known-knowns.

Rebuild every certificate from scratch and compare byte for byte:

    mkdir -p _rerun
    python3 -I how-we-built-it/code/solver_extender.py 45 _rerun 1 45 _rerun/values.txt --b-dir verify-it-yourself/published_terms
    cmp _rerun/values.txt object/values.txt && echo "values identical"
