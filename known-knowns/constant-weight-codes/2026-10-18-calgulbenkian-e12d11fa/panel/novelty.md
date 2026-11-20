# Novelty report for code-56-8-7-4691

context: Claude Code subagent, fresh context [Sonnet 5.5]

role: novelty (skeptic 2 of 3, cwc group, code cells)

claim under test: A(56,8,7) >= 4691, versus live Brouwer table lower bound 4685.

## Primary table (fetched once, no retries)
- URL: https://aeb.win.tue.nl/codes/Andw.html
- fetched 2026-10-18T17:54:24Z, HTTP 200, sha256 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349 (identical to the page hash recorded in the-record-we-beat/README.md).
- value read in cell (56,8,7): the anchor text for this cell is a56.8.7.4685H, shown as 4685 with its source label (Pl) and the printed upper bound much larger than 4691. The claim's M = 4691 is strictly greater than 4685 (margin +6).
- mirror cell A(56,8,49): the page prints weights only up to about n/2 in these sub-tables, so it has no separate cell for weight 49; checked that no a56.8.49. anchor exists. Complement symmetry gives the same number, so nothing higher is hidden there.
- M does not exceed the tabulated upper bound.

## V3R1T4S status
- TROPHY_CASE.md fetched 2026-10-18T17:54:25Z, HTTP 200: the merged row for this cell (if any) lists the table value 4685 or older; nothing at or above 4691.
- Pull requests pages 1 to 5 (api.github.com, all HTTP 200) read by title; bodies read for same-target PRs. Same-target open PR: only 351 (A(31,10,7) upper bound, a different cell). Open PRs 393 and 399 only restate live table values and add no code for this cell. Competing claim on this cell by anyone else: none found.
- Author's earlier filings (not competing values): closed PR 53 (same contributor): 4691, closed unmerged.
- Merged known-knowns folder: INDEX.csv 4685. Dated package folders (freelsgood 2026-10-14, ada95ftw x2 and drzuzzjen 2026-10-17) were listed; INDEX.csv of bigger-codes holds no value above 4685 for this cell.

## Literature (last 24 months)
- arXiv:2608.13906 (Echols, 124 cells): this cell: not listed in Echols table; below 4691. The paper PDF text was fetched once (HTTP 200) and its table rows read.
- arXiv:2607.19550 (Lysenstoen): abstract covers only A(23,6,10), A(24,6,10), A(23,6,11), A(24,6,8); this cell is not among them.
- arXiv:2609.35051 (Yang et al.): kissing numbers only; no constant-weight value for this cell (abstract).
- Two further arXiv API searches on constant-weight codes sorted by date (results through 2026-10-11) showed no paper reporting a lower bound for A(56,8,7).

Sources fetched (name | URL | UTC | HTTP | sha256):
- https://aeb.win.tue.nl/codes/Andw.html | 2026-10-18T17:54:24Z | 200 | 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-18T17:54:25Z | 200 | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1
- https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1 | 2026-10-18T17:54:25Z | 200 | 94c43b06c7c0de25cc0365e56102d6695ff07ab8764916294338801fc5709691
- https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=2 | 2026-10-18T17:54:27Z | 200 | da068aed9e04f2cb868043b5024b60113e6c8f18511e18c70248a0bdde729603
- https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=3 | 2026-10-18T17:54:29Z | 200 | a7bcb41093ddc65dbe6ade594a6eb914631f560fec728d9f238ee15a4d9821f5
- https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=4 | 2026-10-18T17:54:32Z | 200 | 97ed593e02cea0b673aae348f2a8581098488fc8008d670f87e43a73e93c99f6
- https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=5 | 2026-10-18T17:54:34Z | 200 | 5a8e76931e6213dc03d5a5820c42e541ea0259bc00e685c08687440c923e1dda
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns | 2026-10-18T17:54:35Z | 200 | 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011
- https://export.arxiv.org/api/query?id_list=2608.13906 | 2026-10-18T17:54:45Z | 200 | f286e74e6c6b056e1ccad3229839ca273b305f59aebf9cbe585d78c1f6cff2a9
- https://export.arxiv.org/api/query?id_list=2607.19550 | 2026-10-18T17:54:45Z | 200 | 38d53b578ab058081fa7b768e88ea640b63f9b0543b84c53d3d59174c92bfc46
- https://export.arxiv.org/api/query?id_list=2609.35051 | 2026-10-18T17:54:45Z | 200 | 14ad933b9ad8303c2f5cef121e715745ecc8d1ad4524ff244d742f7c508b9e7b
- https://export.arxiv.org/api/query?search_query=all:%22constant+weight+codes%22&sortBy=submittedDate&sortOrder=descending&max_results=15 | 2026-10-18T17:54:46Z | 200 | 354866e18739267a7e6f8a09c514c5c346d60fc52f6e0d2c355c62a1a1424e13
- https://export.arxiv.org/api/query?search_query=all:%22constant-weight%22+AND+all:code&sortBy=submittedDate&sortOrder=descending&max_results=15 | 2026-10-18T17:54:46Z | 200 | a2eda5882ca729d59ea156fb14e94f9bab41a9d2b7412ba0ee70fe58f9f5fb68
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/bigger-codes | 2026-10-18T17:54:52Z | 200 | 2c28c925e21f330656151a6c717352b2150825609d044d0d38474900fa1ce884
- https://arxiv.org/pdf/2608.13906 | 2026-10-18T17:55:12Z | 200 | 915cfa5ebbcdb1cda97bd7c9bb2038a9bc42188538ffd0a4eca409f13c7fcf50
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/bigger-codes/INDEX.csv | 2026-10-18T17:55:29Z | 200 | e7ed745ea3299877231732acb040b97d5e7953c04ef7a76f228856d3b92e2ff7
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/bigger-codes/2026-10-14-freelsgood-9e824e9f | 2026-10-18T17:55:29Z | 200 | 04a6d177e68c2bb5b579ca80116e73bc4e4cc9b267400c388b3a0bffb3afd6ed
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/bigger-codes/2026-10-17-ada95ftw-10f16a89 | 2026-10-18T17:55:30Z | 200 | 28acf93ea09a7dcbf90e68fdda216ffdfb87efe54ee1c849884e669629d931f9
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/bigger-codes/2026-10-17-ada95ftw-37026903 | 2026-10-18T17:55:30Z | 200 | 1b25c0fc709e9d36e1e60931de5eb2ce1e4728bbe8eab16a216aa4edd9553e44
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/bigger-codes/2026-10-17-drzuzzjen-6be5a215 | 2026-10-18T17:55:30Z | 200 | 1cb8bd80d885d5331500e4186c66d564ebfba0827cbea9dcaeafbd32f96c77ec

Note: the first four arXiv requests used http and returned 301 (redirect, no content); each was repeated once over https, which is the request listed above.

unresolved: the table page's own cell and the archive files could be updated by Brouwer after 2026-10-18T17:54Z, and unpublished emails to Brouwer cannot be seen; full texts of papers other than Echols were not read (abstract-level search only). Neither is likely to hold a value of 4691 or more.

verdict: the explicit code of size 4691 strictly exceeds every known value found for A(56,8,7) (live table 4685, Echols and Lysenstoen no higher, no competing PR). The author's own closed earlier filings are not competitors. Strict beat, not a tie.
pass: true
