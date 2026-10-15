# Run it yourself

From this folder, in a fresh shell. Needs python3 (3.9 or newer, standard library only) and gzip. About 30 s.

    sh verify-it-yourself/run_checks.sh

Expected output (the real run is in verify-it-yourself/RECEIPTS.md):

    ALL_PASS
    compare_values: ALL_EQUAL
    ALL_PASS
    my_verify summary: 30 passed, 0 failed, of 30 certificates
    15 certificates n=16..30 verified; 15 calibration certificates n=1..15 equal the published terms; second verifier agrees
    PASS

What it does:
1. Unpacks object/n27.json.gz ... n30.json.gz (gzipped only to respect the 1 MB file limit) next to object/n16.json ...
   n26.json in verify-it-yourself/_work/.
2. verify-it-yourself/ros_cert_check.py (written from the definition, exact fractions) checks every certificate n = 16..30:
   every position (a, b, c) with 0 <= b < n, 0 <= c < n, 0 <= a < n - b listed exactly once (n^2(n+1)/2 rows), forced
   toss at a = 0, P(a, b, c) = max(continue, stop) at a >= 1 with continue = (1/2)(1 - P(0, c, b)) + (1/2) P(a+1, b, c),
   stop = 1 - P(0, c, a + b), P = 1 when a + b >= n, and the claimed action attains the max. It prints P(0, 0, 0).
3. verify-it-yourself/compare_values.py confirms those P(0, 0, 0) equal the 15 claimed terms in object/values.txt.
4. The same checker, with --oeis verify-it-yourself/published_terms, confirms the calibration certificates n = 1..15
   (made by the same solver run) equal the 15 published terms of A387261/A387262 exactly.
5. verify-it-yourself/my_verify.py, a second verifier written independently (integer cross-multiplication, no Fraction),
   re-checks all 30 certificates.

Check a single certificate by hand, for example n = 16:

    python3 -I verify-it-yourself/ros_cert_check.py object/n16.json
    # n16.json: n=16 positions_checked=2176 P000=1599710761252635467097849938052769718961535662524/3090007892803332518177914010771390705108642578125 PASS

Rebuild every certificate from scratch (about 3 s) and compare byte for byte:

    mkdir -p _rerun
    python3 -I how-we-built-it/code/solver_extender.py 30 _rerun 1 30 _rerun/values.txt --b-dir verify-it-yourself/published_terms
    for k in 16 17 18 19 20 21 22 23 24 25 26; do cmp _rerun/n$k.json object/n$k.json && echo n$k identical; done
    for k in 27 28 29 30; do gzip -dc object/n$k.json.gz | cmp _rerun/n$k.json - && echo n$k identical; done
    for k in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do cmp _rerun/n$k.json verify-it-yourself/calibration/n$k.json && echo n$k identical; done
    cmp _rerun/values.txt object/values.txt && echo values identical

Why a passing certificate is a proof: the equations are the Shapley optimality equations of a finite zero-sum game that
ends with probability 1 under every strategy pair (each block of 2n steps contains at least n tosses; if the first n tosses
of a block are all heads, probability at least 2^-n, the player tossing first in the block wins or banks a point; banked
totals never fall and stay below n), so they have a
unique solution, the optimal-value table, and any action attaining the max is optimal (see panel/reproduce.md and
panel/criterion.md for the panel's re-derivation).
