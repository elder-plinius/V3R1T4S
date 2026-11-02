# CRITERION verdict: hsp4-N152

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:16Z

## Value computed here
- Object `claim/hsp4-152.txt` (sha256 c946063b...1d6d, matches CLAIM.md): 152 rows of 4 numbers, 152 distinct, no NaN. The coordinates are float64 reprs (the shortest has 12 significant digits).
- r* (mpmath, 50 digits, no tolerance) = 0.22097502706448416408815908921357097646062824532483
  - half min distance = 0.220975027064484272818718692987 (pair 6,87, 0-based)
  - 1 - max norm = 0.220975027064484164088159089214 (this term binds)
  - A second computation (exact Fractions for the squared terms, then a 60-digit sqrt) agrees to better than 1e-45.
- Live table row (evidence/hsp4_radius_live.txt): `152 0.220960306508`. r* - table = 1.4720556484164e-5.
- The live re-fetch for this panel is the evidence/ set fetched by the repository owner on 2026-11-01T14:32Z from an unrestricted machine. I checked every sha256 in FETCHED.md with sha256sum and all match. I made no web access myself.

## Clauses checked
- **1 Value**: r* = 0.22097502706448416409 (wall term binds); table 0.220960306508; r* - table = 1.472e-5 >= 1e-10. PASS.
- **2 Parser sanity**: the posted hsp4-152.txt (12 decimals) recomputes to r = 0.220960306507267268946652724825, which is header 0.220960306508 minus 7.33e-13. That is within 1e-11 of both the header and the table row, so clauses 3 and 4 apply. PASS.
- **3 Non-isometry**: the maximum absolute difference between the sorted multisets of all 11476 pairwise distances is 7.87e-3 (> 1e-8). The sorted centre norms differ by up to 1.68e-2 (for information). PASS.
- **4 Polish floor**: my own sequential LP (scipy HiGHS) polishes the posted coordinates. Constraints are pairs with d < 2r+margin and walls with |c| > 1-r-margin, linearized. A box trust region bounds every coordinate step. A step is accepted only if the exactly recomputed radius increases; otherwise the trust region shrinks. Each final radius was recomputed at 50 digits from the polished coordinates:

  | step0 | margin | shrink/grow | r (50-digit) | gain over header | its | stop |
  |---|---|---|---|---|---|---|
  | 1e-2 | 1e-2 | 0.5/1 | 0.2209605534331210183 | +2.469e-7 | 254 | no gain >1e-15 in 20 its |
  | 1e-3 | 1e-3 | 0.5/1 | 0.2209605534332860479 | +2.469e-7 | 399 | no gain >1e-15 in 20 its |
  | 1e-4 | 1e-4 | 0.5/1 | 0.2209603973224512727 | +9.08e-8 | 432 | no gain >1e-15 in 20 its |
  | 1e-2 | 5e-2 | 0.3/1 | 0.2209603122670607179 | +5.76e-9 | 43 | trust < 1e-13 |
  | 1e-3 | 2e-3 | 0.7/2 | 0.2209604758430992635 | +1.693e-7 | 289 | no gain >1e-15 in 20 its |
  | 1e-5 | 1e-4 | 0.5/1 | 0.2209605534330635692 | +2.469e-7 | 445 | no gain >1e-15 in 20 its |

  I restarted the best result twice more (step0 1e-3 with margin 5e-3, and step0 1e-6 with margin 1e-4). Both stopped at trust < 1e-13 with no further gain, at 0.2209605534332860479. That is the highest polished radius. r* minus the highest polished radius = 1.447e-5 >= 1e-9. PASS. The posted file itself polishes up by about 2.47e-7, which is an errata note for the table keeper and not part of this claim.
