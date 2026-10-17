# Novelty skeptic report: labs-merit-factor-records, L = 377
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: NEW: E=9452 < 9668 (minimum over every published L=377 value found: Dimitrov arXiv:2206.12070 row L=377, E=9668; the named tables of arXiv:2607.09688, arXiv:2504.00987 and the Boskovic repository have no L=377 row; no newer arXiv paper, TROPHY_CASE.md row or pull request covers L=377)

Times are UTC from `date -u` on this machine (about one minute behind the Date header arXiv returned). Claim files are named relative to claim/ (sequence.txt, parent.txt, baseline.tsv, check_energy.py, CLAIM.md, TROPHY_CASE.md). Scratch files are in work/.

## 1. Exact recomputation (no network)
- `python check_energy.py "$(cat sequence.txt)"` printed `377 9452`.
- My own integer code (work/recompute.py) agrees: L = 377, alphabet {0,1}, E = 9452, F = 142129/18904 = 7.518461701227253. E is unchanged under negation and under reversal (9452 both). max |C_k| = 21. The sequence is skew-symmetric (s[m+j] = (-1)^j s[m-j] for all j), as expected for an edit of a skew-symmetric parent.
- Parent (parent.txt): length 379, E = 9789 (F = 7.336857697415466). `parent[1:-1] == sequence.txt` is True.
- sha256 of sequence.txt: 3d5479897f41072e607194f037190cf3c8536ad0c6f59978bce66a6127dc7c0c.

## 2. Status source, fetched once
- Command: `curl -s -A "V3R1T4S-novelty-skeptic/1.0 (+https://github.com/elder-plinius/V3R1T4S)" https://arxiv.org/abs/2607.09688`
- URL: https://arxiv.org/abs/2607.09688. Time: 2026-10-17T00:27:06Z. HTTP 200, 43398 bytes, sha256 c14c75eae85c1e30dcedf2fc98aa5295188e681aef1f15020b5e4e7c45c4420c (work/abs_2607.09688.html).
- Value found: "Prioritizing Search Space Regions in the Low Autocorrelation Binary Sequences Problem" (Psenicnik, Boskovic, Popic, Brest); "[Submitted on 17 Jun 2026]"; submission history lists only "[v1] Wed, 17 Jun 2026 09:17:04 UTC (752 KB)". Abstract: improves the previous best-known results "for 35 sequence lengths in the range 450 <= L <= 527 and for L=573", and gives a sequence with merit factor above 8.0 at L=451.
- The page was served from a CDN cache (Age header about 16 days, Last-Modified Mon, 24 Aug 2026), so I cross-checked freshness: the live arXiv API listing (section 4, 00:29:52Z) shows 2607.09688v1 with published = updated = 2026-06-17, and the source download is named arXiv-2607.09688v1. No v2 existed at that time.
- The status source was readable, so this is not a PENDING STATUS CHECK case.

## 3. The sources named by the bank criterion, checked for L = 377
| source | how read | UTC | status | L = 377 row? | coverage seen |
|---|---|---|---|---|---|
| arXiv:2607.09688 TeX source (v1) | `curl .../src/2607.09688` | 00:27:40Z | HTTP 200, sha256 738c297c53b58cbd7ed4cddd7a05f25e379604427d201e2354471bebe47b43a0 | no | TAB_RECORDS.tex has 35 distinct lengths, min 450, max 573: 450-452, 455-465, 475-484, 490, 491, 494-498, 516-518, 573. No "377" anywhere in the source. |
| arXiv:2504.00987 TeX source (v2) | `curl .../src/2504.00987` | 00:28:30Z | HTTP 200, sha256 bc0b444f8dddf0a13c28c5e4ee8a75cc034befada7231d4047797af80c72f5cd | no | Results for 92..120 only (row-leading integers in main.tex run 20..120). It cites the Boskovic archive as https://github.com/borkob/git_labs. |
| Boskovic et al. records repository | `git clone --depth 1 https://github.com/borkob/git_labs.git` | 00:28:48Z | exit 0, HEAD 1aa123407636e48630174e0bf122037e369c1d68 (2020-09-15, "results 2018") | no | results-2016/2016-labs-skew.txt and results-2018/2018-labs-skew.txt: 124 skew-symmetric rows, L = 5..449; lengths above 300 are 301, 303, 341, 381, 401, 449 only. Knauer 2004 table stops at 304. Every "377" hit in the repository is an energy value for L = 83. I recomputed the energies of the rows with L >= 300 and they match the printed values. |
| newer arXiv results | arXiv API, 2 queries | 00:29:52Z, 00:30:35Z | HTTP 200 both | no | see section 4 |

Under the bank's literal rule (minimum over the tables of the named sources) there is no L = 377 entry at all, so the operative baseline has to come from the wider literature. The bank text itself says "Lengths 121..449 and above 527 may be softer" and warns that tables are scattered; the claim correctly used Dimitrov's table as the baseline.

