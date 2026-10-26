# NOVELTY skeptic — dna-codes-gc-king-table, A_4^GC(15,11,7)

context: subagent (fresh knowledgeWork context, inputs claim/ only, plus public web)
injection_suspected: no (no page read contained instructions aimed at the reviewer)

## Claim under test
claim/CLAIM.md: objects/A4GC_15_11_7_M42.txt has 42 words, n=15, GC weight w=7, pairwise Hamming distance >= 11,
so A_4^GC(15,11,7) >= 42 vs. the King/Gaborit GC-only table entry 34. The GC,RC table is not claimed.

## 1. Status source — one honest fetch (no retries)
- URL: https://rambutan.umassmed.edu/king/dnacodes.html
- Fetched once with curl at 2026-10-25T08:42:10Z (09:42 Europe/Madrid): HTTP 200, 18096 bytes,
  sha256 25d6e9f88262fbb07c95841225cb3202aa29eb31f7f72d24b43e9c595bdb18c5 — identical to claim/data/dnacodes.html.
- First table, heading "Lower bounds for A_4^GC(n,d,w):", row 15, 9th cell (d=11), raw HTML:
  `<td>  34<sup>v </sup></td>` -> value **34**, superscript v ("variable neighborhood search from [MS] or [MS2]"),
  no '.' or ':' (so not marked optimal). Row neighbours: d=10 "124 x", d=12 "15 v".
- Page footer: "Last updated June 23, 2010". The second table (A_4^GC,RC) has 18 at (15,11); not the claimed problem.

## 2. Literature (any lower bound >= 35 for (n=15, d=11) with GC?)
| Source | Read? | Value at (15,11) | >=35? |
|---|---|---|---|
| Smith-Aboluion-Montemanni-Perkins (SAMP), Discrete Math 311 (2011) 1207-1219, doi:10.1016/j.disc.2010.03.005 | Publisher PDF: HTTP 403 (sciencedirect pdfft). Its results are read via (a) King's table, which cites it as [SAMP] ("x"), and (b) the Aboluion thesis below, which holds the same constructions | thesis's own algebraic best (cosets/shortening, superscript "a"): **31**; table entry 34 is "v", not "x" | no |
| N. Aboluion, PhD thesis, Glamorgan 2011 (pure.southwales.ac.uk ws/portalfiles/portal/991721/PhD_thesis_Niema.pdf), fetched 2026-10-25T08:42:52Z, sha256 c58666c3…bed3 (same as scout) | yes | "Best known lower bounds for max_w(A_4^GC(n,d,w)) 3<=d<=11", row 15: `... 240  124  34m2` (m2 = VNS/SA from Montemanni-Smith). This is the max over w, so it also bounds w=7 | no (34) |
| Aboluion-Smith-Perkins, Discrete Math 312 (2012) 1062-1075, doi:10.1016/j.disc.2011.11.021 (GC + reverse complement) | **Full text not readable: ScienceDirect pdfft HTTP 403, core.ac.uk download HTTP 403, CORE page timed out. PENDING STATUS CHECK for its own pages.** Abstract read (Pure / ScienceDirect landing page): it is about the GC,RC problem. Its GC,RC values appear in the thesis's GC,RC tables (n=15, d=11: 18gk) and in the 2016 survey (Table XIII, n=15, d=11: 18) | GC,RC 18 (secondary). A GC,RC bound would also be a GC bound, and 18 < 35 | no, by secondary sources; primary unread |
| Montemanni-Smith-Koul, LNMS 6 (2014) 167-175 (orlabanalytics.ca/lnms/archive/v6/lnmsv6p167.pdf), fetched 2026-10-25T08:43:30Z, sha256 8b715b52…d658 | yes (Table 1 is an image; read from the rendered image) | Table 1 "Lower bounds for A4GC(n,d,w)", n=15, d=11: V = **34^N** (bold = new best), B = 30. Table 2 (GC,RC) n=15 d=11: V 16, B 18 | no (34) |
| Limbachiya-Rao-Gupta, "The Art of DNA Strings: Sixteen Years of DNA Coding Theory", arXiv 1607.00266, fetched 2026-10-25T08:44:07Z | yes | only GC,RC (Tables XII-XIII) and RC (Table XIV) tables; GC,RC n=15 d=11 = 18; no GC-only table | no |
| Limbachiya-Gupta-Aggarwal, IEEE Comm. Lett. 22(10) 2018, altruistic algorithm (GC + no-run + Hamming) | IEEE full text not tried (paywalled). Its Table is reprinted "with permission" as Table 6.1 in D. Limbachiya's PhD thesis (guptalab.org …/dixitaphd.pdf, fetched 2026-10-25T08:44:16Z): rows n=4..13, d=2..10 only. Frontiers/PMC 2023 (PMC10067891) also says: "The altruistic algorithm … obtained results by utilizing 4 <= n <= 13 and 1 <= d <= 13" | no entry for n=15 (and its problem adds a no-run constraint, i.e. it is a subset) | no |
| arXiv 1903.03535 (Sangroniz-Martinez, GC-content of Galois-supplemented cyclic codes), read 2026-10-25 | yes | only improves A_4^GC,RC bounds: (17,4), (17,7), (13,5), (29,11). Nothing at (15,11) | no |
| arXiv 2108.02033 (Korban-Sahinkaya-Ustun, reversible G^k-codes), read 2026-10-25 | yes | tables for n in {16,24,32,36,48,56,60,64,72} only, RC and RC,GC | no |
| Later work found by search: arXiv 2403.11551, 2409.06519, 2510.01750 (algebraic, n mostly >=16 or no table at n=15); Rasool et al. 2023 MFOS (PMC10067891, n<=13, with a no-run constraint); Cao et al. KMVO/DMVO 2020 (n<=10, per PMC10067891) | snippets / abstracts / PMC text | none at (15,11) | no |

Repo checks: this repo's TROPHY_CASE.md has no DNA / GC entry. Open pull requests at github.com/elder-plinius/V3R1T4S
(read 2026-10-25 ~08:43Z, searches "is:pr is:open dna" and "dna-codes-gc-king-table n=15"): GC-only claims are only at
(10,7), (13,9), (13,10); nothing at (15,11).

## 3. Spot check (not this skeptic's job; REPRODUCE does the real check)
objects/A4GC_15_11_7_M42.txt: 42 distinct words, all of length 15 over {A,C,G,T}, all with GC=7, min pairwise distance 11;
sha256 7164f7dd…5089 matches claim/REPRODUCE.md.

## Verdict
The best value at (n=15, d=11) in the live table is 34 (fetched 2026-10-25T08:42:10Z), and it matches every source I could
read: Aboluion 2011 max_w 34m2, Montemanni-Smith-Koul 2014 34^N. Nothing I found reaches 35 at (15,11) with GC, with or
without RC. 42 > 34, a strict improvement, not a tie.
Caveat: the primary full text of Aboluion-Smith-Perkins 2012 and of SAMP 2011 could not be opened (403), so those two are
PENDING STATUS CHECK for their own pages. Both are covered indirectly: the 2012 paper is GC,RC (n=15 d=11: 18 in the
thesis, the survey and MSK 2014), and SAMP 2011 predates and feeds the 34 (King cites [SAMP]). The status source itself was
read, so per RUN.md step 6 this does not force PENDING on the whole check.
novelty: strictly beats all known values read (42 > 34)
pass: true
