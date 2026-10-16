# NOVELTY skeptic: labs-merit-factor-records, L = 464

context: subagent (Claude Code Agent tool, fresh context, model opus)

Claim under test: claim/sequence_L464.txt, length 464, energy E = 14396 (claim/CLAIM.md).
Criterion: E must be STRICTLY below the best published integer energy for L = 464. The best published value is the
minimum over arXiv:2607.09688, arXiv:2504.00987, the Boskovic et al. git_labs repository and any newer arXiv result.

## Object check (own code, written before reading claim/inputs/author_labs_energy.py)
- I wrote my own checker using exact integer arithmetic, E = sum_{k=1}^{L-1} C_k^2. On claim/sequence_L464.txt it
  gives L = 464, **E = 14396** (F = 464^2/(2*14396) = 7.4776). File sha256 01c27fe0...5e63f2c matches CLAIM.md.
- Construction confirmed: the file is exactly "--" + (the Table 3 L = 461 row of arXiv:2607.09688v1, decoded, E = 13574,
  F = 7.8282 as printed) + "+". It is a trivial end extension of a published sequence. The criterion is about the
  value, not the method, so this does not affect the verdict, but it should be stated wherever the claim is published.

## Status source (one request)
- URL: https://arxiv.org/abs/2607.09688. Fetched 2026-10-16 20:16:47 UTC, HTTP 200. The submission history lists
  **only v1** (Wed, 17 Jun 2026 09:17:04 UTC), so there is no newer version. The page sha256 c14c75ea...4420c is identical
  to the claimant's fetch.
- Value: in Table 3 (p. 12 of the v1 PDF, re-fetched 20:16:58 UTC, HTTP 200, sha256 identical to
  claim/inputs/arxiv_2607.09688v1.pdf), the L = 464 row reads "464 7.2617 7.4569" with a 116-digit hex string beginning
  `fffffff0007fd807...` and ending `...aa5552aaaaaa`. I decoded it with the paper's rule (hex to bits, keep the last 464
  bits, 1 -> +1, 0 -> -1) and computed **E = 14436** myself (F = 7.45691, matching the printed 7.4569).

