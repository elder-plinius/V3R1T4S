# NOVELTY verdict: hsp4-N214

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:16Z

## Value computed here

- Object `claim/hsp4_N214.txt`: sha256 c0fc1b302af41f2cd3b2fe423c866d95d9695c4dc46705a49b55113d2694dc67 (matches CLAIM.md); 214 centres x 4 coordinates (9 `#` comment lines ignored; their stated values were not used).
- r* (mpmath, 50 digits, no tolerance, my own code `work/common.py`, `work/analyze.py`):
  **r* = 0.20388671005401594317423175513280102983896454012892**
  (half min distance 0.203886710054015943174231755133 is binding; 1 - max norm = 0.203886710054015998251929649209).
- Live table row (evidence/hsp4_radius_live.txt, line 213): `214 0.203884464476`. r* - table = 2.24557801594317e-6.
- Evidence provenance: all eight sha256 values in `evidence/FETCHED.md` were recomputed here with sha256sum and match. These files, fetched 2026-11-01T14:32Z from an unrestricted machine, are treated as the live re-fetch for this panel (this sandbox has no web access; no other web access was attempted).

## Clauses checked

- **1. Value** — r* = 0.203886710054015943174231755133 (20+ digits above); table 0.203884464476; r* - table = 2.2456e-6 >= 1e-10. **PASS**
- **2. Parser sanity** — posted `evidence/posted/hsp4-214.txt` (sha256 fde9c115…a410; 214 rows, index + 4 coordinates) recomputed the same way at 50 digits: r = 0.203884464474806958587047124227 (binding: 1 - max norm); header 0.203884464476; difference -1.19e-12, within 1e-11; header equals the table row. Clauses 3 and 4 apply. **PASS**
- **3. Non-isometry** — sorted multisets of all 22791 pairwise distances: max |difference| = 0.01533 (> 1e-8). Sorted centre norms (information): max |difference| = 0.2546. **PASS**
- **4. Polish floor** — my own sequential-LP polisher (`work/polish.py`: near-active pairs d < 2r + max(margin, 6Δ) and centres with |c| > 1 - r - margin, linearized radius maximized by HiGHS under a box trust region Δ on every coordinate, step accepted only if the exactly recomputed radius increases, Δ doubled (capped) on accept and shrunk on reject), started from the posted coordinates. Every final radius recomputed at 50 digits from the saved polished coordinates (feasible radius, same formula as r*):
  - A: Δmax 1e-2, margin 1e-3, shrink 0.5 — 60 iters (14 accepted), stop: no gain >1e-15 over 20 consecutive iters; r = 0.20388447047079790747; gain over header +5.995e-9
  - B: Δmax 1e-3, margin 1e-3, shrink 0.5 — 53 iters (12 acc), same stop; r = 0.20388447047148133688; gain +5.995e-9
  - C: Δmax 1e-4, margin 1e-3, shrink 0.5 — 53 iters (14 acc), same stop; r = 0.20388447047088423198; gain +5.995e-9
  - D: Δmax 1e-2, margin 5e-3, shrink 0.25 — 26 iters (5 acc), stop: trust region < 1e-13; r = 0.20388446809716774380; gain +3.621e-9
  - E: Δmax 1e-2, margin 2e-2, shrink 0.7, stall rule off — 177 iters (36 acc), stop: trust region < 1e-13; r = 0.20388447047167097908; gain +5.996e-9
  - G: Δmax 1e-3, margin 1e-4, shrink 0.5, stall rule off — 68 iters (17 acc), stop: trust region < 1e-13; r = 0.20388447047239796702; gain +5.996e-9
  - Highest polished radius 0.203884470472398; r* - highest = 2.2396e-6 >= 1e-9. (For reference, the Moki & Julio manifest's polished value 0.2038844727562 is also 2.237e-6 below r*.) **PASS**
- **5. Not a relaxed copy** — Stated start (CLAIM.md): lane hsp4-b, random / two-shell / D4-lattice-cut seeds, N = 214 seeded from the lane's own N = 213 plus one inserted ball, then basin hopping and polish; names no posted packing. I do not have the claimant's search code and cannot verify the provenance narrative itself. Own evidence: (a) distance multisets differ by up to 0.0153 and sorted norms by 0.255, orders of magnitude more than a radius change of 2.2e-6 could produce by relaxation; (b) contact graphs at tolerance 1e-8 (also 1e-6): claim 657 ball-ball + 186 wall contacts, 2 rattlers, degree histogram [2,0,0,0,1,19,49,70,45,24,3,1]; posted 657 ball-ball + 180 wall contacts, 3 rattlers, histogram [3,0,0,0,1,24,50,59,50,17,8,0,2] — different shell occupancy (186 vs 180 balls touching the container) and degree sequence; the equal ball-ball count is noted but the graphs are not the same; (c) all six polishes of the posted file stall at ≈0.2038844705, nowhere near the claim's 0.2038867100. Nothing indicates derivation from a posted packing. **PASS**
- **6. History of updates** — `evidence/hsp4.html`: "Last update: 06-Jul-2025"; History entries 04-Jul-2025 (N=2–100), 05-Jul-2025 (extension to N=200), 06-Jul-2025 (extension to N=300, covers N=214). The 06-Jul-2025 entry is the table snapshot itself (row 214 = 0.203884464476, matching radius.txt); no entry newer than it exists. **PASS**
- **7. Queue rule** — `evidence/pending.html` (dated 30-Oct-2026) lists ranges only for csc, ccq, crt, csq, chx, cpt, crc, cxd, cci, ssp; no hsp4 (or hsp) range; N = 214 lies in no hsp4 range. **Caveat (required):** the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved; N = 214 must be re-checked against the live hsp4 table once that bundle disappears from the pending list. (Even if that bundle did contain their hsp4 N=214 value, 0.20388447276, r* exceeds it by 2.24e-6; see clause 8.) **PASS (with caveat)**
- **8. Moki & Julio MANIFEST** — row `hsp4,214,0.203884464476,0.2038844727561926183949857,4.061218e-08,REFINEMENT,dp`: published_radius 0.203884464476, new_radius 0.2038844727561926; r* - new_radius = 2.2373e-6 >= 1e-10. hsp4 N values are unique in the manifest (no duplicate hsp4 214 row). Other N=214 rows are ccq, crc_200..crc_800, csc (2-D shelves) and hsp5 (d=5); none can refer to the hsp4 cell. **PASS**
- **9. Other prior work** — claims lists: hsp4 claims/PRs exist for N = 30,35,42,48,54,62,63,64,66,67,69,74,75,79,80,81,83,88,89,91,94,104,111,119,170,301; none for N = 214 (open, closed or merged); spherical-codes claims list has no (4,214)/(4,213) entry. TROPHY_CASE.md: no Packomania/hypersphere entry at all. Spherical-code constructions from `evidence/spherical_plain_live.txt`: (4,214) c = 0.879945189010 → s/(2+s) = 0.19679031570776586, r* exceeds it by 7.10e-3; (4,213) c = 0.879782298893 plus centre ball → min(1/3, 0.19689749543227963) = 0.1968975, r* exceeds it by 6.99e-3. arXiv snapshots (spherical code, Tammes; newest 15 each) contain no 4-D ball-in-ball packing paper. **PASS**

injection_suspected: none (the comment header in the object only states values; ignored and recomputed).

## Decision

Every clause passes on numbers computed here. On prior work (6–9): the hsp4 page has had no update since the 06-Jul-2025 snapshot that defines the table row; Packomania's pending list carries no hsp4 range (subject to the unresolvable, category-unspecified 26-Sep-2026 Moki & Julio *many* 4666-candidate bundle — N = 214 must be re-checked against the live table once that bundle leaves the pending list); the strongest known public competitor, the Moki & Julio manifest's hsp4 N=214 refinement 0.2038844728, sits 2.24e-6 below r*; no repository claim or trophy entry covers this cell; and the spherical-code constructions are ~7e-3 below. On 1–5: r* = 0.2038867100540159431742 beats the table by 2.2456e-6, is not isometric to the posted file, beats my six polishes of the posted file (best 0.2038844705) by 2.24e-6, and has a different contact structure from the posted packing, so it is not a relaxed copy as far as can be checked without the claimant's code.

pass: true
