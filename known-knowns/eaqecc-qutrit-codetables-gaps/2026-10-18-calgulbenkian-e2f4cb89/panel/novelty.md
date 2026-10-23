# Novelty report: qutrit-16-4-8-4

context: Claude Code subagent, fresh context

Claim: [[16,4,8;4]]_3, table cell [[16,4,7-9;4]]_3.

## Primary table (fetched once for the group)
- URL: https://eaqecc.codetables.de/qutrit.php, fetched 2026-10-18T14:23:13Z, HTTP 200, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c (628039 bytes). The page footer reads "Last change: 10.07.2025". This sha256 equals the one recorded in the open pull requests 331 and 363 for their earlier fetches, so the table did not change in the last two days.
- Value read for the cell, exact markup text: "[[16,4,7-9;4]]" with title "increasing dimension of [[16,0,7;0]] from codetables.de". So d_lower = 7, d_upper = 9. The claimed d = 8 is strictly above 7 and not above 9.
- Neighbours in the same page: [[16,4,6;0]], [[16,4,8-10;5]] (subcode of [[16,5,8;5]]), [[16,4,9-11;6]]. Nothing in the page gives d = 8 at c = 4.

## Repository sources (fetched once for the whole group)
- TROPHY_CASE.md: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, 2026-10-18T14:23:15Z, HTTP 200, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1. It lists no entry for this target family (no EAQECC, covering-design, Erdos 757 or minimizer row).
- Pull requests, pages 1 to 5: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1 to 5, 2026-10-18T14:23:15Z to 14:23:21Z, HTTP 200 each; page sha256 values cca876cd..., 176c41b2..., 20ec05c4..., f5d26a78..., and page 5 is an empty list (2ba33ca0...). 392 pull requests read by title.
- known-knowns folder listing: https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns, 2026-10-18T14:23:22Z, HTTP 200, sha256 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011. Twenty folders; none belongs to this target.

## Pull requests on the same target (all by others, all open)
- Pull request 363 (psmoros, 2026-10-17): [[33,1,31;24]]_3, cell (33,1,24). Different k, so a different cell.
- Pull request 331 (anzal1, 2026-10-17): [[14,3,8;5]]_3, cell (14,3,5). Different cell.
- No pull request in the five pages names the cell (16,4,4), and I found no earlier filing by the author for this cell.

## Literature (arXiv export API; the first attempt over http returned a 301, so each of the four group queries was sent once over https)
- Query: entanglement-assisted AND qutrit, sorted by date, 2026-10-18T14:26:09Z, HTTP 200, sha256 81a4a683d2436e52c89d5302fcbbdc36b86c0ad38e301c6c124f5f3a31ec21d1. Nine hits; the only in-window paper on qutrit EAQECC tables is arXiv 2607.02170 (Generalized Extended Codes with Applications in Entanglement-Assisted Qubit and Qutrit Codes, 2 July 2026). Its abstract says "14 new EA qutrit codes of lengths n <= 25 compared to the best-known codes in Grassl's code tables". I fetched its PDF once (https://arxiv.org/pdf/2607.02170v1, 2026-10-18T14:26:36Z, HTTP 200, sha256 f1b7794181262beaee2fc4fc8fd4a1085960a8b87a7da038159dc1911961dbef) and read its qutrit tables: the codes listed are [[7,1,7;6]], [[8,0,8;6]], [[8,1,8;7]], [[13,3,7;4]], [[17,2,15;15]], [[18,2,16;16]], [[19,2,17;17]], [[19,3,15;16]], [[21..24,2,*]], [[25,2,22;23]], [[25,3,20;22]], [[7,2,5;3]], [[9,0,9;7]], [[15,2,13;13]], [[16,2,14;14]]. None is [[16,4,*;4]].
- The same paper says it compares with "the latest records in [6], [10], [19], [22], [23], [25], [26]" (Cao-Li-Zhu 2025, Fan et al. arXiv 2501.04921, Kim 2023, Li-Zhu 2024 twice, Li et al. 2024, Liu-Li-Shi 2025). I did not read those works. They could in principle hold qutrit parameters not yet in the table.
- I could not run a dedicated AG / norm-trace query inside the four-query budget; the Hermitian-hull paper above is the only construction-type hit.

## Verdict
The live table cell has d_lower 7 and the claimed d = 8 is strictly above it. No pull request, TROPHY_CASE.md entry, known-knowns folder or in-window paper I could read gives d >= 8 for (n,k,c) = (16,4,4).
unresolved: the six newer works cited by arXiv 2607.02170 were not read (they could plausibly hold a small-length qutrit EAQECC, though the citing paper lists no [[16,4,*;4]] code); only four arXiv queries were allowed.
novelty: strictly beats the live table value 7 (new d = 8); no competing value found.

pass: true
