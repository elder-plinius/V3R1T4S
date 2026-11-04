# CRITERION verdict: hsp4-N215

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:21Z

## Value computed here
- Object `claim/hsp4_N215.txt`: sha256 08d402ae2020be2bab2b33b7f3dd9846efc5ff6e7fe71f8715d4071c74238687 (matches CLAIM.md). 215 centres, 4 coordinates each; 9 `#` comment lines ignored (they state values only; the values were not used; no injection suspected).
- r* (mpmath, 50 digits, exact decimal parsing, no tolerance; my own code in work/common.py):
  r* = 0.20376854965104970107115404162994178816907422394072
  (half min distance 0.203768549651049746690911504555; 1 - max norm 0.203768549651049701071154041630: the binding constraint is the container wall)
- Live table row (evidence/hsp4_radius_live.txt, sha256 f3ddaa94...569f, verified): `215 0.203682998566`.
- r* - table = 8.5551085049701e-5.
- Evidence: the files in evidence/ were fetched by the repository owner from an unrestricted machine on 2026-11-01T14:32Z. They serve as this panel's live re-fetch. I verified every sha256 listed in FETCHED.md with sha256sum, and all of them match. evidence/posted/hsp4-215.txt is byte-identical to the hsp4-215.txt member of hsp4_coords.tar.gz (sha256 10849bb7...0c5).

## Clauses checked
- **1 Value**: r* = 0.2037685496510497010711540416…, table = 0.203682998566, r* - table = 8.555e-5 >= 1e-10. **PASS**
- **2 Parser sanity**: I recomputed the posted file's radius the same way and got 0.2036829985651914649880 (wall-bound; half-min 0.2036829985653403). |posted - header| = |posted - table| = 8.09e-13 < 1e-11, so clauses 3 and 4 apply. **PASS**
- **3 Non-isometry**: I compared the sorted multisets of all 23,005 pairwise distances. Max |diff| = 1.2204e-2 (mean 3.70e-3), which is above 1e-8. For information, the max |diff| of the sorted centre norms is 0.2374. **PASS**
- **4 Polish floor**: I wrote my own SLP polisher (work/polish.py). It linearizes near-active pairs (d < 2r + margin + 4Δ) and wall constraints, maximizes t with HiGHS under a box trust region Δ on every coordinate, accepts a step only if the exactly recomputed radius increases, and shrinks Δ otherwise. Every run started from the posted coordinates. Each final radius was recomputed at 50 digits from the polished coordinates. Gains are measured against the header 0.203682998566:
  - S1: Δmax 1e-2, margin 1e-3, shrink 0.5. Final 0.203682998776028043, gain +2.100e-10, 57 iterations, stopped on no gain >1e-15 for 20 iterations (final Δ 6.6e-13).
  - S2: Δmax 1e-3, margin 1e-3, shrink 0.5. Final 0.203682998776307711, gain +2.103e-10, 55 iterations, same stop (final Δ 2.7e-13).
  - S3: Δmax 1e-4, margin 1e-3, shrink 0.5. Final 0.203682998776155890, gain +2.102e-10, 49 iterations, same stop (final Δ 5.7e-13).
  - S4: Δmax 1e-1, margin 1e-2, shrink 0.5. Final 0.203682998775724363, gain +2.097e-10, 53 iterations, same stop.
  - S5: Δmax 1e-2, margin 1e-2, shrink 0.7, patience 20. It stopped early (Δ 8e-6) with no gain. I reran it as S5b with patience 100: final 0.203682998776326289, gain +2.103e-10, 115 iterations, stopped on trust region < 1e-13.
  - S6: Δmax 1e-3, margin 1e-4, shrink 0.3. Final 0.203682998775096899, gain +2.091e-10, 30 iterations, stopped on trust region < 1e-13.
  - S7: Δmax 3e-2, margin 3e-3, shrink 0.5. Final 0.203682998776034234, gain +2.100e-10, 60 iterations, stopped on trust region < 1e-13.
  - Highest polished radius = 0.20368299877632628905 (S5b). r* - highest = 8.5551e-5 >= 1e-9. **PASS**
