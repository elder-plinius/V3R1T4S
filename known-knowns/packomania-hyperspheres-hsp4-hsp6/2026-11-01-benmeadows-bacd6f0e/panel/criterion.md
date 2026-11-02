# CRITERION verdict: hsp4-N216

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:21Z

## Value computed here
- Object `claim/hsp4_N216.txt`: sha256 bacd6f0e…e968, which matches CLAIM.md. It has 216 non-comment rows of 4 coordinates. I ignored the `#` comment lines and computed every value myself (work/common.py, work/c123.py).
- r* (mpmath, 50 digits, no tolerance) = 0.20362333097990599275220577366244339625411531997264
  - half the minimum distance = 0.203623330979906030452213…
  - 1 - max norm = 0.203623330979905992752205… (this term binds)
- Live table row (evidence/hsp4_radius_live.txt): `216 0.203582040585`.
- r* - table = 4.1290394905992752e-5.
- Live data: the evidence/ files are the owner's live re-fetch of 2026-11-01T14:32Z, and I treated them as the live re-fetch for this panel. I recomputed every sha256 in FETCHED.md with sha256sum and all of them match. I made no other web access.
- injection_suspected: none.

## Clauses checked
- **1 Value.** r* - table = 4.129e-5 >= 1e-10. **PASS**
- **2 Parser sanity.** I recomputed the radius of the posted hsp4-216.txt with the same 50-digit code: 0.203582040584506555576…. Its header is 0.203582040585, so the difference is -4.93e-13. That is within 1e-11, and the table row is the same value. The posted file is byte-identical to hsp4-216.txt inside hsp4_coords.tar.gz. Clauses 3 and 4 therefore apply. **PASS**
- **3 Non-isometry.** I sorted all 23,220 pairwise distances of the claim and of the posted file. The maximum absolute difference is 7.89e-3, which exceeds 1e-8. For information, the maximum difference of the sorted centre norms is 0.246. **PASS**
- **4 Polish floor.** I wrote my own sequential-LP polisher (work/polish.py and work/polish2.py) and started every run from the posted coordinates. The LP maximizes the linearized radius over near-active pairs and wall centres, inside a box trust region on every coordinate step. A step is accepted only if the exactly recomputed radius increases; otherwise the trust region shrinks. Each run stops when the trust region falls below 1e-13 or there is no gain above 1e-15 over 20 consecutive iterations. polish2 differs from polish in two ways: variables are scaled to the trust region with HiGHS tolerances at 1e-10, and a conservative second-order wall bound is used. I ran 8 schedules and recomputed every final radius at 50 digits from the polished coordinates:
  - A: step 1e-2, margin 0.05, shrink 0.5. Radius 0.2035820564525963, gain over header 1.587e-8, 95 iterations, stopped on no gain.
  - B: step 1e-3, margin 0.02, shrink 0.5. Radius 0.2035820564524715, gain 1.587e-8, 80 iterations, stopped on no gain.
  - C: step 1e-4, margin 0.01, shrink 0.5. Radius 0.2035820564527029, gain 1.587e-8, 90 iterations, stopped on no gain.
  - D: step 1e-2, margin 0.08, shrink 0.25. Radius 0.2035820563969464, gain 1.581e-8, 89 iterations, stopped on trust region < 1e-13.
  - E: step 1e-2, margin 0.05, shrink 0.5, scaled. Radius 0.2035820564527933, gain 1.587e-8, 81 iterations, stopped on no gain.
  - F: step 1e-3, margin 0.02, shrink 0.5, scaled. Radius **0.2035820564527934** (highest), gain 1.587e-8, 82 iterations, stopped on no gain.
  - G: step 1e-4, margin 0.01, shrink 0.5, scaled. Radius 0.2035820564527933, gain 1.587e-8, 66 iterations, stopped on no gain.
  - H: step 1e-2, margin 0.08, shrink 0.3, scaled. Radius 0.2035820564527933, gain 1.587e-8, 66 iterations, stopped on trust region < 1e-13.

  r* minus the highest polished radius = 4.1274e-5 >= 1e-9. The Moki & Julio manifest reports a refinement of the posted file at 0.20358212768, which is above my polishes. r* still exceeds it by 4.12e-5. **PASS**
- **5 Not a relaxed copy.** The claimant says the claim comes from its own lane hsp4-b, seeded from random, two-shell and D4-cut starts, then N-1 plus one inserted ball. It names no posted packing as a start. I did not receive the claimant's search code and could not inspect it. My own evidence points the same way:
  - Contact graphs differ (tolerance 1e-9). The claim has 666 pair contacts and 188 wall contacts. The posted file has 663 pair contacts and 185 wall contacts.
  - Degree histograms differ. The claim's maximum degree is 11; the posted file's is 10.
  - Shell structure differs. Counting centres with norm < 0.5 / between 0.5 and 0.75 / >= 0.75, the claim has 28/0/188 and the posted 216 file has 28/2/186.
  - The sorted-norm profile differs from posted N = 215, 216 and 217 by at least 0.233 each, even when one ball is allowed to be removed.
  - The distance-multiset difference is 7.9e-3.
  - All 8 polishes of the posted file converge to 0.2035820565, which is 4.1e-5 short of r*. The posted basin does not lead to the claim.

  Nothing indicates the claim was derived from a posted packing. **PASS**
