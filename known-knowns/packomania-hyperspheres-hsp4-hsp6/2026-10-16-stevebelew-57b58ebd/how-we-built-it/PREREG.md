# PREREG (frozen before any attack output is scored)

date_utc: 2026-10-14 02:42 UTC (written right after the checker tests at 02:42:00 UTC; no attack has run yet)
target: packomania-hyperspheres-hsp4-hsp6, dimension d = 4 only (hsp4 table, N = 2..300)

## Criterion (verbatim from the bank)

"the FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin),
computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance, is STRICTLY GREATER
(direction: max) than that file's 12-decimal value for N re-fetched live immediately before claiming, by at least 1e-10
(the table carries 12 decimals; 1e-10 is 200x its rounding), AND the configuration is not isometric to the posted
hsp<d>-<N>.txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere), AND (d, N) does not
appear in a History-of-updates entry on the live hsp<d>.html newer than the one the scout fetched." Plus the queue rule.

## Statistic and checker

- Statistic: r* from checker/hsp_check.py (mpmath, mp.dps = 50, last 4 columns of each line, no tolerance), run on the
  candidate coordinate file exactly as saved by the attack.
- Table value: the row N of data/hsp4_radius.txt fetched 2026-10-14 02:40:17 UTC, and re-fetched once live before any claim.

## Thresholds (fixed now)

- Full win or p1: r*_candidate - r_table >= 1e-10, AND max sorted-distance difference to the posted hsp4-<N>.txt > 1e-8,
  AND N not in any hsp4 pending range, AND no newer history entry for (4, N).
- p3 (audit): a posted row counts as "not reproduced" only if |r*_posted - r_table| >= 1e-11 (the bank's parser-sanity bound).
- Anything with 0 < gain < 1e-10 is recorded as a near-miss, never claimed.
- p2 (extension N = 301..310) is not attempted in this run.

## Null design

null_test: not needed because the claim is an explicit object (a coordinate file) judged by a deterministic checker
against a posted table value, with no search statistic, no "beats chance" claim and no fitted threshold.

## Scope

Lens 1 (warm-polish): rows N in {9..25, 121} (p1 rows) first, then Specht rows N = 26 upward as the deadline allows.
Lens 2 (lattice-D4): D4-lattice fragments for N = 9..300, polished, compared row by row.
