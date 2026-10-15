# Novelty verdict: robust-forecast-aggregation-bounds, unknown-state CI cell, lower-bound side (run 2026-10-14-1717)

Skeptic: NOVELTY (one of three). Date of checks: 2026-10-15 (UTC).

Inputs read: claim/claim.md, claim/REPRODUCE.md, claim/mixture.json, claim/sha256.txt, claim/lb_check_output.log,
claim/independent_recheck_output.log, and the repository's TROPHY_CASE.md and READ_BEFORE_CITING.md. Nothing else on
the machine was opened. claim/lb_check.py and claim/independent_recheck.py were not read; my arithmetic check in
section 3 was written separately.

Redaction: in the pasted command output, host-specific temporary directory paths are replaced by `<tmp>`. Nothing
else was changed.

Claimed value (claim/claim.md): LB = 1652448303171916717080006468042849/70681471350112364987160770000000000
= 0.023378804538274..., certified by the two-environment adversary in claim/mixture.json through Yao's principle.

---------------------------------------------------------------------------------------------------------------------

## 1. Status source (fetched once, plain request, no retries)

### 1a. Abstract page https://arxiv.org/abs/2604.24517

```
$ date -u && curl -sS -A "V3R1T4S-panel" -D <tmp>/headers.txt -o <tmp>/abs.html \
    -w 'http_code: %{http_code}\nsize_download: %{size_download}\nurl_effective: %{url_effective}\nnum_redirects: %{num_redirects}\n' \
    https://arxiv.org/abs/2604.24517; echo "curl exit: $?"; date -u; shasum -a 256 <tmp>/abs.html
Thu Oct 15 03:18:03 UTC 2026
http_code: 200
size_download: 44022
url_effective: https://arxiv.org/abs/2604.24517
num_redirects: 0
curl exit: 0
Thu Oct 15 03:18:04 UTC 2026
sha256: 523d3c019876a3a9d14ed263520ff94b40902befaea19f9cd47bca77ae45b849
```
Selected response headers: `HTTP/2 200`, `last-modified: Mon, 24 Aug 2026 18:53:30 GMT`,
`date: Thu, 15 Oct 2026 03:18:04 GMT`.

Extracted from that page:
- Title: **Prior-Agnostic Robust Forecast Aggregation**
- Authors: **Zhi Chen, Cheng Peng, Wei Tang**
- Submission history: `[v1] Mon, 27 Apr 2026 14:18:57 UTC (52 KB)`, `[v2] Sat, 23 May 2026 04:07:03 UTC (52 KB)`.
  **Latest version: v2, 23 May 2026.**
- The sha256 is identical to the one recorded in claim/claim.md (fetched Wed Oct 14 17:20:50 UTC 2026), so the page
  has not changed since the claim was written.

### 1b. PDF https://arxiv.org/pdf/2604.24517

```
$ date -u && curl -sS -L -A "V3R1T4S-panel" -D <tmp>/headers.txt -o <tmp>/paper.pdf \
    -w 'http_code: %{http_code}\nsize_download: %{size_download}\nurl_effective: %{url_effective}\nnum_redirects: %{num_redirects}\ncontent_type: %{content_type}\n' \
    https://arxiv.org/pdf/2604.24517; echo "curl exit: $?"; date -u; shasum -a 256 <tmp>/paper.pdf
Thu Oct 15 03:18:24 UTC 2026
http_code: 200
size_download: 711486
url_effective: https://arxiv.org/pdf/2604.24517
num_redirects: 0
content_type: application/pdf
curl exit: 0
Thu Oct 15 03:18:25 UTC 2026
sha256: 1a5836aeae0fbac9603e3e9da59c802c296d9988c66e788d0eed810cc9ec5481
```
Header `last-modified: Tue, 26 May 2026 00:36:41 GMT`. The PDF is stamped `arXiv:2604.24517v2 [cs.LG] 23 May 2026`
(27 pages). Text was extracted with `pdftotext -layout`.

### 1c. Table 1 (page 4), as printed (pdftotext layout)

