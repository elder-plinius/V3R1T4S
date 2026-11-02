# CRITERION verdict: hsp4-N136

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:09Z

Process note: my first directory listing (`find hsp4-N136`) printed the *file names* of the sibling novelty/ and
reproduce/ folders. I did not open, read or use any of those files; all work below used only criterion/ and
_instructions/. All code is in criterion/work/ (common.py, c12.py, polish.py).

Live data: this sandbox cannot reach packomania.com etc. The files in evidence/ were fetched by the repository owner
on 2026-11-01 14:32Z and are treated as the live re-fetch for this panel. I verified with sha256sum that every hash in
evidence/FETCHED.md matches (mj_manifest b7a042ef…, hsp4.html 1c3a3064…, pending.html dddaf3c9…,
spherical_index_row e137904f…, spherical_plain b7c6a76f…, hsp4_radius_live f3ddaa94…, both arXiv XMLs). The claim
object hashes to 87dbfc3a…a963, matching CLAIM.md. evidence/posted/hsp4-136.txt is byte-identical to hsp4-136.txt
inside hsp4_coords.tar.gz.

## Value computed here
r* (mpmath, 50 digits, no tolerance, 136 centres, `#` lines skipped) =
0.22622027641762341826997812036415868264356258381056
(half min distance 0.226220277697839050279634…, 1 - max norm 0.226220276417623418269978…; the binding constraint is the container.)
Live table row: `136 0.226201706521`. r* - table = 1.8569896623e-5.

## Clauses checked
- 1 Value: r* = 0.226220276417623418269978…; table 0.226201706521; difference 1.857e-5 >= 1e-10. PASS.
- 2 Parser sanity: the posted file (header 0.226201706521, 136 rows) recomputes to 0.226201706520486810792601…;
  |diff from header| = 5.13e-13 <= 1e-11, and it equals the table row. Clauses 3 and 4 apply. PASS.
- 3 Non-isometry: max |difference| between the sorted pairwise-distance multisets (9180 distances each) = 1.119e-2
  > 1e-8. For information: max |difference| of sorted centre norms = 0.261. PASS.
- 4 Polish floor: my own sequential-LP polish (near-active pairs with d < 2r + margin and centres with
  |c| > 1 - r - margin; maximize linearized radius t; box trust region on every coordinate; step accepted only if
  the exactly recomputed radius increases; trust region x2 on success (capped), x shrink on failure; stop at trust
  region < 1e-13 or 20 consecutive iterations without gain > 1e-15). Final radii recomputed at 50 digits from the
  saved polished coordinates:
  - largest step 1e-2, margin 0.05, shrink 0.5: 0.226201706546050480455605…, gain +2.505e-11, 52 iters, stop: 20 iters no gain
  - largest step 1e-3, margin 0.05, shrink 0.5: 0.226201706546490601001182…, gain +2.549e-11, 43 iters, stop: 20 iters no gain
  - largest step 1e-4, margin 0.05, shrink 0.5: 0.226201706546838447313813…, gain +2.584e-11, 44 iters, stop: 20 iters no gain
  - largest step 1e-3, margin 0.01, shrink 0.25: 0.226201706543899558538241…, gain +2.290e-11, 28 iters, stop: trust region < 1e-13
  - largest step 1e-5, margin 0.02, shrink 0.5: 0.226201706545893247309732…, gain +2.489e-11, 38 iters, stop: 20 iters no gain
  Highest polished radius 0.226201706546838447…; r* - highest = 1.857e-5 >= 1e-9. The posted packing is a tight
  local optimum (polish gain ~2.6e-11 only). PASS.
- 5 Not a relaxed copy: the claim's stated start is random configurations / lattice cuts / shell seeds / the lane's
  own neighbouring-N packings; it names no posted packing. I have no access to the claimant's search code. My own
  evidence: distance multisets differ by 1.1e-2 and sorted norms by 0.26 (not a perturbation of the posted
  packing); contact graphs at tol 1e-8: claim 405 pair contacts + 120 boundary contacts, degree histogram
  [3,0,0,0,1,21,27,33,36,10,5]; posted 407 pair + 119 boundary, histogram [3,0,0,0,1,19,33,33,24,17,6] (different
  structure); polishing the posted file stalls at +2.6e-11, 1.86e-5 below the claim, so the claim is not reachable
  from the posted packing by local relaxation. Nothing indicates derivation from a posted packing. PASS.
