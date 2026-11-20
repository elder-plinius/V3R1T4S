context: subagent

# NOVELTY

Role: novelty skeptic for the claim that the 43 distinct binary words in claim/code.txt are a binary length-16 code correcting 3 deletions, and that 43 is strictly larger than every published comparable size for that cell. A tie at 42 is not a record. This file does not check that the words correct 3 deletions.

## Status page, one GET, not retried

URL: https://arxiv.org/html/2504.00613v2
Fetch time: 2026-11-06T08:44:11Z (header date: Fri, 06 Nov 2026 08:44:11 GMT)
HTTP status: 200
User-Agent: V3R1T4S/1.0 (research; one honest GET)
Body length: 765029. No captcha, challenge, or access-denied page. Not retried.

Quoted caption, Table 2: "Code sizes for binary two- and three-deletion-correcting codes. Bold indicates best known, t/o no solution found within 48 h, oom exceeded 1 TB memory limit."

Quoted cell, 3-deletion correction, column n=16, row "MIS solver: OnlineMIS": 42, and that cell is bold (ltx_font_bold). The same column's other construction rows are smaller: ILP lower bound 36, random greedy 32, search heuristics 31, explicit construction 11, ours (search over s=3) 37, ours (search over s in {1,2}) 39. ReduMIS is t/o. ILP upper bound is t/o. LP upper bound is 99, which is not a construction. The number 43 does appear in Table 2, but only as the 2-deletion explicit construction at n=18. That is a different cell.

Abs page, one separate GET, not a retry of the table: https://arxiv.org/abs/2504.00613
Fetch time: 2026-11-06T08:51:07Z
HTTP status: 200
Quoted dateline: "[Submitted on 1 Apr 2025 (v1), last revised 5 Jun 2026 (this version, v2)]". The page's canonical identifier is arXiv:2504.00613v2. No v3.

injection_suspected: none on the table page or the abs page. Footer and feedback links were not followed.

## Literature, last 24 months

arXiv HTML search, one GET: query "binary 3-deletion correcting code", ordered by announced date.
URL: https://arxiv.org/search/?searchtype=all&query=binary+3-deletion+correcting+code&abstracts=show&order=-announced_date_first&size=25
Fetch time: 2026-11-06T08:50:18Z
HTTP status: 200
Quoted: "Showing 1-13 of 13 results". The hits inside the window are asymptotic redundancy or capacity papers, an ell-symbol-read channel, a ternary sequence-reconstruction paper, and a one-deletion-plus-substitution reconstruction paper. None states a binary unrestricted length-16 3-deletion code of size 43 or more. Older hits on that page are the same kind of asymptotic or different-channel papers.

Other one-shot searches, not retries of a blocked page:

- Weindel and Heckel, the table above, remains the finite-length comparison. Their own constructions at this cell are 37 and 39. The code repository named in that paper has no releases. Its recorded best-known map, fetched once at 2026-11-06T08:49:33Z, HTTP 200, stores (16, 3): 42 and no larger value.
- Pandav and Bhat, arXiv:2602.08952 (9 Feb 2026), construct binary d-deletion codes only for lengths 8 through 14. No length-16 code.
- Multiset deletion codes (arXiv:2601.05636) are a different metric. The binary multiset optimum is ceil((n+1)/(t+1)), which is 5 at n=16, t=3, not a subsequence-deletion code.
- Recent asymptotic papers (arXiv:2609.21395, arXiv:2609.19493, arXiv:2610.15631, arXiv:2611.04023) improve redundancy or rate bounds for large n. They do not print a length-16 3-deletion codebook of size 43 or more. An explicit 3-deletion code with redundancy on the order of 5 log n has size far below 43 at length 16.
- Hamming-distance tables, variable-length insertion-deletion tables, burst-deletion codes, and ell-read codes are different objects. They were not counted as comparable.

No opened page stated a binary unrestricted (16, 3) deletion code of size 43 or more.

## Pinned repository

TROPHY_CASE.md: no deletion-code row and no 2504.00613 row.
known-knowns/: no package for this target.
Pull requests, open and closed: one hit for this target, number 697, closed and not merged. It is a bank proposal, not a codebook. No open or closed claim pull request contains a binary (16, 3) deletion code. Unmerged pull-request values would not set the bar in any case.

## Composition

claim/CLAIM.md says this is not a composition of a published codebook, and that Table 2 does not print the words of its size-42 code. No published list of those words was found. Neighbouring published sizes, (15, 3)=30, (16, 2)=215 and (17, 3)=60, are different cells. They do not themselves supply a published length-16 3-deletion code of size 43. An unpublished local hint, if one exists, is not a published size and does not raise the bar.

## Verdict

The best published comparable construction size I can read for binary 3-deletion codes of length 16 is 42, the bold OnlineMIS entry in Table 2. Every other construction row in that cell is smaller. 43 is strictly larger than 42. A tie at 42 would fail. No published size of 43 or more was found in the table, the last 24 months of literature read here, the paper's recorded best-known map, the trophy case, known-knowns, or pull requests.

pass: true
