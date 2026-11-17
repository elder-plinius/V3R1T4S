Frozen: 2026-10-15 16:49:04 UTC

## Criterion verbatim
- **Question:** for an n whose maximum is not known, give a stable-marriage instance (complete strict preference lists
  for n men and n women) with strictly more stable matchings than the best known instance of size n. Cells in order:
  n = 13 (beat 7,123), n = 14 (beat 20,176; a 24,992 instance of ours awaits its panel), n = 15 (beat our own submitted
  27,510) and n ≥ 17 (beat the OEIS A357271 b-file composition bounds). Calibrate search speed
  first by reproducing the 85 stable matchings claimed at n = 7 from random starts (n = 6 and n = 7 are claimed exact
  by an unreviewed preprint). Do not aim at n = 6, 7, 8, 10, 12 or 16.
- **Shape:** record (explicit preference lists; stable matchings counted exactly by your own enumerator: closed subsets
  of the rotation poset, or exhaustive enumeration, cross-checked).


## Decision rule
First panel inherited n19=896068 versus strict prior bar889780, an audit of an earlier frozen discovery. New searches must exceed all same-size local candidates, regardless of panel status: n13=9796, n14=24992, n15=38986, n17=289548, n18=570272, n19=896068, n20=3548320, n21=5382608, n22=13210944, n23=19025864, n25=160906464, n26=404671616, n27=580593152, n28=2497797760. Independent deterministic exact counting decides each object claim. One cell per claim and its own panel. No maximum claim.

null_test: not needed because explicit strict preference profiles are checked by deterministic exact enumeration and compared to integer bounds.

No new lines after minute84; at most six CPU threads, seven GB RAM, six GB new disk; report by minute110.
