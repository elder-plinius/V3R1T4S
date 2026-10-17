# Novelty skeptic report: labs-merit-factor-records, L = 380 (claimed E = 10058)
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: NEW: E=10058 < 10286 (minimum over the published L=380 rows; the only one is Dimitrov arXiv:2206.12070 at E=10286; no L=380 row in arXiv:2607.09688, arXiv:2504.00987 or the Boskovic git_labs repository; no newer arXiv result covers L=380; no L=380 claim in this repo's TROPHY_CASE.md or pull requests)

All times are UTC from `date -u` taken in the same commands as the requests. All HTTP codes are from `curl -w '%{http_code}'`
(or the exit code of git). I saw only the claim package (claim/) plus the public sources named below. Nothing was
submitted, posted or contacted. Every web request used curl's default client (or the tool's own fetcher for the ERK PDF and
the web searches): no browser imitation, no cookies, no retries after a block.

## 1. The claim as received, recomputed

- claim/sequence.txt (sha256 ab147211509fe3c123e223e8bc69a8f42f111ff1f0d055d713f96200c6ba6bd8): 380 characters over {0,1}.
- `python check_energy.py "$(cat sequence.txt)"` printed `380 10058`. My own code (a direct O(L^2) integer loop and a second,
  big-integer polynomial-product method, both checked on Barker 11 and 13: E = 5 and 6) also gives 380 10058.
- claim/parent.txt: parent_sequence has 383 characters, E = 10367 (my code). `sequence.txt == parent_sequence[1:-2]` is True.
  The parent equals, character for character, the L=383 row of arXiv:2206.12070 as I decoded it myself (section 3).
- F = 144400/20116 = 7.1783654802; 10286 - 10058 = 228 lower (2.217 %). Not a tie.

## 2. What I fetched, with the value found for L = 380

arXiv requests (6 in total, all gaps at least 20 s, none blocked):

| # | UTC start | URL | HTTP | bytes | value for L=380 |
|---|---|---|---|---|---|
| 1 | 2026-10-16T21:17:02Z | https://arxiv.org/abs/2607.09688 (status source) | 200 | 43398 | no row (abstract page) |
| 2 | 2026-10-16T21:17:22Z | https://arxiv.org/src/2607.09688 (its tables) | 200 | 770457 | no row |
| 3 | 2026-10-16T21:18:13Z | https://arxiv.org/src/2504.00987 | 200 | 307131 | no row |
| 4 | 2026-10-16T21:20:00Z | http://export.arxiv.org/api/query?... (my mistake: http form) | 301 | 0 | n/a, empty redirect; counted against the cap |
| 5 | 2026-10-16T21:20:32Z | https://export.arxiv.org/api/query?... (the one date-sorted search) | 200 | 143024 | see section 4 |
| 6 | 2026-10-16T21:23:54Z | https://arxiv.org/src/2206.12070 (the baseline paper) | 200 | 104737 | E = 10286, F = 7.01924946529 |

Request 4 was a protocol redirect, not a block and not a retry of a failed request; request 5 is the same query over https and
is the single search I ran. No 401/403/429/503 or challenge page was seen on any host.

sha256: abs page c14c75eae85c1e30dcedf2fc98aa5295188e681aef1f15020b5e4e7c45c4420c; 2607.09688 source
738c297c53b58cbd7ed4cddd7a05f25e379604427d201e2354471bebe47b43a0; 2504.00987 source
bc0b444f8dddf0a13c28c5e4ee8a75cc034befada7231d4047797af80c72f5cd; search XML
05a3b4c225c69df6486929b99f29bfed1773cf2bc08c3bb01a9186117ee697e3; 2206.12070 source
79806b61419d8ace9351322122bebef2408ea191651b725d4986c3376e53f13a.

### 2a. Status source arXiv:2607.09688
Title "Prioritizing Search Space Regions in the Low Autocorrelation Binary Sequences Problem" (Psenicnik, Boskovic, Popic,
Brest), "[Submitted on 17 Jun 2026]", only v1 listed on 2026-10-16T21:17:02Z. Abstract: improves the previously best-known
results "for 35 sequence lengths in the range 450 <= L <= 527 and for L=573". Its record table (TAB_RECORDS.tex, caption
"... 450 <= L <= 527 and for L=573") has exactly 35 rows: 450-452, 455-465, 475-484, 490, 491, 494-498, 516-518, 573.
The string 380 occurs in none of the paper's .tex files. Value for L=380: no row. Its bibliography also lists Mertens'
open.dat (see section 6 for why I could not read it).

### 2b. arXiv:2504.00987 (Zhang et al.; submitted 2025-04-01, v2 2025-08-14 per the arXiv API listing)
Reports new sequences for sixteen sizes between 92 and 120 ("best known LABS solutions upto problem size 120"). It cites
https://github.com/borkob/git_labs as the Boskovic et al. archive. 380 does not occur in main.tex. Value for L=380: no row.

