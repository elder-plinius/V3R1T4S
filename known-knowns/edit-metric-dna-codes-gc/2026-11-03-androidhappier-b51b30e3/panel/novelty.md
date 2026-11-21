# Panel: NOVELTY. Run 2026-11-03-1435-dnaedit93, cell (9,3)

context: subagent (novelty). Fresh context. I did not read the other panel files or the hunt REPORT.
Scratch copy: [workspace]/scratch/panel-dna93-novelty-151037/claim/ (copied 15:25 EST). Below, file paths are relative to claim/.
I checked the object hash: `sha256sum object/code_n9_d3_k1042.txt` = b51b30e3082648bc6cb0511bd156b71ae51c967f7281a83010d2c0e844e4a93a, 1042 lines (matches CLAIM.md).
Object validity is not my role. I did not re-run the checkers.

## 1. Primary status fetch (one fetch, no retries)
- URL: https://brocku.scholaris.ca/server/api/core/bitstreams/afcc7fb0-758c-4e61-be7a-b5536c9f7fb6/content (DSpace extracted text of
  J. Sun, "Bounds on Edit Metric Codes with Combinatorial DNA Constraints", M.Sc. thesis, Brock, (c)2009, supervisor S. Houghten).
- Time: 2026-11-03 20:25Z = 15:25 EST (box clock read right after the fetch: 15:25:36 EST). Tool: WebFetch, one call, HTTP OK, full text returned.
- Table 7.1 "Best-known Bounds on DNA Codes", row 9, verbatim tokens: `9 32256 15558g 939g 161g 34e lle 5e,g 2 1`
  -> (9,3) = **939**, superscript g. The legend says g means "the best known bound was found by Randomized GA" (a lower bound).
  The cell is not exact and not marked optimal.
- Table 5.2 (Exhaustive Search), row 9: `9 32256 13672* 914* 150* 34* 11 5 2 1` -> (9,3) = **914***. The legend: "* = exhaustive search
  did not finish within two weeks. Thus these values provide lower bounds".
- Same cell in the other tables: Table 5.1 (lexicode) 912. Table 6.4 (RGA Rc=1.0, Rm=0.0) 939. Table 6.5: 869. Table 6.6: 855.
- Constraint set (Sec 1.5): d_edit(x,y) >= d for x != y; d_edit(x^RC, y) >= d for all x, y, including x = y; GC weight w = floor(n/2) = 4.
  This matches CLAIM.md.
- The thesis has no numeric upper bound for (9,3). It gives only Theorem 3, E^{RC,GC} <= 1/2 E^{GC}.
- Neighbour cells in row 9 / column 3: (8,3) = 324g, (9,4) = 161g. Nothing in the thesis implies a value >= 1042 for (9,3).

