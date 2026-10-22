# Novelty report: dna-gcrc-n12-d8-w6

context: Claude Code subagent, fresh context [claude-sonnet-5-5]
novelty role, group codes. Cell: A_4^GC,RC(n,d,w) at (n, d, w) = (12, 8, 6), claimed size 38. Primary table named in the claim record (not shipped): King's DNA-code page.
Pull request data: I used a snapshot of all V3R1T4S pull requests (titles and bodies; 473 pull requests, fetched 2026-10-19T04:30:31Z) instead of the api.github.com pulls pages.

## Sources fetched (honest client, one plain request each, no retries)
Each fetch is described below with its URL, time, HTTP status and sha256; the local copies are not shipped in this package.
- King table page, https://rambutan.umassmed.edu/king/dnacodes.html : 2026-10-19T05:15:07Z, HTTP 200, sha256 25d6e9f88262fbb07c95841225cb3202aa29eb31f7f72d24b43e9c595bdb18c5 (identical bytes to the orchestrator triage fetch and to the page fetched for PRs 367 and 392). Footer: "Last updated June 23, 2010".
- The trophy case file of the V3R1T4S repository (raw GitHub): 2026-10-19T05:15:08Z, HTTP 200, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1. No line mentions DNA codes, polycubes, lattice animals or growth constants.
- known-knowns listing (GitHub contents API): 2026-10-19T05:15:08Z, HTTP 200, sha256 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011. 20 directories; none concerns DNA codes or polycubes.
- Pull requests: not fetched from api.github.com; I used the snapshot of all V3R1T4S pull requests (473 pull requests with title and body; fetch time 2026-10-19T04:30:31Z). No pull request targets dna-codes-gc-king-table or lattice-animal-growth-constant-certified-bounds. Related: open PR 367 (GC,RC cell (20,15) only, a different cell) and open PR 392 (bank facts for dna-codes-gc-rc-king-table; it reports that the Aboluion 2011 thesis is larger than the King table in 32 unmarked GC,RC cells with n <= 20). I checked this cell against the thesis tables directly (see the rows below); it is not among the cells where the thesis exceeds King.
- Closed calgulbenkian pull requests from the 2026-10-14 bulk close: none concerns these targets (searched titles in the snapshot for dna, polycube, lattice, animal).
- Aboluion 2011 PhD thesis, https://pure.southwales.ac.uk/ws/portalfiles/portal/991721/PhD_thesis_Niema.pdf : 2026-10-19T05:15:33Z, HTTP 200, sha256 c58666c3efcd3e16aa540db064521175fe82dc92de0c430b19b1fa3ea806bed3. Read Tables 10.69 to 10.72 (best known lower bounds for the maximum over w of A_4^GC and A_4^GC,RC).
- Survey arXiv 1607.00266 (PDF): 2026-10-19T05:15:33Z, HTTP 200, sha256 8842f894dd26ec0a4bb8592814b90873a3897e0c2a7f7ee952cd7ebef861bb5e. Repeats the thesis RC values; no GC table for these cells.
- arXiv 2409.06519 (PDF) 2026-10-19T05:16:20Z HTTP 200 sha256 6c74125316b71fe6f61567bf40554aabc4be955f31e94fe68e0814648577126f; arXiv 2403.11551 (PDF) 05:16:21Z HTTP 200 sha256 a3cfb49a2d9f4d1a8d07df5cf6aa40fb5e43d9bd519ef252058f886c934d0aef; arXiv 2108.02033 and 1903.03535 (PDF) 2026-10-19T05:20:17Z HTTP 200 sha256 49fbf13bb6afd6340e5f15c84261a9dc7fbf3d531463431e22b381ecbd85f52f and 1e1ca43fc21d57a802e9d7c385f0a1fb8ae017ca40e428ff8561a9132bbff540. Their comparison tables cover n = 16 and n >= 24 (2108.02033), n >= 10 with d = 4, 6 only at n = 10, 12, 16, 18, 20 and n >= 32 (2409.06519), n >= 32 (2403.11551), and A_4^GC,RC(17,4), (17,7), (13,5), (29,11) (1903.03535). None of these has a value for the cell below.
- arXiv API, two queries (DNA codes with GC content; reverse-complement DNA codes), 2026-10-19T05:15:09Z and 05:15:10Z, HTTP 200, sha256 fa555688701baf3bdcf6e2db3558b099ff4af6a37f3e6e914140db21e533d2ad and 568287f7b5102ec1e383fde19ffcd4d5a0f4b039f3abd377a8d7ad7ca6312a89. Newest relevant results since 2024: 2409.06519, 2412.10212, 2506.01236, 2506.19170, 2510.01750, 2512.13295, 2606.06367; by title/abstract these are algebraic-construction papers; only the first has comparison tables (read, see above).

