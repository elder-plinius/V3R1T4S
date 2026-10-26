# PREREG (frozen 2026-10-24T12:25:01Z, before any attack output on the chosen cells is scored)

target: dna-codes-gc-king-table
cells: primary (n,d,w) = (15,12,7), live table value 15 (unmarked, 'v'); secondary (15,11,7), live table value 34
(unmarked, 'v'). Table file data/dnacodes.html sha256 25d6e9f88262fbb07c95841225cb3202aa29eb31f7f72d24b43e9c595bdb18c5,
fetched 2026-10-24T12:17:24Z. Only sanity runs on cells (6,4) and (10,7) exist so far (calibration of gcmc).
Note: in scouting, plotkin_gc.py (plain quaternary Plotkin, no GC term) printed slack 0 at M=16 for (15,12); this is
why King's GC-Plotkin bounds (Theorem 4) are computed in the table-auditor lens. Nothing else has been measured.

## Criterion (verbatim, bank)
A plain-text list of codewords for some (n,d) whose table entry on https://rambutan.umassmed.edu/king/dnacodes.html is NOT followed by '.' or ':' such that a checker confirms all words have length n over {A,C,G,T}, exactly the table's GC-content w (w = floor(n/2), confirm from King 2003), pairwise Hamming distance >= d, are distinct, and the count is strictly greater than the table entry re-fetched live immediately before claiming, AND strictly greater than any value for the same (n,d,w) found by a novelty search of post-2010 literature (e.g. Limbachiya-Gupta-Rao altruistic-algorithm papers, Montemanni-Smith, arXiv 1903.03535, 2108.02033).
Partial wins in scope: tie-unmarked-mid (reproduce an unmarked 'v' entry with n >= 14 from scratch with our own
search, checker-confirmed); new-optimality-proof only if obtained by a method that matches its literal wording.

## Statistic / checker
checker/check_gc_code.py CODEFILE N D data/dnacodes.html (sha256 e9e5554946b8d55d2d957af026a40b182947b8cb7f7e3cfe2f459125adf3700b;
tested on 1 positive and 2 negatives, checker/checker_tests_output.txt): length, alphabet, GC count = floor(N/2),
distinctness, all-pairs Hamming >= D, and size vs the parsed table cell.
Upper bounds: attempts/table-auditor/code/king_bounds.py (King 2003 Theorems 2 and 4, with an exact DP cross-check).

## Thresholds (fixed now)
- size > table value and checker VALID -> candidate for the full criterion; at most PROMISING in this run (needs
  live re-fetch, novelty search and a three-skeptic panel). If such a size exceeds a recomputed King upper bound, it
  is a checker/program bug, never a claim.
- size == table value at an unmarked 'v' cell with n >= 14, produced from scratch by code in attempts/, checker VALID
  -> candidate for partial win tie-unmarked-mid (a tie, never a record); at most PROMISING.
- otherwise negative; report the best size and the space actually covered (heuristic searches cover nothing).
- table audit: an unmarked cell whose table value equals the recomputed King upper bound is reported as "already
  optimal by [K] Theorem 2/4, unmarked on the page" (label KNOWN: it follows from a published theorem); any table
  value above the bound is reported as a table/bound conflict.
Only objects produced by code in attempts/ count (no codewords copied from the site's codes/ files or papers).

## Null design (significance rule for the search lens)
null_test: required
Statistic: size of a valid code (checker VALID) at (15,12,7). Controls: 400 random maximal codes from
attempts/null-and-leak-auditor/code/nullgreedy.c (random-order greedy over all 210,862,080 words), seeds 1..400.
The real result (the largest checker-valid code produced by the attack lenses for (15,12,7)) must be strictly larger
than every control (best_control < real). If time allows, the same with 400 controls at (15,11,7) (reported, not
required). Precision: integer arithmetic only; programs are deterministic given the seed.

## Code freeze (sha256 at freeze time; any later change is re-frozen in a dated PREREG.v2.md)
7d0e5e2415c1caec3f5a7cf1a576ba2cdb6f70513ee28eab2bacd7b8d2d872b7  attempts/evaluator-first/code/gcmc.c
18f05409983739c1467431785074233f0d44b24d45d140a47fabe4508174be33  attempts/null-and-leak-auditor/code/nullgreedy.c
21f90ca3bca4e9e95597c6a97de0343657f693e7f9fdd78bf5abd2d691e0c3de  attempts/far-import/code/mseq.py
8e1dceaf48b115d008be996f5bd368c63aa3b343dd08f5b1b1f509ade207f8bd  attempts/table-auditor/code/king_bounds.py

## Budget
standard: 4 lenses (table-auditor, far-import, evaluator-first, null-and-leak-auditor), ~3 h wall clock from
2026-10-24T12:17:02Z; no new line of work after ~14:40Z. Jobs run with nice -n 19 and timeout, PIDs recorded in
each lens NOTES.md; at most 4 concurrent n=15 jobs (~420 MB each; box has ~2.9 GB available).
