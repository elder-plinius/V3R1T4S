context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report: bklc-q4-n160-k11-d102

Cell: [160,11] over GF(4), claimed d = 102. Target id named by README.md: codetables-binary-linear. Win claimed: Full. The contributor's hash list checked from inside the package folder: all files OK.

## Target coverage 

Bank statement (verbatim from the target's success criterion): "For given [n,k] over GF(q), codetables.de (Grassl) records the best known lower and upper bounds on the maximum minimum distance d. A linear code with d larger than the tabulated lower bound is a new record. Binary tables cover n <= 256." The success criterion reads "a k x n generator matrix over GF(q)" and "the live http://www.codetables.de/ cell for (q,n,k)"; the p2 text reads "no [n,k,d] code over GF(q) exists". Only the target id (codetables-binary-linear), the sentence "Binary tables cover n <= 256" and the bank's verification method (Gaussian elimination over GF(2), 2^k) are binary-specific. So the literal criterion text covers q = 4, 5, 7, 8, 9; the id and the verification method suggest the maintainers had q = 2 in mind. All three merged claims for this target in the pull-request list (#142, #158, #163) are q = 2; the q = 4 filings (#90 to #101) were closed unmerged in the bulk close, so there is no maintainer precedent either way for q other than 2. The live table does hold q = 4, 5, 7, 8, 9 cells (the pages below were fetched and parse), and the same live table page family is the status source.

## Full success criterion, clause by clause

Reproduced criterion (from the target's success criterion): (1) rank exactly k over GF(q), computed independently; (2) exact minimum distance by full enumeration of all q^k - 1 nonzero codewords when feasible, never by sampling; (3) d strictly greater than the lower bound in the live cell and at most the upper bound; (4) not one of the 7 LinCodeEvolve codes or derived from them, and no newer arXiv claim already reaches that d.

My own checker (written from the definition, not shipped in this package; GF(4) symbol v = a + 2b stands for a + b*w with w^2 = w + 1; each codeword kept as two bit-planes; meet-in-the-middle over 4^(k//2) x 4^(k - k//2) message pairs, all-zero message excluded). I did not read or run the author's verifier scripts or receipts for this cell. Output for this cell:

n,k 160 11 claimed 102 2958
rank 11
mindist,count (102, 2958)

- Clause 1 (rank): met. My Gaussian elimination over GF(4) gives rank 11.
- Clause 2 (exact distance, full enumeration): met. All 4^11 messages enumerated (not sampled); minimum nonzero weight 102, number of words of that weight 2958, equal to the claimed A_d.
- Clause 3 (strictly above live lower, at most live upper): met. Live cell fetched once by me: http://www.codetables.de/BKLC/BKLC.php?q=4&n=160&k=11 at 2026-10-19T05:21:10Z, HTTP 200, page sha256 66940d1d63a32c585d0466f9bfc9bdbccacc4ec0b8448439efd301b3fb0ed955; text reads "Bounds on linear codes [160,11] over GF(4) lower bound: 101 upper bound: 111". Claimed 102 is above 101 and at most 111.
- Clause 4 (not LinCodeEvolve / derived; no newer arXiv claim): the seven LinCodeEvolve codes are binary with k in 20, 21, 22 (as quoted in the body of merged PR #142), so a q = 4 code with k = 11 has no parameter overlap. Whether a newer arXiv claim already reaches this d cannot be decided from the folder; I did not search arXiv (novelty skeptic's job).

Fetch note: I fetched each page below once (curl with the honest user agent, no retry); times are UTC from the machine clock, status 200 for all.
Neighbour cells fetched for the propagation test: (159,11) lower 100 (sha256 c452751aa9178944..., 2026-10-19T05:21:06Z); (161,11) lower 102 (sha256 745bec8f5e511049..., 2026-10-19T05:21:15Z); (161,12) lower 100 (sha256 ddfa5967be4b578b..., 2026-10-19T05:21:16Z); (160,12) lower 100 (sha256 4f647fb34e795066..., 2026-10-19T05:21:12Z). Their fetch times and hashes are as listed here.

## Propagation and derivation (PR #350 rule)

Propagation. One-step implied lower bounds from live neighbours (pad (159,11), puncture (161,11) minus 1, shorten (161,12), subcode (160,12)): 100, 101, 100, 100; best 101 (the live cell itself cites a [161,11,102] quasi-cyclic code punctured at one position).
Open question 1: the cell pages for [157,11] and [158,11] (closed PRs #98 and #99) are, if these closed filings were valid, punctures of this record; they are the contributor's own closed filings and by the contributor's review ruling R1 are not prior records. I found no other public claim of [160,11,102]_4 in the snapshot of all V3R1T4S pull requests (titles checked for q = 4 codes: only #90 to #101). Open question 2: not obtainable by a one-step rule from a live neighbour (shown above).

Open questions 3 to 5 (structure of the check, newer arXiv, why #90-#101 closed): Q3: my enumeration is the same full-enumeration idea as the triage's, written separately in a different representation (bit-planes, numpy); the criterion itself names full enumeration for this size, so a structurally different method is optional, not required; I did not run one. Q4: not decided (see clause 4). Q5: nothing known beyond ruling R1 (bulk close of 2026-10-14, no comments).

confirmed_scope: The object is a valid [160,11,102] code over GF(4) (rank 11, exact minimum distance 102 by full enumeration of all 4^11 - 1 messages, 2958 minimum-weight words) whose distance strictly exceeds the live lower bound 101 (upper 111) and is not obtainable from the live neighbours or by puncturing the co-filed [163,11,104] code, under the literal GF(q) reading of the criterion.

pass: true
