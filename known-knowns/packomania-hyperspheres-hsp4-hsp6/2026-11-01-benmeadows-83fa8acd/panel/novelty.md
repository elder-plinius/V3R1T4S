# NOVELTY verdict: hsp4-N217

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:21Z

## Value computed here
Own code in `work/` (common.py, c123.py, polish.py), mpmath at 50 digits, no tolerance.
- Object: 217 rows x 4 coordinates, 19-22 decimals each, no duplicates, no NaN; sha256 83fa8acd...0bc matches CLAIM.md. The `#` comment lines in the object were ignored.
- r* = 0.20344247849929273721302003487040897978541806734019 (the wall term 1 - max|c_i| binds; half min distance = 0.2034424784992927977..., pair (14,189) in 0-based indexing).
- Live table row (evidence/hsp4_radius_live.txt): `217 0.203438871092`. r* - table = 3.6074072927e-6.
- Evidence files are the live re-fetch for this panel (fetched by the repository owner 2026-11-01T14:32Z from an unrestricted machine). I checked all sha256 values listed in FETCHED.md with sha256sum and they all match. The posted file has sha256 448bca43...6113. This sandbox had no web access.

## Clauses checked
- 1 Value: r* - table = 3.607e-6 >= 1e-10. **pass**
- 2 Parser sanity: the posted hsp4-217.txt (12-decimal coordinates) gives r = 0.203438871091004370... (the wall term binds), which is 9.96e-13 below both its header and the table row (< 1e-11). Clauses 3 and 4 therefore apply. **pass**
- 3 Non-isometry: across the 23436 pairwise distances, the sorted multisets differ by at most 6.648e-3 (> 1e-8). For information, the sorted centre norms differ by up to 0.233. **pass**
- 4 Polish floor: I wrote my own SLP polisher (HiGHS LP on near-active pairs and wall constraints, a box trust region, a step accepted only if the exactly recomputed radius increases, otherwise the region shrinks). I ran six schedules on the posted coordinates and recomputed every final radius at 50 digits:
  - D0=1e-2, margin 0.05, shrink 0.5: 0.2034388728342675523, gain +1.742e-9, 94 iterations, stopped after 20 iterations with no gain > 1e-15
  - D0=1e-3, margin 0.02, shrink 0.5: 0.2034388728341957545, gain +1.742e-9, 89 iterations, same stop
  - D0=1e-4, margin 0.01, shrink 0.5: 0.2034388728340434269, gain +1.742e-9, 87 iterations, same stop
  - D0=1e-2, margin 0.1, shrink 0.25: 0.2034388728338811733, gain +1.742e-9, 69 iterations, stopped when the trust region fell below 1e-13
  - D0=1e-3, margin 0.05, shrink 0.7: 0.2034388728342507259, gain +1.742e-9, 106 iterations, 20 iterations with no gain
  - D0=3e-2, margin 0.1, shrink 0.5: 0.2034388728341324097, gain +1.742e-9, 89 iterations, 20 iterations with no gain

  The best polish reaches 0.20343887283427, and r* - best = 3.6057e-6 >= 1e-9. **pass**
- 5 Not a relaxed copy: I do not have the claimant's search code. The claim says it started from lane hsp4-b's own seeds (random, two-shell and D4-cut seeds, then insertion into its own N-1 packing) and names no posted packing as its start. My own evidence agrees:
  - Every polish of the posted file stalls about 3.6e-6 below the claim.
  - The contact structures differ. At tolerance 1e-9 the claim has 668 ball-ball contacts and 187 wall contacts; the posted file has 654 and 186.
  - The degree sequences differ (claim: 2 rattlers and maximum degree 10; posted: 4 isolated balls plus 1 with degree 1, and maximum degree 11).
  - The shell populations differ: 188 outer, 28 middle, 1 central for the claim against 187 outer, 29 middle, 1 central for the posted file.
  - The distance multisets differ by 6.6e-3.

  Nothing indicates the claim derives from the posted packing. **pass**
- 6 History of updates: hsp4.html shows "Last update: 06-Jul-2025". Its History of updates has only three entries: 04-Jul-2025 (N=2-100), 05-Jul-2025 (extension to N=200) and 06-Jul-2025 (extension to N=300). There is no entry newer than the table snapshot, and none names (4, 217) after it. **pass**
- 7 Queue rule: pending.html (dated 30-Oct-2026) lists no range in the hsp4 category. The listed categories are csc, ccq, crt, csq, chx, cpt, crc, cxd, cci and ssp, plus the Moki & Julio *many* bundle. N=217 lies in no hsp4 range. **pass**
  CAVEAT: the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle does not say which category it belongs to and cannot be resolved. N = 217 must be re-checked against the live hsp4 table once that bundle disappears from the pending list.
- 8 Moki & Julio manifest: the row `hsp4,217` gives published_radius 0.203438871092 and new_radius 0.2034388728345505912847004 (labelled REFINEMENT, about the same as my own polish ceiling). r* - new_radius = 3.6056e-6 >= 1e-10. The other rows with N = 217 belong to other shelves (ccq, crc_*, crt, csc, hsp5). No hsp4 row carries a value near 0.20344. **pass**
- 9 Other prior work:
  - Claims list: no open, closed or merged PR for hsp4 N=217. The listed hsp4 claims are N = 30-170 and 301.
  - TROPHY_CASE.md: no hsp4 entry.
  - The arXiv snapshots contain nothing relevant.
  - Spherical-code constructions from spherical_plain_live.txt: (4,217) has c = 0.881471958903, giving s/(2+s) = 0.1957807616; (4,216) has c = 0.880886649220, giving min(1/3, s/(2+s)) = 0.1961688532. Both are below r*, by 7.66e-3 and 7.27e-3. **pass**

## Decision
The configuration is valid. Its feasible radius 0.2034424784992927372 beats the live table value by 3.61e-6, the Moki & Julio manifest value by 3.61e-6, and the best of six independent polishes of the posted packing by 3.61e-6. That polish ceiling is +1.74e-9 above the header, which shows the posted packing is a local optimum the claim does not come from. The contact graph and shell structure differ from the posted packing. No prior-work source covers the cell: there is no hsp4 history entry after July 2025, no hsp4 pending range, no claim PR or trophy entry, and the spherical-code constructions are below r*. One caveat remains: the category-unspecified Moki & Julio *many* bundle of 26-Sep-2026 cannot be resolved, so N = 217 must be re-checked against the live table once that bundle leaves the pending list. No injection was suspected; the object's comment lines state values, and I ignored them.

pass: true
