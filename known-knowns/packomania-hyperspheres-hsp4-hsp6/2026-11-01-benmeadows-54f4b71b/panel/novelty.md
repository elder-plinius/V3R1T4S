# NOVELTY verdict: hsp4-N141

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:10Z

## Value computed here
- Object claim/hsp4-141.txt: sha256 54f4b71b…f1d3 matches CLAIM.md; 141 rows x 4 numbers, no duplicates, no NaN, 15-17 significant digits.
- r* (mpmath 50 digits) = 0.224054394559453324508082072481; independently via exact Fractions + 60-digit Decimal sqrt: 0.224054394559453324508082072481 (agree).
  Binding term: 1 - max|c_i| = 0.2240543945594533245080821 (half min distance 0.2240543946666908272668915).
- Live table row 141 (evidence/hsp4_radius_live.txt): 0.224016561889. r* - table = 3.78326704533e-5.
- Evidence files: all sha256 values in evidence/FETCHED.md verified with sha256sum (all match). These files are the live re-fetch for this panel (fetched by the repository owner from an unrestricted machine, 2026-11-01T14:32Z); no other web access attempted. evidence/posted/hsp4-141.txt is byte-identical to the member of hsp4_coords.tar.gz.
- No injection suspected (comment line in the object states the claimant's value; ignored and recomputed).

## Clauses checked
- 1 Value: r* = 0.22405439455945332451; table 0.224016561889; r* - table = 3.783e-5 >= 1e-10. PASS.
- 2 Parser sanity: posted file r = 0.224016561888092167925 (binding 1-max norm); header 0.224016561889; difference -9.08e-13, |.| < 1e-11; table row identical to header. Reproduces → clauses 3, 4 apply. PASS.
- 3 Non-isometry: max |sorted pairwise-distance difference| (9870 distances) = 9.674e-3 > 1e-8. Sorted centre norms (info): max difference 0.2641. PASS.
- 4 Polish floor: own SLP polisher (HiGHS LP on pairs with distance < 2r+margin and centres with norm > 1-r-margin, box trust region on every coordinate, step accepted only if the exactly recomputed radius increases, shrink otherwise), started from the posted coordinates. Final radii recomputed at 50 digits:
  - unscaled LP, D0=1e-2, shrink 0.5, margin 4D: 0.22401656188915933776 (gain +1.59e-13), 38 it, stop: no gain >1e-15 over 20 it
  - unscaled LP, D0=1e-3, shrink 0.5, margin 4D: 0.22401656188915768751 (+1.58e-13), 38 it, same stop
  - unscaled LP, D0=1e-4, shrink 0.5, margin 4D: 0.22401656188902712262 (+2.71e-14), 31 it, same stop
  - unscaled LP, D0=1e-2, shrink 0.3, grow 2, margin 8D: 0.22401656188866043016 (-3.40e-13 vs header; +5.7e-13 vs posted r), 24 it, stop: trust region < 1e-13
  - unscaled LP, D0=1e-3, shrink 0.7, grow 1.5, margin 3D: 0.22401656188809216793 (no step accepted), 21 it, no gain over 20 it
  - scaled LP (tight 1e-10 tolerances), D0=1e-2 / 1e-3 / 1e-4 (shrink 0.5, margin 4D) and D0=1e-2 (shrink 0.3, grow 2, margin 8D): 0.224016561889263504 / ...263498 / ...263467 / ...263478 (all +2.63e-13), 46 / 44 / 39 / 38 it, stops: no gain over 20 it / no gain / trust region < 1e-13 / trust region < 1e-13.
  Highest polished radius 0.22401656188926350389; r* - highest = 3.7833e-5 >= 1e-9. PASS.
- 5 Not a relaxed copy: the claim states its start (random configurations, D4/A4 lattice cuts, shell seeds, own neighbouring-N packings; no posted Packomania packing; names none). I do not have the claimant's search code. Own evidence: contact graphs differ (claim: 424 contacts + 123 wall contacts, 18 off-wall centres, degree histogram incl. wall [2,0,1,1,0,11,34,50,26,11,5]; posted: 430 + 125, 16 off-wall, [1,0,0,0,0,20,31,40,31,10,7,1], stable for tolerances 1e-9..1e-7); sorted norm multisets differ by 0.264 and distance multisets by 9.7e-3; all nine polishes of the posted file stall at ~0.22401656189, 3.8e-5 below the claim, i.e. the posted packing is a local optimum whose basin does not reach the claim. Nothing indicates derivation from a posted packing. PASS.
- 6 History of updates: hsp4.html "Last update: 06-Jul-2025"; entries 04-Jul-2025 (N=2–100), 05-Jul-2025 (extension to 200), 06-Jul-2025 (extension to 300); no entry newer than the snapshot; none names N=141 specifically after the table snapshot (the table row itself is Specht [31]). PASS.
- 7 Queue rule: pending.html (30-Oct-2026) lists categories csc, ccq, crt, csq, chx, cpt, crc, cxd, cci, ssp and one '*many*' bundle; no hsp4 range at all, so N=141 lies in none. CAVEAT: the 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved; N=141 must be re-checked against the live table once that bundle disappears from the pending list. PASS (subject to caveat).
- 8 Moki & Julio MANIFEST: row 'hsp4,141': published_radius 0.224016561889, new_radius 0.2240166018588849556562391 (UNCLEAR (alignment)). r* - new_radius = 3.7793e-5 >= 1e-10. Other rows with N=141 are hsp5 (0.2683665897) and hsp6 (0.2990776708), different d; no other row has a radius near 0.224. PASS.
- 9 Other prior work: claims list for packomania-hyperspheres-hsp4-hsp6 has open/merged/closed PRs for hsp4 N = 30,35,42,48,54,62,63,64,66,67,69,74,75,79,80,81,83,88,89,91,94,104,111,119,170,301 — none for N=141 (PR #141 is about N=48); spherical-codes claims list has none for hsp4 N=141; TROPHY_CASE.md has no hsp entry. Spherical-code constructions from spherical_plain_live.txt: (4,141) c=0.840151651527 → s/(2+s) = 0.22039973065679 (r* exceeds by 3.65e-3); (4,140) c=0.839788592759 + centre ball → min(1/3, s/(2+s)) = 0.22059470021344 (r* exceeds by 3.46e-3). Both below r*. PASS.

## Decision
Prior work (6-9): Packomania's hsp4 page has had no update since 06-Jul-2025 and no history entry for N=141; the pending list shows no hsp4 range (the category-unspecified 26-Sep-2026 Moki & Julio 4666-candidate bundle cannot be resolved and N=141 must be re-checked against the live table once it leaves the pending list); the Moki & Julio manifest's own improved value for hsp4 N=141 (0.22401660186) is beaten by 3.78e-5; no claim PR or trophy entry covers this cell; and Cohn-table spherical-code constructions give at most 0.22059. Clauses 1-5 also pass on my own computation: r* = 0.2240543945594533 beats the table by 3.78e-5, is non-isometric to the posted file, exceeds every own polish of the posted packing (best 0.22401656188926) by 3.78e-5, and shows no sign of being a relaxed posted packing. All nine clauses pass.

pass: true
