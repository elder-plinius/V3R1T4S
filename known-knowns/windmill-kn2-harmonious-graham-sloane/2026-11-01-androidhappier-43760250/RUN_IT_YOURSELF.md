# Run it yourself

Fresh shell, from this package folder. Requirements: python3 (standard library only). Optional: a C compiler (`cc`
or `gcc`) with unsigned __int128 support, for program P1.

## 1. Verify the decision

    sh verify-it-yourself/run_checks.sh

What it does, in order:
1. `check_decision.py pins`: reads object/DECISION.txt (target, cell n = 8, decision NOT HARMONIOUS) and recomputes
   the sha256 of every pinned file: the run's outputs in object/evidence/ and the four checker programs in
   verify-it-yourself/. The pinned run outputs must state the same n = 8 numbers as DECISION.txt.
2. P2, `mitm.py n` for n = 3..8 (Python): lists every n-subset of Z_q containing 0 with distinct pair sums, then
   joins pairs whose sum masks are complementary and whose labels meet only in 0.
3. P1, `wsearch.c` for n = 3..8 (C, if a compiler is present): nested backtracking, clique A then clique B.
4. `brute_n4.py`: all 3,991,680 injective labelings of K_4^(2), no reduction. Expected 20736.
5. `check_decision.py compare`: every fresh number against the `expect` lines in object/DECISION.txt, including the
   n = 8 verdict of each program.
6. `check_decision.py n4list`: enumerates the n = 4 solutions here, independently, and requires both of the run's
   lists (object/evidence/n4_solutions_P1.txt, _P2.txt) to equal it. Checks 48 x 12 x 3! x 3! = 20736 and two
   negative controls. Then `check_label.py` must accept a known K_4^(2) labeling and reject a repeated-sum and a
   repeated-label copy.

Expected output ends with:

    summary: K_8^(2) has no harmonious labeling mod 56 (0 labelings; 449472 sum-distinct 8-sets containing 0)
    PASS

Time: about 1 minute on a laptop (P1 n = 8 about 40 s, P2 n = 8 about 12 s and 0.75 GB). The full real output is in
verify-it-yourself/RECEIPTS.md.

## 2. Single commands

    gcc -O2 -o wsearch verify-it-yourself/wsearch.c && ./wsearch 8
    # n=8 q=56 sum_distinct_sets_containing_0=449472 solutions_ordered_pairs=0 nodesB=270416160
    # VERDICT n=8: NOT HARMONIOUS
    python3 verify-it-yourself/mitm.py 8
    # n=8 q=56 sum_distinct_sets_containing_0=449472 distinct_masks=407352 solutions_ordered_pairs=0
    # VERDICT n=8: NOT HARMONIOUS

## 3. Rebuild the object

object/DECISION.txt is a text file. Its `expect` lines are the program outputs above. Its `pin` lines are
`sha256sum` of the listed files, with the prefix `pin`:

    sha256sum object/evidence/* verify-it-yourself/wsearch.c verify-it-yourself/mitm.py verify-it-yourself/brute_n4.py verify-it-yourself/check_label.py

The evidence files were produced by the commands in how-we-built-it/BUILD.md. The supporting programs (P3 wjoin.c,
the mod-14 and mod-28 obstructions) are in how-we-built-it/ too.
