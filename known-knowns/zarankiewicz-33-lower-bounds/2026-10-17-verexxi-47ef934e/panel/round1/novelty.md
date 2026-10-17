# Novelty check: z(16,19;3,3) >= 142
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: No published or public value above 136 found for the cell (upper bound 147), but the repo pull-request check could not be read (JS-rendered page, API budget spent), so novelty is not fully confirmed.

## Fetched (one request each, no retries, UA V3R1T4S-verexxi)
- https://arxiv.org/abs/2608.26603 | 2026-10-17T12:26:27Z | HTTP 200 | sha256 cf55f0ef17b3ee5303fb2655a032bcf850069b755485386f3f62f8f902796468 (work/arxiv_abs.html). Abstract: z(13,19)>=118, z(14,19)>=126, z(16,18)>=136, z(14,20)>=126, z(16,19)>=136; prior Figure 2 values of 2605.01120 were 114,121,130,125,132. Submitted 27 Aug 2026, v1 only.
- https://raw.githubusercontent.com/KAVentures/z1322-exact/main/proof/frontier_closure/reports/frontier_propagation.json | 2026-10-17T12:26:27Z | HTTP 200 | sha256 d97267968b917a91fb34ff9bc3fb35c7eaf1753c7b888d9294b0bfef43ef0b22 (work/frontier.json). closed_upper_table (upper bounds only): 16,18 = 140; 16,19 = 147; 16,20 = 154; no 17,x entries. It has no lower-bound table. 142 <= 147, so no contradiction.
- https://export.arxiv.org/api/query?search_query=all:Zarankiewicz&sortBy=submittedDate&sortOrder=descending&max_results=50 | 2026-10-17T12:26:40Z | HTTP 200 | sha256 e932e3ae72a1107591f1a4416056f5f8621d4236f1b461bf993c0b98b621a9a6 (work/arxiv_api.xml).
- A second arXiv API query (Zarankiewicz AND lower bound / K33 / z(16) | 2026-10-17T12:26:54Z | HTTP 200 | sha256 23706ca2c3be4e7fd17d3b5d867c212c2ad8f2b22724ea183e5e9e6a087041e9 (work/api2.xml).
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-17T12:27:02Z | HTTP 200 | sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 (work/trophy.md). Zero occurrences of "zarank", "dfield", "3,3" or "z(16". Its six families do not include Zarankiewicz.
- https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+zarankiewicz | 2026-10-17T12:27:03Z | HTTP 200 | sha256 6d739026e6b8cee5063082ef1df7552a2f46bd4dacb26f4597bacb4fca3d517e. The page is JS-rendered; no PR rows, titles or result counts were in the HTML. INCONCLUSIVE: neither open nor closed PRs could be confirmed absent.
- GitHub tree listings (3 API calls, all HTTP 200, 2026-10-17T12:27:03Z to 12:27:04Z): dfield/finite-zarankiewicz-closures (sha256 511e8a549eacbd27843dd6f1bd7b26096cb9d337dd727bcec87c60000a6cb90b), ShengtengHou/finite-zarankiewicz-seven-values (d85475f6aedd4f1cb41b021f520d152d6e1d06a4b4ec01b3fabdf75de432cce1), KAVentures/z1322-exact (1f19311f8a1054188cb688a40ab1d37145e292b99c3d595f2468cb5e9eef111d). Not truncated.

## Findings
- arXiv: of the 20 newest Zarankiewicz entries, the only one concerning z(m,n;3,3) lower bounds is 2608.26603 (27 Aug 2026). The entries after it (2608.30555, 2609.x, 2610.x) concern second-order, recursive-line, augmented, limited, algebraic, Ramsey or other variants. Their abstracts do not mention K_{3,3} or 3x3. I did not read their full texts or tables. Only the newest 20 entries of the first query were screened, not all 50 and not the second query's other results.
- Public matrices: the three repository trees hold witnesses only for 12x17 to 12x23, 13x17, 13x18, 14x17, 14x18, 15x17, 15x18, 16x17 and 9x23 to 11x23. No 16x20, 17x19, 17x20 or larger-shape matrix exists in them, so no trivial deletion reaches 142. I did not fetch Bhan-Nobili-Langer 2605.01120 code or releases; that is an unchecked gap. I did not recompute any deletion, since no qualifying matrix exists.
- The best stated lower bound for the cell remains 136 (Saurabh padding of 16x18/136). The claim's own baseline reports trivial surgery reaching only 141 in 192000 runs, and notes that its own local search reaches 142 easily, so a priority risk exists (unpublished holders).

## Reasoning
Primary sources are readable and consistent with the claim's table: 136 stated, 147 upper bound, nothing newer than 27 Aug 2026 on this cell, no public larger matrix. 142 would strictly beat 136. However the repository PR check (open and closed) is unconfirmed and the 2605.01120 code was not inspected, and the instruction is to default to false unless genuinely confirmed.

pass: false
