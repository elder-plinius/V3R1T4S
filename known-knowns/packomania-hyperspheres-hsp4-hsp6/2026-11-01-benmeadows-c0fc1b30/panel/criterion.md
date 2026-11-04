# CRITERION verdict: hsp4-N214

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:15Z

## Value computed here
- Object `claim/hsp4_N214.txt`: sha256 c0fc1b30...dc67 (matches CLAIM.md); 214 centres, all 4-dimensional (`#` comment lines skipped, their stated values ignored and recomputed).
- r* (mpmath, 50 digits, no tolerance) = 0.20388671005401594317423175513280102983896454012892
  - min half pair distance = 0.203886710054015943174231755133 (binding)
  - 1 - max |c_i| = 0.203886710054015998251929649209
- Live table row (evidence/hsp4_radius_live.txt): `214 0.203884464476`. r* - table = 2.24558e-6.
- Live re-fetch: the evidence/ files were fetched by the repository owner on an unrestricted machine on 2026-11-01 14:32Z; I verified every sha256 in FETCHED.md with sha256sum (all match) and treat them as the live re-fetch for this panel. No other web access was attempted.
- injection_suspected: none (the claim file's comment lines state r*, which I ignored; my value agrees).

## Clauses checked
- 1 Value: r* = 0.2038867100540159431742317551..., table 0.203884464476, margin 2.2456e-6 >= 1e-10. PASS.
- 2 Parser sanity: posted hsp4-214.txt (214 rows) recomputed at 50 digits = 0.203884464474806958587...; header 0.203884464476 (= table row); difference -1.19e-12, within 1e-11. Clauses 3 and 4 apply. PASS.
- 3 Non-isometry: sorted multisets of all 22791 pairwise distances differ by max 1.533e-2 (mean 5.2e-3; 99.996% of entries differ by > 1e-6) > 1e-8. Sorted centre norms differ by max 0.2546 (info). PASS.
- 4 Polish floor: my own sequential-LP polish (HiGHS) of the posted file from its posted coordinates; near-active pairs (|ci-cj| < 2r + margin + 2*delta) and wall constraints (|ci| > 1 - r - margin - 2*delta), maximize linearized radius under a box trust region delta on every coordinate, accept only if exactly recomputed radius increases (delta*1.5 up to max), else shrink. Final radii recomputed at 50 digits from the polished coordinates (feasible radius, same formula as r*):
  - max step 1e-2, margin 1e-3, shrink 0.5: 0.2038844704721537 (gain over header +5.996e-9), 62 its, stop: no gain > 1e-15 in 20 its
  - max step 1e-3, margin 1e-3, shrink 0.5: 0.2038844704709408 (+5.995e-9), 53 its, stop: no gain > 1e-15 in 20 its
  - max step 1e-4, margin 1e-3, shrink 0.5: 0.2038844704718142 (+5.996e-9), 55 its, stop: no gain > 1e-15 in 20 its
  - max step 1e-3, margin 1e-2, shrink 0.25: 0.2038844683780333 (+3.902e-9), 22 its, stop: trust region < 1e-13
  - max step 1e-2, margin 5e-3, shrink 0.3: 0.2038844677319395 (+3.256e-9), 27 its, stop: trust region < 1e-13
  - Highest polished = 0.2038844704721537; r* - highest = 2.2396e-6 >= 1e-9. (For reference the Moki & Julio refinement of the posted cell, 0.20388447276, is also 2.24e-6 below r*.) PASS.
- 5 Not a relaxed copy: claimant states lane hsp4-b never had posted coordinates; seeds were random/two-shell/D4-cut and, for N=214, the lane's own N=213 best plus one inserted ball; it names no posted packing. I do not have the claimant's search code. My own evidence: shell structure differs (claim: 1 central + 27 inner (|c| 0.41-0.48) + 186 on the outer wall; posted: 1 + 27 + 4 balls at |c| 0.54-0.59 + 182 on the wall); contact graphs at tol 1e-8: claim 657 contacts, 186 wall contacts, 2 rattlers, degree histogram [2,0,0,0,1,19,49,70,45,24,3,1]; posted 657 contacts, 180 wall, 3 rattlers, histogram [3,0,0,0,1,24,50,59,50,17,8,0,2] (equal pair count but different degree sequence and wall count); best orthogonal-alignment + assignment (ICP, 200 random starts) RMS displacement 0.148 (max 0.39), comparable to a ball radius; all polishes of the posted file stall at ~2.038845e-1, 2.24e-6 below r*. Nothing indicates derivation from a posted packing. PASS.
- 6 History of updates: hsp4.html "Last update: 06-Jul-2025"; History entries are 04-Jul-2025 (N=2-100), 05-Jul-2025 (to 200), 06-Jul-2025 (to 300); none newer than the table snapshot names (4, 214). PASS.
- 7 Queue rule: pending.html (30-Oct-2026) lists ranges only for csc, ccq, crt, csq, chx, cpt, crc, cxd, cci, ssp and Moki & Julio crt/ccq/crc singletons; no hsp4 range, so N=214 lies in none. CAVEAT: the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved; N=214 must be re-checked against the live table once that bundle disappears from the pending list. PASS (with caveat).
- 8 Moki & Julio MANIFEST: row `hsp4,214,0.203884464476,0.2038844727561926183949857,4.061218e-08,REFINEMENT,dp`; r* - new_radius = 2.2373e-6 >= 1e-10. No other hsp4 row for 214 (other N=214 rows are ccq/crc_*/csc/hsp5 shelves, different cells). PASS.
- 9 Other prior work: no open or merged claim PR for hsp4 N=214 in either claims list; TROPHY_CASE.md has no 214/hsp4 entry. Spherical codes: (4,214) c = 0.879945189010 -> s/(2+s) = 0.196790315708 (r* exceeds by 7.10e-3); (4,213) c = 0.879782298893 + centre ball -> min(1/3, s/(2+s)) = 0.196897495432 (r* exceeds by 6.99e-3). Both below r*. PASS.

Clause-by-clause reading of the verbatim criterion: d=4 and N=214 listed in live radius.txt (yes); r* defined as min(half min distance, 1 - max norm), unit ball at origin, 50-digit mpmath, no tolerance (done, as above); strictly greater than the 12-decimal live value by >= 1e-10 (2.2456e-6); posted file reproduces header to 1e-11 (1.19e-12), so non-isometry (1.5e-2 > 1e-8) and polish floor (>= 1e-9 above the highest of my 5 schedule polishes; margin 2.24e-6) apply and hold; not a relaxed copy (no evidence of it; claim names no posted start); no newer History entry for (4,214); the COORDINATES UNAVAILABLE paragraph concerns hsp5/hsp6 only and does not apply to hsp4; queue rule holds with the stated Moki & Julio bundle caveat; no submission is made.

## Decision
The 214 centres give a feasible radius 0.20388671005401594... at 50 digits, 2.2456e-6 above the live table value, far beyond the 1e-10 threshold. The posted file is parsed correctly, the claim is clearly not isometric to it, and five independent trust-region polishes of the posted packing top out at 0.20388447047 (+6.0e-9), which is 2.24e-6 below r*. Shell counts, contact degree sequences and alignment show a structurally different packing, consistent with the claimant's stated independent start. No newer History entry, no pending hsp4 range (subject to the unresolved category-unspecified 26-Sep-2026 Moki & Julio 4666-candidate bundle caveat, which requires re-checking N=214 against the live table once that bundle leaves the pending list), the MANIFEST refinement and spherical-code constructions are all below r*. Every clause passes.

pass: true