## Every URL checked
| # | URL | UTC time (date -u) | HTTP | L = 464 value found |
|---|---|---|---|---|
| 1 | https://arxiv.org/abs/2607.09688 | 2026-10-16 20:16:47 | 200 | v1 only (status source) |
| 2 | https://arxiv.org/pdf/2607.09688v1 | 2026-10-16 20:16:58 | 200 | Table 3: E = 14436 (F 7.4569), decoded by me; "Previous" F 7.2617 [42, 19] |
| 3 | https://arxiv.org/pdf/2409.07222 (ref [42]) | 2026-10-16 20:17:20 | 200 | Table 2: E = 14824 (F 7.2617), decoded by me; its "[7]" previous F 7.1347 |
| 4 | https://arxiv.org/pdf/2206.12070 (ref [19], Dimitrov 2022) | 2026-10-16 20:17:20 | 200 | Table XI: class B461∘η1∘η1∘η1, E = 15088 (F 7.13468), decoded by me |
| 5 | https://arxiv.org/pdf/2504.00987 | 2026-10-16 20:17:20 | 200 | none (problem sizes up to 120; no 464 in the text) |
| 6 | https://api.github.com/repos/borkob/git_labs | 2026-10-16 20:18:05 | 200 | last push 2020-09-15 |
| 7 | https://api.github.com/repos/borkob/git_labs/git/trees/HEAD?recursive=1 | 2026-10-16 20:18:05 | 200 | no result file for L = 464 |
| 8 | https://raw.githubusercontent.com/borkob/git_labs/master/results-2016/2004-Knauer-original.txt | 2026-10-16 20:20:28 | 200 | none (no "464" anywhere) |
| 9 | https://raw.githubusercontent.com/borkob/git_labs/master/results-2016/2016-labs-skew.txt | 2026-10-16 20:20:28 | 200 | none (odd L only, 5..449) |
| 10 | https://raw.githubusercontent.com/borkob/git_labs/master/results-2018/2018-labs-skew.txt | 2026-10-16 20:20:28 | 200 | none (odd L only, 5..449) |
| 11 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-16 20:18:06 | 200 | 71 open PRs; the only LABS PR is #255 (L = 463 only, see below) |
| 12 | http://export.arxiv.org/api/query?search_query=all:%22low%20autocorrelation%20binary%22&... | 2026-10-16 20:18:07 | 301 | redirected to https (row 14) |
| 13 | http://export.arxiv.org/api/query?search_query=all:%22merit%20factor%22&... | 2026-10-16 20:18:07 | 301 | redirected to https (row 15) |
| 14 | https://export.arxiv.org/api/query?search_query=all:%22low%20autocorrelation%20binary%22&... | 2026-10-16 20:18:17 | 429 | BLOCKED, not retried |
| 15 | https://export.arxiv.org/api/query?search_query=all:%22merit%20factor%22&... | 2026-10-16 20:18:18 | 503 | BLOCKED, not retried |
| 16 | https://arxiv.org/search/?query=%22low+autocorrelation%22&searchtype=all&abstracts=show&order=-announced_date_first&size=50 | 2026-10-16 20:18:59 | 200 | newest results: 2610.14361, 2511.05778, 2511.04553, 2510.24237, 2506.17391 (checked below) |
| 17 | https://arxiv.org/search/?query=%22merit+factor%22&searchtype=all&abstracts=show&order=-announced_date_first&size=50 | 2026-10-16 20:19:16 | 200 | newest after 2607.09688: 2609.05771 (crosscorrelation moments, no record table) |
| 18 | https://arxiv.org/abs/2610.14361 (v2, 14 Oct 2026) | 2026-10-16 20:19:45 | 200 | the abstract covers N = 27..60 |
| 19 | https://arxiv.org/pdf/2610.14361 | 2026-10-16 20:19:45 | 200 | none (no 464) |
| 20 | https://arxiv.org/abs/2511.05778 | 2026-10-16 20:19:46 | 200 | the abstract has no L = 464 value |
| 21 | https://arxiv.org/pdf/2511.05778 | 2026-10-16 20:19:46 | 200 | none (no 464) |
| 22 | https://arxiv.org/abs/2511.04553 | 2026-10-16 20:19:46 | 200 | the abstract covers N = 27..37 |
| 23 | https://arxiv.org/pdf/2511.04553 | 2026-10-16 20:19:46 | 200 | none (no 464) |
| 24 | https://arxiv.org/abs/2506.17391 (v2, 25 Jan 2026) | 2026-10-16 20:19:46 | 200 | the abstract covers N up to 45 |
| 25 | https://arxiv.org/pdf/2506.17391 | 2026-10-16 20:19:47 | 200 | none (no 464) |
| 26 | https://api.github.com/search/repositories?q=low+autocorrelation+binary+sequences&sort=updated&per_page=50 | 2026-10-16 20:18:07 | 200 | none (newest repo pushed 2024-10-23; no L = 464 records repo besides git_labs) |
| 27 | https://api.github.com/search/repositories?q=%22merit+factor%22+binary&sort=updated&per_page=50 | 2026-10-16 20:21:00 | 200 | none |
| 28 | https://arxiv.org/search/?query=binary+sequences+merit+factor+record&searchtype=all&order=-announced_date_first&size=50 | 2026-10-16 20:21:00 | 200 | only 2206.12070 (row 4) |

Repository copy: the read-only TROPHY_CASE.md has **no LABS entry**. Its only "464" is inside "1102464/439" on the
constant-weight-codes line.

## PR #255 (claimant's own)
Draft, opened 2026-10-16 19:30:57 UTC. Title: "[claim] labs-merit-factor-records: L=463 energy 14047, below 14439 in
arXiv:2607.09688v1 Table 3". The body claims L = 463 only. Its "Not claimed" section mentions L = 464 = 14396 as "a
separate cell, not panelled, not claimed here", and the body publishes no L = 464 sequence. It is not prior art for
this claim. My own check of Table 3 L = 463 gives E = 14439, consistent with the PR.

## Findings
- **Best published E for L = 464: 14436** (arXiv:2607.09688v1, Table 3, computed by me from the published hex).
  The other published L = 464 values, in descending order: 14824 (arXiv:2409.07222, ref [42]) and 15088
  (arXiv:2206.12070, ref [19]). None of arXiv:2504.00987, git_labs, or the newer arXiv LABS papers of 2024-2026 that I
  found reports L = 464.
- Comparison of integers: 14396 < 14436 strictly, a margin of 40. This is not a tie.
- Coverage gap: the arXiv API returned 429 and 503 and was not retried. The arXiv web search pages (rows 16, 17, 28)
  returned 200 and covered the same queries. One newer LABS paper, 2610.14361 (v2, 14 Oct 2026), is missing from
  claim/TABLE_RECORD.md. I checked it and it has no L = 464 value, so the result stands. Venues outside arXiv, GitHub
  and the cited references (for example, journal-only tables) were not searched.
- No injection text was found in any fetched page or file (injection_suspected: none).

novelty: the claimed E = 14396 strictly beats every L = 464 value I could find (best published 14436).

pass: true
