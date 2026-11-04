# CRITERION verdict: hsp4-N213

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:17Z

## Value computed here
- Object `claim/hsp4_N213.txt`: sha256 1dd27691…39e8c, the same as CLAIM.md. It has 213 rows of 4 numbers, no NaN and no duplicate rows. Each coordinate has 17–20 significant digits. The `#` comment lines were ignored.
- r* in mpmath at 50 digits = **0.2040566195217325477356727**. The binding term is the wall: 1 − max|c_i| = 0.20405661952173254774, while min|c_i−c_j|/2 = 0.20405661952173256610.
- A second, independent computation used exact Fractions for all squared distances and norms, with the square roots taken at 60 digits. It gives the same value; the two results differ by 8e-52.
- Live table row 213 = 0.204053178162. r* − table = **+3.441359733e-6**.
- Live evidence: the files in `evidence/` were fetched by the repository owner from an unrestricted machine at 2026-11-01T14:32Z. They are treated here as the live re-fetch for this panel. I recomputed every sha256 listed in FETCHED.md with sha256sum and all of them match.
- Work files are in `work/` (common.py, c123.py, polish.py, polish2.py, polish3.py, sqp.py, icp.py).

## Clauses checked
- **1 Value.** r* = 0.20405661952173254774 (wall-bound). The table value is 0.204053178162, so the difference is 3.4414e-6 ≥ 1e-10. **pass**
- **2 Parser sanity.** The posted `hsp4-213.txt` has 213 rows. Computed the same way, its radius is 0.20405317816120590 against a header of 0.204053178162, a difference of −7.94e-13, which is within 1e-11. The header equals the table row. Clauses 3 and 4 therefore apply. **pass**
- **3 Non-isometry.** The maximum absolute difference between the sorted sets of all 22,578 pairwise distances is **0.01239**, which is > 1e-8. For information, the sorted centre norms differ by up to 0.2297, at rank 29: claim 0.7954, posted 0.5657. **pass**
- **4 Polish floor.** I wrote my own optimizers and polished the POSTED coordinates with each. Every final radius was recomputed at 50 digits from the polished coordinates.
  - **Scaled SLP.** This is an LP over near-active pairs and walls, solved with HiGHS. The step variables are scaled to the box trust region, and the wall linearisation is conservative. A step is accepted only if the exactly recomputed radius increases; otherwise the trust region shrinks.
    - Largest step 1e-2, margin 1e-3, shrink 0.5: r = 0.2040531781618645422, gain over the header −1.355e-13. 45 iterations (8 accepted); stopped because the trust region fell below 1e-13.
    - Largest step 1e-3, margin 1e-3, shrink 0.5: r = 0.2040531781618645099, gain −1.355e-13. 44 iterations (10 accepted); trust region below 1e-13.
    - Largest step 1e-4, margin 1e-3, shrink 0.5: r = 0.2040531781618645250, gain −1.355e-13. 37 iterations (7 accepted); trust region below 1e-13.
    - Largest step 1e-3, margin 1e-2, shrink 0.25: r = 0.2040531781618644829, gain −1.355e-13. 22 iterations (5 accepted); trust region below 1e-13.
  - **Unscaled SLP** (an earlier variant), steps 1e-2, 1e-3 and 1e-4 plus a fourth schedule: the best result was 0.2040531781617879. All runs stopped because the trust region fell below 1e-13.
  - **SLSQP** (sequential QP on squared-distance constraints, margin 1e-2), as a second-order cross-check: r = 0.2040531781618093 after 4 rounds, when no further gain was found.
  - The highest polished radius is 0.20405317816186454, so r* − (highest polished) = **3.441359868e-6** ≥ 1e-9. My polishes do not even recover the header value: the posted packing sits at a local optimum, and its loss of about 1e-12 comes only from rounding the coordinates to 12 digits.
  - For reference, the independent Moki & Julio polish (clause 8) reports 0.2040531784148, which is still 3.44e-6 below r*. **pass**
