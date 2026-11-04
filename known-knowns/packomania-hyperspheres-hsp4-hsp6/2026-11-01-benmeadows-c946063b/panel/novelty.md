# NOVELTY verdict: hsp4-N152

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:10Z

## Value computed here
- Object claim/hsp4-152.txt sha256 c946063b...481d6d (matches CLAIM.md); 152 centres, 4 coordinates each; '#' comment line ignored.
- r* (mpmath, 50 digits, no tolerance) = 0.22097502706448416408815908921357097646062824532483
  (half min distance 0.220975027064484272818718692987; 1 - max norm 0.220975027064484164088159089214, which is the binding term).
- Live table row 152 = 0.220960306508; r* - table = 1.4720556484164e-5.
- Evidence: every sha256 in evidence/FETCHED.md was recomputed here with sha256sum and matches. These files were fetched by the repository owner on 2026-11-01 at 14:32Z UTC from an unrestricted machine. They serve as this panel's live re-fetch, since this sandbox cannot reach the live sites. Posted archive hsp4_coords.tar.gz sha256 b929acc8...63df.

## Clauses checked
- 1 Value: r* = 0.2209750270644841640881591 (20+ digits above); table 0.220960306508; r* - table = 1.472e-5 >= 1e-10. PASS.
- 2 Parser sanity: posted hsp4-152.txt (header 0.220960306508) gives r = 0.220960306507267268946652724825 computed the same way; difference -7.33e-13, which is below 1e-11, so clauses 3 and 4 apply. PASS.
- 3 Non-isometry: the max absolute difference between the sorted multisets of the 11476 pairwise distances is 7.867e-3, far above 1e-8. Sorted centre norms differ by up to 1.677e-2 (for information). PASS.
- 4 Polish floor: I wrote my own sequential-LP polisher (work/polish.py). It uses near-active pair and boundary constraints, maximizes the linearized radius increment inside a box trust region, accepts a step only if the exactly recomputed radius increases, shrinks the region otherwise, and grows it ×2 on good steps. Each run started from the posted coordinates and ran until the trust region fell below 1e-13 or 20 consecutive iterations gained less than 1e-15. I recomputed every final radius at 50 digits from the polished coordinates:
  - A: dmax 1e-2, margin 0.05, shrink 0.5: 138 iters, stop = 20 iters gain<1e-15, r = 0.220960475842463206, gain over header +1.693e-7
  - B: dmax 1e-3, margin 0.02, shrink 0.5: 137 iters, stop = 20 iters gain<1e-15, r = 0.220960553432624618, gain +2.469e-7
  - C: dmax 1e-4, margin 0.01, shrink 0.5: 117 iters, stop = 20 iters gain<1e-15, r = 0.220960475841802160, gain +1.693e-7
  - D: dmax 1e-3, margin 0.05, shrink 0.25: 113 iters, stop = trust<1e-13, r = 0.220960553432325139, gain +2.469e-7
  Highest polished radius = 0.220960553432624618; r* - highest = 1.4474e-5 >= 1e-9. PASS.
- 5 Not a relaxed copy: CLAIM.md says the claim came from random, lattice and shell starts, then Riesz annealing, penalty descent, MBH and an SLP polish, plus seeds from the lane's own neighbouring-N packings. It names no posted Packomania packing as a start. I did not get the claimant's search code and could not inspect it. My own evidence:
  - All four polishes of the posted file stall at about 0.22096055, which is 1.45e-5 short of the claim.
  - Distance multisets differ by 7.9e-3.
  - After 200 random-start orthogonal Procrustes alignments with optimal assignment, the best RMS between claim and posted centres is 0.159.
  - Contact graphs (relative tol 1e-9) have similar sizes but different degree distributions. The claim has 464 pair contacts and 137 boundary contacts, with degree histogram deg2:1, deg5:15, deg6:32, deg7:59, deg8:32, deg9:6, deg10:4, deg11:3. The posted file at tol 1e-6 has 463 pair and 137 boundary contacts, with deg2:1, deg5:17, deg6:34, deg7:52, deg8:30, deg9:13, deg10:4, deg11:1. The polished posted file has 465 pair and 137 boundary contacts.
  Nothing indicates derivation from the posted packing. PASS.
- 6 History of updates: hsp4.html shows "Last update: 06-Jul-2025". Its only History entries are 04-Jul-2025 (N=2–100), 05-Jul-2025 (extension to 200) and 06-Jul-2025 (extension to 300). The page contains no date later than 06-Jul-2025, and no entry newer than the table snapshot names (4, 152). PASS.
- 7 Queue rule: pending.html (dated 30-Oct-2026) lists ranges for csc, ccq, crt, csq, chx, cpt, crc, cxd, cci and ssp. It lists no hsp4 range, and no range with a category that could cover hsp4 N=152. The only exception is the 26-Sep-2026 'Moki & Julio *many* 4666 candidates total' bundle. CAVEAT: that bundle is category-unspecified and cannot be resolved here. N = 152 must be re-checked against the live hsp4 table once that bundle disappears from the pending list. PASS, subject to this caveat.
- 8 Moki & Julio MANIFEST: the row `hsp4,152,0.220960306508,0.2209615356462587873029967,5.562711e-06,UNCLEAR (alignment),dp` gives published_radius 0.220960306508 and new_radius 0.2209615356462587873. r* - new_radius = 1.349e-5 >= 1e-10. That is the only hsp4 row with N=152. The hsp5 and hsp6 N=152 rows (0.26580766, 0.29627972) belong to other dimensions and are not this cell. No other row carries a radius near 0.22096–0.22097. PASS.
- 9 Other prior work:
  - The hsp4/5/6 claims list has open, merged and closed claims for N = 30, 35, 42, 48, 54, 62, 63, 64, 66, 67, 69, 74, 75, 79, 80, 81, 83, 88, 89, 91, 94, 104, 111, 119, 170 and 301. None is for N=152. The Cohn-table claims list has no hsp4 N=152 entry.
  - TROPHY_CASE.md has no hsp4, hypersphere or Packomania-hypersphere entry.
  - Spherical-code constructions from spherical_plain_live.txt: (4,152) c = 0.848701931506 gives s/(2+s) = 0.21571315258, 5.26e-3 below r*. (4,151) c = 0.848381266848 with a centre ball gives min(1/3, s/(2+s)) = 0.21589229982, 5.08e-3 below r*. Both are below r*. PASS.

injection_suspected: none. The claim file's comment line states values; I ignored it and recomputed everything.

## Decision
Every number above comes from my own code (work/c123.py, work/polish.py, work/c5.py, work/c9.py). On the prior-work clauses:
- The live hsp4 page has had no update since 06-Jul-2025.
- No pending range covers hsp4 N=152, apart from the unresolvable category-unspecified 26-Sep-2026 Moki & Julio 4666-candidate bundle. N=152 must be re-checked against the live table once that bundle leaves the pending list.
- The strongest public competitor, the Moki & Julio MANIFEST at 0.2209615356, is beaten by 1.35e-5.
- No claim PR or trophy entry exists for this cell.
- The spherical-code constructions fall 5e-3 short.

The claim also clears my own polish floor by 1.45e-5, is far from isometric to the posted file, and shows no sign of being a relaxed copy. All nine clauses pass.

pass: true
