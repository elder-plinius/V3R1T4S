# NOVELTY verdict: hsp4-N213

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:15Z

## Value computed here

All code is in `work/` (common.py, c123.py, polish.py, polish_sanity.py). It uses mpmath at 50 digits on the coordinate strings exactly as written in the files. I ignored the comment lines in `claim/hsp4_N213.txt`.

- Object sha256 1dd2769172958fa1083d9614660de9dfb4e262f6235d897100991024b4839e8c matches CLAIM.md. It has 213 rows of 4 coordinates.
- half min distance = 0.20405661952173256609552697629056316349631247455091
- 1 - max norm      = 0.20405661952173254773567268004122093725499478795627
- **r* = 0.20405661952173254773567268004122093725499478795627** (20 digits: 0.20405661952173254774)
- Live table row 213 = 0.204053178162. **r* - table = 3.44135973254774e-6.**

Evidence files: I recomputed the sha256 of all eight files listed in `evidence/FETCHED.md` and every one matches. They were fetched from an unrestricted machine on 2026-11-01T14:32Z, and I treat them as this panel's live re-fetch. I made no web access. The posted `evidence/posted/hsp4-213.txt` is byte-identical to the `hsp4-213.txt` member of `hsp4_coords.tar.gz` (sha256 b929acc8…63df, the same archive the bank page names).

## Clauses checked

- **1 Value: PASS.** r* = 0.204056619521732547736… The live row is 0.204053178162, so r* - table = 3.441e-6, which is at least 1e-10.
- **2 Parser sanity: PASS. Clauses 3 and 4 apply.** The posted file has 213 rows of index plus 4 coordinates. Its recomputed radius is 0.204053178161205900238907758508 (header 0.204053178162), a difference of -7.94e-13. That is within 1e-11 of both the header and the table row.
- **3 Non-isometry: PASS.** Across all 22578 pairwise distances, the largest difference between the sorted distance multisets is 1.239e-2, well above 1e-8. For information, the sorted centre norms differ by up to 0.2297.
- **4 Polish floor: PASS.** I wrote my own sequential-LP polisher (HiGHS). On each iteration it:
  - linearizes the pairs with distance < 2r + margin and the centres with norm > 1 - r - margin;
  - maximizes the linearized radius inside a box trust region on every coordinate;
  - accepts a step only if the exactly recomputed radius increases (the trust region then grows ×1.5, capped at its start value) and shrinks the region otherwise.

  Every run started from the posted coordinates. Final radii below are recomputed at 50 digits from the polished coordinates:

  | run | largest step | margin | shrink | iterations | stop reason | polished r (mp50) | gain over header |
  |---|---|---|---|---|---|---|---|
  | A | 1e-2 | 0.02 | 0.5 | 39 | 20 consecutive iterations with no gain above 1e-15 | 0.204053178161720998 | -2.79e-13 |
  | B | 1e-3 | 0.02 | 0.5 | 36 | same | 0.204053178161756258 | -2.44e-13 |
  | C | 1e-4 | 0.01 | 0.5 | 38 | same | 0.204053178161803026 | -1.97e-13 |
  | D | 1e-2 | 0.05 | 0.7 | 20 | same; no step accepted | 0.204053178161205900 | -7.94e-13 |
  | E | 3e-3 | 0.005 | 0.3 | 22 | trust region < 1e-13 | 0.204053178161685221 | -3.15e-13 |

  Highest polished radius: 0.2040531781618030 (run C). r* - highest = 3.4414e-6, which is at least 1e-9.

  Polisher sanity check: starting from the posted file with every coordinate perturbed by up to ±3e-4 (r = 0.20363795), the same code climbs back to 0.2040531781767524 (+1.5e-11 over the header). So the optimizer works, and the posted packing really is at a local optimum near its header value, about 3.44e-6 below the claim.
