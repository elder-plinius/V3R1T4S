# Novelty skeptic, round 2: anomaly-free-atlas-qmax (SMnuR, Q_max = 17 and 18)

Claimed rows (claim/object/counts.txt):
- SMnuR Q_max = 17: 1643386480
- SMnuR Q_max = 18: 2720672222

## 1. Primary table: owner-supplied copy (status/anomaly-free-atlas/)

This container cannot reach arxiv.org, link.springer.com or zenodo.org (section 2), so the primary table for this
round is the copy the workspace owner supplied in status/anomaly-free-atlas/.

sha256 check (`sha256sum -c SHA256SUMS`, run 2026-10-23 ~19:40 UTC):
- JHEP08-2019-064-erratum.pdf: OK (c6fcae4107a1e7306b58d4b0821c8b2f699e5ad06b21629e897af56b341dfcb4)
- arXiv-1812.04602v5.pdf: OK (022355da109e4eef72fb0cb314bea3c282fe49136f2aeae133c1ca262c275b96)

Table facts, which I read myself from the pdftotext extractions:
- arXiv:1812.04602v5, sec. 4.2, printed p. 15 (PDF p. 16), the exact sentence on range: "The full lists are available in
  the form of labelled, easily read ASCII files for public use on Zenodo at http://doi.org/10.5281/zenodo.3345889 [47]
  for Qmax ≤ 10 in the SM and Qmax ≤ 10 in the SMνR. The program itself is also made available there if a larger
  value of Qmax is desired by the user."
- arXiv v5 Table 2 (SM), printed p. 17 (PDF p. 18): rows Q_max = 1..10. Largest tabulated Q_max = 10, Solutions 23800,
  Symmetry 582.
- arXiv v5 Table 3 (SMnuR), printed p. 17 (PDF p. 18): rows Q_max = 1..10. Largest tabulated Q_max = 10, Solutions
  21546920, Symmetry 7540.
- Both captions say: "Each row contains the all-zero charge solution, as well as the solutions indicated in the rows above."
- Erratum JHEP 08 (2019) 064, Table 1 (p. 2): SMnuR, 7 ≤ Q_max ≤ 10. Q_max = 10: Solutions 21546920, Symmetry 7540
  (same values as v5 Table 3). Abstract: "add anomaly-free charge assignments for SMνR with 7 ≤ Qmax ≤ 10".
- The v5 text (p. 16) also says: "If Qmax > 10 is desired in the SMνR ... it may be advantageous to adapt the program
  to run in parallel on many cores". The paper gives no counts beyond 10.

=> The largest published Q_max is 10 for both SM and SMnuR. Both claimed rows (SMnuR 17, 18) lie strictly beyond it.

## 2. Fetch attempts (one plain curl each, no retries)

| URL | UTC time | result |
|---|---|---|
| https://zenodo.org/records/3345889 | 2026-10-23T19:40:50Z | curl: (56) CONNECT tunnel failed, response 403 (proxy refused) |
| https://arxiv.org/html/1812.04602v5 | 2026-10-23T19:40:50Z | curl: (56) CONNECT tunnel failed, response 403 (proxy refused) |
| https://link.springer.com/article/10.1007/JHEP08(2019)064 | 2026-10-23T19:40:50Z | curl: (56) CONNECT tunnel failed, response 403 (proxy refused) |

All three were blocked, as expected. One WebFetch of https://arxiv.org/abs/2508.11583 (for the literature check)
also failed with "getaddrinfo ENOTFOUND arxiv.org". None of these was retried. The verified owner-supplied PDFs
(section 1) are the primary table for this round.

## 3. Literature search (WebSearch, aimed at the last 24 months)

1. "anomaly-free U(1) charge assignments Standard Model right-handed neutrinos number of solutions Qmax larger than 10
   census" returned 1812.04602, 2107.07926 (nu-SUSY atlas: MSSM content, Q_max ≤ 10, July 2021, which is a different
   content and older than 24 months), Zenodo 5062067/3345889 and the Cambridge repository. No count for Q_max > 10.
