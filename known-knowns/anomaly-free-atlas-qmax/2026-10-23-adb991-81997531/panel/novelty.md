# Novelty skeptic, round 2: anomaly-free-atlas-qmax

Inputs read: claim/CLAIM.md, claim/object/counts.txt, claim/status.md; status/anomaly-free-atlas/ (README.md,
SHA256SUMS, table_comparison.txt, both PDFs and their .txt extractions); repo/TROPHY_CASE.md.

## 1. sha256 check of the owner-supplied primary documents

`sha256sum -c SHA256SUMS` in status/anomaly-free-atlas/:

    c6fcae4107a1e7306b58d4b0821c8b2f699e5ad06b21629e897af56b341dfcb4  JHEP08-2019-064-erratum.pdf  -> OK
    022355da109e4eef72fb0cb314bea3c282fe49136f2aeae133c1ca262c275b96  arXiv-1812.04602v5.pdf       -> OK

Both PDFs match the recorded hashes. arXiv stamp on the PDF: "arXiv:1812.04602v5 [hep-ph] 8 Jan 2020".

## 2. Table facts, read by me from the rendered PDF pages (and cross-checked against the .txt extraction)

arXiv:1812.04602v5, PDF page 18 (printed page "- 17 -"):
- Table 2 (SM fermion content): Q_max rows 1..10. Largest tabulated Q_max = 10, Solutions = **23800**
  (Symmetry 582, Quadratics 1580566538, Cubics 7795283, Time/sec 20).
- Table 3 (SMnuR): Q_max rows 1..10. Largest tabulated Q_max = 10, Solutions = **21546920**
  (Symmetry 7540, Quadratics 2117256832910, Cubics 10687426240, Time/sec 24748).
- Both captions: "Each row contains the all-zero charge solution, as well as the solutions indicated in the rows above."

arXiv:1812.04602v5, PDF page 16 (printed "- 15 -"), section 4.2 "Results", exact sentence on the atlas's range:
> "The full lists are available in the form of labelled, easily read ASCII files for public use on Zenodo at
> http://doi.org/10.5281/zenodo.3345889 [47] for Qmax ≤ 10 in the SM and Qmax ≤ 10 in the SMνR. The program
> itself is also made available there if a larger value of Qmax is desired by the user."

PDF page 17 (printed "- 16 -"): "For Qmax much higher than 10 in the SM, run-time may be an issue. [...] If Qmax > 10
is desired in the SMνR, [...] it may be advantageous to adapt the program to run in parallel on many cores."

Erratum JHEP 08 (2019) 064, page 2, Table 1 (SMnuR, 7 <= Q_max <= 10): Q_max 10 Solutions **21546920**
(Symmetry 7540), identical to arXiv v5 Table 3. Abstract (page 1): "add anomaly-free charge assignments for SMνR
with 7 ≤ Qmax ≤ 10." Figure 1 caption: "as a function of Qmax ≤ 10 for the SMνR".