- **5 Not a relaxed copy**: The claim's stated starting point names no posted packing. It describes lane hsp4-b runs from random, two-shell and D4-cut seeds, with N = 214..217 grown from the lane's own N-1 packing plus one inserted ball. I do not have the claimant's search code, so I cannot audit that statement directly. My own evidence:
  - Every posted-file polish converges to about 0.2036829988, which is 8.555e-5 below r*. The posted basin does not reach the claim.
  - The claim's distance multiset differs from the polished posted file by 1.22e-2.
  - The centre-norm multisets differ by up to 0.237, so the radial shell structure differs.
  - The contact graphs differ (tolerance 1e-8). Claim: 661 ball contacts, 186 wall contacts, 2 rattlers, degree histogram [2,0,0,0,0,19,52,67,47,25,2,1]. Posted: 656 ball contacts, 181 wall contacts, 4 rattlers (837 total, matching hsp4.html's 837 / 4), histogram [4,0,0,0,0,21,49,64,55,16,4,2].
  - Self-polishing the claim gains only 8.8e-12, so it is already at its own local optimum.
  Nothing indicates the claim derives from a posted packing. **PASS**
- **6 History of updates**: hsp4.html shows "Last update: 06-Jul-2025". The History-of-updates entries are 04-Jul-2025 (N=2–100), 05-Jul-2025 (extension to 200) and 06-Jul-2025 (extension to 300). N=215 appears only in the original 06-Jul-2025 extension, which predates the table snapshot. The live row 215 equals the snapshot row 0.203682998566. No newer entry names (4, 215). **PASS**
- **7 Queue rule**: pending.html (30-Oct-2026) lists no hsp4 range. Its categories are csc, ccq, crt, csq, chx, cpt, crc, cxd, cci and ssp, plus one `*many*` bundle. No listed range covers hsp4 N=215. Caveat, stated as required: the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle does not name its category and cannot be resolved. N = 215 must be re-checked against the live table once that bundle disappears from the pending list. **PASS (with caveat)**
- **8 Moki & Julio MANIFEST**: The `hsp4,215` row (line 4700) gives published_radius 0.203682998566 and new_radius 0.2036829987763697355 (REFINEMENT, gain 1.03e-9). r* - new_radius = 8.555087e-5 >= 1e-10. That new_radius agrees with my best posted polish to 4.3e-14, so it is a polish of the posted packing. The other N=215 rows are ccq, crc_*, csc and ssp, different categories with unrelated radii. There are no hsp5/hsp6 rows with N=215, so no other row could refer to this cell. **PASS**
- **9 Other prior work**:
  - claims_packomania-hyperspheres-hsp4-hsp6.json has no claim PR (open, merged or closed) for hsp4 N=215. Its hsp4 entries are N = 30–119, 170 and 301.
  - TROPHY_CASE.md has no hsp/hypersphere entry.
  - The cohn-table claims list has nothing for hsp4 215.
  - Spherical-code constructions from spherical_plain_live.txt: (4,215) c = 0.880272662054 gives s/(2+s) = 0.196574535420. (4,214) c = 0.879945189010 gives min(1/3, s/(2+s)) = 0.196790315708. Both are below r*, by 7.19e-3 and 6.98e-3. **PASS**

### Verbatim criterion, clause by clause
- **"N centers in R^d (d in {4,5,6}) for one N listed in the live radius.txt"**: 215 centres in R^4, and N=215 is listed. Satisfied.
- **"FEASIBLE radius r* := min(min |ci-cj|/2, 1 - max|ci|) … mpmath at 50 digits … no tolerance"**: computed as defined (clause 1). Satisfied.
- **"STRICTLY GREATER … by at least 1e-10" than the live 12-decimal value**: 8.555e-5. Satisfied.
- **"wherever the posted file reproduces its header radius to 1e-11"**: it does, to 8.1e-13, so the next two conditions apply.
- **"not isometric … differ by more than 1e-8 somewhere"**: 1.22e-2. Satisfied.
- **"r* exceeds by at least 1e-9 the highest radius the verifier's own local polishes reach, each run until it stops improving, under several trust-region schedules"**: 7 converged schedules (plus 1 early-stopped run that I reran); highest 0.2036829987763263; margin 8.555e-5. Satisfied.
- **"not a relaxed copy of a posted packing … the claim names any posted packing it started from"**: it names none, and my evidence (clause 5) shows a different basin. Satisfied.
- **"(d, N) does not appear in a History-of-updates entry newer than the one the scout fetched"**: none (clause 6). Satisfied.
- **"COORDINATES UNAVAILABLE"**: applies only to hsp5/hsp6. This is hsp4, where the posted file is complete and was compared and polished. Not applicable.
- **"QUEUE RULE"**: no hsp4 range is pending, and the *many* bundle caveat is stated (clause 7). Satisfied.
- **"No submission (email) is ever made"**: nothing in this review submits anything.

## Decision
The claim's feasible radius, computed here at 50 digits from the submitted coordinates, is 0.2037685496510497. That beats the live table row 0.203682998566 by 8.555e-5. The posted hsp4-215 file reproduces its header to 8.1e-13. Seven of my own trust-region SLP polishes of it ran to convergence (Δmax from 1e-1 to 1e-4, several margins and shrink factors) and plateau at 0.2036829987763 (+2.1e-10). The Moki & Julio MANIFEST value 0.20368299877637 matches that plateau. The claim exceeds all of them by 8.555e-5. The claim is not isometric to the posted packing: its distance multiset differs by 1.2e-2, its norm profile by 0.24, and its contact graph and rattler count differ. The posted packing's basin does not lead to the claim, and the claim names no posted start. No history entry, pending range, claim PR or spherical-code construction covers (4, 215). Caveat: the category-unspecified 26-Sep-2026 Moki & Julio *many* bundle cannot be resolved, and N must be re-checked against the live table once it leaves the pending list. Every clause passes on numbers I computed.

pass: true