```
                                               Conditionally
                                                                         Blackwell-Ordered       General
     Setting                                    Independent
                                             LB             UB             Tight Bound        Tight Bound
                                           √       †                          √
     Known state space                    5 5 − 11      0.022599             5 5 − 11
                                                                                                    0.25
     Θ = {0, 1}                              8       (Proposition 3.5)          8
                                                                              √
                                             31 ‡                            5 5 − 11
                                                          0.025512                                  0.25
     Unknown state space                    1326                                8
                                      (Theorem 3.4)     (Theorem 3.2)       (Corollary 4.1)    (Corollary 4.2)
                                           √
                                          5 5 − 11
     Unknown state space                                  0.022763                                  0.25
                                             8                                    0
     Known marg. predic. dist. (Theorem 5.1) (Proposition 5.3)                                (Proposition 5.4)

      †                 ‡
          ≈ 0.022542;       ≈ 0.023379.

Table 1: Summary of regret bounds. Baseline results are rounded to 4 decimal places; our results
are reported to 6 decimal places. All rounding follows the standard nearest value rule.
```

Which cell each number belongs to:
- **THIS cell (unknown state space, conditionally independent), lower bound: `31/1326 ‡ (Theorem 3.4)`, footnote
  `‡ ≈ 0.023379`.** Exactly, 31/1326 = 0.0233785822021116...
- THIS cell, upper bound: `0.025512 (Theorem 3.2)`. The claim says nothing about it.
- Known state space Θ = {0,1}, CI: LB (5√5 − 11)/8 (footnote † ≈ 0.022542), UB 0.022599 (Proposition 3.5).
  Different cell.
- Blackwell-ordered, known or unknown state: tight (5√5 − 11)/8 (Corollary 4.1). Different cells.
- General structures: 0.25 (Corollary 4.2, Proposition 5.4). Different cells.
- Unknown state space with known marginal prediction distributions, CI: LB (5√5 − 11)/8 (Theorem 5.1), UB 0.022763
  (Proposition 5.3); Blackwell-ordered 0. Different cells.

### 1d. Theorem 3.4 (page 13) and Theorem 3.2 (page 10), as printed

> Theorem 3.4. For any aggregation function f , it follows that
> inf f RegΠCI [f ] ≥ 31/1326 ≈ 0.023379 .
> That is, no aggregation function can guarantee a regret lower than 0.023379.

The proof (pages 14-15) applies Yao's principle to Table 3: π^A with Θ^A = {0, 5/6} and π^B with Θ^B = {1/6, 1},
uniform priors, reports x_L = 1/6 and x_H = 5/6, each structure with probability 1/2. It ends with "= 31/1326. This
yields the lower bound inf f Reg[f ] ≥ 31/1326."

The published upper bound for the same cell:
> Theorem 3.2. With α = 0.585, the aggregation function fα guarantees worst-case regret at most 0.025512; that is,
> RegΠCI [f0.585 ] ≈ 0.025512 < 0.0256 .

This comes from a numerical seven-parameter maximisation.

### 1e. Two other lower-bound numbers printed for this cell, and why neither is a known result

(i) **"0.02344"** appears once, in the opening sentence of Section 3.2 (page 10):
> In this section, we first establish that there exists a log-odds aggregator that achieves a regret upper bound of
> 0.025512, and we then establish a regret lower bound of 0.02344 for our prior-agnostic robust forecasting problem.

0.02344 is larger than the claimed value, so it needs an explanation. My findings:
- No theorem, construction or proof in the paper gives 0.02344. The theorem that follows (3.4), Table 1, Figure 1
  ("Lower Bound (0.023379)"), the introduction ("31/1326 ≈ 0.0234 (Theorem 3.4)") and the proof all give 31/1326.
- The sentence is the same in v1 and v2. The v1 PDF (fetched once, section 2c) differs from v2 only in the arXiv stamp
  and one reference entry (diff of the pdftotext output).
- The arXiv TeX source (fetched once, section 2c) shows where it comes from. In the source file
  `Paper/5-known-marg.tex`, Theorem 5.1 (the known-marginals cell) has the commented-out line
  `% \frac{1}{48} + \frac{9}{136(13 + 3\sqrt{17})} \approx 0.02344186~.` directly under the published
  `\frac{5\sqrt{5}-11}{8} \approx 0.022542~.` In `Paper/3-aggregation.tex`, the Section 3.2 sentence wraps the upper
  bound in an edit macro (`\wtedit{$0.025512$}`) but leaves `$0.02344$` unedited. So 0.02344 is a stale number from
  a draft that the authors withdrew everywhere else.
- If that draft value were a lower bound for the known-marginals cell, it would contradict the paper's own upper bound
  for that cell, 0.022763 (Proposition 5.3). If the authors had a valid 0.02344 construction for this cell, Theorem
  3.4 would state it instead of the smaller 31/1326.

