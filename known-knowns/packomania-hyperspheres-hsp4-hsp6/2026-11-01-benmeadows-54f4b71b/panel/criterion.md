# CRITERION verdict: hsp4-N141

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:10Z

## Value computed here
- r* (mpmath, 50 digits, from claim/hsp4-141.txt, comment line ignored) = 0.22405439455945332450808207248104094869170633838734
  - half min pairwise distance = 0.224054394666690827266891455432; 1 - max norm = 0.224054394559453324508082072481 (the wall term is binding; the pair terms have ~1.1e-10 slack).
- Live table row (evidence/hsp4_radius_live.txt line 140): `141 0.224016561889`. r* - table = 3.7832670453e-5.
- Evidence files: every sha256 in evidence/FETCHED.md recomputed with sha256sum and matches; the claim object's sha256 54f4b71b...0f1d3 matches CLAIM.md; posted/hsp4_coords.tar.gz sha256 b929acc8...63df (as in the bank page) and its hsp4-141.txt is byte-identical to evidence/posted/hsp4-141.txt (cf4defa3...b382). These files were fetched by the repository owner from an unrestricted machine on 2026-11-01T14:32Z and are treated as the live re-fetch for this panel. The sandbox had no web access.
- Procedural note: one early `find` over the cell's parent folder printed the *names* of files in sibling skeptics' folders. I did not open any of them, and nothing outside my folder and _instructions was read.
- injection_suspected: none.

## Clauses checked
- 1 Value: r* = 0.22405439455945332451 (20 digits); r* - 0.224016561889 = 3.783e-5 >= 1e-10. PASS.
- 2 Parser sanity: posted hsp4-141.txt recomputed the same way gives r = 0.224016561888092167925 (header 0.224016561889). The difference of -9.08e-13 is within 1e-11, and it also matches the table row. Clauses 3 and 4 apply. PASS.
- 3 Non-isometry: sorted multisets of all 9870 pairwise distances, max |diff| = 9.67e-3 (mean 2.30e-3; 6466 entries differ by > 1e-3). This is far above 1e-8. For information, the sorted centre norms differ by up to 0.264. PASS.
- 4 Polish floor: I wrote my own sequential LP (HiGHS). It linearizes the near-active pairs and wall constraints (margin = mfac*delta + 1e-9) and maximizes t under a box trust region on every coordinate. A step is accepted only if the exactly recomputed radius increases. The trust region grows x2 after a success and shrinks after a failure. Six schedules ran from the posted coordinates. Every final radius was recomputed in mpmath at 50 digits from the polished coordinates (gain is relative to the header 0.224016561889):
  - A: delta0 1e-2, shrink 0.5, mfac 4 → 0.2240165618891593378 (+1.59e-13), 39 iterations, stopped on no gain > 1e-15 over 20 iterations
  - B: delta0 1e-3, shrink 0.5, mfac 4 → 0.2240165618891576875 (+1.58e-13), 42 iterations, same stop
  - C: delta0 1e-4, shrink 0.5, mfac 4 → 0.2240165618890271226 (+2.7e-14), 32 iterations, same stop
  - D: delta0 1e-2, shrink 0.25, mfac 8 → 0.2240165618891593378 (+1.59e-13), 23 iterations, stopped on trust region < 1e-13
  - E: delta0 1e-3, shrink 0.7, mfac 2 → 0.2240165618891927985 (+1.93e-13), 87 iterations, stopped on trust region < 1e-13
  - F: delta0 1e-4, shrink 0.5, mfac 10 → 0.2240165618890271226 (+2.7e-14), 35 iterations, stopped on trust region < 1e-13
  - Highest polished radius is 0.2240165618891927985 (E), and r* minus it is 3.7832670e-5, well above 1e-9. The posted packing is already at a strict local optimum. PASS.