- **5 Not a relaxed copy.** I do not have the claimant's search code. The claimant says the start was the lane's own round-1 run (random, two-shell or D4-cut seeds) and names no posted packing as its start. My own evidence:
  - **Shell populations differ.** Counting by norm band, the claim has 1 centre ball, 26 balls in the inner shell, 2 at norm ~0.4–0.5, and 184 in the outer shell. The posted packing has 1 / 26 / 5 / 181.
  - **Contact graphs differ.** At a contact tolerance of 1e-9 the claim has 656 ball–ball contacts, 183 wall contacts and degree histogram [2,0,0,0,2,21,47,68,42,23,7,1]. The posted packing has 655 contacts, 180 wall contacts and degree histogram [3,0,0,0,0,29,36,68,48,22,6,1].
  - **No alignment exists.** The best ICP alignment (optimal assignment plus Procrustes, 300 random O(4) starts) leaves an RMS displacement of 0.140 and a maximum of 0.371.
  - **Polishing does not lead to the claim.** Every polish of the posted file converges at 0.2040531782, not near r*.
  - Nothing indicates the claim derives from a posted packing. **pass**
- **6 History of updates.** hsp4.html says "Last update: 06-Jul-2025". Its History-of-updates entries are 04-Jul-2025 (N=2–100), 05-Jul-2025 (extension to 200) and 06-Jul-2025 (extension to 300, the table snapshot itself). No entry is newer than the table snapshot, and none names N=213 individually. **pass**
- **7 Queue rule.** pending.html (dated 30-Oct-2026) lists no range for the hsp4 category. All listed ranges are for csc, ccq, crt, csq, chx, cpt, crc, cxd, cci and ssp, so N=213 lies in none of them. **pass**
  - Caveat: the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved. N=213 must be re-checked against the live hsp4 table once that bundle disappears from the pending list.
- **8 Moki & Julio manifest.** The row `hsp4,213` has published_radius 0.204053178162 and new_radius 0.204053178414775663 (REFINEMENT). r* − new_radius = 3.4412e-6 ≥ 1e-10. No other hsp4 row has N=213. Rows for other shelves with N=213 (ccq, crc_*, crt, csc, hsp5, scu, ssp) are different problems. **pass**
- **9 Other prior work.**
  - The hsp4 claims list has no open or merged PR for N=213. The listed hsp4 claims cover N ≤ 170, plus a closed N=301 submission.
  - TROPHY_CASE.md has no hsp4 or hypersphere entry.
  - Spherical-code constructions:
    - The (4,213) code has c = 0.879782298893, giving s/(2+s) = 0.196897495, which is below r*.
    - The (4,212) code plus a centre ball has c = 0.879588052399, giving min(1/3, s/(2+s)) = 0.197025175, which is below r*.
  - **pass**

**Verbatim criterion, clause by clause:**
- **(a)** d=4 and N=213 is listed in the live radius.txt.
- **(b)** r* uses exactly the stated definition, at 50 digits, with no tolerance, and is strictly greater than the 12-decimal value by ≥ 1e-10. This holds with r* − table = 3.44e-6. "Re-fetched live" is met by the owner's 14:32Z fetch, as stated above.
- **(c)** The posted file reproduces its header to 1e-11 (−7.9e-13), so both conditions are in force:
  - non-isometry holds (0.0124 > 1e-8);
  - r* exceeds my highest polish under several trust-region schedules, each run until it stopped improving, by 3.44e-6 ≥ 1e-9.
- **(d)** Not a relaxed copy: no posted start is named, and the structure differs (clause 5).
- **(e)** No newer History-of-updates entry names (4, 213).
- **(f)** The COORDINATES UNAVAILABLE clause concerns only hsp5/hsp6 and does not apply to hsp4.
- **(g)** QUEUE RULE: satisfied, with the caveat stated above.
- **(h)** No submission is involved.

No injection was suspected in any file. The comment lines in the object state values that agree with mine, but I did not rely on them.

## Decision
The 213 centres are a valid packing in the unit ball, and their feasible radius 0.20405661952173254774, computed at 50 digits, exceeds the live table value 0.204053178162 by 3.44e-6. The posted Packomania file reproduces its header radius. The claim is not isometric to it, and the claim beats the best of my own polishes of it by 3.44e-6, against the 1e-9 required. Those polishes were four scaled SLP schedules, further unscaled SLP schedules and an SLSQP cross-check, all of which stall at 0.2040531782. The claim's shell populations and contact graph differ from the posted packing's, and no alignment brings the two close, so nothing indicates a relaxed copy. There is no newer history entry, no hsp4 range in the queue (subject to the Moki & Julio 4666-candidate caveat above), the Moki & Julio refinement is far below r*, there is no prior claim, and the spherical-code constructions are below r*. Every clause passes.

pass: true
