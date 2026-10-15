# The record we beat

Cell: prior-agnostic robust forecast aggregation, two experts with signals conditionally independent given a binary
state whose values are unknown to the aggregator (the class Pi_CI of arXiv:2604.24517v2), squared loss, additive regret
against the omniscient aggregator; **lower bound** on the minimax regret. Larger is better on this side.

Status source: the arXiv abstract page of Zhi Chen, Cheng Peng, Wei Tang, "Prior-Agnostic Robust Forecast
Aggregation", and the v2 full text it links to. One plain request per fetch, no retries. Times are converted from the
`date -u` output recorded with each fetch (for example `Wed Oct 14 17:20:50 UTC 2026` = 2026-10-14T17:20:50Z).

| fetch | URL | fetched (UTC) | HTTP | sha256 of the response | recorded in |
|---|---|---|---|---|---|
| abstract page (scout) | https://arxiv.org/abs/2604.24517 | 2026-10-14T17:20:50Z | 200 | 523d3c019876a3a9d14ed263520ff94b40902befaea19f9cd47bca77ae45b849 | the run's scout record |
| full text HTML v2 (scout) | https://arxiv.org/html/2604.24517v2 | 2026-10-14T17:20:51Z | 200 | d2b20052e3adef7f5190725a002da9ca28afdc2e76d89cc04e066609db8c7bb3 | the run's scout record |
| PDF v2 (scout) | https://arxiv.org/pdf/2604.24517v2 | 2026-10-14T17:20:51Z | 200 | 1a5836aeae0fbac9603e3e9da59c802c296d9988c66e788d0eed810cc9ec5481 | the run's scout record |
| abstract page (NOVELTY skeptic) | https://arxiv.org/abs/2604.24517 | 2026-10-15T03:18:03Z to 03:18:04Z | 200 | 523d3c019876a3a9d14ed263520ff94b40902befaea19f9cd47bca77ae45b849 (identical) | `panel/novelty.md`, section 1a |
| PDF, latest version (NOVELTY skeptic) | https://arxiv.org/pdf/2604.24517 | 2026-10-15T03:18:24Z to 03:18:25Z | 200 | 1a5836aeae0fbac9603e3e9da59c802c296d9988c66e788d0eed810cc9ec5481 (identical to v2) | `panel/novelty.md`, section 1b |

Selected headers (NOVELTY skeptic's fetches; the scout did not record headers): abstract page `HTTP/2 200`,
`last-modified: Mon, 24 Aug 2026 18:53:30 GMT`, `date: Thu, 15 Oct 2026 03:18:04 GMT`; PDF
`last-modified: Tue, 26 May 2026 00:36:41 GMT`, `content_type: application/pdf`, stamped `arXiv:2604.24517v2 [cs.LG] 23 May 2026`.
Submission history on the abstract page: v1 Mon, 27 Apr 2026; v2 Sat, 23 May 2026 (latest). No journal reference is
shown on the page.

## Extracted cell

- Table 1 ("Summary of regret bounds"), row for the unknown state space with conditionally independent signals, lower
  bound: **31/1326** (Theorem 3.4), footnote ≈ 0.023379. The same row's upper bound is 0.025512 (Theorem 3.2), not
  compared against here. Theorem 3.4 states inf_f Reg_PiCI[f] ≥ 31/1326, proved with Yao's principle on a uniform
  mixture of two explicit structures (the paper's Table 3: reports 1/6 and 5/6).
- Exactly, 31/1326 = 0.0233785822021116…; this package's value is
  1652448303171916717080006468042849/70681471350112364987160770000000000 = 0.0233788045382…, larger by
  612886837595654297197253671111/2756577382654382234499270030000000000 ≈ 2.22e-7. Both print as 0.023379 at six
  decimals; the comparison is exact.
- Also printed once in the paper: "0.02344" (opening sentence of Section 3.2) as a lower bound, with no construction or
  proof; traced by the NOVELTY skeptic to a commented-out draft formula in the LaTeX source (`panel/novelty.md`). Not a
  published bound; this package does not claim to exceed it.

Other places checked by the panel (all in `panel/novelty.md`): the v1 PDF (same Theorem 3.4), web and arXiv searches,
OpenAlex, three citing papers; none gives a larger lower bound for this cell. Semantic Scholar and the arXiv API
answered 429, Google Scholar an error page and ACM DL 403; each was requested once and not retried.