- **5 Not a relaxed copy: PASS.**
  - The claimant says (in CLAIM.md) that lane hsp4-b never had Packomania's coordinates, that it started from random, two-shell and D4-cut seeds, and that N = 213 was the lane's own round-1 run. The claim names no posted packing as its start.
  - I did not get the claimant's search code.
  - Contact graphs differ (tolerance 1e-9; the same at 1e-7). The claim has 656 ball-ball contacts, 183 boundary contacts and 2 rattlers. The posted file has 655, 180 and 3, which matches the page row (835 = 655 + 180, 3 rattlers).
  - The degree sequences (ball plus wall) differ: claim [2,0,0,0,2,21,47,68,42,23,7,1], posted [3,0,0,0,0,29,36,68,48,22,6,1].
  - The radial shell structure differs: claim 1 / 28 / 184 (inner, middle, outer shell), posted 1 / 31 / 181.
  - The distance multisets differ by 1.2e-2, and the posted file's polishes stay 3.44e-6 below r*.

  Nothing points to the claim being derived from the posted packing.
- **6 History of updates: PASS.** hsp4.html shows "Last update: 06-Jul-2025". Its History of updates has only three entries: 04-Jul-2025 (N = 2–100), 05-Jul-2025 (extension to 200) and 06-Jul-2025 (extension to 300). The 06-Jul-2025 entry covers N = 213 only as the table's original extension, and it is not newer than the table snapshot. No entry names (4, 213) after the snapshot. The page row 213 equals 0.204053178162, the radius.txt value.
- **7 Queue rule: PASS (with caveat).** pending.html is dated 30-Oct-2026 and lists no range for the hsp4 category. The categories listed are csc, ccq, crt, csq, chx, cpt, crc, cxd, cci and ssp, plus one '*many*' bundle. N = 213 lies in no hsp4 range. **Caveat:** the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved here. N = 213 must be re-checked against the live hsp4 table once that bundle disappears from the pending list.
- **8 Moki & Julio MANIFEST: PASS.**
  - The only matching row is `hsp4,213`: published_radius 0.204053178162, new_radius 0.204053178414775663236279 (REFINEMENT, gain 1.24e-9). r* - new_radius = 3.4411e-6, which is at least 1e-10.
  - The other N = 213 rows belong to other shelves (hsp5, ccq, crc_*, crt, csc, scu, ssp), so they are different cells.
  - Domination check: no hsp4 manifest row with N > 213 has new_radius ≥ r*, and neither does any live-table row with N > 213 (for N = 214 these are 0.2038844728 and 0.203884464476). Deleting balls from a larger known packing therefore does not reach r*.
  - The neighbouring row hsp4 N = 212 (new 0.2042836703) is a different N.
- **9 Other prior work: PASS.**
  - The claims list for packomania-hyperspheres-hsp4-hsp6 has no open, merged or closed claim for hsp4 N = 213. The N values present are 30, 35, 42, 48, 54, 62–64, 66, 67, 69, 74, 75, 79–81, 83, 88, 89, 91, 94, 104, 111, 119, 170 and 301. The cohn-table list has no hsp4 entry except a cross-listed N = 170.
  - TROPHY_CASE.md has no hsp/hypersphere/Packomania entry and no 213.
  - Spherical-code construction from `spherical_plain_live.txt`:
    - (4, 213): c = 0.879782298893, so s/(2+s) = 0.196897495432 and r* is higher by 7.16e-3.
    - (4, 212) plus a centre ball: c = 0.879588052399, so min(1/3, s/(2+s)) = 0.197025175049 and r* is higher by 7.03e-3.

    Both are below r*.

## Decision

The claimed configuration is feasible with r* = 0.20405661952173254774, 3.44e-6 above the live hsp4 row 213 (re-fetched 2026-11-01T14:32Z). It is not isometric to the posted packing. Every one of my five polishes of the posted file stalls about 2e-13 below the header, so the claim is not a polish of the posted packing. Its contact graph and shell structure differ from the posted one, and the claim names no posted start.

On prior work:
- No History-of-updates entry after 06-Jul-2025 names N = 213.
- No hsp4 range is pending.
- The Moki & Julio public record for this cell (0.2040531784148) is 3.44e-6 below r*.
- No claim PR or trophy entry covers this cell.
- Both spherical-code constructions are about 7e-3 lower.

The one standing caveat is the category-unspecified 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle. It cannot be resolved, so N = 213 must be re-checked against the live table once that bundle leaves the pending list. All nine clauses pass on evidence computed or read here.

pass: true
