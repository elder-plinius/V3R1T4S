role: criterion
context: subagent (Agent tool, fresh context, model claude-opus-5-5), saw only claim/

# Criterion verdict: spherical-codes-cohn-table, (d, N) = (6, 256)

Bottom line: I checked every conjunct of the bank criterion (claim/CLAIM.md) against the saved claim-moment files, using my own code written before I ran claim/checker/, and every one holds. The claim is for the full criterion. It is not partial win p1, p2 or p3, and nothing in the files subsumes it. No network requests were made.

Method: I wrote my own scripts first (work-criterion/my_check.py, my_arxiv.py, my_vahteristo.py, my_null.py, my_diff.py) and saved their outputs (work-criterion/*.out). Only after that did I run the REPRODUCE.md commands from inside claim/ (work-criterion/reproduce_run.txt). Diffed against claim/expected_output.txt, the only differences are the echoed command lines (shell quoting and glob expansion); every output line is identical (work-criterion/reproduce_diff.txt). checker/arxiv_read.py reproduces inputs/arxiv/arxiv_read.out byte for byte (work-criterion/arxiv_read_diff.txt is empty). Every saved input matches the sha256 in TABLE_RECORD.md, FETCH_RECORDS.md and ARXIV_RECORD.md (work-criterion/sha256_all.txt).

## Conjuncts, one by one

| # | conjunct (bank wording) | finding (own code) | evidence |
|---|---|---|---|
| 1 | (d, N) row present in the live /plain | `6,256,0.704931969352` is the only line for (6, 256) among the 15262 /plain rows, with no duplicates and no polynomial column | work-criterion/my_check.out |
| 2 | coordinates given to >= 20 digits | 256 lines of 6 tokens. All 1536 coordinates have exactly 26 significant digits (min 26, max 26), and none is zero | work-criterion/my_check.out |
| 3 | normalise in mpmath at 50 digits, c* = max pairwise inner product | c* = 0.7048987224974410014732802770067601805699 at pair (55, 247), over 32640 pairs. The exact-rational recomputation gives the same value to 40 digits | work-criterion/my_check.out |
| 4 | STRICTLY LOWER than the table's 12-decimal cosine by >= 1e-10 | table − c* = 0.00003324685455899852672. Exact rationals: 0 pairs have cosine above 0.704931969352 − 1e-10 | work-criterion/my_check.out |
| 5 | table value re-fetched live immediately before claiming | fetch-log lines: index 2026-10-25T06:26:36Z, /plain 2026-10-25T06:26:38Z (TABLE_RECORD.md, FETCH_RECORDS.md). File times in claim/ (UTC): the object, checkers and inputs were copied at 06:26:34Z (−3 s); the templates and finalize.py were last modified at 06:25:43Z (−54 s); the table pages were written at 06:26:39Z (+2 s); CLAIM.md and TABLE_RECORD.md at 06:26:40Z (+3 s); expected_output.txt at 06:26:44Z (+6 s). The rendered .md files differ from build/templates/ only in filled placeholders | work-criterion/timing.out, work-criterion/file_times_utc.txt, work-criterion/template_diffs.txt |
| 6 | the index row has NO '&ast;' | the one index row is `<td>6</td> <td><a href="/data/6/256">256</a></td> <td>0.704931969352</td> <td>Pavlos Moros, 2026.</td>`. It has no '&ast;' and no '*'. To show the test is not vacuous: 32 index rows do carry '&ast;' | work-criterion/my_check.out |
| 7 | the row does NOT contain 'needs more optimization' | absent (case-insensitive), and the row has no 'optimiz' at all. 4591 other rows carry the label | work-criterion/my_check.out |
| 8 | not superseded by a newer arXiv result for (6, 256) | see the section below: within the saved files, no arXiv source has a (6, 256) code at or below c* | work-criterion/my_arxiv.out, my_vahteristo.out, my_improvevolve.out, my_fulltexts.out |
| 9 | not a kissing-number configuration (9 <= d <= 23 and c* <= 0.5) | d = 6, so the clause does not apply; c* is also above 0.5 | work-criterion/my_check.out |
| — | propagated bar (d' <= 6, N' >= 256) | /plain has 2966 such rows and the index 2967 (the index adds (6, 990)). In both the minimum is (6, 256) at 0.704931969352, and no row is at or below c* + 1e-10. In arXiv:2610.19988's three tables (3076 such rows each, md5 matching the Zenodo record) the minimum is again (6, 256): combined 0.7049931928409804, per_instance 0.7050249538274573, global 0.7053373293588499. The smallest margin over c* is 9.447034353937678e-05. ImprovEvolve's 90 cells all lie in d = 8..16 | work-criterion/my_check.out, my_vahteristo.out, my_improvevolve.out |

## Clause 8: what the saved arXiv files can and cannot show

- **What the feeds cover.** Each feed's opensearch totalResults, the entries returned and the oldest entry returned:
  - "spherical code": 154 results, 100 returned, oldest 2015-09-17
  - Tammes: 474 results, 100 returned, oldest 2023-07-31
  - kissing: 132 results, 100 returned, oldest 2011-11-15
  - (spherical code OR Tammes) AND 256: 3 results, all from before the window
  
  That gives 146 unique entries published or updated on or after 2024-10-25 (work-criterion/my_arxiv.out).
- **Mentions of 256 in the window.** In titles, abstracts and comments, 256 appears only in 2603.10425 and 2411.04916. Both are kissing numbers in dimensions 17 to 21, where 256 is the size of an improvement.
- **Mentions of dimension 6.** Only two entries match: 2606.18984 (60-vector blocks in R^6 inside R^12) and 2609.12640 (contact graphs of kissing configurations in dimensions 5 to 7).
- **Abstracts I read myself.** I read the abstracts of 2610.19988, 2602.10233, 2609.35051, 2608.23691, 2606.10402, 2511.17592, 2609.34845, 2510.06960, 2610.21263, 2609.25288, 2602.01638 and 2510.23609 (work-criterion/abstracts_selected.txt). None posts a code in R^6 with 256 or more points. 2610.19988 is the only one that covers (6, 256), and its values are worse than the table (row above).
- **Full texts.** PackingStar (2511.13391v5) names 6-dimensional configurations of 27, 54, 60 and 72 points only, and has no "dimension 6" or "Tammes" passage. 2411.16038v1 has no "256" and no dimension-6 passage (work-criterion/my_fulltexts.out).
- **What the files cannot show:**
  - arXiv after the feeds' times (about 2026-10-25T05:54Z)
  - papers whose title, abstract or comment lacks the query words
  - papers first submitted before the oldest entry a feed returned and revised inside the window (for the Tammes feed, 374 entries were not returned)
  - the full texts of every paper except the three read here
  - the coordinate files behind 2610.19988's cos values (the zips were not saved, so those values are the author's double-precision maxima)

## Null models and controls

- **The table value is real.** The posted code (inputs/posted_6_256.txt) reproduces the table value: at 50 digits its c* is 0.7049319693516105338952118, which rounds to 0.704931969352, and table − posted c* = 3.89466e-13. The gain is therefore not a rounding artefact of the table's 12 decimals (work-criterion/my_null.out).
- **Where the gain comes from.** The claimed code is a local polish of the posted code. Matched row by row, the normalised points moved by at most 0.0552438 (mean 0.0228845). The posted code was visibly unconverged: it has 1 pair within 1e-14 of its maximum and 998 within 1e-8, while the claimed code has 1331 within 1e-14 (work-criterion/reproduce_run.txt).
- **Hidden-quantifier note on the label.** The criterion decides convergence only by the literal 'needs more optimization' label, and this row is an unlabelled upload. Literally that makes the result a claim and not p2. CLAIM.md discloses the unconverged start. A reader who applies the spirit of p2 might rate the win as an easy one. That reading does not change the literal verdict.
- **Hidden-quantifier note on digits.** The 26 digits are binary64 values printed with `%.25e`: 1536 of 1536 coordinates round-trip (work-criterion/my_null.out). So only about 17 digits carry information. The criterion asks for coordinates given to >= 20 digits, which the file meets, and c* is computed from the file exactly as written.

## Other observations (none changes the verdict)

- **check_exact.py margins.** Its printed lines test ±1e-11, while its VERDICT line uses the bar table − 1e-10. My own exact check at table − 1e-10 found 0 violating pairs, so the CLAIM.md statement holds.
- **arXiv cache.** The `<updated>` field of inputs/arxiv/arxiv_2610.19988_meta.xml reads 2026-10-25T04:59:51Z, while the fetch log gives 05:54:20Z. This is probably a cached arXiv API response.
- **Table edits during the night.** Between this run's three reads (05:50:23Z, 06:05:37Z, 06:26:36Z), rows (13, 597), (13, 599) and (14, 300) changed through uploads by an anonymous user. The (6, 256) row is identical in all three reads, and no changed row has d' <= 6 and N' >= 256 (work-criterion/my_diff.out).
- **Text addressed to reviewers.** No file in claim/ addressed instructions to a reviewer (work-criterion/injection_scan.txt). injection_suspected: none.
- **Partial wins.** The result is not p1 (d is not 3), not p2 (the row is unlabelled, and this is a single row rather than a batch of 20) and not p3 (it is not an exact-angle certificate). It is a full-criterion claim.

confirmed_scope: In the claim package's saved pages, fetched 2026-10-25T06:26:36Z (index) and 06:26:38Z (/plain), 3 s before CLAIM.md was written according to the file times, the 256 vectors of object/code_6_256.txt (26 significant digits per coordinate), normalised in mpmath at 50 digits, have c* = 0.7048987224974410014733 at pair (55, 247), which is 0.00003324685455899852672 below the unstarred, unlabelled /plain row 6,256,0.704931969352 (exact-rational check: no pair above 0.704931969352 − 1e-10) and below every row with d' <= 6 and N' >= 256 in /plain, in the index and in arXiv:2610.19988's three tables; no saved arXiv feed or full text shows a (6, 256) code at or below c*, and d = 6 lies outside the kissing clause; not confirmed are the row's live state after 06:26:38Z (my timing check ran 21.8 minutes after that fetch), any arXiv paper posted after about 05:54Z or missed by the saved title and abstract feeds, and the truth of the fetch-log lines beyond their sha256 matching the saved bytes.

pass: true
