# Novelty skeptic (protocol 2): A_4^GC,RC(20,15,10) >= 16

context: fresh subagent started by the panel orchestrator with no prior conversation, told to read only the `claim/` folder (skeptic_novelty_protocol2 copy). Network access was read-only. Instruction: fetch the primary table once with no retries, search the last 24 months of literature, the repo's TROPHY_CASE.md and its open PRs, and pass only on a strict improvement (a tie does not count).

## 1. Object sanity (own check, written from the definition before running the author's checker)

- `object/code_20_15_16.json` has sha256 `e3a3a885c67a9a34329ed2247d32dfe004b64645b8d2bd97ef528009a77e2de7`, which matches `CLAIM.md`.
- My own check found 16 words, all distinct, all of length 20, alphabet {A,C,G,T}, GC count 10 in every word. The minimum pairwise Hamming distance is 15. The minimum of H(x, rc(y)) over all x, y, including x = y, is 15.
- `checker/check_dna.py` gives the same result: `{"valid": true, "n": 20, "d": 15, "w": 10, "size": 16}`.

## 2. Primary table: one fetch, no retries

- URL: https://rambutan.umassmed.edu/king/dnacodes.html
- Time: request started 2026-10-17T23:07:32Z (local clock, UTC). The server `Date` header was `Sat, 17 Oct 2026 23:07:34 GMT`.
- Response: HTTP 200, 18096 bytes, sha256 `25d6e9f88262fbb07c95841225cb3202aa29eb31f7f72d24b43e9c595bdb18c5`, `Last-Modified: Fri, 07 Jun 2024 15:41:04 GMT`. This page is byte-identical to the author's scout fetch in `table_record/fetch.json`.
- Value: in the second table, "Lower bounds for A_4^GC,RC(n,d,w)", the cell at row n=20, column d=15 is `15<sup>v</sup>`. It has no period and no colon, so it is not marked optimal. The superscript `v` means variable neighbourhood search from [MS]/[MS2] (Montemanni & Smith).
- Result: 16 > 15, so the claim strictly beats the live entry.

## 3. Literature (post-2010 published values for (n,d) = (20,15) with GC and RC constraints)

Supplied sources, which I read myself. Their tables are images, so I rendered them and read the cells.

| Source (relative to claim/) | Table / cell | Value at (20,15) |
|---|---|---|
| `sources/aboluion_smith_perkins_2012_dm312.pdf` (Discrete Math 312, 2012) | Table 9, best known max_w A_4^GC,RC(n,d,w), 12<=d<=30, row 20 | `15_m3` |
| `sources/aboluion_phd_thesis_2011.pdf` | Table 10.72 (same quantity), row 20 | `15_m3`. Its own linear constructions, Table 10.67, are lower. |
| `sources/montemanni_smith_koul_2014_lnms6.pdf` (LNMS 6, 2014) | Table 2, A_4^GC,RC(n,d,w), w = n/2, row 20 | V (their VNS): `15^N`; B (prior best): `14` |

The 2012 value maximises over all w. A code of size 16 with w=10 also strictly exceeds that max_w bound of 15.

arXiv papers I checked (full text):
- arXiv:1903.03535 (Sangroniz & Martinez, 2019), the paper the bank cites. Its improvements are A^GC,RC(13,5) >= 1716 and A^GC,RC(29,11) >= 77558760. Nothing at (20,15).
- arXiv:2403.11551 (Chen, Choi, Liu, 2024). New bounds at lengths 80, 96 and 160 only.
- arXiv:2409.06519 (Wang, Liu, Chen, Sept 2024). For n=20 it lists only d=4 and d=6.
- arXiv:2506.19170 (Garcia-Claro, June 2025). This paper is about distance bounds for reversible and RC codes, with no GC-content lower-bound table.
- arXiv:2108.02033 (2021) and arXiv:1902.04419 (2019) were downloaded. Neither has an n=20 row matching (20,15).

Web searches (4 queries covering 2024-2026: constant GC-content, reverse-complement, new lower bounds, metaheuristics, length 20) turned up no paper reporting A_4^GC,RC(20,15,10) >= 16 or higher. The newest value I found anywhere is 15 (Montemanni-Smith-Koul 2014, matching the live table).

## 4. This repo (https://github.com/elder-plinius/V3R1T4S)

- TROPHY_CASE.md: fetched from https://raw.githubusercontent.com/elder-plinius/V3R1T4S/HEAD/TROPHY_CASE.md at 2026-10-17T23:09:32Z (HTTP 200, 31235 bytes). It contains no line matching `dna`, `GC`, `king` or `rambutan`.
- Open PRs: fetched from https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 at 2026-10-17T23:09Z (HTTP 200, 61 open PRs). No title or body mentions DNA, GC-content, GC,RC, or the King table. An issue/PR search for `dna` returned only #289 (closed), which is about minimizer density and is unrelated.

## 5. Sources not read because of a paywall, login or block

- https://export.arxiv.org/api/query?... (arXiv API full-text search, sorted by date): blocked by HTTP 429 (rate limit). The plain-HTTP attempt returned 301; the HTTPS retry got the 429. I did not retry further. Recent arXiv coverage therefore depends on web search plus the individual papers listed above.
- https://www.sciencedirect.com/science/article/pii/S0012365X11005280, https://pure.southwales.ac.uk/files/991721/PhD_thesis_Niema.pdf and http://orlabanalytics.ca/lnms/archive/v6/lnmsv6p167.pdf: `sources/SOURCES.md` says these returned HTTP 403 to an automated client. I did not request them myself; I read the human-supplied copies in `sources/`.
- I did not attempt subscription databases (Scopus, Web of Science, MathSciNet, Google Scholar citing-works lists). A literature search cannot prove that no result exists.

## Verdict

The object is valid. 16 strictly exceeds the live King-table entry (15^v, fetched once, HTTP 200) and every post-2010 published value I found for (20,15): 15 in DM 2012 Table 9 (max over w), 15 in the 2011 thesis, and 15 in LNMS 2014. None of the 2024-2026 arXiv papers checked, TROPHY_CASE.md, or the 61 open PRs reports a code at these parameters. This is a strict improvement, not a tie. Residual risk: the arXiv API was rate-limited and subscription indexes were not searched.

pass: true
