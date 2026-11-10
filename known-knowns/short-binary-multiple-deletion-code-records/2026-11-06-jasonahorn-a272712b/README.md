# A binary 3-deletion code of length 16 with 43 words

## What

The 43 distinct binary words of length 16 have pairwise disjoint length-13 deletion subsequences and maximum pairwise LCS 12, strictly above the bold best-known size 42 for binary 3-deletion correction at length 16 in Table 2 of arXiv:2504.00613v2, and the claim states the list is not a composition of a published codebook while identifying an unpublished local 42-word hint that shares 31 words.

## Check it yourself

From this folder: `sh verify-it-yourself/run_checks.sh`

Expected last line: PASS

Rough laptop time: under a second.

## Compared to

Table 2 of Weindel and Heckel, arXiv:2504.00613v2, HTML page https://arxiv.org/html/2504.00613v2, fetched 2026-11-06T08:42:34Z, HTTP 200, sha256 4542bd58bc16be9bf47f6fc12f14fe86464c078c5a9c747058ee5698fbc7499a. Binary 3-deletion correction, n=16, MIS solver OnlineMIS: 42, bold. Other construction rows in that cell are 39 or smaller. LP upper bound 99. ReduMIS t/o.

## Not claimed

No code for (15,2), (16,2), or (15,3). No proof that 43 is optimal. The solver status was feasible, not optimal. The LP upper bound remains 99. No decoder and no linearity claim.

## Credits

Franziska Weindel and Reinhard Heckel, arXiv:2504.00613v2, for Table 2 and the size-42 OnlineMIS figure this code beats. Landjev and Haralambiev, Serdica Journal of Computing 2007, for the earlier search heuristics cited in that table. The OnlineMIS and ReduMIS rows are credited there to those solvers.
