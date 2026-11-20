# CRITERION verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (7, 31)

context: fresh reviewer (new context started for the CRITERION role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-19T05:15:39Z

## Value computed here
- Bank entry: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json fetched 2026-11-19T05:10:59Z, HTTP 200, sha256 7c3942f228807b3bd1eae1b636f557aca64344161137e8bda5566081a6b846a2. success_criterion, partial win p1 statement and verification_method compared character for character with the quotes in CLAIM.md: identical.
- Live README: https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md fetched once at 2026-11-19T05:11:01Z, HTTP 200, sha256 699dbe7157363e568d11e019a0ea98178ec9f52f8834e900587c162801b0502d, 296 table rows.
- Extracted row (README line 343, the only row for this cell): d = 7, n = 31, Best Coherence 0.34941560, Lower Bound 0.33806170, Creator jrr, Text File CurrentBestPackings/7x31_jrr.txt, Notes cell empty.
- Optimality marking: the README legend says "&#9675; indicates that the configuration is provably optimal" and "&#9651; indicates that the configuration is conjectured to be optimal"; this row's Notes cell holds neither.
- Object 7x31_bmea.txt: sha256 accf82a6ee2089b168a50f6100f78a3b3a7edf28ca8af3bf01ed8e0386c01d5c (matches CLAIM.md), 434 lines, all numeric, no text or instructions; minimum significant digits per entry 21; largest deviation of a raw vector norm from 1: 2.4365e-16.
- Object coherence, mpmath at 40 digits, vectors[j] = re[j*d:(j+1)*d] + i*im[j*d:(j+1)*d], normalised, max over all n(n-1)/2 pairs: mu = 0.348509313852159918932231015894; 325 pairs lie within 1e-9 of the maximum.
- Best Coherence minus mu = 0.000906286147840081; mu minus lower bound = 0.0104476138521599.
- Posted file https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x31_jrr.txt fetched 2026-11-19T05:11:29Z, HTTP 200, sha256 7d0e57f131750209b9f9d41994093a37c9783f182b9e1eeda2d9c811272b8d84, 434 lines; recomputed in the same layout: mu = 0.34941560406666773277, which differs from the table value by 4.0667e-9 (inside 8-decimal rounding), so the layout reproduces the table.
- Null check (coordinate-major reading of the same numbers): object 0.741505252992082, posted file 0.781639161955139; the wrong layout gives values far from the table, so the agreement above is not an accident of layout.
- Other public packings for this cell in open pull requests to gnikylime/GameofSloanes (listed via the GitHub API at about 2026-11-19T05:13Z, files fetched HTTP 200, same computation):
  - open PR #18 file 7x31_owhs.txt: mu = 0.349359418702982
  The object is below the lowest of these (0.349359418702982) by 8.5010e-04. No V3R1T4S pull request title (95 Game of Sloanes related, all states) names this cell.
- Dictionary: Wiktionary "strict inequality" (https://en.wiktionary.org/api/rest_v1/page/definition/strict_inequality, fetched 2026-11-19T05:14:11Z, HTTP 200): "An inequality where equality is not included." The comparison here has a gap far above zero and above the stated 1e-8 margin, so no reading of "strictly lower ... by at least 1e-8" is in doubt.

## Clauses checked
- 3 <= d <= 7: PASS (d = 7)
- (d, n) is a row of the live README table: PASS (README line 343, fetched 2026-11-19T05:11:01Z)
- mu computed in mpmath at 40 digits after normalising, in the repository layout: PASS (mu = 0.3485093138522; layout confirmed on the posted file, 0.34941560406666773277 vs table 0.34941560)
- mu strictly lower than Best Coherence by at least 1e-8: PASS (0.34941560 - 0.3485093138522 = 9.062861e-04 >= 1e-8)
- row not marked provably optimal: PASS (Notes cell empty; no &#9675; and no &#9651;)
- mu >= listed lower bound: PASS (0.3485093138522 - 0.33806170 = 1.044761e-02 > 0)
- every coordinate given to >= 16 significant digits: PASS (minimum 21 over all 434 entries)
- file in the repository's format: PASS (434 = 2*7*31 newline-separated numbers, real parts vector by vector then imaginary parts, vectors unit-norm to 2.4365e-16; entries are written in exponent notation where the posted files use plain decimals, which the README's format statement does not restrict)
- partial win p1: not applicable (no sporadic row; mu is 1.0448e-02 above the lower bound, not within 1e-10); the claim is for the full criterion.

## Decision
Every clause of the full success criterion holds literally for this cell against the README fetched at 2026-11-19T05:11:01Z. The improvement over the listed Best Coherence is about 9.1e-04, roughly five orders of magnitude above the 1e-8 acceptance margin, and the value sits above the lower bound, so it is not a sign of a bug. The repository layout reproduces the posted file's value for this row, and the wrong layout does not, so the comparison uses the table's own convention. The object is also below every packing for this cell in the open pull requests to the leaderboard, so the result is not subsumed by a public packing known at review time. CLAIM.md and the object carry no instructions to the reviewer; the search history in CLAIM.md was not relied on.

confirmed_scope: The 2dn = 434 numbers in 7x31_bmea.txt (sha256 accf82a6ee2089b1...), read vector by vector in the repository layout and normalised, give 31 unit vectors in C^7 with coherence 0.3485093138522 at 40-digit precision, which is 9.0629e-04 below the Best Coherence 0.34941560 of the unmarked (7, 31) row of the GameofSloanes README fetched 2026-11-19T05:11:01Z and above that row's lower bound 0.33806170.

pass: true
