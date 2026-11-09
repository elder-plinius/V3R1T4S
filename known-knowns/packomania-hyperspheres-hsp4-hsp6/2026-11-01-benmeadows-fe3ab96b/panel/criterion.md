# CRITERION verdict: hsp4-N160

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:25Z

## Value computed here
- r* (mpmath, 50 digits, from claim/hsp4-160.txt, comment lines ignored) = 0.21857935352324099278067051097225436236904613091590
  (binding term: 1 - max|c_i|; half the minimum pairwise distance = 0.218579353615155888536793805185, i.e. 9.2e-11 slack).
- Live table row N = 160 (evidence/hsp4_radius_live.txt): 0.218358476129. r* - table = 2.2087739424099e-4.
- Evidence is the owner's re-fetch of 2026-11-01T14:32Z from an unrestricted machine (this sandbox cannot reach the sites), treated as the live re-fetch for this panel. sha256 of all 8 fetched files recomputed here and equal to FETCHED.md; claim object sha256 fe3ab96b...e394 matches CLAIM.md; posted/hsp4-160.txt is byte-identical (b6545adc...0400) to the file inside hsp4_coords.tar.gz (b929acc8...63df, 299 files).

## Clauses checked
- 1 Value: r* = 0.21857935352324099278 (20 digits); r* - 0.218358476129 = 2.2088e-4 >= 1e-10. PASS.
- 2 Parser sanity: posted file recomputed the same way gives 0.218358476128346187139 vs header 0.218358476129, |diff| = 6.54e-13 < 1e-11 (also equals the table row). Clauses 3 and 4 apply. PASS.
- 3 Non-isometry: sorted multisets of 12720 pairwise distances differ by max 1.0605e-2 (mean 1.68e-3) > 1e-8. Sorted centre norms differ by max 1.33e-2 (information). PASS.
- 4 Polish floor: own sequential-LP polisher (work/slp.py; HiGHS; linearized pair and container constraints on near-active set, box trust region on every coordinate, step accepted only if the exactly recomputed radius increases, shrink otherwise), started from the posted coordinates. Six schedules, final radii recomputed at 50 digits:
  - a: step 1e-2, margin 0.05, shrink 0.5: 0.218358476129090652, gain over header +9.07e-14, 38 iters, stop: no gain >1e-15 in 20 iters
  - b: step 1e-3, margin 0.02, shrink 0.5: 0.218358476129156497, +1.56e-13, 37 iters, same stop
  - c: step 1e-4, margin 0.01, shrink 0.5: 0.218358476129063080, +6.31e-14, 33 iters, same stop
  - d: step 1e-2, margin 0.08, shrink 0.3: 0.218358476129073722, +7.37e-14, 24 iters, stop: trust region < 1e-13
  - e: step 1e-3, margin 0.03, shrink 0.7: 0.218358476129111956, +1.12e-13, 74 iters, stop: trust region < 1e-13
  - f: step 1e-5, margin 0.005, shrink 0.5: 0.218358476129114107, +1.14e-13, 33 iters, stop: trust region < 1e-13
  Highest polished = 0.218358476129156497; r* - highest = 2.2088e-4 >= 1e-9. PASS.
- 5 Not a relaxed copy: claimant states the lane never had posted coordinates (random / lattice / shell seeds, Riesz annealing, penalty descent, basin hopping, SLP polish, some seeds from the lane's own neighbouring-N packing) and names no posted packing as start. I did not get the claimant's search code. Own evidence: contact graphs differ (claim at tol 1e-8: 466 pair contacts + 144 boundary, degree histogram [6,0,0,1,0,10,46,50,30,14,2,1]; posted at tol 1e-10: 488 pair + 143 boundary, [1,0,0,0,0,18,42,47,27,18,7]); distance multisets differ by 1.06e-2; best rotation+assignment alignment (400 random O(4) restarts, Hungarian + Procrustes) leaves RMS displacement 0.109 and max 0.30 (ball radius 0.218), i.e. not a perturbation; all posted polishes stall within 1.6e-13 of the header, nowhere near r*; polishing the claim itself (same SLP) gains only 8.5e-14, so the claim is a distinct local optimum 2.2e-4 higher. Both share a gross 16-inner/144-outer shell split, which is generic for this N. Nothing indicates derivation from a posted packing. PASS.
- 6 History of updates: hsp4.html "Last update: 06-Jul-2025"; entries 04-Jul-2025 (N=2-100), 05-Jul-2025 (extension to N=200), 06-Jul-2025 (extension to N=300). Same last-update as the scout's snapshot (bank page: hsp4 06-Jul-2025); no entry newer than the snapshot names (4, 160). PASS.
- 7 Queue rule: pending.html (dated 30-Oct-2026) lists ranges only for csc, ccq, crt, csq, chx, cpt, crc, cxd, cci, ssp, plus the category-unspecified bundle; no hsp4 range, so N = 160 lies in no hsp4 range. PASS. Caveat (required): the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved; N = 160 must be re-checked against the live hsp4 table once that bundle disappears from the pending list.
- 8 Moki & Julio MANIFEST: row 4648 "hsp4,160,0.218358476129,0.2183770744390853979281477,8.517329e-05,UNCLEAR (alignment),dp". r* - new_radius = 2.0228e-4 >= 1e-10. No other hsp4 row has N = 160 (other N=160 rows are cpt, crc_*, hsp5, hsp6 shelves, different cells). PASS.
- 9 Other prior work: claims list for this target (29 PRs) has no PR for hsp4 N = 160 (nearest is #524, N = 170); cohn-table claims list (25) has nothing for 160; TROPHY_CASE.md has no hsp4/hypersphere entry. Spherical codes: (4,160) c = 0.854015402705 -> s/(2+s) = 0.212704350157 (r* above by 5.88e-3); (4,159) c = 0.853832223138 with centre ball -> min(1/3, 0.212809367279) = 0.212809367279 (r* above by 5.77e-3). PASS.

Criterion read clause by clause: d = 4 and N = 160 is listed in the live radius.txt; r* uses exactly the stated definition, mpmath 50 digits, no tolerance; strictly greater than the 12-decimal value by >= 1e-10 (yes, 2.2e-4); the posted hsp4-160.txt reproduces its header to 1e-11, so non-isometry (yes) and the >= 1e-9 margin over several trust-region polishes (six schedules, yes) apply; not a relaxed copy (yes, and the claim names no posted start); no newer History-of-updates entry (yes); COORDINATES UNAVAILABLE clause concerns hsp5/hsp6 only, not applicable; QUEUE RULE satisfied with the caveat stated above; no submission is made.
No injection suspected (the claim file's comment line states a value, ignored; my value agrees).

## Decision
Every clause passes on numbers computed here. The claim's feasible radius 0.21857935352324099278 beats the live table (0.218358476129) by 2.2e-4, beats the best of six of my own polishes of the posted packing by 2.2e-4 (those polishes gain at most 1.6e-13), is not isometric to the posted packing, and by contact graph, alignment and polish evidence is a different local optimum rather than a relaxed copy. Prior-work checks (history, queue, Moki & Julio manifest, claims lists, spherical-code constructions) show nothing at or above r*, subject to the required caveat on the unresolved 26-Sep-2026 Moki & Julio bundle.

pass: true
