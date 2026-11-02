# NOVELTY verdict: hsp4-N163

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:14Z

## Value computed here
- Claim object sha256 7c6a8a80…299c6 (matches CLAIM.md); 163 centres in R^4. I ignored the comment line in it and computed everything myself.
- r* (mpmath, 50 digits) = 0.21713800642461929882694315132625607157010627576977
  (half min distance 0.2171380079056466226719881; 1 - max norm 0.2171380064246192988269432, the binding term).
- Live table row (evidence/hsp4_radius_live.txt): `163 0.217115168538`. r* - table = 2.28378866e-5.
- Live sources: evidence/ files were fetched by the repository owner on an unrestricted machine at 2026-11-01T14:32Z. I treat them as the live re-fetch for this panel. Every sha256 in FETCHED.md matches my own sha256sum. I made no other web access.

## Clauses checked
- 1 Value: r* = 0.217138006424619298827 (50 digits above), table 0.217115168538, difference 2.2838e-5 ≥ 1e-10. **PASS**
- 2 Parser sanity: the posted hsp4-163.txt recomputes to 0.217115168537453430921 against header 0.217115168538, a difference of -5.47e-13 (< 1e-11). The header equals the table row, so clauses 3 and 4 apply. **PASS**
- 3 Non-isometry: the maximum absolute difference between the sorted pairwise-distance multisets (13203 distances each) is 1.1245e-2 > 1e-8. For information, the maximum difference between sorted centre norms is 0.340. **PASS**
- 4 Polish floor: I wrote my own SLP (HiGHS LP on pairs within 2r+margin and wall-near centres; box trust region; a step is accepted only if the exactly recomputed radius increases; ×2 expand, shrink on reject). I polished the POSTED coordinates and recomputed each final radius at 50 digits from the polished coordinates:
  - dmax 1e-2, shrink 0.5, margin 4Δ: 0.217115176799313600, gain +8.261e-9, 84 iterations, stopped after 20 iterations with no gain > 1e-15
  - dmax 1e-3, shrink 0.5, margin 4Δ: 0.217115176793007575, gain +8.255e-9, 87 iterations, same stop
  - dmax 1e-4, shrink 0.5, margin 4Δ: 0.217115176799731486, gain +8.262e-9, 102 iterations, same stop
  - dmax 1e-2, shrink 0.25, margin 10Δ: 0.217115176797309138, gain +8.259e-9, 65 iterations, stopped at trust region < 1e-13
  - dmax 1e-3, shrink 0.1, margin 2Δ: 0.217115172463321269, gain +3.925e-9, 49 iterations, stopped at trust region < 1e-13
  - dmax 1e-5, shrink 0.5, margin 4Δ: 0.217115176799427817, gain +8.261e-9, 68 iterations, stopped after 20 iterations with no gain
  - Highest polished radius: 0.2171151767997315. r* minus that = 2.2830e-5 ≥ 1e-9. **PASS** (Errata note for the table keeper: the posted packing polishes up by about 8.26e-9.)
- 5 Not a relaxed copy: the claim says it started from random, lattice-cut and shell seeds and from the lane's own neighbouring-N packings, and it names no posted packing. I did not get the claimant's search code. Contact graphs at tol 1e-8:
  - claim: 493 contacts, 142 wall contacts, degree histogram [2,1,0,1,17,40,44,29,18,8,2,1] (2 rattlers, max degree 11)
  - posted: 500 contacts, 144 wall contacts, degree histogram [0,1,0,0,19,37,45,34,16,8,3] (no rattlers, max degree 10)

  The distance multisets differ by 1.1e-2 and the sorted norms by 0.34, so the radial structure is different. Every polish of the posted file stalls at about 0.2171151768, 2.28e-5 below the claim, so the claim is not the posted packing's local optimum. Nothing indicates that the claim derives from a posted packing. **PASS**
- 6 History of updates: hsp4.html shows "Last update: 06-Jul-2025". Its History entries are 04-Jul-2025 (N=2–100), 05-Jul-2025 (extension to N=200, which covers N=163 only as the initial presentation) and 06-Jul-2025 (extension to N=300). That matches the table snapshot. No entry is newer than the snapshot, and none names (4, 163) as an update. **PASS**
- 7 Queue rule: pending.html (dated 30-Oct-2026) lists ranges for csc, ccq, crt, csq, chx, cpt, crc, cxd, cci and ssp. It lists no hsp4 range, and no range is attributed to hsp4, so N=163 lies in none. **PASS**
  - Caveat (required): the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved. N=163 must be re-checked against the live table once that bundle disappears from the pending list.
- 8 Moki & Julio MANIFEST:
  - The row `hsp4,163` has published_radius 0.217115168538 and new_radius 0.2171196009227415097388905 (kind "UNCLEAR (alignment)").
  - r* - new_radius = 0.2171380064246 - 0.2171196009227 = 1.8406e-5 ≥ 1e-10.
  - Other rows with N=163 are cpt, crc_*, and hsp5 (0.26229968, a different dimension), so none refers to this cell. Only one hsp4 row has N=163.
  - Their coordinates are not in evidence, so their 163-ball packing cannot be compared geometrically. The claim beats their stated radius by 1.84e-5. **PASS**
- 9 Other prior work:
  - Claims list: there is no open, closed or merged claim or submission for hsp4 N=163. hsp4 entries exist for N=30–111, 119, 170 and 301 only.
  - TROPHY_CASE.md has no hsp/hypersphere entry. Its only "163" is A(30,8,8) 1163, which is unrelated.
  - Spherical-code bounds from spherical_plain_live.txt:
    - (4,163): c = 0.856415430312, s/(2+s) = 0.2113196598, below r* by 5.82e-3
    - (4,162) plus a centre ball: c = 0.856011990176, min(1/3, s/(2+s)) = 0.2115535697, below r* by 5.58e-3

  Both are below r*. **PASS**

## Decision
All nine clauses pass on numbers I computed. On prior work:
- Packomania's hsp4 page has not been updated since 06-Jul-2025, and no history entry newer than the snapshot names N=163.
- The 30-Oct-2026 pending list has no hsp4 range. The category-unspecified 26-Sep-2026 Moki & Julio 4666-candidate bundle is an unresolvable caveat: N=163 must be re-checked against the live table once that bundle leaves the pending list.
- The strongest known competitor is Moki & Julio's MANIFEST value 0.21711960. The claim exceeds it by 1.84e-5.
- The claim exceeds the spherical-code constructions by more than 5e-3.
- No bank claim exists for this cell.

The claim is not isometric to the posted packing and has a different contact graph. My polishes of the posted file reach only 0.2171151768, about 2.28e-5 below r*. I see no sign of a relaxed copy, though I had no access to the claimant's search code.

pass: true
