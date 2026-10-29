# PREREG (frozen 2026-10-28T22:03:49Z, before any attack output of this run)

criterion (verbatim from bank/targets.json, fmm-catalogue-small-format-rank): see target.md, section "Success
criterion (verbatim ...)", copied unchanged by script from the bank.

carrier: runs/2026-10-25-0343/leads/13x14x15_r1644/D1709_ax2.c8_r1644.json (cut 8). The cut-30 scheme is a second
object of the same rank and cell; it is cited, not claimed (one object per claim). The carrier is exported to the
plain u/v/w text format (one line per term) for the package.

statistic / checker: the scheme (format 14x15x13, sorted (13,14,15)) must (a) satisfy all 14*15*15*13*14*13 =
7,452,900 Brent equations for <14,15,13> exactly over Q, checked by a stdlib package checker (check_scheme.py, as in
the two earlier packages) AND by the independently written checker mycheck.py (run 2026-10-26-2200); (b) have exactly
r = 1644 terms, every term with three nonzero factors, no two terms proportional; (c) agree with exact C = AB on at
least 3 random integer instances; (d) be rebuilt byte-identically from LITA's published 15x15x15 rank-1977 file by a
deterministic script (three cuts with fixed vectors and seeds).

thresholds: r = 1644 must be strictly below 1681 (min of the four live criterion sources as fetched this run) and
strictly below the merged value 1645 (pull request #166; POLICY.md fast-matrix-multiplication rule 1), and strictly
below any rank for (13,14,15) or a permutation in any pull request, open or closed, found by the scan right before the
panel and again right before packaging. Any tie or better: dead line, no claim. Known positive for both checkers: the
merged repo/known-knowns/faster-matrix-multiplication/2026-10-15-anonymous-c6d1e0ab-49ee1c4f/object/13x14x15_r1645_Q.json must PASS; planted mutants of the carrier must FAIL.

null_test: not needed because the claim is an explicit object checked by a deterministic exact checker against a table value (no search statistic).
