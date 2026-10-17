# Novelty check: z(16,19;3,3) >= 142
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: no source fetched states or trivially implies a value above 136 for z(16,19;3,3); 142 strictly beats the stated 136 (caveats on PR coverage below)

## Fetched (each once, no retries; files in work/)
| file | URL | UTC time | HTTP | sha256 |
|---|---|---|---|---|
| work/prs.json | api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+zarankiewicz+is:pr&per_page=100 | 2026-10-17T12:28:32Z | 200 | c9938edecb99d754b2d039ac9eec320a94c769b6a6417921e2dcbef9e2fe01a0 |
| work/lsremote.txt | git ls-remote ... 'refs/pull/*/head' | 2026-10-17T12:28:33Z | ok | (no hash taken; count 338) |
| work/trophy.md | raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-17T12:28:33Z | 200 | 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 |
| work/arxiv_abs.html | arxiv.org/abs/2608.26603 | 2026-10-17T12:28:33Z | 200 | cf55f0ef17b3ee5303fb2655a032bcf850069b755485386f3f62f8f902796468 |
| work/frontier.json | raw.githubusercontent.com/KAVentures/z1322-exact/main/proof/frontier_closure/reports/frontier_propagation.json | 2026-10-17T12:28:33Z | 200 | d97267968b917a91fb34ff9bc3fb35c7eaf1753c7b888d9294b0bfef43ef0b22 |
| work/arxiv_api.xml | export.arxiv.org/api/query (Zarankiewicz, newest 50) | 2026-10-17T12:28:34Z | 200 | e932e3ae72a1107591f1a4416056f5f8621d4236f1b461bf993c0b98b621a9a6 |
| work/bhan_abs.html | arxiv.org/abs/2605.01120 | 2026-10-17T12:28:34Z | 200 | c52d8341ac338914ff33a4a276ed527c0ba2fff8a7df2d2d326c2cef8fb62afd |
| work/tree_dfield_finite-zarankiewicz-closures.json | api.github.com trees (dfield) | 2026-10-17T12:28:55Z | 200 | 511e8a549eacbd27843dd6f1bd7b26096cb9d337dd727bcec87c60000a6cb90b |
| work/tree_ShengtengHou_finite-zarankiewicz-seven-values.json | api.github.com trees (Hou) | 2026-10-17T12:28:55Z | 200 | d85475f6aedd4f1cb41b021f520d152d6e1d06a4b4ec01b3fabdf75de432cce1 |
| work/tree_KAVentures_z1322-exact.json | api.github.com trees (KAVentures) | 2026-10-17T12:28:56Z | 200 | 1f19311f8a1054188cb688a40ab1d37145e292b99c3d595f2468cb5e9eef111d |

GitHub API calls used: 4 of 8.

## Findings
1. Pull requests: the search returned {"total_count":0,...,"items":[]}, so no PR matching "zarankiewicz" (open or closed). git ls-remote lists 338 refs/pull heads, but titles are not available from it, so I could not screen PRs that do not use the word Zarankiewicz. No Zarankiewicz PR found, so none claims z(16,19) or a cell implying it. Limit: GitHub lexical search only.
2. TROPHY_CASE.md (30936 bytes): grep for "zarankiewicz" and "z(16" gives 0 matches.
3. arXiv 2608.26603 (title "Five improved lower bounds for Zarankiewicz numbers z(m,n;3,3)", Submitted on 27 Aug 2026), abstract states: "z(16,19;3,3) >= 136" (by monotone padding of z(16,18;3,3) >= 136), and the earlier Figure 2 values of 2605.01120 as 114, 121, 130, 125 and 132 for the five cells (132 for 16x19). Matches CLAIM.md.
   frontier_propagation.json: (16,19) entry is an upper bound only: old_upper 151, new_upper 147, "column deletion from (16,18)<=140"; (16,20): new_upper 154. new_seed_bounds contain only cells up to 16,17 (133). No lower bound above 136 for (16,19). 142 <= 147, so no contradiction.
4. Literature (arXiv API, 50 newest, all dated 2024-12 to 2026-10-04 screened by title): entries after 27 Aug 2026 are 2608.30555, 2609.02498, 2609.07227, 2609.07475, 2609.11093, 2609.16555, 2609.18429, 2609.20071, 2609.25974, 2609.32937, 2609.33191, 2609.33327, 2609.40288, 2610.04448, 2610.05442. All are on second-order, augmented, recursive-line or limited Zarankiewicz numbers, asymptotic or Ramsey bounds, or algebraic constructions. I read the abstracts of 2610.05442 and 2609.40288 (asymptotic / Ramsey); none addresses explicit z(m,n;3,3) lower bounds for small cells. I did not open the full text of each (no table fetches were warranted). Limit: arXiv only, no OEIS or Google Scholar.
5. Public matrices: the 2605.01120 abs page has no code or data link (only generic huggingface links). Trees: the largest-width witness files are Hou z1518_132, KAVentures z16_17_132_witness_seed201 and z15_18_132, z14_18_124, dfield z12_23_134. No 16x20, 17x19, 17x20 or larger witness exists in the three repos, and no 16x19 witness. So nothing downloadable yields a 16x19 matrix by deletion. Trivial padding of the 16x17/133 or 15x18/132 witnesses gives at most about 133 to 141 by the claim's own surgery runs (141, not independently recomputed by me since no larger witness exists to delete from). The claim's own baseline (192000 runs) tops at 141, below 142.

## Reasoning
Best explicitly stated lower bound found live: 136 (arXiv 2608.26603). Nothing newer or larger found. 142 is strictly above 136 and above the claim's own 141 derivation baseline. Residual risks: PRs whose text omits the word Zarankiewicz were not screened; the claim itself notes 142 is easy to reach by simple local search (priority risk, not a published value); OEIS and printed sources were not checked.

pass: true
