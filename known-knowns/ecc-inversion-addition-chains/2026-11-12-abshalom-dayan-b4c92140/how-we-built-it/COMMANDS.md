# How the chain was built

1. Dictionary search (acw.c, C99, no dependencies). Simulated annealing over a dictionary of integers below 2^21 that must itself be an addition chain; each dictionary is scored by a dynamic program for the main line (states: bit position and deficit, kept in a ranked beam) plus a ladder for the top run of ones.

       cc -O2 -o acw acw.c
       mkdir out2s
       OUT=out2s KB=256 CYC=150000 ./acw 2 1009 21 3600 0.5 0.15 search_init.txt

   The start dictionary (search_init.txt; the original run named it log2/init_c2_s1009.txt and ran under nice -n 15) is the set of values below 2^21 of Brian Smith's published 282 chain. The random seed is fixed and the temperature follows the move count, so a rerun retraces the same moves; the clock only decides when the run stops, and it needs most of an hour of one core to pass move 563,759, where the 281 appears. We replayed this command on 2026-11-12 and got the same four improvements and the same final dictionary. search_out.txt lists the improvements it wrote (the search's narrow beam reads the start dictionary as 284; the exact builder gives 282 for it); the last line, reported at 2026-11-11T21:53:28Z, is the dictionary of this package:

       1 2 4 8 16 32 64 128 256 257 289 513 1026 2052 2309 4361 8722 17444 34888 69776 70033 139809 279618 559236 699045 699061 699062 1258297 1817533 2097151

2. Chain from the dictionary (build_wide.py with build_chain.py, Python 3 standard library, deterministic, about a minute):

       python3 how-we-built-it/build_wide.py 2 "1 2 4 8 16 32 64 128 256 257 289 513 1026 2052 2309 4361 8722 17444 34888 69776 70033 139809 279618 559236 699045 699061 699062 1258297 1817533 2097151" rebuilt.txt 3000
       cmp rebuilt.txt object/chain.txt && echo identical

   Chain file first written 2026-11-11T21:54:26Z.

3. One-edit baseline for the seed (baseline/): trivial_edits.py scores the seed dictionary and every dictionary one edit away from it with acw_big.c (acw.c with a larger state table, beam 2048). Output: baseline/one_edit.txt.

       cd how-we-built-it/baseline && cc -O2 -o acw_big acw_big.c && python3 trivial_edits.py 2 22 seed_dictionary.txt 2048 one_edit_again.txt

PREREG.md is the rule sheet for this cell; PREREG.original.md is the first rule sheet of the search (all four scalar cells, 2026-11-10), unedited.