## 2. Literature and code checks (this session, 15:25-15:30 EST)
| source | how opened | finding for E_4^{RC,GC}(9,3,4) |
|---|---|---|
| Houghten quaternary edit table https://cosc.brocku.ca/~houghten/quaternaryedit.html | WebFetch, read in full | Covers UNCONSTRAINED E_4(9,3) only: 3451-9360. No GC or RC constraint, so it is not a bar. Consistency check: C ∪ C^RC has 2084 GC-4 words at edit distance >= 3, which is <= 9360, so no contradiction. Its change log (to 2017) lists no DNA GC+RC values. |
| Houghten publication list https://cosc.brocku.ca/~shoughten/papers.html | WebFetch | The only GC+RC edit-metric bounds paper is Sun, Houghten & Ross, Congr. Numer. 204 (2010) 65-92, the journal version of the thesis. The other edit-DNA papers (Ashlock/Houghten CIBCB 2005/2009/2015/2017, ACM-BCB 2010, Biosystems 2012, Orth & Houghten CIBCB 2011/2017) appear from their abstracts and the change log to be about unconstrained or GC-only "embeddable biomarker" codes. |
| arXiv:1505.06262 (Bennenni, Guenda, Gulliver) | search snippets (ar5iv) | Only relational bounds (Thm 9, Props 11-15) and Hamming lexicode tables. No numeric (9,3) edit value. |
| Orth M.Sc. thesis / Salmon algorithm (hdl 10464/3929) | search snippet | Unconstrained E_4 and fixed-GC (GC 3-5) edit codes for n = 6-8. No n = 9, no RC. |
| arXiv:2510.01750 (Benerjee & Gupta, 2025 book chapter) | WebFetch | Hamming-metric constraints only. Not a bar. |
| PMC10067891 (2023, evolutionary DNA codes), arXiv:1607.00266, arXiv:2409.06519, Gaborit-King, Montemanni LNMS v6, EJC King 2003 | search snippets | All Hamming metric (e.g. (9, d_H=3) GC,RC = 906). Different metric, not a bar. |
| Benerjee & Banerjee, ISIT 2025, "Single Edit Error-Correcting DNA Codes with Multiple Biological and Combinatorial Constraints" (doi 10.1109/ISIT63088.2025.11195495) | full text NOT opened (doi 403; mirrors 429/504); abstract via search synthesis | Algebraic, Tenengolts-type construction with extra homopolymer and secondary-structure constraints. Per the abstract, the RC/R constraints are Hamming-type. So this is a different constraint set, and I saw no size for n = 9. Residual. |
| Web searches (several queries) for 2024-2026 edit/Levenshtein GC+RC tables | WebSearch | No later edit-metric GC+RC value for (9,3) found. |

## 3. Repository checks
- Local repo/ (HEAD 9a0d19a, 2026-11-02): TROPHY_CASE.md has no DNA or edit-metric entry. No known-knowns/ entry for edit-metric-dna
  (rg hits are unrelated targets). known-unknowns/biology/edit-metric-dna-codes-gc.md says "open as of 2026-10-15".
- Live GitHub (fetched 15:26-15:29 EST): raw TROPHY_CASE.md on main has no DNA edit entry. The known-knowns/ listing from the contents API
  has no edit-metric-dna folder.
- PRs, open and closed, via the GitHub search API (unauthenticated):
  - "edit-metric": 0 results.
  - "levenshtein": 2 results, both unrelated.
  - "dna": 17 results. All are minimizer or Hamming king-table targets (dna-codes-gc-king-table, dna-codes-gc-rc-king-table), none for this target.
  - Literal "edit-metric-dna-codes-gc" (issues and PRs): 0 results.
  - "939": 3 results, all unrelated.
- gh CLI is not logged in. I used the public API and pages instead.

## 4. Comparison and verdict reasoning
- Published bar for the exact cell and constraint set: 939 (Table 7.1, g). Other values for the same cell: 914*, 912, 869, 855.
- Claimed: 1042 > 939 (+103, +11.0 %). This is strictly larger, not a tie.
- Trivial-edit check: the thesis publishes no codeword list for (9,3). The claim object comes from a fresh orbit-graph tabu search
  (search/, per CLAIM.md), not from extending a published object. No published neighbour-cell object implies >= 1042 here.
- I found no later value (2010-2026, including the last 24 months) for this cell that is >= 1042.

## Residuals (not opened)
1. Congr. Numer. 204 (2010) 65-92, Sun, Houghten & Ross, the journal version of the thesis. Only the index pages were reached
   (combinatorialpress vol204, MaRDI). No full text, and zbMATH sits behind a Cloudflare challenge. It adds a frame-shift constraint and could
   in principle carry an updated (9,3) value. This is the main residual risk.
2. Orth & Houghten, CIBCB 2011 (Salmon algorithm) full text. The abstract mentions "codes obeying biological restrictions".
3. Ashlock/Houghten CIBCB 2009/2015/2017, ACM-BCB 2010, and Biosystems 2012 full texts. Their tables are reflected in the Houghten
   unconstrained table change log, but I did not read them for GC+RC.
4. Benerjee & Banerjee, ISIT 2025 full text (paywalled; mirrors rate-limited).

pass: true
