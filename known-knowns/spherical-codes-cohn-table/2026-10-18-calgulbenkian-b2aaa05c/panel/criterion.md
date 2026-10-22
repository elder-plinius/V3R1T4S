context: Claude Code subagent, fresh context [claude-sonnet-5-5]

# Criterion report, sc-30-62: spherical code (d=30, N=62), full claim

Criterion (verbatim from the target's success criterion, split into clauses), checked literally.

Own check: my own checker (written from scratch, not shipped in this package; independent of the author's check_sc.py): parses the-record-we-beat/plain_rows.csv and the-record-we-beat/index_rows.html with its own regex, reads object/30x62.txt, normalises every vector at mp.dps=50, takes the exact maximum over ALL 1891 pairs (no float prefilter). Output (verbatim):

    d=30 N=62 shape=True mindigits=27 c*=0.031273183363813242615 table=0.031273236170 gain=5.28062e-8 star=False needs=False idxcos_eq_plain=True ref=[Ilmari Vahteristo, New spherical codes by tuning an annealing solver, preprint, 2026, arXiv:2610.19988.] gain_ok=True

The contributor's hash list: every file verified OK before the check.

Clause by clause:
1. N vectors in R^d for a (d,N) row present in the live /plain: row (30,62) is in plain_rows.csv with cos 0.031273236170. The shape check passed (62 lines, 30 coordinates each). Met (the live page itself was not re-fetched by me; I used the saved rows with their recorded fetch time 2026-10-18T17:39:49Z and sha256, and the row is a verbatim line; the live value at claiming time cannot be decided from the folder beyond that record).
2. Coordinates given to >= 20 digits: every coordinate token has at least 24 significant digits (file is 30-digit). Met.
3. After normalising at 50 digits the maximum pairwise inner product c* is strictly lower than the table's 12-decimal cosine by at least 1e-10: c* = 0.031273183363813242615, table = 0.031273236170, gain = 5.28062e-8 (the threshold is 1e-10; the gain is at least 26 times the threshold, and 12-decimal rounding of the table value is 5e-13 at most, so rounding cannot change the verdict). Direction is min (lower is better) and the comparison is made against the 12-decimal plain value as the criterion states. Met.
4. Index row has no '&ast;' mark: the verbatim index row shows none after the link text. Met.
5. Index row does not contain 'needs more optimization': absent. Met. (This is the full-claim route, not p2.)
6. Not superseded by a newer arXiv result for the same (d,N): The row's reference cell cites arXiv:2610.19988, so the table already incorporates that newest paper; the claim beats the table value that includes it. arXiv check (one request, response not shipped; the first plain http request returned 301 and was not repeated, the https form of the same URL was fetched once): https://export.arxiv.org/api/query?search_query=all:%22spherical+code%22&sortBy=submittedDate&sortOrder=descending&max_results=15 at 2026-10-18T17:51:29Z, HTTP 200, sha256 8964b046fbaf5b15e78f0f20b60334fd1ecb8c500d3a1a20e9d57876a75f7e61. The only listed paper on this problem is arXiv:2610.19988 (Vahteristo, 2026-10-14), which covers every instance with 3 <= D <= 32 and N <= 1024 and which the live table already credits in its reference cells.
7. Not a kissing-number configuration (only if 9 <= d <= 23 and c* <= 0.5): d=30 is outside 9..23 (and c* is about 0.0312). Clause does not apply. Met.
8. Null models and hidden quantifiers: the index cosine equals the plain cosine for the row; the object is not the table's own posted code (gain is real, nonzero); points are not degenerate (maximum inner product is far below 1, so no duplicate points). No hidden quantifier found: a single (d,N) row, margin and direction explicit. Uploading to /upload-code is not part of the claim and was not done. Whether the object is genuinely new is the novelty role's question, not decided here.

Verdict: all mechanical clauses met; the arXiv-supersession clause is met on the evidence available (one arXiv search).

confirmed_scope: For the single row (d=30, N=62) the saved object has maximum normalised inner product 0.031273183363, which is lower than the saved live /plain cosine 0.031273236170 by 5.28062e-8, at least 1e-10, on an index row with no ast mark and no 'needs more optimization' text and outside the kissing-number range, as fetched 2026-10-18T17:39Z.
pass: true
