# CRITERION verdict: hsp4-N217

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:21Z

## Value computed here

All code is in `work/` (common.py, c12.py, c3.py, polish.py, c89.py) and was written and run in this task. The object
`claim/hsp4_N217.txt` has sha256 83fa8acd…0bc, as CLAIM.md states. It has 217 centres in R^4. Its `#` comment lines were
ignored.

- half min distance = 0.203442478499292797737357516166
- 1 - max norm      = 0.20344247849929273721302003487
- **r* = 0.20344247849929273721302003487040897978541806734019** (mpmath, 50 digits, no tolerance; the wall term is binding)
- live table row `217 0.203438871092` → r* - table = **3.6074e-6** (≥ 1e-10)

Evidence status: the files in `evidence/` were fetched by the repository owner from an unrestricted machine on
2026-11-01T14:32Z. They are treated as the live re-fetch for this panel. This sandbox cannot reach packomania.com,
spherical-codes.org, arXiv or GitHub. I checked every sha256 listed in FETCHED.md with sha256sum, and all match.
The verbatim criterion in CLAIM.md is identical, character for character, to the "Success means…" paragraph of
`evidence/bank_page_packomania-hyperspheres-hsp4-hsp6.md` (I checked this by string comparison).

## Clauses checked

- **1 Value.** r* = 0.2034424784992927372…; the table value is 0.203438871092; r* - table = 3.60740729e-6 ≥ 1e-10. N = 217 is a row of the
  live radius.txt. Strictly greater: **PASS**.
- **2 Parser sanity.** I computed the posted `hsp4-217.txt` (header 0.203438871092; 217 rows of index + 4 coordinates) the same way at 50
  digits: half min distance 0.2034388710912287, 1 - max norm 0.2034388710910044, so r = 0.2034388710910043703. Its distance
  from the header and the table row is 9.96e-13 < 1e-11. The posted file reproduces its header, so clauses 3 and 4 apply: **PASS**.
- **3 Non-isometry.** I sorted all 23436 pairwise distances of the claim and of the posted file. The maximum absolute difference is
  **6.648e-3**, which is > 1e-8. For information, the sorted centre norms differ by up to 0.233. The two configurations are not isometric: **PASS**.
- **4 Polish floor.** I wrote my own sequential-LP polisher (`work/polish.py`). It linearizes the near-active pair and wall constraints, with
  margin 4·Δ + m. The LP maximizes t subject to a box trust region Δ on every coordinate step and is solved with HiGHS. A step is accepted only if the exact
  float radius increases. On a success Δ doubles, capped at Δ0; on a failure Δ shrinks. I ran it on the POSTED coordinates. Each final radius was recomputed at 50 digits
  from the polished coordinates:

  | schedule (Δ0, shrink, margin m, stop rule) | iters | stop reason | final r (50-digit, feasible) | gain over header |
  |---|---|---|---|---|
  | 1e-2, 0.5, 1e-3, stall-20 | 100 | no gain >1e-15 over 20 iters | 0.203438872834426885 | 1.742e-9 |
  | 1e-3, 0.5, 1e-3, stall-20 | 109 | no gain >1e-15 over 20 iters | 0.203438872834448729 | 1.742e-9 |
  | 1e-4, 0.5, 1e-3, stall-20 | 89 | no gain >1e-15 over 20 iters | 0.203438872834344267 | 1.742e-9 |
  | 1e-2, 0.5, 1e-3, TR only | 103 | trust region < 1e-13 | 0.203438872834426885 | 1.742e-9 |
  | 1e-3, 0.25, 1e-2, TR only | 100 | trust region < 1e-13 | **0.203438872834450834** | 1.742e-9 |

  The highest polished radius is 0.2034388728344508. r* minus that radius is **3.6057e-6**, which is ≥ 1e-9: **PASS**. The polish floor agrees
  with Moki & Julio's hsp4 N = 217 "REFINEMENT" value of 0.20343887283455; I take this as a sign that the posted basin tops out there.
