# Novelty panel — claim A384209(11) = 71

Context: fresh-context novelty skeptic; worked only from [scratch]/panel0324-novelty (cp -a of runs/2026-11-03-0324/claim), read-only repo [workdir]/repo (HEAD f3b19b475065f35d0a7f93e8a6078c9b2f12566e, 2026-10-30T10:12:11Z), public web and GitHub API. Did not read attempts/ or other panelists' files.

## Status fetch (one GET, no retries)
- URL: https://oeis.org/search?q=id:A384209&fmt=text (status_source https://oeis.org/A384209)
- Time: 2026-11-03T07:53:58Z (02:53:58 EST), HTTP 200, UA "V3R1T4S novelty panel"
- sha256 a2d2fe9c9ff2aab776502142000c0bd3bc4d5b2e120022d1679f0990a8c84247 — byte-identical to the claim's scout (03:24:38Z) and claim-time (07:36:52Z) fetches.
- Content: `%I A384209 #8 May 22 2025`, `%S A384209 1,1,1,1,2,4,8,14,27` (n = 1..9), keyword `more`. DATA ends at a(9) = 27 as expected. No a(10), no a(11), no comment/b-file/link mentioning n = 10 or 11.

## Repo search (read-only)
- TROPHY_CASE.md: no match for A384209 / graph-automata / A357951.
- known-knowns/: no match.
- known-unknowns/graphs-games-automata/graph-automata-max-period.md: target still "open as of 2026-10-30", lists terms only through n = 9; p2 partial explicitly names "A384209(10) and A384209(11)" as further terms to win.

## GitHub PRs/issues (API, 2026-11-03T07:54Z)
- repo:elder-plinius/V3R1T4S "A384209": 1 result — #904 OPEN (unmerged), "[claim] graph-automata-max-period: A384209(10) = 46", created 2026-11-02T18:47:50Z (13:47 EST Nov 2). Body states "Only one cell, A384209(10). A384209(11) ... not claimed." 0 comments.
- "graph-automata-max-period": #904 plus unrelated #859, #699 (closed, subtraction games), #534. Closed PRs mentioning A384209: 0.
- Global GitHub issue search "A384209": only #904. Repo search "A384209": 0.
- So a(11) is not claimed in any open or closed PR; a(10) = 46 is only in unmerged #904 (same contributor) and is not part of this cell.

## Literature (last 24 months, web)
- Searches: "A384209 Game of Life graph maximum period", "Game of Life on graphs maximum period 11 vertices exhaustive enumeration 2025 2026", "1, 1, 1, 1, 2, 4, 8, 14, 27, 46 Game of Life graph period".
- Hits: OEIS A384209 (through n = 9 only); Krechetov arXiv:2111.01780 (different rule, >24 mo, no max-period terms); Christopherson visual lab (interactive, no terms); LifeWiki integer-sequences page (does not list A384209 terms past 9); MathOverflow 504642 (unrelated).
- One search-engine synthesis said the values run through "46 for n = 10", but the page excerpt it cited ends at 27. This is a summariser error, not a source. No publication, preprint, forum post or repo gives A384209(11) or the value 71.

## Verdict
A384209(11) = 71 is not in the live OEIS entry (DATA ends at a(9) = 27, no pending draft per claim record), not in TROPHY_CASE or known-knowns, not in any open or closed PR (the only related PR #904 is for a(10) and says it does not claim a(11)), and not in the literature found. Novel as a cell. Caveat for other panelists: a(10) = 46 is not yet accepted anywhere; the a(11) claim does not depend on it for novelty, but it is a step below a(11) in the same enumeration.

pass: true
