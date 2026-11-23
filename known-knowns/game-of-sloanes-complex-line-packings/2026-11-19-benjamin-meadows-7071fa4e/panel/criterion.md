# CRITERION verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (7, 24)

context: fresh reviewer (new context started for the CRITERION role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-19T05:15:39Z

## Value computed here
- Bank entry: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json fetched 2026-11-19T05:10:59Z, HTTP 200, sha256 7c3942f228807b3bd1eae1b636f557aca64344161137e8bda5566081a6b846a2. success_criterion, partial win p1 statement and verification_method compared character for character with the quotes in CLAIM.md: identical.
- Live README: https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md fetched once at 2026-11-19T05:11:01Z, HTTP 200, sha256 699dbe7157363e568d11e019a0ea98178ec9f52f8834e900587c162801b0502d, 296 table rows.
- Extracted row (README line 336, the only row for this cell): d = 7, n = 24, Best Coherence 0.32959971, Lower Bound 0.32494624, Creator hlc, Text File CurrentBestPackings/7x24_hlc.txt, Notes cell empty.
- Optimality marking: the README legend says "&#9675; indicates that the configuration is provably optimal" and "&#9651; indicates that the configuration is conjectured to be optimal"; this row's Notes cell holds neither.
- Object 7x24_bmea.txt: sha256 7071fa4e349c69da093b420911b015c646429c1afd746930b1088f6296da6353 (matches CLAIM.md), 336 lines, all numeric, no text or instructions; minimum significant digits per entry 21; largest deviation of a raw vector norm from 1: 1.6115e-16.
- Object coherence, mpmath at 40 digits, vectors[j] = re[j*d:(j+1)*d] + i*im[j*d:(j+1)*d], normalised, max over all n(n-1)/2 pairs: mu = 0.329036058455549063152200685784; 240 pairs lie within 1e-9 of the maximum.
- Best Coherence minus mu = 0.000563651544450937; mu minus lower bound = 0.00408981845554906.
- Posted file https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x24_hlc.txt fetched 2026-11-19T05:11:28Z, HTTP 200, sha256 2ca766817699f823c791df48578140ad5477f9a9c34dfd4a567be0d0620ffc02, 336 lines; recomputed in the same layout: mu = 0.32959971306280416341, which differs from the table value by 3.0628e-9 (inside 8-decimal rounding), so the layout reproduces the table.
- Null check (coordinate-major reading of the same numbers): object 0.755721220754095, posted file 0.849930743570164; the wrong layout gives values far from the table, so the agreement above is not an accident of layout.
- Other public packings for this cell in open pull requests to gnikylime/GameofSloanes (listed via the GitHub API at about 2026-11-19T05:13Z, files fetched HTTP 200, same computation):
  - open PR #18 file 7x24_owhs.txt: mu = 0.329342957521561
  - open PR #20 file 7x24_bmea.txt: mu = 0.329357468738677
  The object is below the lowest of these (0.329342957521561) by 3.0690e-04. No V3R1T4S pull request title (95 Game of Sloanes related, all states) names this cell.
- Dictionary: Wiktionary "strict inequality" (https://en.wiktionary.org/api/rest_v1/page/definition/strict_inequality, fetched 2026-11-19T05:14:11Z, HTTP 200): "An inequality where equality is not included." The comparison here has a gap far above zero and above the stated 1e-8 margin, so no reading of "strictly lower ... by at least 1e-8" is in doubt.

## Clauses checked
- 3 <= d <= 7: PASS (d = 7)
- (d, n) is a row of the live README table: PASS (README line 336, fetched 2026-11-19T05:11:01Z)
- mu computed in mpmath at 40 digits after normalising, in the repository layout: PASS (mu = 0.3290360584555; layout confirmed on the posted file, 0.32959971306280416341 vs table 0.32959971)
- mu strictly lower than Best Coherence by at least 1e-8: PASS (0.32959971 - 0.3290360584555 = 5.636515e-04 >= 1e-8)
- row not marked provably optimal: PASS (Notes cell empty; no &#9675; and no &#9651;)
- mu >= listed lower bound: PASS (0.3290360584555 - 0.32494624 = 4.089818e-03 > 0)
- every coordinate given to >= 16 significant digits: PASS (minimum 21 over all 336 entries)
- file in the repository's format: PASS (336 = 2*7*24 newline-separated numbers, real parts vector by vector then imaginary parts, vectors unit-norm to 1.6115e-16; entries are written in exponent notation where the posted files use plain decimals, which the README's format statement does not restrict)
- partial win p1: not applicable (no sporadic row; mu is 4.0898e-03 above the lower bound, not within 1e-10); the claim is for the full criterion.

## Decision
Every clause of the full success criterion holds literally for this cell against the README fetched at 2026-11-19T05:11:01Z. The improvement over the listed Best Coherence is about 5.6e-04, roughly five orders of magnitude above the 1e-8 acceptance margin, and the value sits above the lower bound, so it is not a sign of a bug. The repository layout reproduces the posted file's value for this row, and the wrong layout does not, so the comparison uses the table's own convention. The object is also below every packing for this cell in the open pull requests to the leaderboard, so the result is not subsumed by a public packing known at review time. CLAIM.md and the object carry no instructions to the reviewer; the search history in CLAIM.md was not relied on.

confirmed_scope: The 2dn = 336 numbers in 7x24_bmea.txt (sha256 7071fa4e349c69da...), read vector by vector in the repository layout and normalised, give 24 unit vectors in C^7 with coherence 0.3290360584555 at 40-digit precision, which is 5.6365e-04 below the Best Coherence 0.32959971 of the unmarked (7, 24) row of the GameofSloanes README fetched 2026-11-19T05:11:01Z and above that row's lower bound 0.32494624.

pass: true
