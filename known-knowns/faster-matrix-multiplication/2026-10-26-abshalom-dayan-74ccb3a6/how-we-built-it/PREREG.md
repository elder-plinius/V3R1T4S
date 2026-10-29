# PREREG (frozen 2026-10-26T22:03:13Z, before any attack output of this run)

criterion (verbatim from bank/targets.json, fmm-catalogue-small-format-rank): see target.md, section "Success
criterion (verbatim ...)", copied unchanged.

statistic / checker: the scheme in runs/2026-10-25-0343/leads/14x15x15_r1836/stage/object/ (or a byte-identical copy)
must (a) satisfy all 14*15*15*15*14*15 = 9,922,500 Brent equations for <14,15,15> exactly over Q, checked by the
package checker check_scheme.py AND by an independently written checker; (b) have exactly r = 1836 terms, every term
with three nonzero factors; (c) agree with exact C = AB on at least 3 random integer instances.

thresholds: r = 1836 must be strictly below 1848 (min of the four live criterion sources as fetched this run) and
strictly below the merged 1842; and strictly below any rank for (14,15,15) or a permutation in any pull request of
the repo, open or closed, found by the search right before the panel and again right before packaging. Any tie or
better: dead line, no claim.

null_test: not needed because the claim is an explicit object checked by a deterministic exact checker against a table value (no search statistic).