- **6 History of updates.** hsp4.html shows "Last update: 06-Jul-2025". Its History-of-updates entries are 04-Jul-2025 (N = 2-100), 05-Jul-2025 (to N = 200) and 06-Jul-2025 (to N = 300, the table snapshot itself). No entry newer than the snapshot names (4, 216). **PASS**
- **7 Queue rule.** pending.html is dated 30-Oct-2026. It lists ranges only for the categories csc, ccq, crt, csq, chx, cpt, crc, cxd, cci and ssp, plus explicit Moki & Julio lists for crt, ccq and crc (79/271/280 and 251/429/500). It lists no hsp4 range, so N = 216 lies in none. Caveat, as required: the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle does not name a category, so this check cannot rule it out. N = 216 must be re-checked against the live table once that bundle disappears from the pending list. **PASS (with caveat)**
- **8 Moki & Julio manifest.** The row `hsp4,216` gives published_radius 0.203582040585 and new_radius 0.2035821276819616514336772 (REFINEMENT). r* - new_radius = 4.1203e-5 >= 1e-10. The other N = 216 rows are for different containers or dimensions (ccq, crc_*, crt, csc, hsp5, hsp6, ssp). hsp5 216 is 0.24829 and hsp6 216 is 0.28171, both in other dimensions, so neither can refer to this cell. **PASS**
- **9 Other prior work.**
  - Claims lists: no open, merged or closed claim or PR for hsp4 N = 216. The hsp4 claims are for N = 30-119, 170 and 301.
  - TROPHY_CASE.md: no hsp4 or hypersphere entry.
  - Spherical-code constructions: the (4,216) cosine is 0.880886649220, which gives s/(2+s) = 0.196168853249; r* exceeds it by 7.45e-3. The (4,215) cosine is 0.880272662054, and with a centre ball min(1/3, s/(2+s)) = 0.196574535420; r* exceeds it by 7.05e-3. Both are below r*.

  **PASS**

### Clause-by-clause reading of the verbatim criterion
- "N centers in R^d (d in {4,5,6}) for one N listed in live radius.txt": d = 4, 216 centres, and N = 216 is listed. Met.
- "FEASIBLE radius r* … mpmath 50 digits … no tolerance": r* = 0.2036233309799059927… was computed exactly as defined, with both terms reported. Met.
- "STRICTLY GREATER … than the 12-decimal value … by at least 1e-10": the margin is 4.129e-5. Met.
- "wherever the posted file reproduces its header to 1e-11": it does (-4.9e-13), so the next two conditions apply.
  - Not isometric: the distance multisets differ by 7.9e-3. Met.
  - r* exceeds the highest of my several-schedule polishes by at least 1e-9: 8 schedules, each run to its stop rule; the best is 0.2035820564528 and the margin is 4.13e-5. Met.
- "not a relaxed copy of a posted packing … the claim names any posted packing it started from": the claim names none, and my contact-graph, shell, norm-profile and polish evidence shows no derivation. Met.
- "(d, N) not in a History-of-updates entry newer than the scout's": the newest entry is 06-Jul-2025, which is the snapshot. Met.
- "COORDINATES UNAVAILABLE" clause: it covers only hsp5 and hsp6, so it does not apply to hsp4.
- "QUEUE RULE": no hsp4 range is listed, and the 26-Sep-2026 *many* caveat is stated above. Met.
- "No submission (email)": none was made by me.

## Decision
I recomputed every clause myself on the sha256-verified live re-fetch.
- r* = 0.20362333097990599275… beats the live table row 0.203582040585 by 4.13e-5, far above the 1e-10 threshold.
- The posted N = 216 file is a sound comparison: it reproduces its header to 5e-13.
- The claim is far from isometric to the posted file: the distance multisets differ by 7.9e-3.
- Eight independent sequential-LP polish schedules of the posted file all plateau at 0.2035820565, a gain of only 1.6e-8. The claim beats that ceiling by 4.13e-5, and it also beats the Moki & Julio refinement (0.2035821277).
- Contact graph and shell structure differ from posted N = 215, 216 and 217, and the claim names no posted start.
- No newer history entry, pending range, manifest row, claim PR or spherical-code construction reaches r*.

All clauses pass. The one condition left open is the queue-rule caveat: the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle does not name a category and cannot be resolved here, so N = 216 must be re-checked against the live table once that bundle leaves the pending list.

pass: true