2. "\"anomaly-free atlas\" extension Qmax 2025 OR 2026 flavour-dependent U(1) enumeration" returned the same papers.
   No 2025/2026 extension of the atlas. (The tool's summary attributed the SMnuR numbers to the SM. That summary is
   wrong, so I ignored it and relied on my own reading of the tables.)
3. "enumeration all anomaly-free family non-universal U(1) charges SM three right-handed neutrinos exhaustive scan
   arXiv 2025" returned 1812.04602, 1705.05643 (basis parametrisation, no bounded counts), 2606.25951 (FCC-hh Z'/HNL
   phenomenology, not an enumeration). Nothing relevant.
4. "counting integer solutions anomaly cancellation conditions Standard Model U(1) bounded charges 2025 2026 arXiv
   Qmax 11 12 right-handed neutrinos" returned 2508.11583 (Gripaios-Nguyen, "Anomaly cancellation for a U(1)
   factor", JHEP 01 (2026) 055: arithmetic geometry and infinite parametrisations, with no bounded-Q_max counts
   reported), 2205.03428, 2610.26092 (Gripaios, millicharged particles, a neighbouring problem), 1905.06073 (quotes
   the Q_max = 6 figure). No count for Q_max ≥ 11.
5. "\"Anomaly cancellation for a U(1) factor\" 2508.11583 bounded charges count solutions" returned 2508.11583 and
   2607.09879 ("Anomaly cancellation for two U(1) factors"). Per the search results, both are parametric, with no
   bounded-charge census. The full text could not be opened (arxiv blocked), so this rests on search snippets.
6. "\"SMνR\" OR \"SM+3νR\" anomaly-free solutions \"Qmax\" 11 OR 12 OR 17 OR 18 inequivalent charge assignments
   count" returned 1812.04602, the erratum, 2206.11271 (Flatland), 1905.06073 and Zenodo. Published SMnuR data stops at
   Q_max ≤ 10.

No search turned up any published count of anomaly-free family-dependent U(1) assignments for SM or SMnuR at
Q_max ≥ 11, nor any extension of the atlas's census.

## 4. TROPHY_CASE.md and open pull requests

- repo TROPHY_CASE.md: a case-insensitive grep for anomal|atlas|qmax|Q_max|U(1)|neutrino found no match. It lists no
  entry for this target.
- github.com/elder-plinius/V3R1T4S open PRs: the GitHub MCP refused this repository (not configured for the session),
  so I used WebFetch on the public pages. https://github.com/elder-plinius/V3R1T4S/pulls shows 306 open PRs. I read
  the titles on page 1 (#599-#632) and none is on this target.
  - Search "is:pr is:open anomaly": 2 hits. #610 (coord_loader / errata lint) and #311 (Packomania erratum) are both
    unrelated.
  - Search "is:pr is:open U(1)": 0 hits.
  - Search "is:pr is:open neutrino": 0 hits.
  No open PR claims these counts. Limitation: I did not read PR bodies page by page.
- claim/CLAIM.md notes that rows SMnuR 11..16 (and SM 11..31) of the same census were panelled in other workspace
  runs. They are not published and not in TROPHY_CASE.md. Rows 17 and 18 extend them and do not duplicate them.

## Scope note

This panel checks novelty only, not correctness. Whether 1643386480 and 2720672222 are right, and whether the list
hashes match, is for the other skeptics. I did not recompute the "ours" column of
status/anomaly-free-atlas/table_comparison.txt. I did confirm that its "paper" column matches Tables 2 and 3 of v5
and Table 1 of the erratum as I read them.

novelty: both claimed rows (SMnuR Q_max = 17, 18) lie strictly beyond the largest published Q_max (10, arXiv:1812.04602v5 Table 3 / JHEP 08 (2019) 064 Table 1, sha256-verified owner copy); no literature, TROPHY_CASE entry or open PR gives these counts, so this is not a tie.
context: subagent (fresh, saw only claim/ and status/anomaly-free-atlas/)
pass: true
