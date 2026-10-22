# Independent CRITERION review for A(25,6,11), M = 8734
context: fresh subagent with its own continuations; independently written checker and independent reading of original source bytes, without adopting another current reviewer verdict
reviewed_utc: 2026-10-19T11:53:11.411894+00:00
target_id: constant-weight-codes
mathematical_validity: PASS
literal_criterion: PASS
confirmed_scope: The 8734 distinct binary words of length25 and weight11 in CANDIDATE_M8734.txt (SHA256 f9f280613ee2a5c500220a9f022d35d83264a14f96d940c9a517a15cebdf6fde) have pairwise Hamming distance at least6, establishing A(25,6,11)>=8734, exceeding Brouwer's printed lower bound8718 by16 and the strongest located same-cell public claim8720 by14 as of2026-10-19, while remaining below the tabulated upper bound24630.

This final review incorporates new source receipts supplied after the earlier pending reviews. The earlier reviews and addenda are preserved. This is one CRITERION review; it does not assign an honesty-gate status, validate a submission package, or claim external acceptance or historical priority.

## Literal criterion

> Success means an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even), where M is STRICTLY GREATER (direction: max) than the lower bound shown at verification time in the (n,d,w) cell of https://aeb.win.tue.nl/codes/Andw.html (also checking the mirror cell A(n,d,n-w)), and also strictly greater than any value for that cell in arXiv:2608.13906 (Echols, 124 improved cells), arXiv:2607.19550 (Lysenstoen) or any newer arXiv paper. M must not exceed the tabulated upper bound; exceeding it means a bug.

The claim satisfies the full constructive lower-bound criterion for one cell. It is not an upper-bound certificate, a first-listing partial claim, a proof of optimality, or a new search-algorithm claim.

## Independent exact verification

PROVED-HERE: CANDIDATE_M8734.txt has SHA256 f9f280613ee2a5c500220a9f022d35d83264a14f96d940c9a517a15cebdf6fde and contains exactly 8734 distinct binary rows of length 25 and weight 11. The independently written checker enumerated all 480370 nine-element subsets of all row supports; all were unique. For two weight-11 supports S and T, Hamming distance equals 22 - 2|S intersection T|. Thus distance at least 6 is equivalent to intersection at most 8, which is equivalent to no shared nine-element subset. This is an exact complete certificate, not sampled pair testing.

The checker accepted a known distance-6 pair and a singleton, and rejected seven controls for the intended reasons: a weight-valid distance-4 pair, duplicate, wrong weight, wrong length, altered bytes against the pinned hash, wrong row count and invalid alphabet. All nine controls passed. Checker SHA256: 597f1f66ecca299fa4e3aaabecaf65161493ce7fda2fb9234f74a55b9a87e239. Execution: 2026-10-19T11:23:00.506170+00:00 to 2026-10-19T11:23:00.718441+00:00, exit 0, wall time 0.2121678750263527 seconds, peak RSS 32391168 bytes. A one-process guard enforced a 256 MiB and 900-second budget with no violation. Deterministic verification of an explicit object makes a statistical 400-control null experiment unnecessary.

## Table, mirror and contributions

KNOWN from original source 1: the live table responded HTTP 200 at 2026-10-19T11:22:35.492936+00:00. In the distance-6 table, row 25 and weight column 11 read 8718Pl-24630. Therefore 8718 < 8734 <= 24630. The row has no separately printed weight-14 cell. Complementing every bit is a bijection from weight 11 to weight 14 preserving distances, so A(25,6,11) = A(25,6,14); there is no independently larger printed mirror value in this page.

The current upstream family INDEX lists 8718. The current TROPHY_CASE body, source E2, independently hashes to the Git blob 571f24117c6b128ffe751a39f22fcab68c498e66 in the supplied current recursive tree and lists 8718 for this cell. The recursive tree is not truncated and contains 5166 entries. Six all-state pull-request API pages contain 554 distinct PR records. Searching their titles and bodies identifies open PR 437, A(25,6,11) >= 8720, as the strongest located direct same-cell public claim. Its claimed value is lower by 14. Its statements about its own reviewers are not used as evidence that those reviewers or its object passed. PR comments and arbitrary unreturned file contents are outside this inventory's scope.

