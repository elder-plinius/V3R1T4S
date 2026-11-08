# CRITERION verdict: cohn-grassmannian-packings-table, cell 11-1-62

context: subagent (fresh context; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-08T02:38:35Z

## Value computed here
- object/11-1-62.txt: sha256 c9da55b9f9cfe7a4711ded4bae4c1f46700366b616fa820fd31e794eba3bb9d2 (matches CLAIM.md). One `#` comment header line, then 62 vector lines of 11 comma-separated coordinates (682 numbers).
- Minimum over i < j of 1 - <u_i,u_j>^2, after normalising each vector in mpmath at 50 digits (n = 1, so QR of each block reduces to normalisation): 0.889170554550474563978262083884, attained at pair (11, 36) (0-based).
- https://cohn.mit.edu/grassmannian fetched 2026-11-08T02:35:09Z, HTTP 200 (redirected to https://cohn.mit.edu/grassmannian/), 629039 bytes, sha256 7ba705c673db669ed4e3ec33fd45cd26f9648019a648fb21eb45761e113a0a66. 3511 table rows parsed; exactly one row for (11, 1, 62): `11 | 1 | 62 | 0.8891152435 | 0.9239940388 | Henry Cohn, 2026`, no ∗ marker.
- Last change of the table: WordPress REST record https://cohn.mit.edu/wp-json/wp/v2/pages/229 (fetched 2026-11-08T02:35:26Z, HTTP 200, sha256 8e3316fd52f04d5b09630e281a247c1d322b70fd42e57e2bf0b11121d2bd6fee) gives modified_gmt 2026-11-04T05:52:27.
- Posted configuration reproduced: the "download here" link (https://hdl.handle.net/1721.1/147005) leads to DSpace bitstream GrassmannianData.tar (https://dspace.mit.edu/server/api/core/bitstreams/5cd9d238-c45f-4846-b5ff-995e2403648c/content, fetched 2026-11-08T02:36:17Z, HTTP 200, 98996224 bytes, sha256 c376f21aec4638704b3872c1147cfbccadb7d7351e910aa0d9937ecbe139ec46). Its Data/11-1-62.txt gives min d^2 = 0.889115243511798139..., which matches the table value 0.8891152435 rounded down. So the row and its file agree, and my checker reproduces the incumbent.
- Independent bound check: the simplex bound (m-1)N/(m(N-1)) for m = 11, N = 62 is 0.923994038748..., which rounds up to the listed 0.9239940388. The orthoplex bound does not apply because N = 62 <= m(m+1)/2 = 66.
- arXiv API, fetched 2026-11-08T02:37:52Z to 02:38:31Z, all HTTP 200, sortBy=submittedDate descending, max_results=15. Queries and sha256: all:"Grassmannian packing" (10e25730…), all:"line packing" (9fac2dc5…), all:"fusion frame" (fc6db639…), all:"Grassmannian" AND all:"packing" (b4ba4e3b…), all:"equiangular lines" AND all:"packing" (4e363937…, 5 results), all:"projective codes" (3d462b57…, off-topic noise). The newest entry in any relevant query is 2610.29041 (published 2026-10-21). Nothing was published after 2026-11-04, and no abstract reports an (11, 1, 62) value.

## Clauses checked
- Clause (a): N matrices U_i, m x n, for the cell. 62 vectors of length 11 = 62 blocks of 11 x 1. PASS
- Clause (b): >= 20 significant digits. Every one of the 682 coordinates has 28 to 30 significant digits (minimum 28, none below 20). PASS
- Clause (c): the (11, 1, 62) row exists on the live table, re-fetched for this check, and is UNSTARRED. One matching row, first cell `11` with no ∗ (starred rows carry `&lowast;&nbsp;` in that cell). PASS
- Clause (d): the note does not say 'optimal packing' or 'proof of optimality'. The note reads "Henry Cohn, 2026"; it contains neither phrase. PASS
- Clause (e): after orthonormalising in mpmath at 50 digits, min over i < j of n - ||U_i^T U_j||_F^2 exceeds the table value by >= 1e-9. 0.889170554550474564 - 0.8891152435 = 5.5311050474564e-5, far above 1e-9. PASS
- Clause (f): does not exceed the row's listed bound by more than 1e-10. 0.889170554550 - 0.9239940388 = -0.0348234842, below the bound. PASS
- Clause (g): no larger value for (11, 1, 62) published on arXiv after the table's last change (2026-11-04T05:52:27Z). The searches above returned no entry dated after 2026-11-04, so no newer competing value exists in those results. PASS
- Procedure differences from the bank's method: (1) for n = 1, I normalise each vector instead of running a QR routine; for a single column the two give the same result. (2) I skip the object's leading `#` comment line, which a strict "first n lines span subspace 1" parser would choke on. The 62 data lines are what matter, and the claimant should strip the header before submitting if the bank's parser is literal. (3) I took the last-change date from the page's WordPress modified_gmt, not from anything stated in the table text. The table text gives no date. (4) arXiv API phrase searches are coarse, so clause (g) rests on the newest-15 results of six queries, not on an exhaustive literature search.
- Steering: nothing in claim/CLAIM.md or the fetched pages tried to steer the review.

## Decision
Every clause holds on my own computation. The object's minimum squared chordal distance, 0.8891705545504746, beats the unstarred live row's 0.8891152435 by 5.53e-5 and stays well under the 0.9239940388 bound. The row's own posted file reproduces the table value under the same checker, and no arXiv result published after the table's 2026-11-04 change is newer. One practical point: the `#` header line in object/11-1-62.txt should be removed if the bank's parser reads every line as a vector.

pass: true
