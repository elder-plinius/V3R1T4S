# PREREG (frozen 2026-10-27T22:02:57Z, before any attack output of this run)

criterion (verbatim from bank/targets.json, fmm-catalogue-small-format-rank): see target.md, section "Success
criterion (verbatim ...)", copied unchanged (checked equal to the bank string by script).

statistic / checker: the scheme in runs/2026-10-25-0343/leads/12x13x13_r1270/claim/object/ (or a byte-identical
copy) must (a) satisfy all 12*13*13*13*12*13 = 4,112,784 Brent equations for <12,13,13> exactly over Q, checked by
the lead's package checker check_scheme.py AND by an independently written checker; (b) have exactly r = 1270 terms,
every term with three nonzero factors, no duplicate terms; (c) agree with exact C = AB on at least 3 random integer
instances.

thresholds: r = 1270 must be strictly below 1274 (min of the four live criterion sources as fetched this run) and
strictly below any rank for (12,13,13) or a permutation merged in this repo or in any pull request, open or closed,
found by the search right before the panel and again right before packaging. Any tie or better: dead line, no claim.

null_test: not needed because the claim is an explicit object checked by a deterministic exact checker against a table value (no search statistic).