Conclusion from the primary table: largest published Q_max = 10 for SM and 10 for SMnuR. Values at Q_max = 10:
SM 23800, SMnuR 21546920. These agree with the values claim/status.md had from a web-search tool, and with
status/anomaly-free-atlas/table_comparison.txt (I did not rerun the workspace counters; that is not this skeptic's job).

## 3. Fetch attempts (one each, plain curl, no retries)

| URL | UTC time | result |
|---|---|---|
| https://zenodo.org/records/3345889 | 2026-10-23T19:39:02Z | curl: (56) CONNECT tunnel failed, response 403 (HTTP 000) |
| https://arxiv.org/html/1812.04602v5 | 2026-10-23T19:39:03Z | curl: (56) CONNECT tunnel failed, response 403 (HTTP 000) |
| https://link.springer.com/article/10.1007/JHEP08(2019)064 | 2026-10-23T19:39:03Z | curl: (56) CONNECT tunnel failed, response 403 (HTTP 000) |

All three blocked by the container proxy, as expected. For this round the primary table is the owner-supplied,
hash-checked copy of arXiv:1812.04602v5 (Tables 2, 3) and the erratum (Table 1), not a live fetch.
Also tried once: WebFetch of the INSPIRE citation API (refersto:arxiv:1812.04602, last 24 months) ->
"getaddrinfo ENOTFOUND inspirehep.net" (not reachable; no retry).

## 4. Literature search, last 24 months (WebSearch tool)

1. "anomaly-free U(1) charge assignments Standard Model right-handed neutrinos number of solutions Qmax larger than
   10 atlas extension" (extended): returned the Zenodo record 3345889, the original paper (arXiv html v5, Springer),
   the erratum, ResearchGate copies, "A ν supersymmetric anomaly-free atlas" (JHEP02(2022)144, MSSM + 3 singlet
   superfields, Q_max <= 10; different field content, older than 24 months). No count for SM or SMnuR with Q_max >= 11.
2. "\"anomaly-free atlas\" Allanach Davighi Melville citing 2025 2026 enumeration family-dependent U(1) charges":
   original paper, arXiv:2107.07926 (the ν-SUSY atlas), unrelated ATLAS-detector anomaly-detection papers. No
   2025-2026 extension of the census.
3. "count anomaly-free flavour-dependent U(1) charges SM \"Q_max\" 11 12 enumeration solutions 2024 2025 arXiv"
   (extended): Zenodo 1478085 and 3345889 (the atlas data, Q_max <= 10), Zenodo 5062067 (ν-SUSY atlas, MSSM content,
   Q_max <= 10), arXiv:1909.02021, EPJC anomaly-free models paper. No Q_max >= 11 count.
4. "enumeration integer solutions anomaly cancellation conditions Standard Model U(1) family non-universal charges
   bounded charge new counts 2025 2026" (extended): arXiv:2103.06783 (scan with |charge| <= 10 plus exotics, 2021),
   Podo-Revello arXiv:2205.03428 (G x U(1) class, 2022), older U(1)' papers. Nothing in the last 24 months giving
   these counts.

Limits: arXiv listing and INSPIRE could not be queried directly from here; the search covers what the WebSearch
index returns. Within that, no published count for SM or SMnuR at any Q_max > 10 was found, and no extension of
the atlas.

## 5. TROPHY_CASE.md and open pull requests

- repo/TROPHY_CASE.md: 53 rows in six families (degree-diameter, constant-weight codes, matrix multiplication,
  Lehmer, VNN-COMP, RobustBench) plus cipher commitments. No row on anomaly-free U(1) charges, the atlas, or Q_max.
- github.com/elder-plinius/V3R1T4S open pull requests (306 open), via WebFetch:
  - page 1 of open PRs (#599-#632): none on this target.
  - search `is:pr is:open anomaly`: 2 hits (#610 kit lint, #311 Packomania erratum): not this target.
  - search `is:pr is:open atlas`: 1 hit (#464 erdos-699): not this target.
  - search `is:pr is:open U(1)`: 0 hits.
  - search `is:pr is:open Qmax`: 0 hits.
  No open PR claims these counts or any anomaly-free-atlas-qmax row.

## 6. Row-by-row comparison

Every row of claim/object/counts.txt: SMnuR Q_max 12..16 (largest published SMnuR Q_max = 10) and SM Q_max 12..31
(largest published SM Q_max = 10). Each claimed Q_max is strictly greater than the largest published one for its
content (12 > 10). Nothing found (primary tables, literature search, TROPHY_CASE, open PRs) already gives any of
these counts. Not a tie: no published value exists at these Q_max. (Q_max = 11 is not claimed; that gap does not
affect novelty of the claimed rows.) Novelty is about the target; whether the counts are correct and in the
paper's convention is for the other skeptics (the 40/40 match in table_comparison.txt supports the convention).

novelty: new. All 25 claimed rows (SMnuR 12-16, SM 12-31) are past the largest published Q_max = 10 (arXiv:1812.04602v5 Tables 2-3, erratum Table 1), and no source found gives these counts.
context: subagent (fresh, saw only claim/ and status/anomaly-free-atlas/)
pass: true
