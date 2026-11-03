context: Claude Code subagent, fresh context [claude-sonnet-5-5]

# Criterion report, sc-p2-d7-batch24: partial win p2, dimension 7, 24 rows

Criterion text (partial win p2, verbatim): "A batch of at least 20 certified improvements (margin 1e-10 each) to rows labeled 'needs more optimization' in one dimension d in 4..32, delivered as one file set with the largest improvement reported; these rows are flagged unconverged by the table, so the batch is a partial win, never a claim."

Own check: my own checker (written from scratch, not shipped in this package; independent of the author's check_sc.py): parses the-record-we-beat/plain_rows.csv and the-record-we-beat/index_rows.html with its own regex, reads each object file, normalises every vector at mp.dps=50, takes the exact maximum over all N(N-1)/2 pairs. The contributor's hash list verified OK for every listed file first. Per-row results (the full output is shown below):

    N=177  gain=1.25766e-7  star=False  needs_more_optimization=True  min_sig_digits=27
    N=178  gain=3.11665e-8  star=False  needs_more_optimization=True  min_sig_digits=28
    N=204  gain= 1.4256e-7  star=False  needs_more_optimization=True  min_sig_digits=26
    N=212  gain=7.02945e-6  star=False  needs_more_optimization=True  min_sig_digits=26
    N=215  gain=8.31524e-7  star=False  needs_more_optimization=True  min_sig_digits=27
    N=308  gain=0.000137712  star=False  needs_more_optimization=True  min_sig_digits=27
    N=309  gain=4.93074e-5  star=False  needs_more_optimization=True  min_sig_digits=27
    N=310  gain=1.83725e-5  star=False  needs_more_optimization=True  min_sig_digits=27
    N=312  gain=1.34691e-5  star=False  needs_more_optimization=True  min_sig_digits=27
    N=313  gain=2.83723e-5  star=False  needs_more_optimization=True  min_sig_digits=27
    N=314  gain=1.01001e-5  star=False  needs_more_optimization=True  min_sig_digits=25
    N=315  gain=0.000135693  star=False  needs_more_optimization=True  min_sig_digits=28
    N=316  gain=9.19892e-6  star=False  needs_more_optimization=True  min_sig_digits=27
    N=317  gain=4.66303e-6  star=False  needs_more_optimization=True  min_sig_digits=27
    N=318  gain=2.54296e-6  star=False  needs_more_optimization=True  min_sig_digits=27
    N=322  gain=2.04946e-6  star=False  needs_more_optimization=True  min_sig_digits=27
    N=323  gain=1.82744e-5  star=False  needs_more_optimization=True  min_sig_digits=27
    N=325  gain=5.06717e-6  star=False  needs_more_optimization=True  min_sig_digits=27
    N=362  gain=3.18991e-9  star=False  needs_more_optimization=True  min_sig_digits=27
    N=364  gain=2.61775e-6  star=False  needs_more_optimization=True  min_sig_digits=27
    N=365  gain=2.02494e-5  star=False  needs_more_optimization=True  min_sig_digits=26
    N=366  gain=1.77698e-5  star=False  needs_more_optimization=True  min_sig_digits=27
    N=367  gain=1.87396e-6  star=False  needs_more_optimization=True  min_sig_digits=27
    N=368  gain= 1.5196e-6  star=False  needs_more_optimization=True  min_sig_digits=24

Summary line of my checker: rows 24 gain_ok 24 min gain 3.1899e-9 N 362 max gain 0.00013771 N 308

Clause by clause:
1. At least 20 improvements: 24 files, 24 rows judged individually; all 24 pass the margin test, so 24 of 24 pass (smallest margin 3.1899e-9 at N=362, which is about 32 times 1e-10; each of the 24 rows has its own file, shape (N lines, 7 coordinates) verified). Met.
2. Margin 1e-10 each, direction lower: every gain is positive and at least 3.19e-9, measured against the 12-decimal /plain cosine of the same row. Met for all 24.
3. "Certified": the check is a 50-digit mpmath computation over all pairs on 24 to 30 digit coordinates (mindigits shows 24 to 28 for the shortest token per file), not interval arithmetic. This is the bank's own verification method, and gains exceed any rounding by more than three orders of magnitude, so I read "certified" as the bank's checker standard. Met under that reading.
4. Rows labeled 'needs more optimization': all 24 index rows read "Henry Cohn, 2026, needs more optimization." with no ast mark. Met.
5. One dimension d in 4..32: all rows are d=7. Met. The batch is one claim, delivered as one file set (object/).
6. Distinct rows: 24 distinct N values (177, 178, 204, 212, 215, 308, 309, 310, 312 to 318, 322, 323, 325, 362, 364 to 368); none repeated. Met.
7. Largest improvement reported: The claim record (not shipped) states "the largest about 1.38e-4 (N = 308)" and "the smallest gain about 3.19e-9 (N = 362)". My check: largest gain 0.00013771 at N=308, smallest 3.1899e-9 at N=362. Met.
8. Null models and traps: the claim is labelled partial p2 and says it is not a full claim; the 'needs more optimization' rows are not eligible for the full claim, and the batch does not pretend otherwise. Index cosine equals plain cosine for every row. Rows of the table are by definition unconverged, so beating them is easy, but the bank text asks for exactly that; nothing in the text excludes it. Nothing is subsumed: the 24 rows are not the same as any full-claim cell. The live table state was not re-fetched by me; I rely on the saved verbatim rows with recorded fetch time 2026-10-18T17:39:49Z and page sha256, so currency at claiming time cannot be decided from the folder. Whether anyone else already posted better codes is the novelty role's question.
9. arXiv: one search (fetched 2026-10-18T17:51:29Z, HTTP 200, sha256 8964b046fbaf5b15e78f0f20b60334fd1ecb8c500d3a1a20e9d57876a75f7e61). The p2 text has no supersession clause, so this is information only: the table itself still labels all 24 rows unconverged.

Verdict: p2 is met literally: 24 of 24 rows pass, which is at least 20.

confirmed_scope: In dimension 7, 24 distinct rows (N = 177, 178, 204, 212, 215, 308 to 310, 312 to 318, 322, 323, 325, 362, 364 to 368) that the saved index rows label 'needs more optimization' each have a saved object whose 50-digit maximum normalised inner product is lower than the saved /plain cosine by at least 3.19e-9 (largest 1.377e-4 at N=308), which meets partial win p2 and no wider claim.
pass: true