- **5 Not a relaxed copy**: The claim says it started from random, lattice-cut and shell seeds and from the lane's own neighbouring-N packings, and it names no posted packing as its start. I did not get the claimant's search code. My own evidence:
  - Contact graphs at tolerance 1e-9 differ. The claim has 464 pair contacts and 137 wall contacts, with degree histogram (deg 2..10) 1,0,13,30,59,33,8,5,3. The posted file has 461 pair and 136 wall contacts, with histogram (deg 0..10) 1,0,0,1,12,37,46,37,12,5,1.
  - The sorted distance multisets differ by 7.9e-3. They still differ by 8.2e-3 (mean 1.2e-3) from the polished posted packing.
  - The polished posted packing converges at 0.22096055, which is 1.45e-5 below the claim, so the claim is not in the posted packing's local basin.
  - Both packings share the generic 137-outer + 15-inner shell structure, but the inner-shell norms differ (claim 0.365..0.453, posted 0.371..0.436).

  Nothing indicates the claim derives from a posted packing. PASS.
- **6 History of updates**: hsp4.html shows "Last update: 06-Jul-2025". Its History entries are 04-Jul-2025 (N = 2–100), 05-Jul-2025 (extension to N = 200) and 06-Jul-2025 (extension to N = 300). None is newer than the table snapshot, and none names (4, 152) as an update. Row 152 shows 0.220960306508, the same as radius.txt. PASS.
- **7 Queue rule**: pending.html (dated 30-Oct-2026) lists no hsp4 range. The listed categories are csc, ccq, crt, csq, chx, cpt, crc, cxd, cci and ssp, plus one category-unspecified bundle, and no hsp4 range covers 152. PASS. **Caveat:** the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved. N = 152 must be re-checked against the live table once that bundle disappears from the pending list.
- **8 Moki & Julio MANIFEST**: the row `hsp4,152` has published_radius 0.220960306508 and new_radius 0.2209615356462587873029967 ("UNCLEAR (alignment)"). r* - new_radius = 1.349e-5 >= 1e-10. The other N = 152 rows are on other shelves (cpt, crc_*, hsp5, hsp6), and none refers to this cell. PASS.
- **9 Other prior work**:
  - The claims list has 29 entries and none is for hsp4 N = 152 (there are hsp4 claims for N = 170, 119 and others).
  - TROPHY_CASE.md has no hsp/hypersphere entry.
  - Spherical-code construction: (4,152) has c = 0.848701931506, which gives s/(2+s) = 0.21571315257953195861 (r* exceeds it by 5.26e-3). (4,151) with a centre ball gives min(1/3, 0.21589229982354240333) = 0.2158923 (r* exceeds it by 5.08e-3). Both are below r*.

  PASS.
- **Clause-by-clause reading of the verbatim criterion**:
  - d = 4 is in {4,5,6}, and N = 152 is listed in the live hsp4 radius.txt.
  - r* is the feasible radius in the unit ball centred at the origin, computed in mpmath at 50 digits with no tolerance.
  - r* is strictly greater than the 12-decimal live value, by 1.47e-5 >= 1e-10.
  - The posted file reproduces its header to 7.3e-13 < 1e-11, so the extra conditions apply:
    - The configuration is non-isometric (7.9e-3 > 1e-8).
    - r* exceeds every polish of mine (6 schedules plus 2 restarts, largest steps 1e-2, 1e-3 and 1e-4, each run until it stopped improving) by 1.45e-5 >= 1e-9.
  - The configuration is not a relaxed copy (clause 5), and the claim names no posted start.
  - No newer History entry names (4, 152).
  - The 'coordinates unavailable' clause concerns hsp5/hsp6 only and does not apply.
  - Queue rule: N is in no range, and the caveat is stated above.
  - No submission is made.

  All conditions are met.

## Decision
Every clause passes on numbers I computed myself. r* = 0.22097502706448416409 beats the live table (0.220960306508) by 1.47e-5. It beats the best of my own trust-region polishes of the posted packing (0.22096055343329) by 1.45e-5, and it beats the Moki & Julio manifest radius by 1.35e-5. The configuration is clearly non-isometric to the posted packing, and nothing indicates it is a relaxed copy of it. Two qualifications remain. The "live" data is the owner's 2026-11-01T14:32Z fetch, with the hashes verified here. The 26-Sep-2026 Moki & Julio *many* bundle is category-unspecified and cannot be resolved, so N = 152 must be re-checked against the live table once that bundle leaves the pending list.

pass: true
