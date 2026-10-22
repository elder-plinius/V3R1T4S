# Novelty skeptic: dna-codes-gc-king-table, cell (n,d) = (10,7), w = 5

context: subagent (Claude Code Agent tool, general-purpose)

Claim under review (claim/CLAIM.md): the 44 words in claim/gc_n10_d7_m44.txt form a quaternary code of length 10,
exactly 5 G/C per word, minimum Hamming distance 7; the table value is 34 (superscript v).

## 1. Status page (one honest fetch, no retries)

- URL: https://rambutan.umassmed.edu/king/dnacodes.html
- Time (date -u): request sent 2026-10-19T16:59:33Z, finished 2026-10-19T16:59:35Z
- HTTP status (curl -w '%{http_code}'): 200
- Bytes: 18096; sha256 25d6e9f88262fbb07c95841225cb3202aa29eb31f7f72d24b43e9c595bdb18c5
  (identical to the author's claim/king_table_live_refetch.html)
- First table ("Lower bounds for A4^GC(n,d,w)"), row n=10, column d=7, verbatim cell: `34<sup>v  </sup>`
- Value: 34, superscript v (variable neighbourhood search, [MS] Montemanni-Smith 2008 or [MS2] 2009).
  No '.' and no ':' follows it, so the cell is open (not proven optimal).
- No instructions found in the page; no injection suspected.

## 2. Montemanni-Smith-Koul 2014, Table 1 (claim/msk2014_table1_gc.png)

Read directly from the image, row n=10, column d=7:
- V (their result) = **34** (bold)
- B (previous best) = 32

So the 2014 post-2010 value is 34, equal to the King table value.

## 3. Literature search (values for A_4^GC(10,7,5) >= 44?)

| source | URL | time (UTC) | status | read? | (10,7) finding |
|---|---|---|---|---|---|
| Chee & Ling 2008, IEEE TIT 54 | https://arxiv.org/pdf/0803.3657 | 2026-10-19T17:00:13Z | 200 | yes, full | Table II is GC,RC only: A^GC,RC(10,7) = 16. No GC (weak) value at (10,7); only GC remarks are (9,5,4) >= 134 and (10,4,5) >= 1710. |
| Smith-Aboluion-Montemanni-Perkins, Discrete Math 311 (2011), doi:10.1016/j.disc.2010.03.005 | https://doi.org/10.1016/j.disc.2010.03.005 -> https://linkinghub.elsevier.com/retrieve/pii/S0012365X10000749 | 17:00:14Z / 17:00:34Z | 302 then 200 | NO (200 is a JavaScript "Redirecting" stub, no article text) | not read directly; content covered by the thesis below and by the King table's 'x' entries |
| Aboluion 2011 PhD thesis (Glamorgan), on which SAMP is based | https://pure.southwales.ac.uk/ws/portalfiles/portal/991721/PhD_thesis_Niema.pdf | 2026-10-19T17:01:05Z | 200 | yes, full (sha256 c58666c3...bed3) | Table 10.69 (best known max_w A^GC, n<=20): (10,7) = 34_m1. Table 10.65 (its own linear constructions): (10,7) = 12. Table 10.27 after shortening/puncturing: (10,7) = 12. Nothing >= 44. |
| Limbachiya-Rao-Gupta, arXiv 1607.00266 | https://arxiv.org/pdf/1607.00266 | 2026-10-19T17:00:13Z | 200 | yes, full | Has only GC+RC tables (XII, XIII) and HD+RC (XIV); GC,RC (10,7) = 17. No plain A^GC table. |
| Conflict-free DNA codes, arXiv 1902.04419 | https://arxiv.org/pdf/1902.04419 | 2026-10-19T17:00:14Z | 200 | fetched, not assessed in detail | stricter constraint set (adds homopolymer/conflict rules), so its codes are also GC codes; not read, so any (10,7) value in it is unchecked |
| 2024-2026 papers | WebSearch (4 queries on constant-GC DNA code lower bounds, 2024/2025, arXiv) | 2026-10-19 ~16:59-17:01Z | n/a | search results only | no 2024-2026 paper giving A^GC(10,7,5) found; hits were 2003-2023 (King, Chee-Ling, MS 2008, 1903.03535 GC,RC, 2108.02033 long lengths, 1902.04419) |

## 4. Repository checks

- TROPHY_CASE.md: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md,
  2026-10-19T17:00:35Z, HTTP 200, 31235 bytes. Zero lines matching dna / dnacodes / GC-content.
  No DNA-code entry, so nothing at (10,7).
- Open PRs: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 (page 1, 17:00:35Z, 200),
  pages 2 and 3 via the Link header (17:00:42Z and 17:00:43Z, both 200). 260 open PRs; 12 DNA-related.
  - No open PR for dna-codes-gc-king-table at (10,7). GC-table PRs are #490 (13,9) and #489 (13,10).
  - #493 is dna-codes-gc-rc-king-table GC,RC (10,7,5) with 20 words. A GC,RC code is also a GC code, so that
    gives A^GC(10,7,5) >= 20 < 44; it does not tie or beat the claim.
  - #392 (bank pitfalls for the GC,RC entry) is about GC,RC cells; nothing at GC (10,7).

## 5. Independent sanity check of the object

Own script (not author_checker.py) on claim/gc_n10_d7_m44.txt: 44 lines, 44 distinct, all length 10 over {A,C,G,T},
GC-content set = {5}, minimum pairwise Hamming distance = 7. The object is what it says.

## 6. Decision

Best value known for A_4^GC(10,7,5), from everything I could read: 34 (King table, live, 34^v; MSK 2014 V row;
Aboluion 2011 Table 10.69). Claimed 44 > 34 strictly. Not a tie.

Gaps that affect confidence:
- SAMP (Discrete Math 2011) not readable (Elsevier JS stub). Low impact: its constructions are linear/nonlinear
  codes summarised in the Aboluion thesis (best own (10,7) value 12), and the King table already includes SAMP ('x').
- The 2024-2026 search was web search only (no Scholar / paywalled databases). A recent paper with a value of 44+
  that is not indexed by these searches cannot be excluded. Nothing found suggests one exists.
- Side note for the panel (not a novelty issue): claim/W_CONVENTION_AND_REFETCH.md talks about n = 11 and (11,8),
  apparently copied from another claim; it does not change the (10,7) w = 5 = floor(10/2) convention.
- The jump from 34 to 44 is large for a cell attacked by VNS, but the code checks, so this is a plausibility note only.

Within the sources I could read, the claim strictly beats everything known.

pass: true