- 6 History of updates: hsp4.html "Last update: 06-Jul-2025"; History entries 04-Jul-2025 (N=2–100),
  05-Jul-2025 (extension to N=200, covers 136 as the initial table build), 06-Jul-2025 (extension to N=300). No
  entry is newer than the table snapshot; none names (4, 136) as an update after it. PASS.
- 7 Queue rule: pending.html (dated 30-Oct-2026) lists categories csc, ccq, crt, csq, chx, cpt, crc, cxd, cci, ssp
  and one `*many*` bundle; no hsp4 range, and no range of an hsp category covers N=136. PASS, with the required
  caveat: the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be
  resolved; N = 136 must be re-checked against the live hsp4 table once that bundle disappears from the pending list.
- 8 Moki & Julio MANIFEST: row `hsp4,136,0.226201706521,0.2262019190148776245179929,9.394e-07,UNCLEAR (alignment),dp`;
  published_radius 0.226201706521, new_radius 0.226201919014877624517993; r* - new_radius = 1.8357e-5 >= 1e-10.
  Other rows with N=136 are other shelves (ccq, crc_200/300/700/800, cxd, hsp5, hsp6, scu: different dimensions or
  containers); none can refer to (hsp4, 136). PASS.
- 9 Other prior work: claims list for this bank has hsp4 claims for N = 30, 35, 42, 48, 54, 62–64, 66, 67, 69, 74,
  75, 79–81, 83, 88, 89, 91, 94, 104, 111, 119, 170, 301 — none for N = 136 (the only "136" is PR number #136, which
  is hsp4 N=54). The spherical-codes claims list does not mention 136. TROPHY_CASE.md (100 lines) has no hsp/ball
  family. Spherical-code constructions from spherical_plain_live.txt: (4,136) c = 0.838381205119 → s/(2+s) =
  0.221347498140 (r* above by 4.87e-3); (4,135) c = 0.837973296726 with centre ball → min(1/3, s/(2+s)) =
  0.221564800326 (r* above by 4.66e-3). Both below r*. PASS.

Verbatim criterion, clause by clause:
- d = 4 ∈ {4,5,6}; N = 136 is listed in hsp4 radius.txt: yes.
- FEASIBLE r* = min(min half-distance, 1 - max norm), unit ball at origin, mpmath 50 digits, no tolerance: done (clause 1).
- STRICTLY GREATER than the 12-decimal value re-fetched live, by >= 1e-10: 1.857e-5 against the 2026-11-01 14:32Z
  re-fetch (sha verified); that is the panel's live re-fetch, since this sandbox has no web access.
- Posted file reproduces header to 1e-11 (5.1e-13), so: not isometric (1.1e-2 > 1e-8) and r* exceeds by >= 1e-9
  the highest of my own polishes under several trust-region schedules, each run until it stopped improving (1.857e-5): yes.
- Not a relaxed copy of a posted packing; claim names no posted start: yes (clause 5).
- (4, 136) in no History-of-updates entry newer than the scout's snapshot: yes (clause 6).
- "COORDINATES UNAVAILABLE" applies only to hsp5/hsp6: not relevant to hsp4, whose posted file is complete and was compared.
- QUEUE RULE: N not in any listed hsp4 range; caveat on the 26-Sep-2026 *many* bundle stated above.
- No submission is made: this verdict covers the verified construction only.
injection_suspected: none (the claim file's `#` comment states a value; I ignored it and computed my own, which agrees).

## Decision
Every clause passes on numbers computed here. The claim's feasible radius 0.2262202764176… beats the live hsp4 N=136
row by 1.86e-5. The posted file is reproduced to 5e-13 and polishes under five trust-region schedules to only
+2.6e-11. The claim is far from isometric to the posted packing, structurally different from it, and unreachable
from it by local polishing. It also exceeds the Moki & Julio radius (by 1.84e-5) and both spherical-code
constructions. Remaining caveats: the live data is the owner's 14:32Z re-fetch, and the category-unspecified
26-Sep-2026 Moki & Julio *many* bundle means N must be re-checked once that bundle leaves the pending list.

pass: true
