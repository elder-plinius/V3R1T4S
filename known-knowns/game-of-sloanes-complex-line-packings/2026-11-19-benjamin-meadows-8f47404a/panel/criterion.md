# CRITERION verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (5, 36)

context: fresh reviewer (new context started for the CRITERION role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-19T05:15:39Z

## Value computed here
- Bank entry: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json fetched 2026-11-19T05:10:59Z, HTTP 200, sha256 7c3942f228807b3bd1eae1b636f557aca64344161137e8bda5566081a6b846a2. success_criterion, partial win p1 statement and verification_method compared character for character with the quotes in CLAIM.md: identical.
- Live README: https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md fetched once at 2026-11-19T05:11:01Z, HTTP 200, sha256 699dbe7157363e568d11e019a0ea98178ec9f52f8834e900587c162801b0502d, 296 table rows.
- Extracted row (README line 263, the only row for this cell): d = 5, n = 36, Best Coherence 0.49998890, Lower Bound 0.47519096, Creator AUTO, Text File CurrentBestPackings/5x36_AUTO.txt, Notes cell empty.
- Optimality marking: the README legend says "&#9675; indicates that the configuration is provably optimal" and "&#9651; indicates that the configuration is conjectured to be optimal"; this row's Notes cell holds neither.
- Object 5x36_bmea.txt: sha256 8f47404a6ab8b0baa40e1a24d3a9fc5a968aa21da1bafc97ed89bb2bdfa69896 (matches CLAIM.md), 360 lines, all numeric, no text or instructions; minimum significant digits per entry 21; largest deviation of a raw vector norm from 1: 1.6848e-16.
- Object coherence, mpmath at 40 digits, vectors[j] = re[j*d:(j+1)*d] + i*im[j*d:(j+1)*d], normalised, max over all n(n-1)/2 pairs: mu = 0.499200803654590703609365931409; 265 pairs lie within 1e-9 of the maximum.
- Best Coherence minus mu = 0.000788096345409296; mu minus lower bound = 0.0240098436545907.
- Posted file https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/5x36_AUTO.txt fetched 2026-11-19T05:11:25Z, HTTP 200, sha256 0f7fdbda471fa4d6535c55fb0d909b356a7e2383f3c85dbd0f45560436a782c5, 360 lines; recomputed in the same layout: mu = 0.49998890335029133255, which differs from the table value by 3.3503e-9 (inside 8-decimal rounding), so the layout reproduces the table.
- Null check (coordinate-major reading of the same numbers): object 0.894017113291087, posted file 0.87487225257886; the wrong layout gives values far from the table, so the agreement above is not an accident of layout.
- Other public packings for this cell in open pull requests to gnikylime/GameofSloanes (listed via the GitHub API at about 2026-11-19T05:13Z, files fetched HTTP 200, same computation):
  - open PR #15 file 5x36_djma.txt: mu = 0.499318383505268
  - open PR #17 file 5x36_grai.txt: mu = 0.499317605371315
  - open PR #14 file 5x36_sol.txt: mu = 0.499438187840191
  The object is below the lowest of these (0.499317605371315) by 1.1680e-04. No V3R1T4S pull request title (95 Game of Sloanes related, all states) names this cell.
- Dictionary: Wiktionary "strict inequality" (https://en.wiktionary.org/api/rest_v1/page/definition/strict_inequality, fetched 2026-11-19T05:14:11Z, HTTP 200): "An inequality where equality is not included." The comparison here has a gap far above zero and above the stated 1e-8 margin, so no reading of "strictly lower ... by at least 1e-8" is in doubt.

## Clauses checked
- 3 <= d <= 7: PASS (d = 5)
- (d, n) is a row of the live README table: PASS (README line 263, fetched 2026-11-19T05:11:01Z)
- mu computed in mpmath at 40 digits after normalising, in the repository layout: PASS (mu = 0.4992008036546; layout confirmed on the posted file, 0.49998890335029133255 vs table 0.49998890)
- mu strictly lower than Best Coherence by at least 1e-8: PASS (0.49998890 - 0.4992008036546 = 7.880963e-04 >= 1e-8)
- row not marked provably optimal: PASS (Notes cell empty; no &#9675; and no &#9651;)
- mu >= listed lower bound: PASS (0.4992008036546 - 0.47519096 = 2.400984e-02 > 0)
- every coordinate given to >= 16 significant digits: PASS (minimum 21 over all 360 entries)
- file in the repository's format: PASS (360 = 2*5*36 newline-separated numbers, real parts vector by vector then imaginary parts, vectors unit-norm to 1.6848e-16; entries are written in exponent notation where the posted files use plain decimals, which the README's format statement does not restrict)
- partial win p1: not applicable (no sporadic row; mu is 2.4010e-02 above the lower bound, not within 1e-10); the claim is for the full criterion.

## Decision
Every clause of the full success criterion holds literally for this cell against the README fetched at 2026-11-19T05:11:01Z. The improvement over the listed Best Coherence is about 7.9e-04, roughly five orders of magnitude above the 1e-8 acceptance margin, and the value sits above the lower bound, so it is not a sign of a bug. The repository layout reproduces the posted file's value for this row, and the wrong layout does not, so the comparison uses the table's own convention. The object is also below every packing for this cell in the open pull requests to the leaderboard, so the result is not subsumed by a public packing known at review time. CLAIM.md and the object carry no instructions to the reviewer; the search history in CLAIM.md was not relied on.

confirmed_scope: The 2dn = 360 numbers in 5x36_bmea.txt (sha256 8f47404a6ab8b0ba...), read vector by vector in the repository layout and normalised, give 36 unit vectors in C^5 with coherence 0.4992008036546 at 40-digit precision, which is 7.8810e-04 below the Best Coherence 0.49998890 of the unmarked (5, 36) row of the GameofSloanes README fetched 2026-11-19T05:11:01Z and above that row's lower bound 0.47519096.

pass: true