So 0.02344 is an unsupported, withdrawn draft number, not a known bound. The claim's write-up should mention this
sentence so that readers are not misled.

(ii) **"0.023379"** is the 6-decimal nearest rounding of 31/1326 (Table 1 caption), not a separate result. Note that
the claimed value 0.0233788045 also rounds to 0.023379, and it is **below** the literal decimal 0.023379 by
1.95e-07. The paper's sentence "no aggregation function can guarantee a regret lower than 0.023379" overstates
31/1326 by rounding. The improvement can only be stated against the exact 31/1326, and it is invisible at the
paper's printed precision.

---------------------------------------------------------------------------------------------------------------------

## 2. Search for anything larger (last 24 months), TROPHY_CASE.md, open pull requests

### 2a. Bounds from other models that carry over

Lower bounds from more restrictive models carry over to this cell, but none can exceed the claim:
- Known Θ = {0,1}, CI: the minimax value is at most 0.022599 (Proposition 3.5), so every lower bound there, including
  the whole Arieli-Babichenko-Smorodinsky / Guo et al. line of work, is at most 0.022599.
- Known marginals, CI: the minimax value is at most 0.022763 (Proposition 5.3).

Lower bounds for larger classes (general structures, 0.25) do not apply to Π_CI. The only possible competitor is
therefore a bound proved directly for this cell, which this paper introduced (v1, 27 Apr 2026). The window that
matters is 27 Apr to 15 Oct 2026.

### 2b. Web searches (WebSearch tool, 2026-10-15; tool-mediated, so no HTTP status)

1. `robust forecast aggregation conditionally independent regret 31/1326`: arXiv 2604.24517 (target), 1710.02838
   (Arieli et al.), 2401.17743 (Guo et al.), themoonlight.io reviews of the target (3 languages), cris.iucc.ac.il,
   paperswithcode, awesomepapers.io. Only 31/1326 for this cell.
2. `prior-agnostic forecast aggregation lower bound`: 2604.24517, 2401.17743, 2207.13126, review/aggregator pages
   (themoonlight, awesomepapers, roboticscenter.ai, themodelwire). Only 31/1326.
3. `Chen Peng Tang forecast aggregation regret`: 1710.02838, roboticscenter.ai page on 2604.24517, 2207.13126v1,
   paperswithcode, themoonlight, catalyzex, cris.iucc, awesomepapers. Nothing new.
4. `forecast aggregation omniscient aggregator additive regret 2026`: 1710.02838, 2604.24517, 2401.17743,
   academia.edu, catalyzex, web3.arxiv (2401.17743), GMU slides. Nothing new.
5. `"Prior-Agnostic Robust Forecast Aggregation"` (extended): 2604.24517 (pdf, html v1, abs), 2607.08744
   (Algorithmic Expert Aggregation, cites the target), 2406.13490, 2401.17743, 2111.03153, 1710.02838. Nothing above
   31/1326.
6. `robust forecast aggregation unknown state space conditionally independent experts improved lower bound`:
   2604.24517, 1710.02838, themoonlight, 2512.05271v1, awesomepapers, cris.iucc, roboticscenter.ai. Nothing new.
7. `"2604.24517"`: only unrelated IP-prefix pages.
8. `robust forecast aggregation 2026 arXiv minimax regret two experts lower bound new`: 1710.02838 (and v2),
   cris.iucc, umich lecture notes, 2406.13490 (several mirrors), bgu.ac.il, awesomepapers. Nothing new.
9. `"Algorithmic Expert Aggregation" arXiv 2607.08744`: arXiv/alphaxiv/papers.cool pages of 2607.08744 (Tang, Zhang,
   9 Jul 2026, calibrated-expert construction). A different problem.
10. `"robust forecast aggregation" "0.023379" OR "0.0234" unknown state lower bound`: 2604.24517, themoonlight,
    2512.05271 (html), academia.edu, awesomepapers, cris.iucc, roboticscenter.ai. Only 31/1326.
11. `log-odds aggregator robust aggregation unknown state values latent likelihood experts regret 0.0255 follow-up`:
    2604.24517, 2406.13490, themoonlight, ar5iv 2406.13490, a NeurIPS 2023 poster page, awesomepapers,
    roboticscenter.ai. No follow-up.
