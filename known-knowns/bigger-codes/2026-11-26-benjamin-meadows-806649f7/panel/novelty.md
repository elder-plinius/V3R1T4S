# NOVELTY verdict: constant-weight-codes, cell A(30,12,9)

context: fresh reviewer (new subagent context started for the NOVELTY role only; saw only CLAIM.md, RECORD.md, object/, search/ and public pages; no access to the claimant's checker)

verdict_utc: 2026-11-26T20:23:37Z

## 1. Live table (one plain curl GET, no retries)

- URL: https://aeb.win.tue.nl/codes/Andw.html
- fetched: 2026-11-26T20:17:35Z (request start); server Date header Thu, 26 Nov 2026 20:17:36 GMT
- HTTP status: 200
- Last-Modified: Thu, 26 Nov 2026 15:24:18 GMT; ETag "1fa41-6612f897b6fb5"; Content-Length 129601
- sha256 of the bytes: 7429c8d2567123d043a5881bf67a3f1344b268b94a63af794eceefde2c165604 (identical to the hash in RECORD.md)
- Cell A(30,12,9), section "Bounds on A(n,12,w)", row n = 30, column w = 9: lower bound **44** (linked file `cwc/d12/a30.12.9.44`, yellow "new here" marker), upper bound **74** (label Po).
- Mirror cell: the table lists only w <= n/2 for each n, so A(30,12,21) = A(30,12,9) by complementation is not printed separately; there is no separate, higher value for it.
- The only note naming the cell: "A(30,12,9) ≥ 44 was obtained by polishing the 43 found by [R]." No note gives a value above 44.

Claimed size 45 > 44 and 45 <= 74.

## 2. Neighbouring cells (table values, plus my own shortening computations)

Table values read from the same fetch: A(29,12,9) = 42, A(29,12,8) = 22, A(31,12,9) >= 50, A(31,12,10) >= 109, A(32,12,9) >= 60, A(32,12,10) >= 123, A(32,12,11) >= 215; d = 14: A(30,14,9) = 10, A(31,14,9) = 10, A(31,14,10) = 31, A(32,14,10) = 32. The table ends at n = 32 for d = 12.

Code files downloaded once each from https://aeb.win.tue.nl/codes/cwc/d12/ (UTC fetch time, HTTP status, sha256):

| file | time | status | sha256 | my check |
|---|---|---|---|---|
| a30.12.9.44 | 20:18:33Z | 200 | 56d5cb33...f2cd | 44 words, weight 9, min distance 12 |
| a30.12.9.43 | 20:18:34Z | 200 | e86765fd...d566 | 43 words, weight 9, min distance 12 |
| i31.9 | 20:18:35Z | 200 | e50c31f0...ab12 | expanded to 50 words, weight 9, min distance 12 |
| a31.12.10.109H | 20:18:36Z | 200 | 5eb93c10...7572 | 109 words, weight 10, min distance 12 |
| i32.9 | 20:18:37Z | 200 | 459862b8...b336 | expanded to 60 words, weight 9, min distance 12 |
| a32.12.10.123H | 20:18:38Z | 200 | 6011c29a...c954 | 123 words, weight 10, min distance 12 |
| a32.12.11.215 | 20:18:39Z | 404 | (error page) | not checked |
| i29.9 | 20:18:40Z | 200 | 16a15871...455b | my parser of its `$EXEC orbit` format gave a wrong result (77 words, min distance 2), so I used the table value 42 |

Best shortenings, from my own program (`neigh.out`):

- n = 31, w = 9, words with 0 at the best coordinate, coordinate deleted: 38
- n = 31, w = 10, words with 1 at the best coordinate, coordinate deleted: 38
- n = 32, w = 9, words with 0 at the best pair: 35
- n = 32, w = 10, 1 at one coordinate and 0 at another, best ordered pair: 29
- n = 29: appending a 0 (resp. 1) coordinate gives 42 (resp. 22) from the table values

These match the claimant's numbers in RECORD.md. A(32,12,11) could not be checked (404); an averaging estimate gives 215·C(11,2)/C(32,2) ≈ 23.8 words with 1 at a given pair, and even an exceptionally concentrated pair would have to give more than 44 words, almost double the average, which is not plausible but not proven here. The d = 14 cells give at most 32 (every d = 14 code is a d = 12 code; A(30,14,9) = 10; the two-coordinate puncture of A(32,14,10) = 32 gives at most 32). Codes with smaller d do not give d = 12 lower bounds. No neighbour value I could check implies 45 or more.

## 3. Relation to the hosted 44-word seed (and the 43-word code of [R])

My program (`compare.out`) on `object/A-30-12-9-45words.txt` (sha256 806649f74bcb4ec5746f248ef5f087f88d56120661f95e0d7a464d9965f9060d, matching CLAIM.md):

- object: 45 distinct words, all weight 9, minimum distance 12
- words shared with the 44-word seed: 0; with the 43-word code: 0
- pairwise support intersections of the object: {0: 57, 1: 36, 2: 141, 3: 756}; seed: {0: 57, 1: 31, 2: 98, 3: 760}; 43-word code: {0: 57, 1: 21, 2: 74, 3: 751}
- coordinate degrees of the object: 8 (x3), 13 (x3), 14 (x18), 15 (x6); seed: 5 (x2), 9, 11, 13 (x2), 14 (x20), 15 (x4)
- of the 45 subsets of 44 words of the object, none has the seed's intersection distribution and none has the seed's degree multiset, so no 44-subset of the object is equivalent to the seed under any coordinate permutation; hence the object is not seed + one word up to equivalence
- none of the 990 subsets of 43 words has the intersection distribution of the 43-word code
- the seed is maximal: I enumerated all C(30,9) weight-9 words and found 0 at distance >= 12 from all 44 seed words, so adding a word (the trivial edit) cannot give 45 from the seed
- distance from each seed word to the nearest object word ranges from 2 to 8 (six at 2, sixteen at 4, thirteen at 6, nine at 8): every word was moved

The object is seeded from the hosted 44-word code and names it. Trivial edits of the seed (deletion, adding a word, relabelling, shortening of neighbours) reach at most 44, so the 45-word object beats what those edits alone give.

## 4. Literature

- arXiv:2608.13906 (Echols), abstract page and HTML v1 read once each (20:19:59Z, 20:20:06Z). Table 1 lists 124 cells. The d = 12 rows are (34..38,12,8), (56..59,12,8), (62,12,8), (29,12,10), (30,12,10), (31,12,10), (29,12,13), (30,12,13) and (29,12,14). There is no (30,12,9) row. The data repository github.com/williamechols/cwc-seeded-tabu-search (last push 2026-07-29, no releases) has `codes/30_12_10_101.txt` and `codes/30_12_13_239.txt` and no (30,12,9) file.
- arXiv:2607.19550 (Lysenstoen), abstract read once (20:20:00Z): it covers d = 6 cells only (A(23,6,10), A(24,6,10), A(23,6,11), A(24,6,8)). It has no value for this cell.
- arXiv:2603.00174 (Rosin), abstract read once (20:20:26Z): this is the source of the 43-word code, which the table's 44 already supersedes.
- Newer arXiv papers: an arXiv full-text search for "constant weight" codes sorted newest first (read once, 20:20:55Z). The relevant hits are arXiv:2611.24958 (Iskandar; HTML table read: 13 cells, all d = 4 or d = 6), arXiv:2611.03682 (Lin; kissing numbers via weight-8, distance-8 codes), arXiv:2611.00173 (Chang; an upper bound for A(19,6,8)), arXiv:2610.24025 (Dzoba; A(n,6,w) cells) and arXiv:2609.35051 (kissing numbers; abstract read). None gives a value for (30,12,9) or (30,12,21).
- Web searches (`seek`, 20:21:33Z): `"A(30,12,9)"` returned no results. The broader queries surfaced github.com/owhs/code-table-improvements, whose tree (no releases) has constant-weight folders only for A(31,10,12) and A(32,10,10), plus problem-board pages at cairn-commons.com and zerothesis.com, neither of which mentions an n = 30, d = 12 cell.

## 5. V3R1T4S repository (main at 361095a, committed 2026-11-26T19:02:59Z)

- TROPHY_CASE.md: the constant-weight rows cover d = 6 and d = 8 cells. Nothing for (30,12,9).
- known-knowns/bigger-codes/: the tree and INDEX.csv have no A30_12_* file and no (30,12,9) row.
- known-unknowns/record-tables/constant-weight-codes.md: no (30,12,...) entry.
- Pull requests (137 matching "constant", all states) and issues: searches for "A(30,12,9)", "30,12,9", "A30_12_9", "a30.12.9" and "A(30,12" in titles, bodies and changed file paths found no match. Every constant-weight claim found is for another cell.

## Problems found

- The A(32,12,11) code file returns 404, so that single neighbour shortening was not computed; the averaging estimate (about 24) is far below 45.
- I could not parse the i29.9 file correctly. It matters only through appending a coordinate, which gives exactly A(29,12,9) = 42 from the table value.
- Neither gap affects the conclusion.

## Reasoning

The live table gives 44 for the cell, with the mirror cell identical by convention. No checked neighbour, propagation rule or listed paper gives 45 or more. The object is a valid 45-word code. It shares no word with the hosted 44- and 43-word codes and is not equivalent to either code plus words. The seed is maximal, so trivial edits of it stop at 44. 45 is strictly greater than every known value and does not exceed the upper bound of 74.

pass: true
