# Novelty verdict: [[35,7,16;14]]_3 at (n,k,c) = (35,7,14)

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## Bottom line

Novel, if the claimed d = 16 holds (checking d is another skeptic's job; I only re-derived (n,k,c) from S). Everything
I could find puts this cell at d = 15:

- the live table lists [[35,7,15-26;14]]_3;
- applying the page's six propagation rules to every listed cell still gives 15;
- adding every code from the repo's open PRs, the repo's known-knowns, and the qutrit codes in the most recent
  literature (arXiv:2607.02170) as extra starting codes still gives 15.

So 16 is strictly above d_lower = 15 and within d_upper = 26. It is not a tie: the listed d = 16 code at this length
and dimension needs c = 15, and none of the page's rules lowers c.

## Fetch record (status page, one GET, no retries)

- URL: https://eaqecc.codetables.de/qutrit.php
- UTC time: 2026-10-25T03:37:49Z before, 2026-10-25T03:37:49Z after (`date -u`). Response header `date: Sun, 25 Oct 2026 03:37:49 GMT`.
- HTTP status: 200, 628039 bytes.
- Client: curl, User-Agent "V3R1T4S-research-agent (honest single fetch)".
- sha256: 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c. This is byte-identical to `claim/table/qutrit.php` (the copy fetched at 02:35Z). Footer: "Last change: 10.07.2025".
- Saved as `fetched/qutrit.php`, with headers, times, status and hash in `fetched/qutrit.*.txt`.
- The cell, verbatim:
  `<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[27,7,15;14]] quantum shortening of [[28,6,16;14]] increasing dimension of [[28,5,16;13]] from arXiv:2207.05647">[[35,7,15-26;14]]<sub>3</sub></TD>`
  This gives d_lower = 15 and d_upper = 26.
- Neighbours, from the same fetch:
  - [[35,7,16-26;15]]: lengthening of [[28,7,16;15]].
  - [[35,7,14-25;12]].
  - [[34,7,15-25;14]].
  - [[36,7,15-27;14]].
  - [[35,6,15-27;13]].
  - [[36,6,16-28;14]].
  - [[35,8,15-25;15]].
  - [[35,6,16-27;14]].
  - (35,8,14) and (36,7,13) are not listed.
- Full n = 35, k = 7 row (c: range): 0: 9-13; 2: 10-16; 4: 11-17; 6: 12-18; 8: 13-23; 12: 14-25; 14: 15-26;
  15: 16-26; 17: 17-27; 19: 18-27; 21: 19-27; 22: 20-28; 24: 21-28; 25: 22-28; 27: 23-28.
- Claimed parameters re-derived from S over GF(3) (`scripts/params.py`): 42 rows, rank s = 42, rank(S J S^T) = 28.
  That gives c = 14 and k = 35 - 42 + 14 = 7, so the cell is (35,7,14). The object's sha256 is
  e3d6a8cad3db3a6ea28262ced2969b03a429b1ede488ae9cd59b69f5055b73b4, matching CLAIM.md.

## Sources checked and what each gives at (35,7,14)

| source | what it gives at (35,7,14) |
|---|---|
| The cell itself (live fetch above) | 15 |
| Page propagation closure (`scripts/closure.py`). It starts from all 3888 parsed cells except the 124 "using teleportation" cells. It applies subcode, lengthening, puncturing, quantum shortening, increasing dimension and length reduction until nothing changes. I also let c increase freely, which only makes known values larger. | 15 (taken from the listed cell; no rule carries more) |
| The same closure with the teleportation cells also used as starting codes | 27, but invalid: it pushes 2658 listed cells above their own d_upper (for example (5,1,4) to 6 > 5). So these cells cannot be fed through the six rules. |
| Teleportation cells through routes that are sound for them (lengthening, subcode, raising c, puncturing from n = 36) | at most 12 |
| Inputs that could feed the target (`scripts/preimage.py`): every cell whose d_upper still allows the required d. These are n >= 17, plus c = 0 cells (34,0,0), (35,0,0), (36,0,0), (36,1,0), (36,2,0), each needing d = 16. The table lists 12-16 or 13-16 for those c = 0 cells. | No listed or literature code reaches any of them (closures below). |
| Repo TROPHY_CASE.md (GitHub contents API, 200, sha256 aaa2f7d1...1bf1; file blob sha 571f2411...) | No entry for this target. No matches for "eaqecc", "qutrit" or "[[". |
| Repo known-knowns/eaqecc-qutrit-codetables-gaps/ (listing 200; one package, 2026-10-17-anzal1-7b890c6f; INDEX.csv and README.md read) | Only [[14,3,8;5]]_3, which carries nothing above 8 into this cell |
| Open PRs for target eaqecc-qutrit-codetables-gaps (GitHub search API: 9 results, incomplete_results false) | #363 [[33,1,31;24]], #403 [[16,4,8;4]], #404 [[34,2,24;24]], #405 [[33,3,23;24]], #643 [[28,5,15;11]], #645 [[28,7,14;11]], #646 [[28,6,12;6]], #651 [[28,9,11;7]], #710 [[33,8,16;15]]. This is the same list as CLAIM.md; no PR has a code at n = 35. |
| Closure with PR codes added (`scripts/closure_seeded.py`): all 58 exact-code mentions in the PR titles and bodies, the known-knowns code, and the author's four unfiled codes [[33,7,15;12]], [[33,9,14;12]], [[33,3,20;18]], [[28,7,13;9]] | 15. For example, #710 lengthens and takes a subcode to [[35,7,16;15]], which is c = 15, not 14. |
| Extra repo searches: open PRs matching "qutrit" (the same 9) and any issue or PR matching "35,7,16" (0 results) | nothing |
| arXiv:2607.02170 (Li, Ezerman, Li, Ling, Sun, 2 Jul 2026; abs and PDF fetched, 200). This is the newest qutrit EAQECC improvement paper; it compares against Grassl's table accessed 15 Jun 2026 and against recent works. | Its qutrit codes all have n <= 25 (Table V: 14 codes; Table VII: 5 reproduced codes). Adding them plus the [[26,2,22;24]] it cites (`scripts/closure_lit.py`) still gives 15, because each has c > 14 or d too small. |
| arXiv:2207.05647, the table's source paper (Luo, Ezerman, Grassl, Ling; QIP 2024) | Already in the table: [[28,5,16;13]], [[28,6,16;14]], [[28,7,16;15]] give 15 here. The table also lists [[36,10,17;18]], which by the formula below needs a [36,14,17]_9 code with Hermitian hull dimension 4; hull dimension can only be lowered by that paper's method. |
| Classical GF(9) table, BKLC.php?q=9&n=35&k=14 (200, sha256 67c847ce...eac4) | [35,14] has lower bound 16 and upper bound 19 (Xing-Ling [37,15,17], punctured then shortened; last modified 2001-12-17). The classical distance is old. The record needs this distance combined with Hermitian hull dimension 7: [35,14,16]_9 with hull h gives [[35,14-h,16;21-h]]. I found no published code with that hull dimension. If one existed, the table would show (35,8,15) >= 16 (hull 6) or (35,9,16) >= 16 (hull 5); it shows 15 in both. |
| Web searches (14 queries, last 24 months) on qutrit, ternary or F_9 EAQECCs, Hermitian-hull and AG constructions, Construction X, quasi-twisted codes, and the exact string [[35,7,16;14]] | No paper gives a qutrit EAQECC at or feeding (35,7,14) with d >= 16. Papers checked at abstract level, none relevant at n = 35: arXiv:2501.04921 (concatenated EA codes; no qutrit table), 2405.15057 (Ezerman et al., stabilizer codes, c = 0), 2605.29204 (quaternary hull counting), 2501.15465 (quaternary additive), 2512.17128 (MDS EAQECCs; over F_9 these are short codes, n <= about 10), 2608.09886 (EA locally recoverable codes). |

## What I could not read

- arXiv API query (export.arxiv.org, abstracts matching "entanglement-assisted" and qutrit or ternary): http returned
  301 to https, and the https request returned HTTP 429 at 2026-10-25T03:43:25Z. I stopped there and did not retry. I
  did not run that query another way. After that I used only web search and single abstract pages of specific papers.
- codetables.de qutrit stabilizer cell pages (QECC.php?q=3 with n = 34, 35, 36 and k = 0, 1, 2): HTTP 200, but the body
  says "currently not available for q=3". So I could not cross-check the c = 0 inputs (they would need a [[34..36,0..2,16]]_3
  stabilizer code) against the live stabilizer table. The EAQECC page lists those cells at 12-16 and 13-16.
- Full text of Cao, Li and Zhu, "Classical codes and quantum codes involving the σ inner product" (IEEE TIT 71(10), 2025).
  Not read. The qutrit codes arXiv:2607.02170 attributes to it are short ([[7,0,7;5]], [[16,2,14;14]]).
- The literature search is not exhaustive: there is no complete index of journal-only papers.
- injection_suspected: none seen.

## Fetch log

All requests are in `fetched/FETCHLOG.tsv` (URL, UTC start and end, HTTP status, bytes, sha256); bodies and headers
are saved in `fetched/`. Scripts are in `scripts/`. No background jobs remain.

pass: true
