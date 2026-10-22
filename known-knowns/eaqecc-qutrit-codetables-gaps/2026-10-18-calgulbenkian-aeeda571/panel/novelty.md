# Novelty report: qutrit-33-3-23-24

context: Claude Code subagent, fresh context

Claim: [[33,3,23;24]]_3, table cell [[33,3,22-30;24]]_3.

## Primary table (fetched once)
- URL: https://eaqecc.codetables.de/qutrit.php, fetched 2026-10-18T14:23:13Z, HTTP 200, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c (628039 bytes). The page footer reads "Last change: 10.07.2025". This sha256 equals the one recorded in the open pull requests 331 and 363 for their earlier fetches, so the table did not change in the last two days.
- Value read for the cell: "[[33,3,22-30;24]]" with title "subcode of [[33,5,22;24]] quantum shortening of [[34,4,23;24]] from arXiv:2207.05647". So d_lower = 22, d_upper = 30. The claimed d = 23 is strictly above 22 and not above 30.
- Related cells on the page: [[33,3,21-30;21]], [[33,3,19-30;18]], [[33,3,20-30;19]]. The lower bound 22 at c = 24 comes from shortening the table code [[34,4,23;24]]. This is context, not a competing value for (33,3,24).

## Repository sources (fetched once)
- TROPHY_CASE.md: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, 2026-10-18T14:23:15Z, HTTP 200, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1. It lists no entry for this target family (no EAQECC row).
- Pull requests, pages 1 to 5: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1 to 5, 2026-10-18T14:23:15Z to 14:23:21Z, HTTP 200 each; page sha256 values cca876cd..., 176c41b2..., 20ec05c4..., f5d26a78..., and page 5 is an empty list (2ba33ca0...). 392 pull requests read by title.
- known-knowns folder listing: https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns, 2026-10-18T14:23:22Z, HTTP 200, sha256 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011. Twenty folders; none belongs to this target.

## Pull requests on the same target (all by others, all open)
- Pull request 363 (psmoros, 2026-10-17): [[33,1,31;24]]_3, cell (33,1,24). Different k, so a different cell.
- Pull request 331 (anzal1, 2026-10-17): [[14,3,8;5]]_3, cell (14,3,5). Different cell.
- No pull request in the five pages names the cell (33,3,24). The author's claim record (not shipped) says "a new filing, not a refile", and I found no earlier filing by the author for this cell.
- Pull request 363 is at n = 33, c = 24 but with k = 1, which is a different cell from (33,3,24).

## Literature (arXiv export API; the first attempt over http returned a 301, so each of the four queries was sent once over https)
- Query: entanglement-assisted AND qutrit, sorted by date, 2026-10-18T14:26:09Z, HTTP 200, sha256 81a4a683d2436e52c89d5302fcbbdc36b86c0ad38e301c6c124f5f3a31ec21d1. Nine hits; the only in-window paper on qutrit EAQECC tables is arXiv 2607.02170 (Generalized Extended Codes with Applications in Entanglement-Assisted Qubit and Qutrit Codes, 2 July 2026). Its abstract says "14 new EA qutrit codes of lengths n <= 25 compared to the best-known codes in Grassl's code tables". I fetched its PDF once (https://arxiv.org/pdf/2607.02170v1, 2026-10-18T14:26:36Z, HTTP 200, sha256 f1b7794181262beaee2fc4fc8fd4a1085960a8b87a7da038159dc1911961dbef) and read its qutrit tables: the codes listed are [[7,1,7;6]], [[8,0,8;6]], [[8,1,8;7]], [[13,3,7;4]], [[17,2,15;15]], [[18,2,16;16]], [[19,2,17;17]], [[19,3,15;16]], [[21..24,2,*]], [[25,2,22;23]], [[25,3,20;22]], [[7,2,5;3]], [[9,0,9;7]], [[15,2,13;13]], [[16,2,14;14]]. None is [[33,3,*;24]].
- The same paper says it compares with "the latest records in [6], [10], [19], [22], [23], [25], [26]" (Cao-Li-Zhu 2025, Fan et al. arXiv 2501.04921, Kim 2023, Li-Zhu 2024 twice, Li et al. 2024, Liu-Li-Shi 2025). I did not read those works. They could in principle hold qutrit parameters not yet in the table.
- I could not run a dedicated AG / norm-trace query inside the four-query budget; the Hermitian-hull paper above is the only construction-type hit.

## Verdict
The claimed d = 23 beats d_lower = 22 by one, the smallest possible margin. Nothing found gives d >= 23 for (33,3,24).
unresolved: the cited newer works were not read for n = 33; only four arXiv queries were allowed.
novelty: strictly beats the live table value 22 (new d = 23); no competing value found.

pass: true
