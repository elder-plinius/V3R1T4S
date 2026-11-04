# CRITERION verdict: hsp4-N163

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:17Z

## Value computed here
- Claim object `claim/hsp4-163.txt`: sha256 7c6a8a80df2a86665a9af3715802976054a9223efa6181be86d745d1264299c6 (matches CLAIM.md); 163 rows x 4 coordinates (comment line ignored; I computed my own values).
- r* (mpmath, 50 digits, no tolerance) = 0.21713800642461929882694315132625607157010627576977
  (half min distance 0.217138007905646622671988117608; 1 - max norm 0.217138006424619298826943151326 is the binding term).
- Live table row (evidence/hsp4_radius_live.txt): `163 0.217115168538`. r* - table = 2.2837886619298826943e-5.
- Evidence: the files in `evidence/` were fetched by the repository owner from an unrestricted machine on 2026-11-01 14:32Z and serve as the live re-fetch for this panel (this sandbox cannot reach packomania.com etc.). I re-ran sha256sum on every file; all values listed in FETCHED.md match (hsp4_radius_live.txt f3ddaa94..., hsp4.html 1c3a3064..., pending.html dddaf3c9..., mj_manifest.csv b7a042ef..., spherical_plain_live.txt b7c6a76f...). The posted archive hsp4_coords.tar.gz has sha256 b929acc8...63df, and its hsp4-163.txt is byte-identical to evidence/posted/hsp4-163.txt.
- Process note: my first `find` listed the file names in the sibling skeptics' folders under hsp4-N163/. I did not open, read or use any of those files.

## Clauses checked
- **1 Value**: r* = 0.21713800642461929883 (20 digits). r* - 0.217115168538 = 2.2838e-5 >= 1e-10. **PASS**.
- **2 Parser sanity**: the posted hsp4-163.txt (header 0.217115168538, 163 rows of index + 4 coordinates) recomputes at 50 digits to 0.217115168537453430921. That is header - 5.47e-13, within 1e-11 of both the header and the table row. Clauses 3 and 4 therefore apply. **PASS**.
- **3 Non-isometry**: I sorted the 13203 pairwise distances of the claim and of the posted file. The maximum absolute difference is 1.1245e-2, and all 13203 entries differ by more than 1e-8. For information, the sorted centre norms differ by up to 0.340: the claim has 18 inner centres (norm < 0.5) and 145 on the outer shell, while the posted file has 19 and 144. **PASS**.
- **4 Polish floor**: I wrote my own sequential-LP polisher (work/polish.py), seeded from the posted coordinates. It uses HiGHS linprog, linearizes the near-active pairs (|ci-cj| < 2r+margin) and the near-wall centres (|ci| > 1-r-margin), and maximizes t inside a box trust region on every coordinate. A step is accepted only if the exactly recomputed radius increases: the trust region then grows x2 up to its maximum. Otherwise it shrinks. Each run stops when the trust region falls below 1e-13 or there is no gain above 1e-15 for 20 consecutive iterations. I recomputed every final radius at 50 digits from the polished coordinates:
  - dmax 1e-2, margin 0.05, shrink 0.5: 92 its, stop = no gain >1e-15 in 20 its, r = 0.2171151767998458736 (gain over header +8.262e-9)
  - dmax 1e-3, margin 0.02, shrink 0.5: 92 its, same stop, r = 0.2171151767996926982 (+8.262e-9)
  - dmax 1e-4, margin 0.01, shrink 0.5: 91 its, same stop, r = 0.2171151767998138039 (+8.262e-9)
  - dmax 1e-2, margin 0.10, shrink 0.3: 69 its, stop = trust < 1e-13, r = 0.2171151767996508670 (+8.262e-9)
  - dmax 3e-2, margin 0.15, shrink 0.5: 98 its, no-gain stop, r = 0.2171151767988348924 (+8.261e-9)
  - dmax 1e-5, margin 0.005, shrink 0.5: 61 its, no-gain stop, r = 0.2171151767992748073 (+8.261e-9)
  
  All six runs agree to about 2e-13, so the posted packing has converged. Highest polished radius = 0.2171151767998458736. r* minus that = 2.2829e-5 >= 1e-9. **PASS**.
- **5 Not a relaxed copy**: The claim says it came from random starts, lattice/shell seeds, annealing, basin hopping and its own neighbouring-N packings. It names no posted packing as its start. I did not have the claimant's search code. My own evidence:
  - Contact graphs differ. Within 1e-7 the claim has 493 ball-ball and 142 wall contacts, against 500 and 144 for the posted file. The degree histograms differ too: the claim has 2 rattlers, the posted file has none.
  - Shell populations differ: 18 inner + 145 outer in the claim, 19 + 144 in the posted file.
  - The distance multisets differ by 1.1e-2 (clause 3).
  - Polishing the posted file stalls at 0.21711517680, which is 2.28e-5 below r*.
  - I ran a rigid registration: anchor-quadruple Procrustes over all candidate correspondences, with reflections allowed, then Hungarian assignment and refinement (work/c5b.py). The best alignment of the claim onto the polished posted packing has RMSD 0.113, and only 2 of 163 centres match within 0.02. As a control, a randomly rotated posted file registers onto its polished version with all 163 matched at RMSD 1e-4.
  
  Nothing indicates the claim derives from the posted packing. **PASS**.
