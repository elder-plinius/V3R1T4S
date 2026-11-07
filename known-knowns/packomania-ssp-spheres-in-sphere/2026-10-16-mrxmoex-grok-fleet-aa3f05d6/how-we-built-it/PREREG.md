# PREREG (written 2026-10-16T16:07:58Z)
NOTE (honesty): the 90-row result was already measured (results_ssp.tsv, repro_local_output.txt) before this file existed. This PREREG freezes the rule only for the cross-checks and the control run made after it. It is not a pre-measurement freeze of the original discovery.
criterion: for every N in the N column of object/ssp_radiustxt_errata.csv: (1) the coordinate file has N spheres; (2) r*(coords) < radius.txt(N) - 1e-10; (3) |ssp.html(N) - r*(coords)| <= 1e-10.
statistic: r* = min(min_{i<j}|ci-cj|/2, 1 - max|ci|), container radius 1, at >= 50 significant digits (mpmath dps=50, Decimal prec 60, or exact rationals).
thresholds: margin 1e-10 (12-decimal tables). The claim holds iff all 90 rows satisfy (1)-(3) in each cross-check.
null_test: not needed because the claim is an explicit deterministic comparison of posted numbers, not a search or a "beats chance" statistic.
control (sanity, not a kit null test): the same checker on every other N>1000 row that has coordinates (the 21 non-flagged rows) must NOT flag them. Also: a corrupted copy (radius.txt value replaced by the html value) must make the row fail criterion (2).