## Required papers and located newer work

Echols 2608.13906v1 was checked from the full HTML and complete 124-construction Table 1. It has no target or mirror row. Its two n = 25 results have (d,w,M) = (8,11,1722) and (10,12,141). Lysenstoen 2607.19550v1 was checked from the full HTML; its finite improvements and discussed cells do not include the target or mirror. Their current abstract/version receipts list v1.

Five additional full HTML bodies were checked against the exact cached hashes below; raw live abstract sources 14–18 independently identify the same v1 versions in their og:url metadata:

- Rosin 2603.00174v1, full Table 1: 24 finite improvements, none for the target or mirror; its n = 25 distance-8 weight-11 construction has 1702 words.
- Chee, Xing and Yeo 1008.1610v1: Theorems II.1–II.3 give coset/intersection and average propagation methods; the paper does not demonstrate an equal-or-better target-cell bound. For example, the displayed Preparata average rule after shortening to length 25 gives ceil(C(25,11)/2048) = 2177. A generic method without an actual same-cell bound does not subsume this explicit code.
- Yang et al. 2609.35051v1, full Theorem 5.4 and tables: the finite constant-weight support families are distance 8, weight 8, at lengths 33, 34, 37, 38 and 39, with sizes 1803, 1960, 2843, 3077 and 3383. The dimension-25 kissing configuration is not a printed A(25,6,11) bound.
- Chee 2610.10973v1, full Section 5.2 and Corollary 18: asymptotic attainment with an unspecified o(1) term does not establish a finite n = 25 bound; no target-cell bound is demonstrated.
- Ota, Osa and Harada 2610.11609v1, full Proposition 3.1 and explicit lists: general binary codes of sizes 84, 196 and 65 at different parameters do not demonstrate an equal-or-better target constant-weight code.

The fresh supplementary search located Milshtein 2610.23626v1, submitted 16 October. Its original abstract and full HTML are sources E4 and E5. I independently read the full body: its four improvements are general binary codes (16,3072,3), (17,6144,3), (18,12288,3), (19,24576,3). It demonstrates no target or mirror bound and does not subsume this candidate.

## Current literature search: evidenced scope

Source E1 is a complete official API response for all:"constant weight" OR all:"constant-weight", fetched 19 October at 11:48:17.975465 UTC, with 309 returned entries against 309 total results and 309 unique IDs. The query has no date restriction and covers the topic over the requested last 24 months and earlier. Its latest returned update is 12 October at 09:17:17 UTC; no entry was updated after the previous authorized 17 October batch. Source E3 supplements this with the query "binary codes" AND ("lower bounds" OR "constructions"), for submissions from 1 January 2025 through 19 October 2026. It returned all 71 of 71 results at 11:48:48.678032 UTC; its latest update is 16 October at 15:33:22 UTC. Relevant returned titles and abstracts were screened, and the newly located finite-code paper above was read in full.

These receipts close the actual 17–19 October source gap identified in the earlier reviews. They describe finite query coverage, not an exhaustive all-phrase census or proof that no unpublished code exists. The known relevant papers outside literal metadata wording, including Yang, were separately read. No material equal-or-better target/mirror value was identified in the supplied literature, table, trophy, index or PR evidence.

## Ancillary blocked file and non-subsumption

Original source 20 returned HTTP 403 for an archive file of the different cell A(27,6,11). The event remains recorded; no retry or bypass was attempted. It does not make the successfully read primary status_source return a failure. No supplied evidence demonstrates a target-cell value at least 8734 from that unavailable object. Requiring evaluation of every possible transformation of every neighboring code would add a quantifier absent from the bank criterion.

As an additional finite check, source 19's actual A(26,6,12) 14854-row list was independently parsed; the largest of its 26 one-coordinate one-slices has 6868 rows, so direct one-coordinate shortening of that supplied list cannot subsume this candidate. This useful check is not represented as an exhaustive exclusion of all constructions.