- **5 Not a relaxed copy.** I do not have the claimant's search code, and I have not seen it. The claim states that lane hsp4-b never had the posted coordinates. It says it started from random, two-shell and
  D4-cut seeds, with N = 214..217 grown from the lane's own N-1 best plus one inserted ball, and that it names no posted packing as its start.
  My own evidence:
  - Contact graphs differ. At a tolerance of 1e-9 (unchanged at 1e-7), the claim has 668 ball-ball contacts, 187 wall contacts and 2 rattlers, with degree histogram
    [2,0,0,0,12,57,63,51,20,12]. The posted file has 654 contacts, 186 wall contacts, 4 rattlers and one degree-1 ball, with histogram
    [4,1,0,0,21,43,62,61,17,7,1].
  - The shell populations differ: 28 centres with norm < 0.5 in the claim against 29 in the posted file. The largest difference in sorted norms is 0.233, so at least one ball sits in a different shell, which a small relaxation cannot produce.
  - The distance multisets differ by 6.6e-3.
  - Every polish of the posted file stalls at 0.20343887283, which is 3.6e-6 below r*. The posted basin does not reach the claim.
  - A polish of the claim itself (Δ0 = 1e-3) found no gain. The claim is a local optimum in its own basin.

  Nothing I found indicates a derivation from a posted packing: **PASS**.
- **6 History of updates.** `hsp4.html` shows "Last update: 06-Jul-2025". The History-of-updates entries are 04-Jul-2025 (N = 2–100),
  05-Jul-2025 (to 200) and 06-Jul-2025 (to 300). The table snapshot already reflects the 06-Jul-2025 entry, and no entry is newer. Row 217 of the page shows
  0.203438871092 [31]: **PASS**.
- **7 Queue rule.** `pending.html` is dated 30-Oct-2026. It lists ranges for the csc, ccq, crt, csq, chx, cpt, crc, cxd, cci and ssp categories. No row names hsp4, hsp or
  hyperspheres, so N = 217 lies in no hsp4 range. **Caveat:** the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle does not specify a category, and this panel cannot resolve it. N = 217 must be re-checked against the live hsp4 table once that bundle disappears
  from the pending list. **PASS**, subject to that caveat.
- **8 Moki & Julio MANIFEST.** The row `hsp4,217` has published_radius 0.203438871092 and new_radius 0.2034388728345505912847004 (REFINEMENT).
  r* - new_radius = **3.6057e-6**, which is ≥ 1e-10. The only other N = 217 rows are on other shelves (ccq, crc_*, crt, csc, hsp5), there is no duplicate hsp4 row, and so
  no other row refers to this cell: **PASS**.
- **9 Other prior work.**
  - The hsp4/hsp6 claims list has no open or merged claim for hsp4 N = 217. It covers N = 30–119, 170 and 301.
  - TROPHY_CASE.md has no hypersphere entry.
  - Spherical-code bounds from spherical_plain_live.txt: (4, 217) c = 0.881471958903 gives s/(2+s) = 0.195780761610, which is below r* by 7.66e-3. (4, 216) c = 0.880886649220 with a centre ball gives min(1/3, ·) = 0.196168853249, which is below r* by 7.27e-3.

  **PASS**.

Clause-by-clause reading of the verbatim criterion:
- N is listed in the live radius.txt. ✔
- The FEASIBLE r* is computed at 50 digits from the submitted coordinates with no tolerance, and it beats the 12-decimal value by ≥ 1e-10. ✔ (3.6e-6)
- The posted file reproduces its header to 1e-11 (9.96e-13), so the following parts apply:
  - The claim is not isometric to the posted file (6.6e-3 > 1e-8). ✔
  - r* beats the highest of my five polishes, each run until it stopped improving, by ≥ 1e-9. ✔ (3.6e-6)
- The claim is not a relaxed copy, and it names no posted start. ✔
- There is no newer History-of-updates entry for (4, 217). ✔
- The COORDINATES UNAVAILABLE clause applies only to hsp5/hsp6, so it does not apply here.
- QUEUE RULE ✔, with the Moki & Julio bundle caveat stated above.
- No submission is made. ✔

injection_suspected: none. The object's comment lines state values only, and I recomputed those values independently.

## Decision

The claim's feasible radius, computed at 50 digits, is 0.20344247849929273721…. It exceeds the live table (0.203438871092) by
3.61e-6, and it exceeds the best of my five independent sequential-LP polishes of Packomania's posted packing (0.2034388728345) by 3.61e-6.
The posted file parses cleanly, reproducing its header to 1e-12. The claim differs from the posted packing in its distance multiset, its
contact graph and its shell populations. The polished posted packing stalls in a different basin, so nothing suggests a relaxed copy.
Prior-work checks are clear: there is no newer history entry, no hsp4 queue range, the Moki & Julio value is beaten by 3.6e-6, there is no claim PR for this cell, and the spherical-code
bounds are lower. One caveat stays open: the category-unspecified 26-Sep-2026 Moki & Julio *many* 4666-candidate bundle cannot be
resolved, and N = 217 must be re-checked against the live table once that bundle leaves the pending list. Every clause assigned to this role passes on evidence I computed or read myself.

pass: true