## 4. Newer arXiv results (arXiv API, metadata only)
- Query 1 (00:29:52Z, HTTP 200, 23 results, sha256 fe2b6e26fb025de2275f87d7a08d53e6e963b450520f4f8c20a242ea487065b2): `export.arxiv.org/api/query?search_query=all:"low autocorrelation binary sequences"&sortBy=submittedDate&sortOrder=descending&max_results=100`.
- Query 2 (00:30:35Z, HTTP 200, 40 results, sha256 b16a5c8e17b8de508a970afdb497d0aaeac0940f44690c164585b7f7d2b6bc0c): merit factor AND (binary OR sequences OR autocorrelation), OR "autocorrelation binary sequence", OR "skew-symmetric binary", newest first.
- Papers since Sep 2024 (I read each abstract): 2610.14361 (9 Oct 2026, subsystem heuristics, N in 27..60), 2609.05771 (4 Sep 2026, crosscorrelation demerit-factor moments, theory), 2607.09688 (17 Jun 2026, 450..573), 2511.05778 (TOPSIS-like mutation, evolutionary), 2511.04553 (quantum-enhanced MTS, N in 27..37), 2510.24237 (PUBO solver benchmark), 2506.17391 (qubit-efficient solver, N up to 45), 2504.11549 (QPE-QITE), 2504.01694 (QAOA schedules), 2504.00987 (92..120), 2409.20538 (annealing), 2409.07222 (Dual-Step, 450..527). None reports an L = 377 sequence or any record near that length. The only two papers newer than 2607.09688 are 2609.05771 and 2610.14361, neither a record table.
- That was 6 arXiv-host requests in total (abs, src x3, API x2), at 00:27:06, 00:27:40, 00:28:30, 00:29:52, 00:30:35 and 00:31:05 UTC (the last one is the 2206.12070 source in section 5), each at least 30 s after the previous one. All HTTP 200. No further arxiv.org or export.arxiv.org request was made. Web searches returned arxiv.org links but I opened none of them.

## 5. The best published value for L = 377
- Source: Dimitrov, arXiv:2206.12070 "New Classes of Binary Sequences with High Merit Factor" (source fetched 00:31:05Z, HTTP 200, sha256 79806b61419d8ace9351322122bebef2408ea191651b725d4986c3376e53f13a, file name arXiv-2206.12070v1.tar.gz, so v1 is the latest version).
- Its table row L = 377 (method B_377^{27,13,10,5}): old merit factor 7.2249, new merit factor 7.35048613984. I decoded the printed hex myself (leading zero padding stripped) and recomputed: E = 9668, F = 7.35048613984 (matches every printed digit). The old value 7.2249 corresponds to E = 9836.
- Calibration on neighbouring rows of the same table, all matching their printed F to 11 digits: L = 375 E = 9499, 376 E = 9708, 378 E = 10037, 379 E = 9789, 380 E = 10286, 381 E = 10078.
- The L = 379 row decoded from the hex equals parent_sequence in parent.txt bit for bit, and sequence.txt equals that decoded row with its first and last element removed. sequence.txt is not the published L = 377 row (not equal, not its reversal).
- Only lines 852 and 853 of the TeX source mention 377 (the L = 377 row and the L = 378 row built from it). The table has a row for all 75 odd lengths 301..449.
- Margin: 9668 - 9452 = 216 (2.234 % lower energy), a strict improvement, not a tie.

## 6. Wider literature, last 24 months and older
- Group that holds the long-length records (Brest, Boskovic, Psenicnik): their own text in 2607.09688 places J. Comput. Sci. 2024 at 171..247, MENDEL 2022 at 201..303, Dual-Step (DSP 2025) at 450..527 and calls Dimitrov 2022 the previous best for the rest. 2607.09688 also says the previous longest sequence with F >= 8.0 was L = 309 from Dimitrov.
- ERK 2025 conference paper "Integer Partitions and the Merit Factor Problem" (Psenicnik, Boskovic, Brest): fetched once at 2026-10-17T00:36:31Z, HTTP 200, sha256 72574b63061ac62707b26b77c02698ef20ac8d0bcde1956e9f7060a443149605. It improves all lengths 400 <= L <= 450 (Table 3 prints only 405, 422, 433, 441, 450; for example F = 7.5199 at L = 405). Nothing below L = 400, so nothing at 377. Its comparison baseline for 400..450 is Dimitrov 2206.12070.
- Brest group bibliography (labraj.feri.um.si, `?tgid=2` at 00:36:32Z and `?tgid=3` at 00:36:34Z, HTTP 200 both). Merit-factor items listed there since 2024: 2607.09688, the ERK 2025 paper above, Dual-Step DSP 2025 (450..527), the Slovene Elektrotehniski vestnik 2025 paper (fetched at 00:39:10Z, HTTP 200, no "377" in the text; it studies the distance between sequences optimised for merit factor versus PSL), the MELECON 2024 neural-network paper (IEEE Xplore, not readable here; its title suggests a search-method study, and I could not see its lengths), J. Comput. Sci. 2024 (171..247), and the preprints.org PSL preprint below. The other items (Expert Syst. Appl. 2024 and IEEE Access 2024) are about peak sidelobe level, not energy.
- preprints.org 202605.0907 "Binary Sequences with Low Aperiodic Autocorrelations: Small Peak Sidelobe Levels": one request at 2026-10-17T00:37:13Z returned HTTP 403 ("Access Denied", 450-byte block page). Per the rules I stopped using preprints.org and record it as blocked. A web-search snippet of its abstract says it concerns Rudin-Shapiro and Legendre sequences and PSL, with merit factor about 5.0, so it is not a merit-factor record source.
- Web searches (9 queries) for "length 377", for new 2025-2026 records in the 300..450 range, for the DSP 2025 Dimitrov journal paper and for github record tables returned only the papers listed above. The DSP 2025 Dimitrov paper is the algorithm paper arXiv:2106.03377; the claim's sources_checked.md records a single tabulated length (449) for it, and I did not re-fetch it because the arXiv request budget was used. I found no table, repository, blog or preprint giving an L = 377 energy below 9668.
- Older records: Knauer 2004 (to 304), Boskovic 2017 / arXiv:1406.5301 (skew rows 301, 303, 341, 381, 401, 449), Brest-Boskovic IEEE Access 2018 (same repository rows), Packebusch-Mertens (optimal to 66). None has an L = 377 value better than Dimitrov's.