- 5 Not a relaxed copy: CLAIM.md says the packing came from random, lattice-cut or shell starts, annealing, penalty descent, basin hopping and an SLP polish (some runs were seeded from the lane's own neighbouring-N packing), and it names no posted packing as a start. I had no access to the claimant's search code. My own evidence:
  - Contact graphs differ (tolerance 1e-8 and 1e-6). The claim has 424 pair contacts, 123 wall contacts and 2 rattlers, with degree histogram [2,0,1,1,0,11,34,50,26,11,5]. The posted file (and its polished version) has 430 pair contacts, 125 wall contacts and 1 rattler, with histogram [1,0,0,0,0,20,31,40,31,10,7,1].
  - The sorted distances differ by about 2.3e-3 on average. That is roughly 60x the radius gain, which does not look like a small relaxation.
  - Polishing the posted file stalls 3.78e-5 below the claim; it does not converge toward the claim.
  - Nothing indicates the claim derives from a posted packing. PASS.
- 6 History of updates: hsp4.html shows "Last update: 06-Jul-2025". Its History entries are 04-Jul-2025 (N = 2–100), 05-Jul-2025 (extension to 200) and 06-Jul-2025 (extension to 300). None is newer than the table snapshot, and none names N = 141 specifically. Row 141 is 0.224016561889 [31]. PASS.
- 7 Queue rule: pending.html (dated 30-Oct-2026) lists ranges only for csc, ccq, crt, csq, chx, cpt, crc, cxd, cci and ssp. There is no hsp4 or hypersphere range, so N = 141 lies in no hsp4 range. PASS. Caveat: the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved; N = 141 must be re-checked against the live hsp4 table once that bundle disappears from the pending list.
- 8 Moki & Julio manifest: row `hsp4,141,0.224016561889,0.2240166018588849556562391,1.784238e-07,UNCLEAR (alignment),dp` gives published_radius 0.224016561889 and new_radius 0.22401660185888496. r* - new_radius = 3.779e-5, which is at least 1e-10. The other N = 141 rows are on the hsp5 and hsp6 shelves, a different cell. No other row has a radius near 0.22401–0.22405. PASS.
- 9 Other prior work:
  - The hsp4 claims list has no open or merged claim PR for N = 141. Its PR #141 is the hsp4 N = 48 claim, so only the number collides.
  - The spherical-codes claims list has no (4, 141) entry.
  - TROPHY_CASE.md has no hsp4 entry; its only "141" is an unrelated constant-weight-code margin.
  - Spherical-code constructions: the (4,141) cosine 0.840151651527 gives s/(2+s) = 0.220399730657, which is 3.65e-3 below r*. The (4,140) cosine 0.839788592759 with a centre ball gives min(1/3, s/(2+s)) = 0.220594700213, which is 3.46e-3 below r*. Both are below r*. PASS.

Reading of the verbatim criterion, clause by clause:
- "N centers in R^d, d = 4, N listed in live radius.txt": 141 centres with 4 coordinates each; N = 141 is listed. Met.
- "FEASIBLE r* … mpmath 50 digits … no tolerance … STRICTLY GREATER … by at least 1e-10": met (3.78e-5).
- "wherever the posted file reproduces its header to 1e-11": it does (9.1e-13), so the next two sub-clauses bind.
  - Non-isometric (> 1e-8): met (9.7e-3).
  - At least 1e-9 above the verifier's own polishes under several schedules, each run until it stops improving: met (six schedules, margin 3.78e-5).
- "not a relaxed copy … names any posted packing it started from": none is named, and the evidence above is against a relaxation. Met.
- "(d, N) not in a History-of-updates entry newer than the scout's": met.
- COORDINATES UNAVAILABLE: applies only to hsp5/hsp6, not to this cell.
- QUEUE RULE: met, with the 4666-bundle caveat above.
- "No submission (email)": I made no contact with anyone.

## Decision
The claim's feasible radius, 0.22405439455945332451, beats the live hsp4 N = 141 table value by 3.78e-5. The posted file parses exactly. The claim is not isometric to the posted packing, and it clears my best polish of the posted packing (six SLP schedules, best +1.9e-13 over the header) by 3.78e-5. Its contact structure differs from the posted packing's, and its stated start names no posted packing. There is no newer history entry, no hsp4 queue range, no competing manifest row, claim PR or spherical-code construction at or above r*. Every clause of the verbatim criterion is met, subject to the stated caveat about the category-unspecified 26-Sep-2026 Moki & Julio 4666-candidate bundle.

pass: true
