# Novelty skeptic, round 2: anomaly-free-atlas-qmax

Claim (claim/CLAIM.md, claim/object/counts.txt): at Q_max = 11, 37006 inequivalent anomaly-free family-dependent U(1)
charge assignments for SM (15 charges) and 45378378 for SMnuR (18 charges), in the Allanach-Davighi-Melville (ADM)
atlas convention. Rows claimed: SM Q_max 11 and SMnuR Q_max 11 only.

## 1. Primary table: owner-supplied copy, sha256 check

This container cannot reach arxiv.org, link.springer.com or zenodo.org (section 2), so for this round the primary
table is the owner-supplied copy in status/anomaly-free-atlas/ (arXiv:1812.04602 v5 PDF and the erratum JHEP 08 (2019)
064 PDF), not a live fetch.

`sha256sum -c SHA256SUMS` (run 2026-10-23 ~19:38 UTC):
- JHEP08-2019-064-erratum.pdf: OK, c6fcae4107a1e7306b58d4b0821c8b2f699e5ad06b21629e897af56b341dfcb4
- arXiv-1812.04602v5.pdf: OK, 022355da109e4eef72fb0cb314bea3c282fe49136f2aeae133c1ca262c275b96

Note: the SHA256SUMS file was supplied alongside the PDFs, so this check shows the files are intact since they were
saved, not that they match arxiv/Springer byte-for-byte. The text is internally consistent (header
"arXiv:1812.04602v5 [hep-ph] 8 Jan 2020"; erratum header "JHEP08(2019)064", Received July 30, 2019, Published
August 12, 2019).

## Table facts (read from the pdftotext extractions of the two PDFs)

arXiv:1812.04602v5, section 4.2 "Results", PDF page 16 (printed page 15), exact sentence:
> "The full lists are available in the form of labelled, easily read ASCII files for public use on Zenodo at
> http://doi.org/10.5281/zenodo.3345889 [47] for Qmax ≤ 10 in the SM and Qmax ≤ 10 in the SMνR . The program
> itself is also made available there if a larger value of Qmax is desired by the user."

On PDF page 17 (printed page 16) the paper also says: "If Qmax > 10 is desired in the SMνR , for which we have not
found analytic simplifications analogous to Eq. (3.22), it may be advantageous to adapt the program to run in
parallel on many cores."

arXiv v5 Table 2 (SM), PDF page 18 (printed page 17): rows Qmax = 1..10. Largest tabulated Qmax = 10:
Solutions 23800, Symmetry 582 (Quadratics 1580566538, Cubics 7795283, Time 20 s). Caption: "Each row contains the
all-zero charge solution".

arXiv v5 Table 3 (SMνR), same page: rows Qmax = 1..10. Largest tabulated Qmax = 10: Solutions 21546920,
Symmetry 7540 (Quadratics 2117256832910, Cubics 10687426240, Time 24748 s).

Erratum JHEP 08 (2019) 064, Table 1 (SMνR, 7 ≤ Qmax ≤ 10), printed page 2: Qmax 10 row gives Solutions 21546920,
Symmetry 7540, the same as v5 Table 3. Abstract: "add anomaly-free charge assignments for SMνR with 7 ≤ Qmax ≤ 10."
Neither document tabulates any row with Qmax ≥ 11 for either content.

Largest published Q_max: SM 10 (count 23800); SMnuR 10 (count 21546920). Both claimed rows are at Q_max = 11,
strictly beyond. status/anomaly-free-atlas/table_comparison.txt reports that the workspace counter reproduces all 40
published numbers (Q_max 1..10, solutions and symmetry, both contents), so the counting convention matches. I did not
re-run that comparison; reproduction is a different panel's job.

## 2. Fetch attempts (one plain curl each, no retries, from this container)

| URL | UTC time | result |
|---|---|---|
| https://zenodo.org/records/3345889 | 2026-10-23T19:39:01Z | `curl: (56) CONNECT tunnel failed, response 403` (proxy block), http_code 000 |
| https://arxiv.org/html/1812.04602v5 | 2026-10-23T19:39:01Z | `curl: (56) CONNECT tunnel failed, response 403` (proxy block), http_code 000 |
| https://link.springer.com/article/10.1007/JHEP08(2019)064 | 2026-10-23T19:39:01Z | `curl: (56) CONNECT tunnel failed, response 403` (proxy block), http_code 000 |

All three were blocked, as expected. Under the "a block means fail" rule a live fetch was impossible. For this round the
owner-supplied, hash-checked PDFs (section 1) are the primary table, and the facts above are quoted from them.

