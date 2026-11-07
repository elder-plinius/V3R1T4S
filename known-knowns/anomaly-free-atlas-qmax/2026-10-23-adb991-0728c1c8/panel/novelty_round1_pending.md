# Novelty skeptic: anomaly-free-atlas-qmax (SMnuR Q_max = 17, 18)

Claim under review: in the Allanach-Davighi-Melville atlas convention, the SM + 3 nu_R census gives
1643386480 inequivalent anomaly-free family-dependent integer U(1) assignments for |F| <= 17 and 2720672222 for
|F| <= 18. The claim's status.md says the largest Q_max published is 10 for both field contents, but that came from
a web-search summary, not from a page anyone read.

## Status source fetches (one request per URL, no retries, no header changes)

status.md lists three status_source URLs. I sent plain curl requests (proxy as configured, default user agent):

| UTC time | URL | result |
|---|---|---|
| 2026-10-20T09:20:26Z | https://zenodo.org/records/3345889 | HTTP 000, curl: (56) CONNECT tunnel failed, response 403 (proxy refused) |
| 2026-10-20T09:20:26Z | https://arxiv.org/html/1812.04602v5 | HTTP 000, curl: (56) CONNECT tunnel failed, response 403 (proxy refused) |
| 2026-10-20T09:20:27Z | https://link.springer.com/article/10.1007/JHEP08(2019)064 | HTTP 000, curl: (56) CONNECT tunnel failed, response 403 (proxy refused) |

I also tried the WebFetch tool once per URL, at about 2026-10-20T09:20:37Z:

| URL | result |
|---|---|
| https://zenodo.org/records/3345889 | error: getaddrinfo ENOTFOUND zenodo.org |
| https://arxiv.org/html/1812.04602v5 | error: getaddrinfo ENOTFOUND arxiv.org |
| https://link.springer.com/article/10.1007/JHEP08(2019)064 | error: getaddrinfo ENOTFOUND link.springer.com |

None of the requests returned a page, so I could not read any published value or the largest tabulated Q_max at
first hand. That matches the run's own scout on 2026-10-18, which recorded 403 proxy refusals for Springer
(JHEP02(2019)082 PDF), the Zenodo record and the Zenodo API.

## Literature search (WebSearch, last 24 months; search summaries only, no pages opened)

1. Query: "anomaly-free U(1) charge assignments Standard Model right-handed neutrinos Qmax count atlas extension".
   Results: Allanach-Madigan-Tooby-Smith, "A nu Supersymmetric Anomaly-free Atlas" (arXiv:2107.07926, JHEP 2022;
   Zenodo 5062067). It covers MSSM + up to 3 singlets with Q_max <= 10, which is a different field content. Zenodo
   3345889 also came back. No SMnuR count for Q_max >= 11.
2. Query: "Allanach Davighi Melville "anomaly-free" atlas Qmax 10 SMnuR solutions enumeration larger Qmax 2025 2026".
   Results: arXiv:1812.04602, arXiv:2107.07926, arXiv:1912.10022, talk slides (IPPP Durham, Bonn HerbiFest) and an
   EPJC 2024 article. The summary says nothing from 2025 or 2026 enumerates beyond Q_max = 10, and the slides say the
   scan stopped at |charge| <= 10.
3. Query: ""anomaly-free" U(1) "Qmax" 17 OR 18 number of solutions Standard Model three right-handed neutrinos family
   non-universal 2025". Results: arXiv:1812.04602 (fit formula only), 1705.05643, 1309.1709, 1905.06073, 2007.08733,
   1612.07660. None gives a count at Q_max 17 or 18.
4. Query: "exhaustive enumeration anomaly-free gauged U(1) flavour-dependent charges Standard Model arXiv 2025 2026
   counting solutions bounded charges". Results: arXiv:1812.04602 and its erratum, 2107.07518, 1909.02021,
   2209.14404, hep-ph/0510181. No 2025 or 2026 enumeration past Q_max = 10 found.

What this shows: no source the searches surfaced gives an SMnuR count for Q_max >= 11. This rests on search-engine
summaries only. They are not the primary table, and they cannot rule out a newer Zenodo version or a paper the
index missed.

## TROPHY_CASE.md and open pull requests

- TROPHY_CASE.md (local read-only copy of the V3R1T4S repository): a case-insensitive grep for anomal, u(1), atlas,
  davighi, allanach, qmax, q_max, neutrino and charge found no match (grep exit status 1). The listed families are
  degree-diameter graphs, Lehmer, matrix multiplication, VNN-COMP, RobustBench, constant-weight codes and cipher
  commitments. No entry for this target.
- Open PRs, https://github.com/elder-plinius/V3R1T4S/pulls (WebFetch, about 09:21Z): page 1 of 12, 279 open PRs.
  PRs #568 to #592 on that page are about Shannon capacity, codetables, IEA37, AME states, covering designs,
  percolation and similar. None concerns anomaly-free U(1) charges.
- Searched the open PRs for "anomaly" (WebFetch): 1 result, #311, a Packomania sphere-in-cube erratum. Not this
  target.
- Searched the open PRs for "atlas" (WebFetch): 1 result, #464, erdos-699-binomial-gcd. Not this target.
- I did not read pages 2 to 12 of the open PR list one by one. Both keyword searches covered all open PRs.

## Verdict

I could not read the status source: all three status_source URLs were blocked or unreachable on a single honest
request each, by curl and by WebFetch. So I cannot confirm from the primary table that the largest published SMnuR
Q_max is below 17. That leaves the claim's "strictly beats everything known" unestablished. The secondary checks
(literature search, TROPHY_CASE, open PRs) found nothing that matches or beats the claim. Under the panel rule they
cannot stand in for the status source.

novelty: PENDING STATUS CHECK
context: subagent (fresh, saw only claim/)
pass: false