## 7. This repository (github.com/elder-plinius/V3R1T4S)
- `git clone --depth 1` at 2026-10-17T00:32:18Z, exit 0, branch main, HEAD 8b5ba829baa4711791f2dda18e139ae2bd3beeff (2026-10-16T18:18:58-04:00, "bank: ebl-unidentified-fragment-overlaps, three pitfalls from two negative runs (#252)").
- TROPHY_CASE.md on main: 31036 bytes, sha256 cdfe852481ba85e35ccbc386d64ce88de92a56eb73d1ec3e44cdc9a3b86345ad, 53 rows in 7 families (constant-weight codes 35, degree-diameter 7, fast matrix multiplication 5, Lehmer 1, RobustBench 1, sealed envelopes 2, VNN-COMP 2). No LABS or merit-factor row; the single regex hit is "3773" inside a code row. It differs from the copy in the claim package (sha256 b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412) only by newer supersession notes in rows 26, 45, 46 and 48 and the matrix-multiplication summary line; neither copy has a LABS row.
- Pull requests, GitHub REST API (3 unauthenticated calls, the maximum): `GET /repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=N` for N = 1, 2, 3 at 00:34:26Z, 00:35:00Z, 00:35:01Z, all HTTP 200 (sha256 b121405500027fd7ac050f52f7e956e75e594ff5152ae3885823851338ee3c92, 80dd6c5cb6b8ca90c750d559c843ead705267b0173702efaf8a99583f7699f1b, 3be41902c15f94df0c4495932bc80090444bb9e02d02b310c3ce300d41047b83). 281 pull requests, numbers 1 to 289, open and closed, titles and bodies scanned.
- Claims on labs-merit-factor-records: #255 (L=463), #283 (L=232), #284 (L=242), #285 (L=328), #288 (L=464), all open drafts created 2026-10-16. I read the bodies (the two long ones only in part) and regex-scanned every title and body for "labs", "merit factor", "377", "9452" and "9668". None is L = 377 and none mentions 377 or 9452 in a LABS context. The only other "377" hit is #18, a matrix-multiplication claim. The `known-knowns` and `known-unknowns` folders contain no LABS claim folder.
- Pull requests opened after about 00:35Z were not seen.

## 8. Reasoning
1. The claim's number is verified exactly: E = 9452 at L = 377 (two independent codes, plus the parent relation and the published L = 379 parent decoded from the arXiv source).
2. The three named table sources contain no L = 377 entry (checked in the TeX sources and in a fresh clone of the repository), and no newer arXiv paper has one (two API listings plus abstracts).
3. The lowest published L = 377 energy I can find anywhere is Dimitrov's 9668, which I re-derived from the printed hex. 9452 is 216 lower, so it is a strict improvement rather than a tie. The claim's baseline.tsv figure of 9668 is correct.
4. Neither TROPHY_CASE.md nor any pull request claims this length.

Caveats the panel should weigh, none of which changes my verdict:
- The edit is Dimitrov's own operator eta_0 (strip the first and last element of a skew-symmetric sequence, listed in the operator table of 2206.12070 and used in 21 of its rows for other lengths) applied to his published B_379. The paper simply did not apply it to 379 -> 377 and lists B_377 directly. The criterion compares against published energies, and 9452 is not published anywhere I could find, but the object is a one-step derivation of a published sequence by a published operator.
- Unreadable here: preprints.org (403), IEEE Xplore and ScienceDirect journal versions. Their preprints or the authors' own summaries place those papers at other length ranges, so I judge the risk low but not zero.
- Trend risk: the same group published new records for 450..527 (2025) and 400..450 (Sep 2025, F = 7.52 at L = 405). A paper covering 305..399 could appear at any time; none existed at the times above.

pass: true