## Value read for this cell
- King live table, row n = 12, column d = 8 of the A_4^GC,RC(n,d,w) table: 29 (no period or colon, so not marked optimal). Read from the page fetched at 2026-10-19T05:15:07Z (HTTP 200, sha256 given above). The claim's own table_value is 29: it agrees.
- Aboluion 2011 thesis (maximum over w; Tables 10.69 to 10.72): 29m1 at (n,d) = (12,8); this is the same number as King's, so no published value in the sources read is above 29. Because the thesis reports a maximum over w, a thesis value could only exceed the fixed-w value, and it does not exceed the claim anyway.
- Claim: 38 words, margin 9 over the live table and over the thesis.
- Quick independent validity check (my own script, not shipped in this package): (38, True, 8, 8, True) (size, all letters and GC counts correct and words distinct, minimum Hamming distance, minimum Hamming(x, rc y) over all pairs including x = y for RC cells, overall result). This is only context; the reproduce skeptic judges validity.

## Propagation test (PR 350 ruling: a value that follows by a standard rule is not a separate record)
- monotone in d: King value at (n,d+1) is 12, below the claim
- append one letter to a code of length n-1 (A when n is odd, C when n is even, GC content stays floor(n/2)): King value at (n-1,d) is 14, below the claim; for RC cells with odd n, inserting a fixed middle letter keeps the RC distance, and the best RC value at (n-1,d) (best known) is None
- no standard rule turns a GC value or a length n+1 value into a lower bound for a GC,RC code, so the closure of the table gives nothing above 29 here
None of these rules reaches 38. The claim is not implied by table values.

## Literature and pull requests
- No open or merged pull request targets this cell or this target id (PR 367 is the GC,RC cell (20,15); PR 392 edits bank text only). The trophy case has no entry. No known-knowns folder exists for it.
- arXiv 1903.03535, 2108.02033, 2403.11551 (named by the bank) and the 2024 paper 2409.06519 were read: none gives a value for (12,8) with GC content floor(n/2).
- Open question 1 (a published value at or above 38?): none in any source I could read; King and the thesis give 29. See unresolved line.
- Open question 2 (do the three named arXiv papers give a value at or above the claim?): no; checked in the PDFs, they do not contain this (n,d).
- Open question 3 (independent re-implementation agrees?): my own checker agrees with the claimed size and with all conditions listed above (see validity line); detailed re-derivation belongs to the reproduce role.
- Open question 4 (obtainable by a standard rule such as King doubling?): no, see the propagation test above.
unresolved: Montemanni, Smith, Koul, Lecture Notes in Management Science 6 (2014) 167-175 and Aboluion, Smith, Perkins, Discrete Math. 312 (2012) 1062-1075 were not retrievable without paywall or a second request; the 2012 paper is the basis of the thesis tables read above (per PR 392), the 2014 chapter is the one source that could plausibly hold a few-word improvement on a variable-neighbourhood-search entry (the v superscripts in King's table come from the same authors' 2008 and 2009 work). Google Scholar was not searched (no browser).

## Verdict
novelty: every readable source (live King table, Aboluion thesis, survey, four arXiv papers, PR list, trophy case) is strictly below the claim (38 against 29, margin 9); no standard propagation reaches it. A margin of 9 words is not plausibly closed by the one unread 2014 metaheuristic chapter, so I confirm strict novelty for this cell.

pass: true
