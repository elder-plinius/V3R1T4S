# The record we beat
Cell: z(16,19;3,3), the largest number of ones in a 16 x 19 0/1 matrix with no all-ones 3 x 3 submatrix.

Primary status page (read once by the NOVELTY reviewer, no retry)
- URL: https://arxiv.org/abs/2608.26603 (Saurabh, "Five improved lower bounds for Zarankiewicz numbers z(m,n;3,3)", v1 27 Aug 2026)
- fetched (UTC): 2026-10-17T12:28:33Z; HTTP status 200
- selected headers: not recorded by the reviewer
- sha256 of the page as fetched: cf55f0ef17b3ee5303fb2655a032bcf850069b755485386f3f62f8f902796468
- extracted cell: the abstract states z(16,19;3,3) >= 136 (monotone padding of z(16,18;3,3) >= 136); it also lists the earlier values 114, 121, 130, 125, 132 for the five cells, 132 for (16,19)

Second status source (same reviewer, same minute)
- URL: https://raw.githubusercontent.com/KAVentures/z1322-exact/main/proof/frontier_closure/reports/frontier_propagation.json
- fetched (UTC): 2026-10-17T12:28:33Z; HTTP status 200; sha256 d97267968b917a91fb34ff9bc3fb35c7eaf1753c7b888d9294b0bfef43ef0b22
- extracted cell: entry (16,19) is an upper bound only, 147 (old 151); no lower bound above 136 for this cell

Value compared: 142 (object/z_16x19_142.txt) is 6 above the best explicitly stated lower bound 136 and 5 below the best upper bound 147.
Derivable baseline: 141, the best of 192000 saved trivial-surgery runs on the 12 public witness matrices (how-we-built-it/baseline/output/).
The saved scout behind these numbers is how-we-built-it/status_source/scout_record.md (written 2026-10-17 before the reviewers' fetches).
The reviewers' working copies of the fetched pages are not included here (no third-party pages are copied into the package).
