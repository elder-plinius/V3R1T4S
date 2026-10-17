# How we found it

Contributor text, unverified.

A small team of language-model agents worked this target on 2026-10-15 after reading pull request #149 on this
repository, which lowered the <4,6,7> count with a transposed common-subexpression search; that was the prompt to try
the transposition principle on the W map of every format with sides at most 8. The brief fixed the bank's criterion,
the eligibility rule (the scheme's rank must equal the live best rank) and the counting convention before any search.

What failed first: plain pair-greedy common-subexpression elimination (`rectopt.c`, `slpopt.c`) reproduced Perminov's
counts but rarely beat them, and a Kronecker-structured two-stage program for the product schemes was worse than a
direct search. What worked: a distance-guided search with cancellation (Boyar-Peralta style) restricted to ternary
intermediates, run on the tall maps U, V and W^T with many random restarts, keeping Perminov's own program for a map
whenever ours was not strictly shorter. The counter was calibrated first: it reproduces the cr value of every
addition_reduced_ZT file at the best rank with sides at most 8 (49 files).

tools/opt_scheme.py splits the scheme into its three maps and runs, per map, (a) a Boyar-Peralta-style distance-guided
search with cancellation over ternary vectors (src/bpopt.c) on the tall maps U, V and W^T (the W program is then obtained
by the transposition principle, cost(W) = cost(W^T) + r - n*p), and (b) randomized iterated pair-greedy CSE on the
transposed maps (src/slpopt.c), keeping Perminov's own program for any map where ours is not strictly better.

Before claiming, the orchestrator re-fetched Perminov's repository tree, the Lille page, fmm_sota.json and
matmulcatalog's COVERAGE.md once each, read the 2026 preprints on addition reduction (including IACR ePrint 2026/849,
whose PDF needed a manual download), and ran a fresh three-skeptic panel (reproduce, novelty, criterion). The 3x3x3
rank-23 program from the same sweep (57 additions) was withdrawn when the novelty check found published comparable
counts of 56 and 55; it is not part of this package.
