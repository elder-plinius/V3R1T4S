# Novelty skeptic verdict: labs-merit-factor-records, L = 463, E = 14047
context: subagent (Claude Code Agent tool, fresh context, model opus)

Scope: only claim/ was read (CLAIM.md, TABLE_RECORD.md, sequence_L463.txt, inputs/arxiv_2607.09688v1.pdf). Scratch in claim/../mywork/.
All fetches: one plain curl per URL, User-Agent "V3R1T4S/1 novelty check (curl)", no retries. Times are UTC (date -u), status from curl -w '%{http_code}'.

## Status source
- https://arxiv.org/abs/2607.09688 , 2026-10-16T17:50:00Z, HTTP 200. Latest version: v1 only ("Submitted on 17 Jun 2026"); no v2. sha256 c14c75ea...4420c (same bytes as claim/inputs/arxiv_2607.09688_abs.html).

## Sources checked for the best published E at L = 463
| URL | time (UTC) | HTTP | value found at L = 463 |
|---|---|---|---|
| https://arxiv.org/pdf/2607.09688v1 | 2026-10-16T17:50:07Z | 200 | Table 3 (p. 12): Previous F [42,19] = 7.3885, Our F = 7.4233. I decoded the printed hex sequence myself: 463 bits, E = 14439 (F = 7.4233, E ≡ 3 mod 4). Same sha256 (53941410...b31) as claim/inputs/arxiv_2607.09688v1.pdf |
| https://arxiv.org/pdf/2409.07222 (ref [42], Dual-step, v1 only) | 2026-10-16T17:52:08Z | 200 | Row 463: old F 7.2525, new F 7.3885. Decoding the printed hex to length 463 gives E = 14507 (F = 7.38847). This matches the "Previous F" in 2607.09688 |
| https://arxiv.org/pdf/2206.12070 (ref [19], Dimitrov) | 2026-10-16T17:52:09Z | 200 | Table row 463 (class B461∘η1∘η1), F = 7.25248663644. Decoded E = 14779 |
| https://arxiv.org/abs/2504.00987 | 2026-10-16T17:50:41Z | 200 | Abstract says sizes "up to 120" (v1, v2) |
| https://arxiv.org/pdf/2504.00987 | 2026-10-16T17:52:09Z | 200 | Largest length in the tables is 120. No L = 463 |
| https://api.github.com/repos/borkob/git_labs | 2026-10-16T17:50:42Z | 200 | Last push 2020-09-15 |
| https://api.github.com/repos/borkob/git_labs/git/trees/HEAD?recursive=1 | 2026-10-16T17:50:42Z | 200 | 146 entries, not truncated. The only result tables are results-2016/*, results-2018/* |
| https://raw.githubusercontent.com/borkob/git_labs/master/README.md | 2026-10-16T17:50:55Z | 200 | No L = 463 |
| https://raw.githubusercontent.com/borkob/git_labs/master/results-2018/2018-labs-skew.txt | 2026-10-16T17:50:56Z | 200 | Skew table goes up to L = 449. No L = 463 |
| https://raw.githubusercontent.com/borkob/git_labs/master/results-2016/2016-labs-skew.txt | 2026-10-16T17:50:56Z | 200 | Goes up to L = 449. No L = 463 |
| https://raw.githubusercontent.com/borkob/git_labs/master/results-2016/2004-Knauer-original.txt | 2026-10-16T17:50:56Z | 200 | Goes up to L = 222. No L = 463 |
| https://export.arxiv.org/api/query?... (LABS / merit factor search; the http:// form returned 301 at 17:51:24Z) | 2026-10-16T17:51:30Z | 429 | PENDING, not retried, not counted as checked |
| https://arxiv.org/search/?query=low+autocorrelation+binary+sequences&searchtype=all&order=-announced_date_first&size=100 | 2026-10-16T17:51:48Z | 200 | Newer than 2607.09688: 2610.14361 (Oct 2026) only |
| https://arxiv.org/search/?query=%22merit+factor%22&searchtype=all&order=-announced_date_first&size=100 | 2026-10-16T17:51:51Z | 200 | Newer: 2609.05771 (crosscorrelation demerit moments, theory, no tables) |
| https://arxiv.org/abs/2610.14361 and /pdf/2610.14361 | 2026-10-16T17:52:01Z / 17:52:08Z | 200 / 200 | Small-subsystem heuristic, N in [27, 60] (66 max). No L = 463 |
| https://arxiv.org/abs/2511.05778 and /pdf/2511.05778 | 2026-10-16T17:52:01Z / 17:52:08Z | 200 / 200 | TOPSIS-like metaheuristic, size 50 only. No L = 463 |
| https://arxiv.org/abs/2511.04553 | 2026-10-16T17:52:01Z | 200 | QE-MTS, N in [27, 37]. No L = 463 |
| https://arxiv.org/abs/2409.07222 | 2026-10-16T17:52:02Z | 200 | v1 only (11 Sep 2024) |
| WebSearch "low autocorrelation binary sequences new best merit factor long lengths 2026" | ~2026-10-16T17:52Z | n/a | No newer long-length records. Only older LABS work and a Preprints.org PSL paper (not merit-factor records) |
| https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-16T17:50:43Z | 200 | 100 lines. No LABS / merit factor / 463 entry |
| https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-16T17:50:43Z | 200 | 53 open PRs. Titles and bodies have no LABS / merit factor / 463 match |

Dimitrov's skew-symmetric / merit-factor line (2011.00068, 2106.03377) appears in the arXiv search. Both papers are older than 24 months, and 2206.12070 (ref [19], checked above) supersedes them for L = 463.

## Best published energy for L = 463
min(14439 [2607.09688v1 Table 3], 14507 [2409.07222], 14779 [2206.12070]) = **E = 14439** (F = 7.4233), from arXiv:2607.09688v1.
I found no L = 463 value in arXiv:2504.00987, borkob/git_labs, newer arXiv papers, TROPHY_CASE.md or the open PRs.

## Claim
- Independent energy check of claim/sequence_L463.txt (sha256 24118ce2...4707): length 463, E = 14047, F = 463^2/(2*14047) = 7.6304. My own code; I did not open the author's checker.
- 14047 < 14439, a margin of 392. This is strict, not a tie.
- One search source (the arXiv API) is PENDING (429). The arXiv HTML search that covers the same ground returned 200.

novelty: CONFIRMED (strictly beats every verified published value for L = 463)
pass: true
