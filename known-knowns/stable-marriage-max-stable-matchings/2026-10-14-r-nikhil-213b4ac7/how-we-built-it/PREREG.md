# PREREG: stable-marriage-max-stable-matchings (lane A)
written: Wed Oct 14 15:20:44 UTC 2026 (before any attack output exists; the dry run of 2026-10-14-1426 ran no search)

## Criterion (verbatim from charter.md)
> for an n whose maximum is not known, give a stable-marriage instance (complete strict preference lists for n men
> and n women) with strictly more stable matchings than the best known instance of size n. Cells in order: n = 13
> (beat 7,123), n = 15 (beat 27,059), n = 14 (beat 20,176; no search has touched it), and n = 7 (beat 81) as a cheap
> calibration cell. Do not aim at n = 6, 8, 10, 12 or 16, which are conjectured exact.

## Bars used this run (from this run's fetch of https://oeis.org/A357271/a357271_1.txt, sha256
95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47, and the dry run's re-count of Jo 2026)
- n = 13: strictly more than 7123 stable matchings.
- n = 15: strictly more than 27059.
- n = 14: strictly more than 20176.
- n = 7 (calibration only, no claim): 85 (Jo 2026, Zenodo, unreviewed; OEIS shows 81). Reaching 85 is a tie, not a win.
A tie is not a record. One cell (one n) per claim.

## Statistic / checker
The exact number of stable matchings of an explicit n x n instance (complete strict lists both sides), computed by
checker/count_stable.py (two independent exact methods: rotation-lattice walk with per-matching stability re-check,
and brute-force backtracking) and by the C counter written this run (attempts/quoter/code/smcount.c), all three
agreeing. A result counts only if the instance file is saved and all counters agree on the same integer.

## Thresholds
win for cell n  <=>  exact count > bar(n) above, instance saved, three counters agree.
Any count <= bar(n) is not a win (ties included). No partial wins are enumerated for this quarry.

null_test: not needed because the result is an explicit object (a preference profile) checked by a deterministic
exact counter against a table value; there is no statistic that could beat chance.
