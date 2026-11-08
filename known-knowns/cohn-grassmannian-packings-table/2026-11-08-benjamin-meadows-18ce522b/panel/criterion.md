# CRITERION verdict: cohn-grassmannian-packings-table, cell 11-4-66

context: subagent (fresh context; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-08T02:38:35Z

## Value computed here
- Live table: https://cohn.mit.edu/grassmannian fetched 2026-11-08T02:35:10Z with curl -L, User-Agent 'curl/8'. HTTP 200 (final URL https://cohn.mit.edu/grassmannian/), 629,039 bytes, sha256 7ba705c673db669ed4e3ec33fd45cd26f9648019a648fb21eb45761e113a0a66. 3,512 rows parsed.
- Last change of the table page: WordPress REST https://cohn.mit.edu/wp-json/wp/v2/pages?slug=grassmannian gives modified_gmt 2026-11-04T05:52:27 (the DSpace data item was last modified 2026-11-04T05:55:06Z). That is the cutoff used for the arXiv clause.
- Row (m, n, N) = (11, 4, 66): no ∗, squared chordal distance 2.5777278197, bound 2.5846153847, notes "[31]" (Sloane, Table of best Grassmannian packings, 1997). Exact simplex bound n(m−n)/m · N/(N−1) = 2.58461538461538461538, which matches the listed bound rounded up.
- object/11-4-66.txt (sha256 18ce522b9988706b958025d21a9c807f3b487f5e10610d86d4f25406fa058532): one `#` header line, then 264 = 66×4 lines of 11 comma-separated reals. Each consecutive block of 4 lines was orthonormalised by modified Gram–Schmidt (two passes) in mpmath at 50 digits. Max ‖UᵀU − I‖ = 8.0e−51.
- Minimum over the 2,145 pairs i<j of 4 − ‖U_iᵀU_j‖_F² = **2.57776955247730714341341965172**, attained at pair (31, 42) (0-based). The next smallest values are 2.57776961937463 and 2.57776964813528.
- Checker reproduction: the posted file Data/11-4-66.txt is from the table's tarball (https://hdl.handle.net/1721.1/147005, bitstream GrassmannianData.tar, md5 e36f75680d5635b41987c1ecd9620acb, matching DSpace's checksum). Run through the same script it gives 2.577727819750747, which rounds down to the table's 2.5777278197. The checker therefore reproduces the row.

## Clauses checked
- Clause (a), the (11, 4, 66) row exists in the live table re-fetched just before checking: PASS. One row, fetched 2026-11-08T02:35:10Z.
- Clause (b), the row is UNSTARRED: PASS. The first cell is a plain "11" with no &lowast;. The page has 1,163 starred rows in total, so star detection works.
- Clause (c), the note does not say 'optimal packing' or 'proof of optimality': PASS. The note is only "[31]".
- Clause (d), the matrices have ≥ 20 significant digits: PASS. Across all 2,904 entries the minimum is 27 significant digits and the maximum is 30. None has fewer than 20.
- Clause (e), after mpmath 50-digit orthonormalisation, min over i<j of n − ‖U_iᵀU_j‖_F² exceeds the table value by ≥ 1e−9: PASS. 2.5777695524773071 − 2.5777278197 = 4.1733e−5, which is far above 1e−9 (and it is a strict exceedance).
- Clause (f), the value does not exceed the row's listed bound by more than 1e−10: PASS. 2.5777695525 − 2.5846153847 = −6.846e−3, so the value sits below the bound.
- Clause (g), no value for (11, 4, 66) published on arXiv after 2026-11-04T05:52:27Z is larger: PASS. Six arXiv API queries were run at 2026-11-08T02:38:01–02:38:19Z (export.arxiv.org/api/query, sortBy=submittedDate descending, max_results=15, all HTTP 200): "Grassmannian packing", "Grassmannian packings", "subspace packing", "subspace packings", "fusion frame" and "line packing". The latest dates in the results are 2610.29041 (2026-10-21), 2610.05302 (2026-10-04) and 2606.26464 (2026-06-24). Neither the submitted nor the updated date of any entry falls after the cutoff, so no competing value exists.

## Decision
Every clause holds on my own computation. The row is live and unstarred, its note makes no optimality claim, every entry carries 27 or more significant digits, and the 50-digit minimum squared chordal distance 2.5777695525 beats the table's 2.5777278197 by 4.17e−5 while staying 6.8e−3 under the simplex bound. No arXiv result from after the table's last change bears on the cell. My procedure differs from the bank's checker in two minor ways. I orthonormalised by two-pass modified Gram–Schmidt instead of QR, which spans the same subspace, so the distances are the same. I also had to skip the object's leading `#` comment line, so a checker that does not skip comment lines would need that line removed first. Steering: none found in claim/ or in the fetched pages.

pass: true