There is no currently identified finite missing evidence for this CRITERION decision. This conclusion is based on the actual source snapshots and bounded searches above. The manager must still evaluate the other independent panel reports, the honesty gate, final source freshness, the package and real workspace/package CHECK_RUN outputs before publication.

## Original public source receipts

| Source | URL | HTTP | UTC response | SHA256 |
|---|---|---|---|---|
| 1 | https://aeb.win.tue.nl/codes/Andw.html | 200 | 2026-10-19T11:22:35.492936+00:00 | 13c8fdd428059d82986d63cdba9beeaf5a436464c7ec18ced8b17bf0ec6c0851 |
| 2 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1&sort=updated&direction=desc | 200 | 2026-10-19T11:22:48.962759+00:00 | c2eae7b435e96673fbf78e7db5853e67e768a4655b8fb8fb1105fdc23d3dcf84 |
| 3 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=2&sort=updated&direction=desc | 200 | 2026-10-19T11:22:59.310259+00:00 | 4b86c7b49d912f052f2cabdac6aadc7380f0d2e8b5d347650abe6ab77c6cb6a5 |
| 4 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=3&sort=updated&direction=desc | 200 | 2026-10-19T11:23:00.452253+00:00 | fbafff7175cc9bc9fb85091f9eb84d3b019ee29d91246d3ae06a1635d4b874ec |
| 5 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=4&sort=updated&direction=desc | 200 | 2026-10-19T11:23:01.558676+00:00 | 2f519f0ae18f68c5a0569eee4b95e7f754bf2c2995f0639f41da9e9a21015d62 |
| 6 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=5&sort=updated&direction=desc | 200 | 2026-10-19T11:23:02.675551+00:00 | bf454d11f745d5696c2edc53ecb8bf1cc940b9978449013ec3a9a6e1a30a666e |
| 7 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=6&sort=updated&direction=desc | 200 | 2026-10-19T11:23:03.633987+00:00 | 6aa1f9a35c5b924fda1daf14567723fda817ba64ba8319fac9e00a2ef7b189fc |
| 8 | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | 200 | 2026-10-19T11:23:22.263065+00:00 | 74e28ac7f4827deaff1fef045da5fde5635ea2bb04a067f333e44c4d186375b8 |
| 9 | https://arxiv.org/abs/2608.13906 | 200 | 2026-10-19T11:23:22.806006+00:00 | cc9f1406799ec21ab93ca205599958f354524ca478d2a87e1d38921088027dd9 |
| 10 | https://arxiv.org/abs/2607.19550 | 200 | 2026-10-19T11:23:23.025829+00:00 | 6aa83d5b31b4443688dc57e54e000d5272f744fd918b6b115f6636d5291344f1 |
| 11 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/bigger-codes/INDEX.csv | 200 | 2026-10-19T11:23:45.219938+00:00 | e7ed745ea3299877231732acb040b97d5e7953c04ef7a76f228856d3b92e2ff7 |
| 12 | https://arxiv.org/html/2608.13906v1 | 200 | 2026-10-19T11:23:45.426316+00:00 | 57b3e5fd6679385eb244a7a1171631204b0aa48cc61c68a37d6421ec2fe742a4 |
| 13 | https://arxiv.org/html/2607.19550v1 | 200 | 2026-10-19T11:23:45.597830+00:00 | 138e693dab62b9ce51829de318209faa0986ba167778ebbe5d2b9aa259cd190c |
| 14 | https://arxiv.org/abs/2603.00174 | 200 | 2026-10-19T11:26:52.578928+00:00 | 1e66da3a946247d00e3cd33497d108c47014108ab4ab0e44b475824eef4203d6 |
| 15 | https://arxiv.org/abs/1008.1610 | 200 | 2026-10-19T11:26:53.494611+00:00 | 3d26bb4254b72942f9a57d04af95ac732f06a9a97711bf488cb10a4db96ff0d0 |
| 16 | https://arxiv.org/abs/2609.35051 | 200 | 2026-10-19T11:27:47.026671+00:00 | d4458556ab8b83608bcea941a33a7b410f6054550dfe61adc0b423102cb5832c |
| 17 | https://arxiv.org/abs/2610.10973 | 200 | 2026-10-19T11:27:47.236854+00:00 | 0d45a4971e5c9cf1daa01c29174802690bdc523316416020529184f3e2229f0e |
| 18 | https://arxiv.org/abs/2610.11609 | 200 | 2026-10-19T11:27:47.462767+00:00 | 4e6fefc1ca07acdf9ebf90d9e501d2f17f9d3847b524a6ab1ce7908c7c15ca23 |
| 19 | https://aeb.win.tue.nl/codes/cwc/d6/a26.6.12.14854H | 200 | 2026-10-19T11:28:20.822706+00:00 | cde1edf846a27f1eb3d65aab7df65f0759ff0707b00b309b3b025fd2037b0e97 |
| 20 | https://aeb.win.tue.nl/codes/cwc/d6/a27.6.11.19344H | 403 | 2026-10-19T11:28:21.353363+00:00 | 57559551c35735c4acd1ede5a7d3df31a3f9b55acc087fdbb0811813b13d63d3 |
| E1 | https://export.arxiv.org/api/query?search_query=all%3A%22constant+weight%22+OR+all%3A%22constant-weight%22&start=0&max_results=500&sortBy=lastUpdatedDate&sortOrder=descending | 200 | 2026-10-19T11:48:17.975465+00:00 | c8720105f95d9999438fe026b5d4b55c19fa5da38495929ed2cdecbad63201f4 |
| E2 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 200 | 2026-10-19T11:48:47.244978+00:00 | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 |
| E3 | https://export.arxiv.org/api/query?search_query=%28all%3A%22binary+codes%22+AND+%28all%3A%22lower+bounds%22+OR+all%3A%22constructions%22%29%29+AND+submittedDate%3A%5B202501010000+TO+202610192359%5D&start=0&max_results=500&sortBy=lastUpdatedDate&sortOrder=descending | 200 | 2026-10-19T11:48:48.678032+00:00 | c4b490c36e486999621aaee7b41cddd66069ef383d2ee03f7eeaa4f65d4a4a7d |
| E4 | https://arxiv.org/abs/2610.23626 | 200 | 2026-10-19T11:49:35.072279+00:00 | 1d74319c754e104b8942d9c2530149ed6548eb2053f15c5b89e5468fd04786cb |
| E5 | https://arxiv.org/html/2610.23626v1 | 200 | 2026-10-19T11:49:43.724199+00:00 | eb2949c5d995f28e91e714522fcd887afab35f7fcb8cef41b1039f202a996f3b |

