# How the decision was built (exact commands)

Run from this how-we-built-it/ folder in a fresh shell. Needs gcc (or clang) with unsigned __int128 and python3
(standard library only). No other dependencies; nothing is downloaded.

## The decision (criterion branch (b))

    gcc -O2 -o wsearch wsearch.c
    ./wsearch 8            # P1: n=8 q=56 sum_distinct_sets_containing_0=449472 solutions_ordered_pairs=0 nodesB=270416160
    python3 mitm.py 8      # P2: n=8 q=56 sum_distinct_sets_containing_0=449472 distinct_masks=407352 solutions_ordered_pairs=0
    for n in 3 4 5 6 7; do ./wsearch $n | tail -1; python3 mitm.py $n | tail -1; done   # only n=4 HARMONIOUS
    python3 brute_n4.py    # brute_force_labelings 20736 expected 20736 (no reduction at all)
    python3 check_label.py 4 "0 2 6 11" "3 7 9"   # VALID (a known K_4^(2) labeling)

The run's captured outputs are object/evidence/P1_wsearch_n8.txt and P2_mitm_n8.txt (with the shell's `time`
lines: about 40 s and 12 s; P2 peaks at about 0.75 GB).

## The n = 4 solution lists (object/evidence/n4_solutions_P1.txt, n4_solutions_P2.txt)

    gcc -O2 -o wsearch_printall wsearch_printall.c && ./wsearch_printall 4 | grep '^SOLUTION'

wsearch_printall.c is wsearch.c without the 20-solution print cap. The run turned the SOLUTION lines of P1 and of
P2 (all 48 pairs) into sorted `A|B` rows and compared them (identical). The exact text-conversion commands were not
kept. verify-it-yourself/check_decision.py n4list does not depend on them: it re-derives the 48 pairs from the
definition and compares both files with that list.

## Supporting evidence (not needed for the decision)

    gcc -O2 -o wjoin wjoin.c && ./wjoin 8 14           # P3: 449472 sets; d=14 compatible 0; solutions 0 (object/evidence/P3_wjoin_n8.txt)
    gcc -O2 -o mod14 mod14.c && for d in 2 4 7 8 14 28; do ./mod14 $d; done   # object/evidence/mod_projection_n8.txt
    python3 mod_multiset.py 28    # about 3 min; compatible ordered pairs (no Sidon condition) = 0 (object/evidence/mod_multiset_n8.txt)

mod14.c checks a necessary condition only: every residue class mod d must receive exactly 56/d of the 56 edge sums.
mod_multiset.py is a Sidon-free version on label multisets mod d.

## Files
- wsearch.c (P1), mitm.py (P2), brute_n4.py, check_label.py: byte-identical to the copies in verify-it-yourself/,
  whose sha256 are pinned in object/DECISION.txt.
- wsearch_printall.c, wjoin.c (P3), mod14.c, mod_multiset.py: the run's other programs.
- REPRODUCE_run.md: the run's claim write-up, copied unchanged. It contains the proof of the translation reduction
  and the exhaustiveness argument. Paths in it (checkers/..., result/...) are the run's names. Here they are
  how-we-built-it/ (or verify-it-yourself/) and object/evidence/.
- PREREG.md: the run's preregistration, copied unchanged (frozen 2026-11-01T23:45:17Z, before any n = 8 output). It
  states null_test: not needed (an exhaustive decision checked by deterministic exact programs).
