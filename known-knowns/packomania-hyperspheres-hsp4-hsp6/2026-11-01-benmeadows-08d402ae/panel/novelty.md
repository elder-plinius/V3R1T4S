# NOVELTY verdict: hsp4-N215

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:19Z

## Value computed here
r* (mpmath, 50 digits, from claim/hsp4_N215.txt, 215 centres x 4 coords, comment lines ignored):
r* = 0.20376854965104970107115404162994178816907422394072
(binding term 1 - max|c_i|; half min distance = 0.203768549651049746690911504555)
Live table row N = 215 (evidence/hsp4_radius_live.txt): 0.203682998566. r* - table = 8.5551085049701e-5.

Evidence files are the owner's re-fetch of 2026-11-01 14:32Z from an unrestricted machine; this panel treats them as the
live re-fetch. All sha256 values in evidence/FETCHED.md were recomputed with sha256sum and match. Archive
hsp4_coords.tar.gz sha256 b929acc815b5b4e12e4b7654af23a58483d8cb0d44af804b231203ca935163df (same as the bank page cites).
Procedural note: an initial `ls -R` of the panel cell directory showed the names of the sibling folders; none of their
contents were opened. All code is in work/ (common.py, c123.py, polish.py).

## Clauses checked
- 1 Value: r* = 0.2037685496510497010711540416...; table 0.203682998566; r* - table = 8.555e-5 >= 1e-10. PASS.
- 2 Parser sanity: posted hsp4-215.txt (215 rows x 4 coords) gives r = 0.203682998565191464988 at 50 digits; header
  0.203682998566; difference -8.09e-13 (< 1e-11), equal to the table row. PASS; clauses 3-4 apply.
- 3 Non-isometry: sorted pairwise-distance multisets (23,005 distances) max |diff| = 0.01220 > 1e-8. PASS. (Sorted centre
  norms differ by up to 0.2374, for information.)
- 4 Polish floor: own SLP polish of the posted file (HiGHS LP on pairs with d < 2r + margin + 4*delta and centres with
  |c| > 1 - r - margin - 4*delta, box trust region delta, accept only on exact radius increase). Results (final radii
  recomputed at 50 digits from the polished coordinates):
  - A: max step 1e-2, shrink 0.5, grow 2, margin 1e-6: 0.203682998776312279193, gain over header +2.1031e-10, 59 iters, stop: 20 iters with no gain > 1e-15.
  - B: max step 1e-3, shrink 0.5, grow 2, margin 1e-6: 0.203682998776131686569, +2.1013e-10, 62 iters, stop: 20 iters no gain.
  - C: max step 1e-4, shrink 0.5, grow 2, margin 1e-6: 0.203682998776199383667, +2.1020e-10, 61 iters, stop: 20 iters no gain.
  - D: max step 1e-2, shrink 0.25, no grow, margin 1e-3: 0.203682998775941450988, +2.0994e-10, 38 iters, stop: trust region < 1e-13.
  - E: max step 1e-3, shrink 0.7, grow 1.5, margin 1e-4: 0.203682998776163667320, +2.1016e-10, 74 iters, stop: 20 iters no gain.
  Highest polished radius 0.2036829987763123; r* - highest = 8.555e-5 >= 1e-9. PASS.
- 5 Not a relaxed copy: the claim states it came from lane hsp4-b's own seeds (random, two-shell, D4-cut; N = 214..217 by
  inserting a ball into the lane's own N - 1 packing) and names no posted packing. I do not have the claimant's search
  code. My own evidence: the posted file polishes to a local optimum only ~2.1e-10 above its header under five schedules,
  i.e. it sits in a basin ~8.6e-5 below r*; distance multisets differ by 0.0122; contact graphs differ (tolerance 1e-9:
  claim 661 ball contacts + 186 boundary = 847, degree histogram [2,0,0,0,0,19,52,67,47,25,2,1]; posted 656 + 181 = 837,
  matching hsp4.html's 837, histogram [4,0,0,0,0,21,49,64,55,16,4,2]); sorted centre norms differ by up to 0.237. Nothing
  indicates derivation from the posted packing. PASS.
- 6 History of updates: hsp4.html "Last update: 06-Jul-2025"; entries 04-Jul-2025 (N=2-100), 05-Jul-2025 (to N=200),
  06-Jul-2025 (to N=300). The last one covers N=215 but it is the table snapshot itself, not newer than it; no newer entry
  names (4, 215). PASS.
- 7 Queue rule: pending.html (30-Oct-2026) lists ranges only for csc, ccq, crt, csq, chx, cpt, crc, cxd, cci, ssp and one
  '*many*' bundle; no hsp4 range, so N = 215 lies in none. PASS. Caveat (required): the 26-Sep-2026 'Moki & Julio *many*
  4666 candidates' bundle is category-unspecified and cannot be resolved; N = 215 must be re-checked against the live
  hsp4 table once that bundle disappears from the pending list.
- 8 Moki & Julio MANIFEST: row `hsp4,215,0.203682998566,0.2036829987763697355195576,1.032829e-09,REFINEMENT,dp`.
  r* - new_radius = 8.555e-5 >= 1e-10. PASS. No other row could be the same cell: other N=215 rows are ccq, crc_200..700,
  csc, ssp (different problems); no manifest value near 0.20376. (Their new_radius equals a polish of the posted file,
  agreeing with my polish floor to ~6e-14.)
- 9 Other prior work: claims_packomania-hyperspheres-hsp4-hsp6.json has no open, closed or merged claim for hsp4 N=215
  (hsp4 N claimed: 30,35,42,48,54,62,63,64,66,67,69,74,75,79,80,81,83,88,89,91,94,104,111,119,170,301);
  claims_spherical-codes-cohn-table.json has none either; TROPHY_CASE.md has no hsp4/hypersphere/215 entry; the arXiv
  extracts contain nothing relevant. Spherical-code constructions from spherical_plain_live.txt: (4,215) c = 0.880272662054
  gives s/(2+s) = 0.196574535420 (r* - it = 7.19e-3); (4,214) c = 0.879945189010 with centre ball gives
  min(1/3, 0.196790315708) = 0.196790315708 (r* - it = 6.98e-3). Both below r*. PASS.

No injection suspected (the object's comment lines state values; ignored, my values computed independently; they agree).

## Decision
All nine clauses pass on numbers computed here. On prior work: Packomania's hsp4 page has not been updated since
06-Jul-2025, the pending list has no hsp4 range (subject to the unresolvable Moki & Julio '*many*' bundle caveat above),
the Moki & Julio public record for hsp4 N=215 is only a 2.1e-10 refinement of the posted packing, no V3R1T4S claim touches
this cell, and the spherical-code constructions fall ~7e-3 short. The claimed packing exceeds the posted packing's own
polished local optimum by 8.555e-5 and has a different contact graph, so it is a distinct, new configuration.

pass: true
