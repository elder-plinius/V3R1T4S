# Novelty report: feigenbaum-z4-p2 (quartic Feigenbaum constants alpha_4 and delta_4, partial win p2)

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

role: novelty (skeptic 1 of 3). Read: the claim statement, INDEX.csv and the record files. I did not read or run the author's verifier scripts or receipts. Residual checks of the functional equations are for reproduce; this report compares the claimed digit counts with what is published.

## Sources fetched (one plain GET each; the log is not shipped in this package; 2026-10-19 UTC)
| Source | URL | UTC | HTTP | sha256 |
|---|---|---|---|---|
| OEIS A195102 (json) | https://oeis.org/search?q=id:A195102&fmt=json | 05:37:36 | 200 | 5761a679e8ccdb464615f6a89348ca1701337e8f8c8c82fc27acba951931db13 |
| OEIS search for further biquadratic Feigenbaum sequences | https://oeis.org/search?q=Feigenbaum+biquadratic&fmt=json | 05:39:34 | 200 | 5761a679e8ccdb464615f6a89348ca1701337e8f8c8c82fc27acba951931db13 (the only hit is A195102) |
| OEIS A218453 (json) | https://oeis.org/search?q=id:A218453&fmt=json | 05:37:37 | 200 | d0efbfac17269e939d8d647f2315a3a499b0ad7bb1a63458b04ba10fe54be826 |
| OEIS A098587 (json) | https://oeis.org/search?q=id:A098587&fmt=json | 05:37:37 | 200 | bb1c6ab4a933d3c1dd0fc8661da6ad26b2ef101ef09c560d917c1969092a325e |
| arXiv API, query 3 (Feigenbaum with digits, precision or accumulation; newest first; 26 results) | export.arxiv.org api query, https | 05:37:39 | 200 | 43b613e951685ee2484607881f7dde79c6e34c7875206a87b2102f5835a50813 |
| arXiv 2409.20457v2 (validated Chebyshev enclosures of renormalization fixed points), PDF | https://arxiv.org/pdf/2409.20457v2 | 05:39:13 | 200 | 41175a8dab0bcd5061c013318d94a571f1e7803aaf81e7135b9ab3ac4aae1bff |
| arXiv 1602.02357v1 (Molteni, 10,000 digits), PDF | https://arxiv.org/pdf/1602.02357v1 | 05:39:47 | 200 | 1120a43d95c6c052a7bb2310af541476607bee8e529191cc904e9effd1a7fc05 |
| TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 05:37:22 | 200 | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 |
| known-knowns listing | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns | 05:37:22 | 200 | 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011 |

I did not refetch the Thurlby thesis PDF or Plouffe's page (triage fetched them; their values are in the package folder); OEIS A195102 itself cites the thesis as "approx 330 digits on page 86". Pull requests: used the saved list of all V3R1T4S PRs (473 entries, highest 481, fetched 2026-10-19T04:30:31Z, sha256 0a1d00562d9b2af7d165703ebb9732af8e1bc3328848eba98c8cc3096dd5bb14) instead of the pulls pages. No PR title or body mentions Feigenbaum, period doubling or Myrberg; known-knowns has no Feigenbaum folder (20 folders); the trophy-case file has no Feigenbaum entry. The arXiv API request used https (no redirect).

## Values read
- OEIS A195102 (live, fetched 05:37:36Z, revision 15, last change 2026-05-19): data field has 49 digits, 1,6,9,0,3,0,2,9,7,1,4,0,5,2,4,4,8,5,3,3,4,3,7,8,0,1,5,0,3,2,4,1,6,1,3,4,8,2,2,8,2,7,8,0,5,9,7,0,9 (alpha_4 = 1.690302971405244853343780150324161348228278059709). Its link list cites Briggs, Quispel and Thompson (1991), Mathar (arXiv 1008.4608) and Thurlby's thesis ("Gives approx 330 digits on page 86"). No OEIS sequence for delta_4 exists (the search for biquadratic Feigenbaum sequences returned only A195102).
- Thurlby (2021), Table 4.6: alpha_4 331 digits and delta_4 325 digits proven (value from the cell's README; consistent with OEIS's "approx 330").
- arXiv 2409.20457 (30 Sep 2024, within 24 months), Theorem 1.6 and Table 2: validated enclosures for the quartic (d=4) fixed point for order m=2 with 41 digits for the eigenvalue: lambda_2 = 7.28468621707334336430893056799555306947804 plus or minus 1e-41, and 46 digits for m=3. The text says the quadratic case is computed to about 500 correct digits; the quartic case only to about 41. This agrees with the claim's delta_4 = 7.28468621707334336430893056799555... on the first 41 digits.
- arXiv 1602.02357 (Molteni, 10,000 digits): quadratic constants only (its text does not mention a quartic or other critical-order case).
- arXiv 2102.11239 (rigorous Hausdorff dimension bounds, quadratic, cubic and quartic) works with the fixed points but reports only dimensions to 3-4 digits.
- Other arXiv hits from query 3 are unrelated to quartic fixed-point digits.

## Comparison
Claimed agreement between two resolutions: 1085 decimals (alpha_4) and 1082 decimals (delta_4) as stated in the claim, and 1084 as measured by the triage record. The best digit counts found anywhere: 49 (OEIS A195102), 331 and 325 proven (Thurlby, 2021), 41 (2409.20457). The claim exceeds every one of them by a factor of more than 3 even if only 400 digits were right (the digit counts matter only as being above 331 and 325). The first digits (alpha_4 1.6903029714052448533437801503241613482282780597095619666824 and the delta_4 prefix 7.2846862170733433643089305679955530694780466197997906590721) agree with the OEIS data and with 2409.20457 on all digits those sources give; I compared the claim sentence text, not the object file (reproduce does that).

## Propagation / PR 350 rule
alpha_4 and delta_4 do not follow from any table value by a standard propagation rule; there is no table or merged claim for z=4 beyond OEIS/Thurlby. Not applicable.

## Open questions answered (novelty side)
- Literature after the thesis with more than 1000 digits for z=4: none found. Searched arXiv (query 3, 26 hits, plus abstracts of 2409.20457, 1602.02357 and 2102.11239) and OEIS (two requests). The newest quartic-digit paper is 2409.20457 with 41 digits.
- The other open questions (residual evidence, equations, leading eigenvalue, 1082 vs 1084) belong to reproduce and criterion.
- unresolved: Briggs, Quispel and Thompson (1991) and Mathar's note (arXiv 1008.4608, 2010) give z=4 digits but are older than 24 months and, per OEIS (49 digits in the data field), carry fewer digits than Thurlby; Thurlby's own papers (Burbanks, Osbaldestin, Thurlby) cited by 2409.20457 were not read in full. None can plausibly hold 1000 digits for a proof-grade constant, since OEIS cites Thurlby at about 330 as the maximum.

## Verdict
The claim strictly exceeds the largest published digit count for the quartic constants (331 and 325 proven digits, Thurlby 2021; 49 in OEIS; 41 in 2409.20457) and there is no competing PR or trophy. The main-win comparison (Molteni 10,022 digits, quadratic) is not claimed.

novelty: NEW against all readable sources (digit count 1082 to 1085 against 331 and 325)

pass: true