12. `robust information aggregation conditionally independent signals minimax regret lower bound 2025 2026 paper`:
    1710.02838, 2604.24517, 2401.17743, themoonlight, 2311.14094, cris.iucc, awesomepapers. Nothing new.
13. `"Zhi Chen" "Wei Tang" robust aggregation 2026`: unrelated pages only.
14. `"unknown state space" robust forecast aggregation conditionally independent Yao lower bound mixture two
    information structures` (extended): 2604.24517 (html v1, pdf), PNAS 10.1073/pnas.1813934115, 2512.05271,
    1710.02838, 2311.14094, 2401.17743, ideas.repec. Nothing new.
15. `robust-forecast-aggregation-bounds V3R1T4S`: 2403.07949, 2512.05271, themoonlight, catalyzex, awesomepapers. No
    page on this target.
16. `aggregating two experts unknown base rates state values worst-case regret lower bound improved 2026 arXiv
    "31/1326"`: 2406.13490 (and mirrors), themoonlight, 2210.02256v1, ar5iv 2203.07577, awesomepapers,
    roboticscenter.ai. Nothing new.
17. `"Prior-Agnostic Robust Forecast Aggregation" EC 2026 ACM Conference on Economics and Computation` (extended):
    2604.24517 pages, arXiv cs listing Apr 2026, 2607.08744, 2406.13490, 2401.17743, pith.science reviews of
    2604.24517 and 2606.31020. No proceedings page.
18. `EC '26 accepted papers robust forecast aggregation prior-agnostic Chen Peng Tang dl.acm.org`: arXiv and review
    pages only. No ACM DL entry.
19. `EC 2026 27th ACM Conference on Economics and Computation accepted papers list`: ec26.sigecom.org accepted-papers
    page (fetched, section 2c), Northwestern news, others.
