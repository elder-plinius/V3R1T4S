# Receipts: real output of verify-it-yourself/run_checks.sh

Machine: Linux x86-64, 8 cores, Python 3.13.5, gcc (Debian 14.2.0-19) 14.2.0. Run on 2026-11-01 (America/New_York),
from this package folder. Wall time 1m0.0s (shell `time`).

## 1. This package as shipped

    == 1. object/DECISION.txt: header and pinned sha256 of the evidence files and of these checkers
    OK header target: windmill-kn2-harmonious-graham-sloane
    OK header cell: n = 8
    OK header decision: NOT HARMONIOUS
    OK sha256 object/evidence/P1_wsearch_n8.txt
    OK sha256 object/evidence/P2_mitm_n8.txt
    OK sha256 object/evidence/P3_wjoin_n8.txt
    OK sha256 object/evidence/brute_n4.txt
    OK sha256 object/evidence/mod_multiset_n8.txt
    OK sha256 object/evidence/mod_projection_n8.txt
    OK sha256 object/evidence/n4_solutions_P1.txt
    OK sha256 object/evidence/n4_solutions_P2.txt
    OK sha256 object/evidence/run_DECISION.txt
    OK sha256 verify-it-yourself/wsearch.c
    OK sha256 verify-it-yourself/mitm.py
    OK sha256 verify-it-yourself/brute_n4.py
    OK sha256 verify-it-yourself/check_label.py
    OK object/evidence/P1_wsearch_n8.txt sum_distinct_sets_containing_0=449472
    OK object/evidence/P1_wsearch_n8.txt solutions_ordered_pairs=0
    OK object/evidence/P2_mitm_n8.txt sum_distinct_sets_containing_0=449472
    OK object/evidence/P2_mitm_n8.txt solutions_ordered_pairs=0
    PINS: PASS
    == 2. P2 (mitm.py, Python, enumerate all sum-distinct sets then join complementary sum masks), n = 3..8
    n=3 q=6 sum_distinct_sets_containing_0=10 distinct_masks=8 solutions_ordered_pairs=0
    VERDICT n=3: NOT HARMONIOUS
    n=4 q=12 sum_distinct_sets_containing_0=120 distinct_masks=91 solutions_ordered_pairs=48
    VERDICT n=4: HARMONIOUS
    n=5 q=20 sum_distinct_sets_containing_0=1460 distinct_masks=1252 solutions_ordered_pairs=0
    VERDICT n=5: NOT HARMONIOUS
    n=6 q=30 sum_distinct_sets_containing_0=13608 distinct_masks=12344 solutions_ordered_pairs=0
    VERDICT n=6: NOT HARMONIOUS
    n=7 q=42 sum_distinct_sets_containing_0=90888 distinct_masks=81948 solutions_ordered_pairs=0
    VERDICT n=7: NOT HARMONIOUS
    n=8 q=56 sum_distinct_sets_containing_0=449472 distinct_masks=407352 solutions_ordered_pairs=0
    VERDICT n=8: NOT HARMONIOUS
    == 3. P1 (wsearch.c, C, nested backtracking clique A then clique B), n = 3..8
    n=3 q=6 sum_distinct_sets_containing_0=10 solutions_ordered_pairs=0 nodesB=32
    VERDICT n=3: NOT HARMONIOUS
    n=4 q=12 sum_distinct_sets_containing_0=120 solutions_ordered_pairs=48 nodesB=1280
    VERDICT n=4: HARMONIOUS
    n=5 q=20 sum_distinct_sets_containing_0=1460 solutions_ordered_pairs=0 nodesB=46508
    VERDICT n=5: NOT HARMONIOUS
    n=6 q=30 sum_distinct_sets_containing_0=13608 solutions_ordered_pairs=0 nodesB=1194308
    VERDICT n=6: NOT HARMONIOUS
    n=7 q=42 sum_distinct_sets_containing_0=90888 solutions_ordered_pairs=0 nodesB=21315612
    VERDICT n=7: NOT HARMONIOUS
    n=8 q=56 sum_distinct_sets_containing_0=449472 solutions_ordered_pairs=0 nodesB=270416160
    VERDICT n=8: NOT HARMONIOUS
    == 4. unreduced brute force over all injective labelings of K_4^(2) (validates the translation reduction)
    brute_force_labelings 20736 expected 20736
    == 5. every fresh number against the expect lines of object/DECISION.txt
    OK P1 n=3 sum_distinct_sets_containing_0=10
    OK P1 n=3 solutions_ordered_pairs=0
    OK P1 n=4 sum_distinct_sets_containing_0=120
    OK P1 n=4 solutions_ordered_pairs=48
    OK P1 n=5 sum_distinct_sets_containing_0=1460
    OK P1 n=5 solutions_ordered_pairs=0
    OK P1 n=6 sum_distinct_sets_containing_0=13608
    OK P1 n=6 solutions_ordered_pairs=0
    OK P1 n=7 sum_distinct_sets_containing_0=90888
    OK P1 n=7 solutions_ordered_pairs=0
    OK P1 n=8 sum_distinct_sets_containing_0=449472
    OK P1 n=8 solutions_ordered_pairs=0
    OK P1 n=8 nodesB=270416160
    OK P2 n=3 sum_distinct_sets_containing_0=10
    OK P2 n=3 solutions_ordered_pairs=0
    OK P2 n=4 sum_distinct_sets_containing_0=120
    OK P2 n=4 distinct_masks=91
    OK P2 n=4 solutions_ordered_pairs=48
    OK P2 n=5 sum_distinct_sets_containing_0=1460
    OK P2 n=5 solutions_ordered_pairs=0
    OK P2 n=6 sum_distinct_sets_containing_0=13608
    OK P2 n=6 solutions_ordered_pairs=0
    OK P2 n=7 sum_distinct_sets_containing_0=90888
    OK P2 n=7 solutions_ordered_pairs=0
    OK P2 n=8 sum_distinct_sets_containing_0=449472
    OK P2 n=8 distinct_masks=407352
    OK P2 n=8 solutions_ordered_pairs=0
    OK BRUTE n=4 brute_force_labelings=20736
    OK P1 n=8 verdict: NOT HARMONIOUS
    OK P2 n=8 verdict: NOT HARMONIOUS
    COMPARE: PASS
    == 6. n = 4 positive control: the 48 ordered pairs, enumerated independently here; label checker controls
    independent enumeration here: 48 ordered pairs for n = 4
    OK n4_solutions_P1.txt: the same 48 ordered pairs
    OK n4_solutions_P2.txt: the same 48 ordered pairs
    OK 48 x 12 x 3! x 3! = 20736 (unreduced brute force)
    OK control (repeated label) rejected
    OK control (same clique twice) rejected
    N4LIST: PASS
    VALID
    known K_4^(2) labeling: VALID as expected
    INVALID: edge sums repeat
    repeated-sum control: INVALID as expected
    INVALID: labels not distinct
    repeated-label control: INVALID as expected
    summary: K_8^(2) has no harmonious labeling mod 56 (0 labelings; 449472 sum-distinct 8-sets containing 0)
    PASS

## 2. Damaged copies (run on scratch copies of this folder; the shipped files are unchanged)

a. object/DECISION.txt with the line `expect P2 8 solutions_ordered_pairs 0` changed to `... 1`
(exit status 1). Lines from the output:

    object/evidence/P2_mitm_n8.txt: solutions_ordered_pairs=0 disagrees with DECISION.txt (1)
    PINS: FAIL
    P2 n=8 solutions_ordered_pairs: got 0, DECISION.txt says 1
    COMPARE: FAIL
    FAIL

b. object/evidence/n4_solutions_P1.txt with its first row `0,1,2,8|0,5,7,11` changed to `0,1,2,8|0,5,7,10`
(`check_decision.py pins` and `check_decision.py n4list`, output lines other than OK):

    sha256 MISMATCH object/evidence/n4_solutions_P1.txt (got 286d0ea71b349e768512e5783dbbad4e2776e8a764b36e7259013ac3d2251b9b)
    PINS: FAIL
    independent enumeration here: 48 ordered pairs for n = 4
    n4_solutions_P1.txt: differs from the independent enumeration (48 rows)
    N4LIST: FAIL