- **6 History of updates**: hsp4.html shows "Last update: 06-Jul-2025". Its History-of-updates entries are 04-Jul-2025 (N=2-100), 05-Jul-2025 (extension to N=200) and 06-Jul-2025 (extension to N=300). None is newer than the table snapshot, and no later entry names (4, 163). **PASS**.
- **7 Queue rule**: pending.html (dated 30-Oct-2026) lists no hsp4 or hyperspheres category. Its categories are csc, ccq, crt, csq, chx, cpt, crc, cxd, cci, ssp, and one bundle marked *many*. N=163 lies in no hsp4 range. **PASS**, with this caveat: the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved. N = 163 must be re-checked against the live hsp4 table once that bundle disappears from the pending list.
- **8 Moki & Julio MANIFEST**: the row reads `hsp4,163,0.217115168538,0.2171196009227415097388905,2.041490e-05,UNCLEAR (alignment),dp`, so published_radius = 0.217115168538 and new_radius = 0.21711960092274151. r* - new_radius = 1.8406e-5 >= 1e-10. This is the only hsp4/163 row. The other N=163 rows belong to other shelves (hsp5 0.26230, crc_*, cpt), and no other row carries published_radius 0.217115168538. **PASS**.
- **9 Other prior work**:
  - Claims lists: the hsp4 claims cover N = 30, 35, 42, 48, 54, 62-64, 66, 67, 69, 74, 75, 79-81, 83, 88, 89, 91, 94, 104, 111, 119, 170 and 301. There is none for N=163, open or merged.
  - TROPHY_CASE.md has no hsp entry.
  - Spherical codes (spherical_plain_live.txt): the (4,163) code has c = 0.856415430312, giving s/(2+s) = 0.211319659762. The (4,162) code has c = 0.856011990176, and with a centre ball min(1/3, s/(2+s)) = 0.211553569705. Both are below r*, by 5.8e-3 and 5.6e-3.
  - The arXiv feeds contain nothing on 4-ball packings at N=163.
  
  **PASS**.

## Clause-by-clause reading of the verbatim criterion
- "N centers in R^d (d in {4,5,6}) for one N listed in the live radius.txt": d=4, 163 centres. N=163 is listed: OK.
- "FEASIBLE radius r* ... computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance": done, r* = 0.21713800642461929883.
- "STRICTLY GREATER ... than that file's 12-decimal value ... re-fetched live ... by at least 1e-10": the margin is 2.28e-5, against the 2026-11-01 14:32Z re-fetch: OK.
- "wherever the posted hsp4-163.txt reproduces its own header radius to 1e-11": it does (5.5e-13), so both of the following apply.
  - "not isometric (sorted multisets differ > 1e-8 somewhere)": 1.12e-2: OK.
  - "r* exceeds by >= 1e-9 the highest radius of the verifier's own local polishes ... each run until it stops improving, under several trust-region schedules": six schedules, highest 0.21711517679985, margin 2.28e-5: OK.
- "not a relaxed copy of a posted packing ... the claim names any posted packing it started from": none is named, and the structural evidence (clause 5) shows a distinct packing: OK.
- "(d, N) does not appear in a History-of-updates entry on the live hsp4.html newer than the one the scout fetched": no such entry; the page is unchanged since 06-Jul-2025: OK.
- COORDINATES UNAVAILABLE clause: it applies only to hsp5/hsp6. hsp4 coordinates are available and were used, so it does not apply.
- QUEUE RULE: N=163 is in no listed hsp4 range. The *many* bundle caveat is stated above: OK.
- "No submission (email) is ever made": nothing was submitted or contacted by this skeptic.

## Decision
Every clause of the verbatim criterion holds on numbers I computed myself:
- The claimed 163-centre packing in the unit 4-ball has feasible radius r* = 0.21713800642461929883. That beats the live table (0.217115168538) by 2.28e-5.
- The posted Packomania file parses correctly. My six trust-region SLP polishes of it all converge to about 0.21711517680, which is 2.28e-5 below r*.
- The claim is not isometric to the posted packing and shows no sign of being a relaxed copy: its contact graph and shell populations differ, and rigid registration fails.
- The claim also exceeds the Moki & Julio manifest value (by 1.84e-5) and both spherical-code constructions.
- No newer History-of-updates entry exists, and no pending hsp4 range covers N = 163. The unresolved category-unspecified 26-Sep-2026 Moki & Julio *many* 4666-candidate bundle remains a caveat: N must be re-checked against the live table once it leaves the pending list.

pass: true