## Cached full-text bodies independently verified

Each version was revalidated by the corresponding original live abstract receipt 14–18 above. Cached bodies were read offline; no new HTTP request was made by this review context.

| Version | Original URL | Bytes | SHA256 |
|---|---|---|---|
| 2603.00174v1 | https://arxiv.org/html/2603.00174v1 | 303156 | 8d99461f7d1d081ed6c2a18342a642783db09b4ec16a93f59ad6e574abb7b829 |
| 1008.1610v1 | https://arxiv.org/html/1008.1610v1 | 197390 | 09570e9ea01c6bc82ac945b9cdcd1c5212be7de96466953078b402128c4c1e16 |
| 2609.35051v1 | https://arxiv.org/html/2609.35051v1 | 1202235 | 4f198ce63a12587570c5630f18a5d5b1119d4e97a190d66bb2e0ec7f361b9ed1 |
| 2610.10973v1 | https://arxiv.org/html/2610.10973v1 | 625569 | 61abd61e8c4205d7e08b66b81bc4347f5c1502738980842cf5a766a16df58d11 |
| 2610.11609v1 | https://arxiv.org/html/2610.11609v1 | 72337 | e832cec72ef0cf0313d9e7daf47f4468879d2daf6e43dea5301063ec45017cab |

pass: true
