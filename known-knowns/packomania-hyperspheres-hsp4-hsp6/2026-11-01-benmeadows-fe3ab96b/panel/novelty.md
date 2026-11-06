# NOVELTY verdict: hsp4-N160

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:14Z

## Value computed here
- Object `claim/hsp4-160.txt`: sha256 fe3ab96b...6e394, which matches CLAIM.md. It has 160 centres in 4 coordinates. I ignored the comment line.
- r* (mpmath, 60 digits working precision, no tolerance) = 0.2185793535232409927806705109722543623690461309159
  - half min distance = 0.2185793536151558885367938; 1 - max norm = 0.2185793535232409927806705. The container is the binding term.
- Live table row (`evidence/hsp4_radius_live.txt`, line 159) is `160 0.218358476129`.
- r* - table = 2.2087739424099e-4.
- Evidence files: I recomputed every sha256 listed in `evidence/FETCHED.md` with sha256sum and all of them match. The owner fetched these files on 2026-11-01T14:32Z from an unrestricted machine. I treat them as the live re-fetch for this panel; this sandbox has no web access.
- Posted archive files: posted/hsp4-160.txt sha256 b6545adc...0d400; hsp4_coords.tar.gz sha256 b929acc8...63df.

## Clauses checked
- **1 Value:** r* = 0.21857935352324099278. Table = 0.218358476129. Difference = 2.209e-4, which is at least 1e-10. **PASS**
- **2 Parser sanity:** I recomputed the posted file's radius as 0.21835847612834618714. The header and the table both read 0.218358476129, so the difference is -6.54e-13, within 1e-11. Clauses 3 and 4 therefore apply. **PASS**
- **3 Non-isometry:** max |difference| between the sorted multisets of all 12720 pairwise distances is 1.0605e-2, which exceeds 1e-8. For information, the max |difference| between the sorted centre norms is 1.333e-2. **PASS**
- **4 Polish floor:** I wrote my own sequential LP (HiGHS). It linearizes the near-active pairs and the wall constraints, using margin k·Δ + 1e-9. Each coordinate step is limited by a box trust region Δ. A step is accepted only if the exactly recomputed radius increases; otherwise Δ shrinks. Δ grows ×2 on success, up to the schedule's maximum. I ran it from the posted coordinates under six schedules and recomputed each final radius at 50 digits from the polished coordinates:
  - max step 1e-2, shrink 0.5, k=5: 0.21835847612909068501. Gain over header +9.07e-14. 38 iterations. Stopped: no gain >1e-15 in 20 iterations.
  - max step 1e-2, shrink 0.3, k=10: 0.21835847612912034212. Gain +1.20e-13. 27 iterations. Stopped: trust region below 1e-13.
  - max step 1e-3, shrink 0.5, k=5: 0.21835847612915660640. Gain +1.57e-13. 37 iterations. Stopped: no gain >1e-15 in 20 iterations. **This is the highest.**
  - max step 1e-3, shrink 0.7, k=5: 0.21835847612834618714. Gain -6.54e-13 (no step was accepted). 20 iterations. Stopped: no gain.
  - max step 1e-4, shrink 0.5, k=5: 0.21835847612906708540. Gain +6.71e-14. 36 iterations. Stopped: no gain.
  - max step 1e-5, shrink 0.5, k=5: 0.21835847612907861495. Gain +7.86e-14. 28 iterations. Stopped: no gain.
  - Extra check, for information: I perturbed the posted file by ±3e-4 and polished it again. It reached 0.2183584764037 (+2.7e-10 over the header), so a slightly higher local maximum may exist near the posted file. The claim is still 2.2e-4 above it.
  - r* - highest polished radius = 2.2087739e-4, which is at least 1e-9. **PASS**