### 2c. Boskovic et al. records repository (https://github.com/borkob/git_labs)
`git clone --depth 1` at 2026-10-16T21:18:34Z, exit 0. HEAD 1aa123407636e48630174e0bf122037e369c1d68 (committed
2020-09-15, "results 2018"); single branch master; `git ls-remote` at 21:27:15Z shows only two old pull requests (a 2017
README citation fix and a 2018 directory rename); I fetched both heads and neither adds a result.
Result files: results-2016/2004-Knauer-original.{html,txt} (Knauer's table, up to L = 304 by its own note; the string 380
does not occur in the .txt copy), results-2016/2016-labs-skew.txt and results-2018/2018-labs-skew.txt (124 rows each, odd lengths only,
L=5..449). The only row in 370..400 is L=381, F=7.0893, E=10238 (I recomputed 10238). No even length and no L=380 anywhere
in the tree. The Merit_Factor_Records-2013-even/odd.html pages that the Knauer page links are not in the tree.
The Maribor lab page (https://labraj.feri.um.si/en/B.labs, 2026-10-16T21:28:09Z, HTTP 200 after two redirects) lists
git_labs as the "Binary sequences and MF" archive and https://github.com/J-Brest/LABS as "Binary sequences and PSL values";
I cloned the latter at 21:28:30Z (exit 0): 18 peak-sidelobe .seq files for L >= 2047, no merit-factor table.
Value for L=380: no row.

## 3. The baseline row, checked independently (arXiv:2206.12070, Dimitrov)

In bare_jrnl.tex the only L=380 row is line 855: `B_379 o eta_1 o eta_1 o eta_3`, previous F "-", F = 7.01924946529.
I decoded the hexadecimal field myself (concatenate the two blocks, convert to bits, keep the last L bits) for rows 377..388:
the exact integer energy reproduces the printed F to 10+ digits in every row (E = 9668, 10037, 9789, **10286**, 10078, 10299,
**10367**, 10400, 10224, 10449, 10401, 10658 for L = 377..388). The only integer E consistent with printed F(380) is 10286.
So baseline_E = 10286 in claim/baseline.tsv is confirmed, and claim/source_excerpts.txt is a faithful quote of that source.
The sequence in the claim differs from the published L=380 sequence (Hamming distance 143, 237 against its complement)
and has different energy, so it is not a re-statement of it.

## 4. Literature search, last 24 months (and the date-sorted arXiv search)

arXiv API, one query, 2026-10-16T21:20:32Z: `all:"low autocorrelation" OR all:"merit factor" OR all:"autocorrelation binary
sequences" OR all:"skew-symmetric binary"`, sortBy=submittedDate descending, max_results=100: 70 results in total (newest
published 2026-10-09). Recall check: it returned the known LABS papers (1406.5301, 2011.00068, 2106.03377, 2206.12070,
2210.15962, 2409.07222, 2504.00987, 2607.09688). LABS-related items since 2024-10: 2610.14361 (2026-10-09, small-subsystem
heuristic, N in [27,60]); 2609.05771 (crosscorrelation moments, theory); 2607.09688 (status paper); 2511.05778 (TOPSIS-like
evolutionary metaheuristic, ICAISC 2025); 2511.04553 (quantum-enhanced MTS, N in [27,37]); 2510.24237 (PUBO solver benchmark);
2506.17391 (PCE solver, N <= 45); 2504.11549 and 2504.01694 (quantum algorithms on small LABS); 2504.00987 (N <= 120).
I read abstracts and metadata only for the ones other than 2504.00987 and 2607.09688; none claims merit-factor records near 380.
Not re-fetched because of the six-request arXiv cap: 1406.5301, 1512.02475, 2011.00068, 2106.03377, 2210.15962, 2409.07222. For
these I rely on claim/sources_checked.md (no row for 380; ranges 181..401 [only L=381 near 380], 67..119, 201..303, 449 only,
171..247, 450..527), on the git_labs files above (which carry the 1406.5301 results: L=381 only), and on the ERK paper below.

Web searches (5 queries through the search tool; no arXiv page was fetched through it) and one non-arXiv download:
- ERK 2025 conference paper, Psenicnik-Boskovic-Brest, "Integer Partitions and the Merit Factor Problem" (downloaded
  2026-10-16T21:26:13Z, HTTP 200, 607359 bytes, sha256 72574b63061ac62707b26b77c02698ef20ac8d0bcde1956e9f7060a443149605):
  improves "all previously published binary sequences for lengths 400 <= L <= 450" over Dimitrov; Table 3 lists L = 405, 422,
  433, 441, 450 only; no 380 in the text. It is the most recent published work close to 380, and its range starts at 400.
  (The tool's own fetcher could not parse the PDF; I re-downloaded it with curl and read it with pdftotext.)
- arXiv:2106.03377 (same title as Dimitrov's DSP 156:104793, 2025; I could not read the journal version): its abstract
  describes a memory-reduction algorithm giving F > 5 for lengths up to 10^5+1, not a table of records. The J. Comput. Sci.
  2024 paper has the title of arXiv:2210.15962; the dual-step paper (DSP 165:105316, 2025) has the title of arXiv:2409.07222
  (450..527). The lab's own publication list (labraj.feri.um.si, read 21:28Z) shows no other merit-factor record paper.
- No search hit gave any L=380 energy or merit factor from any source other than Dimitrov 2206.12070.

## 5. This repository (github.com/elder-plinius/V3R1T4S)

- `git ls-remote` 2026-10-16T21:21:47Z, exit 0: main = ab114dcb1aad5cc1b2a53c58bc3ad3fcacd1107c (committed 2026-10-15T15:18:21-07:00);
  261 pull-request refs.
- Blobless `git clone --depth 1` at 21:22:42Z, then `git show HEAD:TROPHY_CASE.md` (sha256
  738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9): no mention of LABS, merit factor, autocorrelation or
  sidelobe. The copy in claim/TROPHY_CASE.md (sha256 b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412) is older
  (18 diff lines, all "overtaken/superseded" annotations on one constant-weight-code row and three matrix-multiplication
  rows) and also has no LABS text. The tree has no known-knowns/labs-merit-factor-records
  folder; the only LABS file is known-unknowns/record-tables/labs-merit-factor-records.md (sha256
  f9ed5acf88dbe97bcfc9012a962912db0a1c9185b5527cbac84d6b393d83a675), whose success rule matches the one quoted in claim/CLAIM.md and
  which says "assemble the baseline from all cited sources and state which one was beaten".
- GitHub REST API, exactly 3 unauthenticated calls, `GET /repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=N`:
  page 1 at 21:22:01Z, page 2 at 21:22:04Z, page 3 at 21:22:07Z, each HTTP 200. Together
  261 pull requests: 78 open, 124 closed unmerged, 59 merged (numbers 1..268; the missing numbers are not pull requests).
  I scanned title, body, branch name and labels of all 261 for labs, merit, autocorrel, sidelobe, skew, "binary sequence",
  380 and 10058. Hits: #255 (open, user elevenbrands, created 2026-10-16T19:30:57Z) "labs-merit-factor-records: L=463
  energy 14047, below 14439": same target, different length, and its body says it claims nothing about any other length
  (it mentions L=464 only as an unclaimed cell). #218 and #14 matched "380" but are fmm-additive-complexity-records (380 is a
  count of additions). No pull request, open or closed, claims labs-merit-factor-records at L=380.

## 6. What I could not read

- Mertens' open.dat (cited in the status paper's bibliography): http://www.ovgu.de/mertens/research/labs/open.dat answered HTTP 301
  at 21:25:04Z, then the https URL answered HTTP 404 (page not found) at 21:25:13Z; the labs index page answered 404 at
  21:25:24Z. I made no further requests to that host. The bank criterion does not list it (the bank's own source list is
  2607.09688, 2504.00987 and 1512.02475), so its absence does not block the comparison, but I could not look inside it.
- Journal-only versions (Elsevier, IEEE, MENDEL) were not opened. Their arXiv or conference counterparts, or repository files
  (the git_labs 2018 skew file for the IEEE Access 2018 paper), were read by me or by the claimant and none has an L=380 row;
  a difference between a journal version and its arXiv version cannot be excluded.
- Issues (as opposed to pull requests) of the repository were not read; the rule asks for pull requests.

## 7. Reasoning

1. The bank defines the best published energy as the minimum over the tables in arXiv:2607.09688, arXiv:2504.00987, the Boskovic
   repository and any newer arXiv result. I checked all four for L=380 (both papers' tables in full, the repository tree, and the
   newer-arXiv search) and none has a row. The only published L=380 energy I can find anywhere is the Dimitrov row, E = 10286,
   which I re-derived from the source (not only from claim/source_excerpts.txt).
   The claim therefore beats the strictest reading (empty set) and the practical reading (10286) alike.
2. 10058 < 10286 by 228. It is a strict improvement, not a tie; the integers are exact and were recomputed by the claim's
   script and by my two independent methods.
3. The same Dimitrov table shows why the margin is plausible: the published E(381) = 10078 is already below the published
   E(380) = 10286, so the L=380 row is weak. By my own computation, appending one element to the published L=379 sequence
   gives 10118 and deleting one element of the published L=381 sequence gives 10306, so even simpler derivations land below or
   near 10286. The claim's trim of the L=383 row is better still (10058; trimming 1+2 and 2+1 both give 10058, 0+3 and 3+0
   give 10598). This is an observation about difficulty, not about novelty: the criterion compares published energies, and
   derivation from a published sequence is not excluded by the rule text I was given (that is the CRITERION skeptic's call).
4. Fragility to flag for the human: (a) the Maribor group has moved down to L = 400..450 (ERK 2025) with F up to 7.80, so a
   lower L=380 energy is likely to appear soon; novelty holds as of 2026-10-16T21:29Z only. (b) PR #255 shows another claimant
   is already scanning this target with end-extensions of published records, so a competing L=380 claim is plausible.
   (c) My negative findings cover the named sources, the date-sorted arXiv search, the git archive and the pull requests;
   they cannot exclude a value that sits in an unreadable journal-only or unindexed place.

pass: true
