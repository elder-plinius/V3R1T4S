# NOVELTY verdict: cohn-grassmannian-packings-table, cell 11-1-62

context: subagent (fresh context; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-08T02:39:05Z

## Value computed here
- Object: object/11-1-62.txt, sha256 c9da55b9f9cfe7a4711ded4bae4c1f46700366b616fa820fd31e794eba3bb9d2 (matches CLAIM.md). It has 62 vectors of 11 coordinates plus one `#` header line. Every coordinate has at least 28 significant digits. No text in the object or the claim tries to steer the panel.
- Live table: https://cohn.mit.edu/grassmannian, fetched 2026-11-08T02:34:24Z, HTTP 200, 629039 bytes, sha256 7ba705c673db669ed4e3ec33fd45cd26f9648019a648fb21eb45761e113a0a66. The server sent no Last-Modified header.
- Row (11, 1, 62): squared chordal distance 0.8891152435, bound 0.9239940388, no star. The m cell is a plain `11`, while starred rows carry `&lowast;` before m. The note reads "Henry Cohn, 2026" and credits Henry Cohn. It contains neither "optimal packing" nor "proof of optimality".
- Minimum squared chordal distance computed here: each vector normalised by mpmath QR at 60 digits, all 1891 pairs checked. The result is 0.889170554550474563978262083884, reached at pair (11, 36), 0-indexed.
  - Margin over the live value 0.8891152435: +5.53110504746e-5, which clears the 1e-9 threshold.
  - Distance below the bound 0.9239940388: 0.0348234842495, so the value does not exceed the bound.
  - Only one pair lies within 1e-12 of the minimum, so the packing is not balanced and could probably be pushed higher. That does not affect novelty.
- Dominance check across the live table. I parsed 3511 rows. No row with n = 1, m ≤ 11 and N ≥ 62 has a value ≥ 0.88917055. Such a row would contain an embedded 62-line subset beating the claim, and none exists. Neighbouring live rows:
  - (11, 1, 61) = 0.8899909089
  - (11, 1, 63) = 0.8888902317
  - (11, 1, 64) = 0.8888902317
  - The claimed value fits between them in the expected order.
- Sloane's classical table: https://neilsloane.com/grass/grassTab.html, fetched 2026-11-08T02:37:58Z, HTTP 200, 149883 bytes, sha256 d2e8e777b8ad9593c16daa1bde6734790056795e82478a173182b831042675b5. It lists (11, 1, 62) = 0.889115077969925, below both the live value and the claim. No entry there with n = 1, m ≤ 11, N ≥ 62 reaches 0.88917055.
- Prior claims at https://github.com/elder-plinius/V3R1T4S:
  - `gh pr list --state all` searches for "grassmannian" (2 hits), "grassmannian in:body", "11-1-62" (14 hits), "(11, 1, 62)" (0), "11,1,62" (0), "cohn-grassmannian-packings-table" (0), "chordal" (0), "cohn" (27 hits) and "line packing" (64 hits).
  - None of the hits is a Grassmannian or real line-packing claim. The "grassmannian" and "11-1-62" hits are polytof, A384209 and other unrelated work. The "cohn" hits are all spherical-codes-cohn-table. The "line packing" hits are Packomania claims and game-of-sloanes complex packings.
  - An issue search for "grassmannian" returned 0.
- TROPHY_CASE.md on main: blob 18b731d7d4bf99efd323d48740284daccb8501b0, last commit 2026-10-27T16:42:35Z, 31306 bytes after decoding, sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113. It has no match for grassmann, cohn, chordal, 11-1-62 or line pack.
- arXiv API searches (https://export.arxiv.org/api/query, newest 15 each by submittedDate, fetched 2026-11-08T02:37Z, all HTTP 200):
  - "Grassmannian packing" (15 total results) and "Grassmannian packings" (same set)
  - "line packing" (20 total) and "line packings"
  - "equiangular lines" (100 total, newest 2609.21892)
  - "fusion frame" (137 total, newest 2610.29041)
  - None of the 2025–2026 entries gives a packing value for 62 lines in R^11. They cover modulation and beamforming codes, equiangular-line upper bounds and constructions in other dimensions (2606.29392, 2606.10421), and fusion-frame theory.
  - Equiangular lines cannot dominate here: 62 lines in R^11 is beyond the equiangular maximum for that dimension.

## Clauses checked
- Live table re-fetched now (2026-11-08T02:34:24Z, HTTP 200): PASS
- Row (11, 1, 62) is unstarred: PASS
- The note does not say "optimal packing" or "proof of optimality". It reads "Henry Cohn, 2026": PASS
- Computed minimum 0.88917055455047 > live 0.8891152435 by at least 1e-9 (margin 5.53e-5): PASS
- Computed minimum does not exceed the bound 0.9239940388 by more than 1e-10 (it is 0.0348 below): PASS
- No prior V3R1T4S PR (open, merged or closed), issue or TROPHY_CASE entry claims this cell: PASS
- No arXiv result in the newest 15 of each query gives a larger value for (11, 1, 62): PASS
- No classical or embedded construction beats the claim, checked against Sloane's 1997 table and against live rows with m ≤ 11, N ≥ 62: PASS

## Decision
The object reaches 0.8891705546, beating the live unstarred value 0.8891152435 for (11, 1, 62) by 5.5e-5 while staying well below the bound. No prior V3R1T4S claim, TROPHY_CASE entry, recent arXiv paper or classical table entry reaches it. Some novelty risk remains:
- Each arXiv query covered only the newest 15 results and abstracts only, not full texts.
- I could not read the table's last-change date. The server sends no Last-Modified header, and the Wayback CDX returned 504, then empty, then 429.
- Two follow-up arXiv queries hit HTTP 429 and were not retried.
- The MIT DSpace archive of configurations is a single-page app and was not read.
- Unpublished improvements sent privately to Henry Cohn would be invisible to every source checked here.

pass: true