- **5 Not a relaxed copy:** CLAIM.md says the claim came from random, lattice-cut and shell starts followed by annealing, basin hopping and SLP, with some runs seeded from the lane's own neighbouring-N packings. It says no posted Packomania packing was used and names none as a start. I do not have the claimant's search code. My own evidence:
  - Contact graphs differ. At tolerance 1e-9, the claim has 465 pair contacts and 144 wall contacts, with degree histogram [6,0,0,1,0,10,46,52,28,14,2,1]. The posted file has 488 pair contacts and 143 wall contacts, with degree histogram [1,0,0,0,0,18,42,47,27,18,7].
  - The distance multisets differ by up to 1.06e-2.
  - The best rigid alignment I found (400 random O(4) starts, each with Procrustes plus Hungarian assignment) leaves an RMS displacement of 0.115 and a maximum of 0.277. That is comparable to the ball radius, not a small relaxation.
  - Every polish of the posted file stalls within about 1.6e-13 of its header (2.7e-10 after the perturbation), far below r*.
  - Nothing indicates the claim derives from a posted packing. **PASS**
- **6 History of updates:** hsp4.html shows "Last update: 06-Jul-2025". Its History of updates lists three entries:
  - 04-Jul-2025: N = 2–100.
  - 05-Jul-2025: extension to N = 200. This entry covers N = 160 and is the table snapshot itself.
  - 06-Jul-2025: extension to N = 300.
  - No entry newer than the snapshot names (4, 160), and the page row for 160 is 0.218358476129, the same as radius.txt. **PASS**
- **7 Queue rule:** pending-requests.html is dated 30-Oct-2026. It lists ranges only for csc, ccq, crt, csq, chx, cpt, crc, cxd, cci and ssp. No hsp4 range appears, and none of the listed ranges is for an hsp category, so N = 160 is in no hsp4 range. **PASS**, with this caveat: the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved. N = 160 must be re-checked against the live hsp4 table once that bundle disappears from the pending list.
- **8 Moki & Julio manifest:** row 4648 reads `hsp4,160,0.218358476129,0.2183770744390853979281477,8.517329e-05,UNCLEAR (alignment),dp`. So published_radius = 0.218358476129 and new_radius = 0.21837707443908540. r* - new_radius = 2.0228e-4, which is at least 1e-10.
  - That is the only hsp4 row for N = 160. The other N = 160 rows are on other shelves (cpt, crc_*, hsp5, hsp6).
  - No row's radius lies near 0.21858 or 0.218358 apart from row 4648.
  - **PASS**
- **9 Other prior work:**
  - The hsp4–hsp6 claims list has no open, closed or merged claim or PR for hsp4 N = 160. The nearest is N = 170 (#524/#106).
  - TROPHY_CASE.md has no hsp or N = 160 entry.
  - Spherical-codes.org (`spherical_plain_live.txt`): the (4,160) cosine 0.854015402705 gives s/(2+s) = 0.212704350157, below r* by 5.88e-3. The (4,159) cosine 0.853832223138 with a centre ball gives min(1/3, s/(2+s)) = 0.212809367279, below r* by 5.77e-3.
  - **PASS**

## Decision
The claim beats every piece of prior work I could check by a wide margin:
- the live table (+2.21e-4)
- Moki & Julio's manifest radius for hsp4 N = 160 (+2.02e-4)
- the spherical-code constructions (+5.8e-3)
- every polish of the posted file under six trust-region schedules (+2.21e-4 over the best)

The live hsp4 page has had no update since 06-Jul-2025, and no claim PR or trophy entry covers this cell. The configuration is not isometric to the posted packing and its contact graph differs from it. The best rigid alignment I found leaves an RMS displacement of 0.115, so it is not a relaxed copy. This rests on my own geometry, since I cannot see the claimant's search code.

One caveat stands: the category-unspecified 26-Sep-2026 Moki & Julio "*many* 4666 candidates" bundle in Packomania's queue cannot be resolved. N = 160 must be re-checked against the live hsp4 table once that bundle leaves the pending list. All nine clauses pass on numbers I computed here.

pass: true