## 3. Literature search, last 24 months (WebSearch, 2026-10-23)

1. "anomaly-free atlas U(1) charge assignments Standard Model Qmax 11 number of solutions": returned arXiv:1812.04602,
   Zenodo records 3345889 / 5062066 / 5062067, Springer JHEP02(2019)082, a Cambridge repository copy, and
   par.nsf.gov. No Q_max = 11 count. (The tool's summary attributed the SMnuR numbers to the SM. That is the
   summariser's error; the PDF is authoritative.)
2. "anomaly-free family-dependent U(1) charges right-handed neutrinos enumeration larger maximum charge 2025 2026":
   returned the ADM atlas, arXiv:2107.07926 (nu-SUSY atlas, MSSM content, Q_max ≤ 10), and older non-enumerative
   papers. Nothing from 2025-2026 extends the SM/SMnuR census.
3. (extended) "\"anomaly-free\" \"U(1)\" charges \"Standard Model\" Diophantine enumeration solutions \"Q_max\" arXiv
   2025": returned the ADM atlas (arxiv.org/html/1812.04602v5), arXiv:1905.13729 (general solution, 2019),
   arXiv:2511.05976 (an anomaly-free leptophilic U(1)'_l completion, a single model, not a census), and ResearchGate
   copies. No Q_max ≥ 11 counts.
4. (extended) "Allanach Davighi Melville anomaly-free atlas extended Qmax beyond 10 SMnuR solutions count": returned the
   ADM paper, the erratum, Zenodo 3345889 ("augments v1.0.0 with the SMnuR solutions up to and including Qmax=10"), and
   the nu-SUSY atlas JHEP02(2022)144 / arXiv:2107.07926 (a different field content). No extension past Q_max = 10 for
   SM or SMnuR.
5. "anomaly cancellation U(1) flavour-dependent charges right-handed neutrinos complete list solutions 2024 2025 2026
   arXiv scan": returned the ADM atlas, Zenodo, arXiv:2011.12973 (hidden photons, 2020), and older papers. Nothing in
   the window.

Limitation: WebSearch is a summarising search engine, not a full arXiv/INSPIRE citation crawl, and arXiv itself is
unreachable from here. Across five queries, none found any SM or SMnuR count at Q_max ≥ 11, or any published Q_max = 11
list.

## 4. TROPHY_CASE.md and open pull requests

- repo/TROPHY_CASE.md (100 lines): grep for anomaly|atlas|U(1)|qmax|allanach|charge returned no matches. The listed
  families are degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench, and
  cipher commitments. None is this target.
- github.com/elder-plinius/V3R1T4S open PRs (WebFetch, 2026-10-23): https://github.com/elder-plinius/V3R1T4S/pulls
  shows 306 open PRs; the first page (#599-#632) has nothing relevant. Filtered open-PR searches:
  `anomaly` gave 2 hits, #610 (kit: coord_loader + errata whitelist lint) and #311 (Packomania scu), both unrelated;
  `U(1)` gave 0; `atlas` gave 1 hit, #464 (erdos-699 binomial gcd), unrelated; `Allanach` gave 0; `Qmax` gave 0.
  No open PR claims anomaly-free U(1) counts at any Q_max.

## Assessment

- SM row: claimed Q_max 11 > largest published 10 (Table 2, count 23800). Strictly beyond, and no prior count found.
- SMnuR row: claimed Q_max 11 > largest published 10 (Table 3 / erratum Table 1, count 21546920). Strictly beyond,
  and no prior count found.
- The ADM program on Zenodo could in principle produce Q_max = 11 for anyone who runs it. A published or posted
  count is what counts as "known", and none was found. This is an extension of an exact census, not an improvement of
  an optimisation bound, so "beats" here means "past the published range", which is what the charter criterion asks.
- Caveat: counts are only comparable under the ADM convention. Matching all 40 published values (table_comparison.txt)
  supports that convention; checking the numbers themselves belongs to the reproduce panel.

novelty: both claimed rows (SM 37006, SMnuR 45378378 at Q_max = 11) lie strictly beyond the largest published Q_max = 10 in arXiv:1812.04602v5 Tables 2-3 and erratum JHEP08(2019)064 Table 1; no later literature, TROPHY_CASE entry or open PR gives Q_max >= 11 counts.
context: subagent (fresh, saw only claim/ and status/anomaly-free-atlas/)
pass: true
