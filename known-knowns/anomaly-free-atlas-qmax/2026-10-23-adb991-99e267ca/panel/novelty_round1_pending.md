# Novelty skeptic: anomaly-free-atlas-qmax

Claim under review (from claim/CLAIM.md): Q_max = 11, SM count 37006, SMnuR count 45378378, in the
Allanach-Davighi-Melville (ADM) convention; claimed to lie beyond the largest published Q_max (10 for both contents).

## Status-source fetches (one request each, no retries, no user-agent changes)

Shell, plain `curl -sS -o <file> -w '%{http_code}'`, through the session's outbound proxy:

| URL | UTC time | result |
|---|---|---|
| https://zenodo.org/records/3345889 | 2026-10-18T07:16:15Z | HTTP code 000, no body; curl: (56) CONNECT tunnel failed, response 403 (proxy refused) |
| https://arxiv.org/html/1812.04602v5 | 2026-10-18T07:16:15Z | HTTP code 000, no body; curl: (56) CONNECT tunnel failed, response 403 (proxy refused) |
| https://link.springer.com/article/10.1007/JHEP08(2019)064 | 2026-10-18T07:16:15Z | HTTP code 000, no body; curl: (56) CONNECT tunnel failed, response 403 (proxy refused) |

WebFetch tool, one call each, about 2026-10-18T07:16:20Z:

| URL | result |
|---|---|
| https://zenodo.org/records/3345889 | error: getaddrinfo ENOTFOUND zenodo.org |
| https://arxiv.org/html/1812.04602v5 | error: getaddrinfo ENOTFOUND arxiv.org |
| https://link.springer.com/article/10.1007/JHEP08(2019)064 | error: getaddrinfo ENOTFOUND link.springer.com |

Value read from the status source: none. No page, table or file list of the status source was read. The
published values in claim/status.md (SM Q_max 10: 23800; SMnuR Q_max 10: 21546920; largest published Q_max 10)
come from a web-search tool's text summary, not from a byte-exact page, and this skeptic could not confirm them either.
Unconfirmed as a result: (a) that 10 is the largest tabulated Q_max on the current Zenodo record (version and file
list unread), and (b) that the claim's counting convention matches the published counts.

## Literature search (WebSearch, last 24 months, i.e. 2024-10 to 2026-10)

1. "anomaly-free U(1) charge assignments Standard Model Q_max count extension Allanach Davighi Melville atlas"
   returned the ADM paper (arXiv:1812.04602, JHEP02(2019)082), its erratum, Zenodo record 3345889, the nu-SUSY atlas
   (Allanach-Madigan-Tooby-Smith, JHEP02(2022)144, Q_max = 10, MSSM content) and PRD 106 116020 (2022, integer
   solutions for a class of chiral theories). No SM/SMnuR count with Q_max >= 11.
2. "number of anomaly-free family-dependent U(1) charge assignments right-handed neutrinos Qmax 11 12 enumeration
   2025 2026" returned the same records plus arXiv:2007.08733 (U(1)^m extensions) and Zenodo 5062067 (nu-SUSY lists).
   No enumeration at Q_max = 11 or 12.
3. "\"anomaly-free\" \"Q_max\" Standard Model U(1) charges exhaustive scan arXiv 2025" returned the same atlas
   records and Cambridge repository copies. No 2025 or 2026 census.
4. "anomaly-free atlas Standard Model U(1) charge assignments larger Qmax new census 2025 OR 2026 arXiv" returned
   the same records plus arXiv:2511.05976 (a single leptophilic U(1)' model, not a census). No extension of the ADM table.

Search summary: no published count for SM or SMnuR at Q_max >= 11 was found, and no extension of the ADM atlas
table was found. Search snippets are not the status source and cannot stand in for it.

## V3R1T4S repository check

- TROPHY_CASE.md (read-only copy of github.com/elder-plinius/V3R1T4S): six result families (degree-diameter graphs,
  constant-weight codes, matrix multiplication, Lehmer bound, VNN-COMP counterexamples, RobustBench attack) plus
  cipher-challenge commitments. No entry for anomaly-free charges, U(1), atlas or Allanach.
- Open pull requests, https://github.com/elder-plinius/V3R1T4S/pulls pages 1 to 3 (WebFetch, about 07:17Z): 69 open PRs
  (#9 to #376). None of the titles mentions anomaly-free, U(1), atlas, charge assignments, Allanach, Davighi, gauge
  or neutrino. A query of all PRs for "anomaly" (is:pr anomaly) returned one unrelated PR (#311, Packomania
  spheres-in-a-cube). Only titles were checked, not PR bodies.

## Verdict

The status source (Zenodo 3345889, arXiv 1812.04602v5, Springer erratum JHEP08(2019)064) could not be read: shell
requests were refused by the proxy (CONNECT 403), and WebFetch could not resolve the hosts. As a result, "strictly
beats everything known" cannot be established against the primary table. Neither the literature nor the repository
shows a competing count at Q_max >= 11, but that is not enough to pass.

novelty: PENDING STATUS CHECK
checked: zenodo.org/records/3345889, arxiv.org/html/1812.04602v5, link.springer.com/article/10.1007/JHEP08(2019)064
(all unreadable, 2026-10-18T07:16Z); 4 web searches (no Q_max >= 11 count found); TROPHY_CASE.md and 69 open PR
titles (no matching target).
context: subagent (fresh, saw only claim/)
pass: false