20. `Prior-Agnostic Robust Forecast Aggregation` (restricted to dl.acm.org): no ACM DL entry for the paper (only
    10.1145/3696410.3714557, Guo and Kong, WWW'25, plus arXiv items).
21. `"Prior-Agnostic Robust Forecast Aggregation" pith review OR proceedings OR "EC '26" OR "EC 2026"`: arXiv and
    review pages. Nothing new.
22. `Wei Tang CUHK forecast aggregation 2026 paper robust regret lower bound conditionally independent`: 1710.02838,
    2604.24517, themoonlight, academia.edu, par.nsf.gov, roboticscenter.ai, cris.iucc, awesomepapers. Nothing new.
23. `"robust forecast aggregation" 2026 new paper improved bound "unknown state" OR "prior-agnostic" -"2604.24517"`
    (extended): 2604.24517 (abs/pdf/html), arXiv cs listing, 2607.08744, pith.science reviews, 2401.17743,
    2512.05271. Nothing new.

Every secondary summary that gives a number for this cell gives 31/1326 ≈ 0.023379. None gives a larger lower bound.

### 2c. Direct requests (one plain request each, `curl -A "V3R1T4S-panel"` unless noted; real output)

```
# v1 PDF of the target
Thu Oct 15 03:21:05 UTC 2026
http_code: 200
size_download: 711014
url_effective: https://arxiv.org/pdf/2604.24517v1
num_redirects: 0
content_type: application/pdf
curl exit: 0
Thu Oct 15 03:21:07 UTC 2026
sha256: beccada426c32005ad247a00426f264e885f6b2c0c1041b2be6dd94bb2ebc86f

# citing paper 2607.08744 (PDF)
Thu Oct 15 03:21:07 UTC 2026
http_code: 200
size_download: 916319
url_effective: https://arxiv.org/pdf/2607.08744
num_redirects: 0
content_type: application/pdf
curl exit: 0
Thu Oct 15 03:21:08 UTC 2026
sha256: adafbf34be739f63ac3e25a8df8d4e68fe134062fbd219e0b1ae9d6461920bcd

# Semantic Scholar citing-papers listing (blocked; not retried)
Thu Oct 15 03:21:09 UTC 2026
http_code: 429
size_download: 174
url_effective: https://api.semanticscholar.org/graph/v1/paper/arXiv:2604.24517/citations?fields=title,authors,year,externalIds,publicationDate&limit=100
curl exit: 0
Thu Oct 15 03:21:09 UTC 2026
{"message": "Too Many Requests. Please wait and try again or apply for a key for higher rate limits. https://www.semanticscholar.org/product/api#api-key-form", "code": "429"}

# arXiv API listing search (blocked; not retried)
Thu Oct 15 03:21:10 UTC 2026
http_code: 429
size_download: 14
url_effective: https://export.arxiv.org/api/query?search_query=abs:%22forecast%20aggregation%22&sortBy=submittedDate&sortOrder=descending&max_results=60
curl exit: 0
Thu Oct 15 03:21:42 UTC 2026

# arXiv title search "forecast aggregation", newest first
Thu Oct 15 03:22:30 UTC 2026
http_code: 200
size_download: 116162
url_effective: https://arxiv.org/search/?query=forecast+aggregation&searchtype=title&abstracts=hide&order=-announced_date_first&size=50
curl exit: 0
Thu Oct 15 03:22:53 UTC 2026
Showing 1&ndash;50 of 77 results
   (relevant hits since 2024: 2606.31020 Robust Aggregation of Calibrated Forecasts; 2604.24517 the target;
    2512.05271 Robust forecast aggregation via additional queries; 2402.06062; 2401.17743; the rest are
    energy/LLM/time-series forecasting papers)

# Google Scholar (HTTP 200 but an error page with no results, "the system cannot perform this action right now,
# try again later"; counted as unreachable, not retried)
Thu Oct 15 03:22:54 UTC 2026
http_code: 200
size_download: 154357
url_effective: https://scholar.google.com/scholar?q=%22Prior-Agnostic+Robust+Forecast+Aggregation%22
curl exit: 0
Thu Oct 15 03:22:56 UTC 2026

# abstract pages of the two in-window robust-aggregation papers from the title search
Thu Oct 15 03:23:53 UTC 2026
http_code: 200
url_effective: https://arxiv.org/abs/2606.31020
curl exit: 0
Thu Oct 15 03:23:54 UTC 2026
Thu Oct 15 03:23:55 UTC 2026
http_code: 200
url_effective: https://arxiv.org/abs/2512.05271
curl exit: 0
Thu Oct 15 03:23:55 UTC 2026

# OpenAlex record of the target
Thu Oct 15 03:23:56 UTC 2026
http_code: 200
url_effective: https://api.openalex.org/works/doi:10.48550/arXiv.2604.24517
curl exit: 0
Thu Oct 15 03:23:57 UTC 2026
id: https://openalex.org/W7156823476
title: Prior-Agnostic Robust Forecast Aggregation
publication_date: 2026-04-27
cited_by_count: 0
cited_by_api_url: None

# arXiv advanced search, author + "aggregation" (one request per author; these stand in for the arxiv.org/a/
# author pages, which need author identifiers)
Thu Oct 15 03:24:34 UTC 2026
author=Tang%2C+Wei http_code: 429          (blocked; not retried)
Thu Oct 15 03:24:36 UTC 2026
author=Chen%2C+Zhi http_code: 200
   Showing 1–15 of 15 results               (forecast-aggregation hits: 2609.33257, 2604.24517)
Thu Oct 15 03:24:56 UTC 2026
author=Peng%2C+Cheng http_code: 200
   Showing 1–10 of 10 results               (forecast-aggregation hits: 2609.33257, 2604.24517)
Thu Oct 15 03:25:10 UTC 2026

# later paper by the same authors, abstract and PDF
Thu Oct 15 03:25:19 UTC 2026
http_code: 200
url_effective: https://arxiv.org/abs/2609.33257
curl exit: 0
Thu Oct 15 03:25:20 UTC 2026
Thu Oct 15 03:25:29 UTC 2026
http_code: 200
size_download: 767603
content_type: application/pdf
curl exit: 0
Thu Oct 15 03:25:30 UTC 2026

# EC'26 accepted papers
Thu Oct 15 03:26:17 UTC 2026
http_code: 200
size_download: 260892
url_effective: https://ec26.sigecom.org/program/accepted-papers/
curl exit: 0
Thu Oct 15 03:26:21 UTC 2026
   "182. Prior-Agnostic Robust Forecast Aggregation Authors: Zhi Chen (The Chinese University of Hong Kong),
    Cheng Peng (The Chinese University of Hong Kong), Wei Tang (Chinese University of Hong Kong)"

# ACM Digital Library search (challenge page; not retried)
Thu Oct 15 03:26:52 UTC 2026
http_code: 403
size_download: 5709
url_effective: https://dl.acm.org/action/doSearch?AllField=%22Prior-Agnostic+Robust+Forecast+Aggregation%22
curl exit: 0
Thu Oct 15 03:26:52 UTC 2026
title: ['Just a moment...']

# arXiv TeX source of the target: e-print answered with a redirect; one request to the redirect target
Thu Oct 15 03:28:39 UTC 2026
http_code: 301
size_download: 217
content_type: text/html; charset=utf-8
url_effective: https://arxiv.org/e-print/2604.24517
curl exit: 0
Thu Oct 15 03:28:39 UTC 2026
Thu Oct 15 03:28:52 UTC 2026
http_code: 200
size_download: 53706
content_type: application/gzip
url_effective: https://arxiv.org/src/2604.24517
curl exit: 0
Thu Oct 15 03:28:53 UTC 2026

# PDF of 2606.31020 (scanned for citations of the target)
Thu Oct 15 03:30:47 UTC 2026
http_code: 200
size_download: 524671
content_type: application/pdf
curl exit: 0
Thu Oct 15 03:30:48 UTC 2026
```

What the fetched papers contain (pdftotext + grep for `1326|0.023|0.0255|prior-agnostic|2604.24517|lower bound`):
- arXiv:2607.08744, "Algorithmic Expert Aggregation" (Wei Tang, Hanrui Zhang; v1 9 Jul 2026). It cites the target only
  in a related-work list ("Recent works study a variety of extensions and variants of this robust information
  aggregation problem [... CPT26]"). No bound for this cell.
- arXiv:2609.33257, "Two Heads Are Better Than One: Aggregating Weaker LLMs for Better Forecasts" (Cheng Peng, Ruixi
  Luo, Zhi Chen, Wei Tang; v1 27 Sep 2026). An empirical ForecastBench study that uses the target's α-log-odds rule as
  a baseline (α = 0.56) and cites the target as "In ACM Conference on Economics and Computation". It has no bound, and
  neither 1326 nor any 0.023x value appears.
- arXiv:2606.31020, "Robust Aggregation of Calibrated Forecasts" (Xinxiang Guo, Yingkai Li, Yifen Mu; v1 30 Jun 2026).
  A different model (calibrated forecasts, max-min payoff benchmark) that cites the target only in related work. No
  bound for this cell.
- arXiv:2512.05271, "Robust forecast aggregation via additional queries" (Frongillo, Monroe, Neyman, Waggoner; 4 Dec
  2025). A query/elicitation model that predates this cell. Not applicable.
- The target was accepted at EC'26 (entry 182). The ACM DL proceedings version could not be read (403). arXiv v2
  postdates acceptance, and the TeX source is dated 26 May 2026.

### 2d. TROPHY_CASE.md (repository)

```
$ grep -c -i -E "forecast|aggregat|robust-forecast|31/1326|0\.0233|2604\.24517|regret" TROPHY_CASE.md
0
trophy-case grep exit: 1
```
Its 53 rows cover degree-diameter graphs, constant-weight codes, the Lehmer bound, matrix multiplication,
cipher-challenge commitments, VNN-COMP and RobustBench. None concerns this target or this cell.

### 2e. Open pull requests of https://github.com/elder-plinius/V3R1T4S

`gh pr list --repo elder-plinius/V3R1T4S --state open --limit 100` was run at 03:22:56Z (exit 0). Its display was cut
by my own `head -c 6000` pipe, not by GitHub, so I repeated the identical command once at 03:23:30Z (exit 0) and saved
the output to a file. No request was blocked, and nothing was retried after a block. Summary of the saved output
(author and branch names omitted):
```
open PRs returned: 30 (limit 100, so the list is complete); PR numbers 1 to 147
   1  claim codetables-binary-linear
   1  claim constant-weight-codes
   1  claim degree-diameter-table
   1  claim fmm-catalogue-small-format-rank
  12  claim packomania-hyperspheres-hsp4-hsp6
   2  claim stable-marriage-max-stable-matchings
   6  claim thomson-problem-live-tables
   1  claim vnncomp-2026-unsolved-instance-counterexample
   4  other: fix
   1  review A(34,8,7) ≥ 603
PRs whose title or branch matches forecast|aggregat|regret|robust-forecast|1326|2604.24517: none
```
No open PR targets robust-forecast-aggregation-bounds or this cell.

---------------------------------------------------------------------------------------------------------------------

## 3. Independent arithmetic check of the comparison

I wrote my own exact-rational evaluation of the Yao bound: sum over report pairs of
E_D[w p f_Bayes^2] - E_D[w p f_Bayes]^2 / E_D[w p]. It also recomputes each environment's reports and prior mean
from its likelihoods. It was run on claim/mixture.json and on the paper's Table 3 as a control:
```
paper Table 3 mixture LB: 31/1326 | equals 31/1326: True
   report pair ('1/6', '1/6') best response 7/78
   report pair ('1/6', '5/6') best response 1/2
   report pair ('5/6', '1/6') best response 1/2
   report pair ('5/6', '5/6') best response 71/78
env weight 1/2 theta ['0', '33307/40000'] computed reports ['6693/40000', '33307/40000'] | listed ['6693/40000', '33307/40000'] | match: True | mu 417121/1000000 listed 417121/1000000 match: True
env weight 1/2 theta ['6693/40000', '1'] computed reports ['6693/40000', '33307/40000'] | listed ['6693/40000', '33307/40000'] | match: True | mu 582879/1000000 listed 582879/1000000 match: True
distinct report pairs: 4
LB: 1652448303171916717080006468042849/70681471350112364987160770000000000
LB equals claimed value: True
LB float: 0.023378804538274   31/1326 float: 0.023378582202112   margin: 2.223362e-07
LB > 31/1326: True | LB > 0.023379 (paper's 6-d.p. rounding): False | LB > 0.02344: False
6-d.p. rounding of LB: 0.023379  of 31/1326: 0.023379
```
```
claimed - 31/1326 = 612886837595654297197253671111/2756577382654382234499270030000000000 = 2.223362e-07
matches claim.md/REPRODUCE margin: True
0.023379 - claimed = 1.9546e-07
0.02344 - claimed = 6.1195e-05
relative margin over 31/1326 = 9.510e-06
1/48 + 9/(136(13+3*sqrt17)) = 0.02344186
```
The control reproduces the paper's best responses 7/78, 1/2, 71/78 and the value 31/1326 exactly.

---------------------------------------------------------------------------------------------------------------------

## 4. Decision

- Claimed value for this cell (unknown state values, CI experts, lower-bound side):
  1652448303171916717080006468042849/70681471350112364987160770000000000 = 0.023378804538274...
- Best known lower bound for this cell: **31/1326 = 0.023378582202112...**, from Theorem 3.4 and Table 1 of
  arXiv:2604.24517v2 (latest version, 23 May 2026; also EC'26). No later paper, citing paper, repository row or open
  PR states a larger supported value. Bounds that carry over from the known-state and known-marginals cells are at
  most 0.022599 and 0.022763.
- The claimed value is **strictly larger** than 31/1326, by 612886837595654297197253671111/2756577382654382234499270030000000000
  ≈ 2.2234e-07 (relative 9.5e-06). In exact rational arithmetic this is not a tie.

Caveats that must go with any citation of this result:
1. The margin is tiny. At the paper's printed 6-decimal precision both values read 0.023379, and the claimed value
   is below the literal decimal "0.023379" that the paper prints as a rounding of 31/1326. The result must be stated
   as "> 31/1326 (exact)", never as "> 0.023379".
2. The paper prints an unsupported "0.02344" once (Section 3.2, v1 and v2). As shown in 1e, it is a withdrawn draft
   value with no construction or proof. The write-up should say so explicitly.
3. Sources I could not reach in one plain request: Semantic Scholar citations (429), arXiv API (429), the arXiv
   author search for one author (429), Google Scholar (error page) and ACM DL (403 challenge; the EC'26 proceedings
   version was not read). The gap is partly covered by 23 web searches, the arXiv title search, two of three author
   searches, OpenAlex and the three citing papers found. This cell was created in April 2026, so the relevant
   window is short.
4. The object has the same shape as the paper's own Table 3 adversary, with reports moved from 1/6 and 5/6 to
   6693/40000 and 33307/40000 and the priors adjusted. The authors' construction should be credited.
5. This is a novelty verdict only. Validity of the certificate is for the other skeptics, although my separate
   recomputation in section 3 agrees exactly.

Verdict: the claimed lower bound strictly beats every known lower bound for this cell (exact comparison with
31/1326), subject to the caveats above. It is not a tie.

novelty: PASS (strictly above the published 31/1326 for the unknown-state CI cell, lower bound side)

context: subagent
pass: true
