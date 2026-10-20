# REPRODUCE skeptic report — V3R1T4S run 2026-10-20-0858 (N=3949)

context: subagent

Role: REPRODUCE skeptic (fresh context). I read ONLY the `claim/` package
(CLAIM.md, candidate_n3949.txt, posted_cci3949.txt, checker.py was executed but
my own checker was written from the definition first, radius_3949.txt,
table-record.txt, REPRODUCE.md, SHA256SUMS). No attempts/, dossiers, or logs
were consulted. Every number below was recomputed independently.

## Quoted definition (from CLAIM.md success criterion, verbatim)

> Success means a file of N centers (x_i, y_i) for one N listed in
> https://packomania.com/cci/txt/radius.txt such that the FEASIBLE radius r* := min(
> min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ), computed in mpmath at 50 digits directly
> from the submitted coordinates (no tolerance), is STRICTLY GREATER (direction: max) than
> the 30-decimal radius for that N re-fetched live immediately before claiming, by at
> least 1e-11, AND the configuration is not isometric to the posted cci<N>.txt one (sorted
> distance multisets differ) ...

## Check 1 — candidate file sanity (my own parser)
- `candidate_n3949.txt`: exactly 3949 lines, each `index x y` (3 tokens),
  indices sequential 1..3949, all coordinates finite. PASS.

## Check 2 — my own feasible-radius computation (written from the definition above)
Double precision, full O(N^2) pair scan + container scan, independent code:
- min_{i<j}|c_i−c_j|/2 = 0.014967852371309442 (arg pair indices 3690, 3928)
- 1 − max_i|c_i|      = 0.014967835309584898 (arg index 3928, binding term)
- r*_double = 0.014967835309584898 (container binds; pair term sits +1.706e-11 above it)
- margin vs table value 0.014965462848801963307763269064: 2.372461e-06
  → ≥ 1e-11 ✓ and of the claimed order (+2.372e-06) ✓.

## Check 3 — high-precision (mpmath, 50 digits) independent spot check
Written independently; parses decimal strings directly at 50 digits:
- max_i|c_i| over all 3949 points = 0.98503216469041505557920787516989941153168434632378 (idx 3928)
- r* (50-digit) = 1 − max|c_i| = 0.014967835309584944420792124830100588468315653676217
- closest-pair spot check |c_3690 − c_3928|/2 = 0.014967852371309441032286020207121459235624664169877
  (agrees with the double value to 1e-16; sits above the container term, so the
  container term binds with 1.7e-11 slack — seven orders of magnitude above
  double rounding error, so the binding choice is robust)
- 250-point subset: all pairwise half-distances at 50 digits ≥ 0.014968336923799925,
  consistent (nothing tighter than the binding term).
- 50-digit margin = r* − table = 2.372460782981113e-06 ≥ 1e-11 ✓.
- Note: the author's checker prints values through float() (display only); its
  printed r* 0.014967835309584944999961031442 is exactly the nearest-double
  expansion of my 50-digit r* (verified: float(cont) formats to that string).
  Underlying values agree exactly.

## Check 4 — author's checker run (background, exit 0)
`python3 checker.py candidate_n3949.txt 3949` printed:
- N=3949  r*=0.014967835309584944999961031442
- table=0.014965462848801963299805173335
- margin r*-r_table = 2.372e-06  (need >= 1e-11 to beat)
→ PASS. Observation: checker.py reads its table value from the run-level
`data/radius.txt` (relative path `../data`), not from `claim/radius_3949.txt`;
the N=3949 line in both files is byte-identical
(`3949 0.014965462848801963307763269064`), so the margin is unaffected.

## Check 5 — non-isometry (my own code, sorted pairwise-distance multisets)
- 7,795,326 pairs in each file (= 3949·3948/2) ✓
- pairs differing > 1e-9: 7,795,316 of 7,795,326
- max abs diff: 0.0050562414439589976; median abs diff: 0.0002720113633978283
→ multisets differ → NON-ISOMETRIC ✓.

## Check 6 — SHA256SUMS
`sha256sum -c claim/SHA256SUMS` (from the run dir):
- claim/candidate_n3949.txt: OK
- claim/posted_cci3949.txt: OK
Both match the hashes quoted in CLAIM.md.

## Caveats / notes
- Determinism: all computations are deterministic; mpmath pair loop and my own
  code agree; no randomness anywhere.
- The 50-digit r* (…444207921248301…) rounds to the claim's stated
  0.0149678353095850 ✓.
- table-record.txt's queue/history caveats (Moki & Julio "*many*" 4666 bundle,
  category-unspecified) are out of REPRODUCE scope; noted for the panel.

pass: true
