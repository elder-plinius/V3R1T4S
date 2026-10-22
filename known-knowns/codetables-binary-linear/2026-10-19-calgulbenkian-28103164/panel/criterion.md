context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report: bklc-q4-n163-k11-d104

Cell: [163,11] over GF(4), claimed d = 104. Target id named by README.md: codetables-binary-linear. Win claimed: Full. The contributor's hash list checked from inside the package folder: all files OK.

## Target coverage 

Bank statement (verbatim from the target's success criterion): "For given [n,k] over GF(q), codetables.de (Grassl) records the best known lower and upper bounds on the maximum minimum distance d. A linear code with d larger than the tabulated lower bound is a new record. Binary tables cover n <= 256." The success criterion reads "a k x n generator matrix over GF(q)" and "the live http://www.codetables.de/ cell for (q,n,k)"; the p2 text reads "no [n,k,d] code over GF(q) exists". Only the target id (codetables-binary-linear), the sentence "Binary tables cover n <= 256" and the bank's verification method (Gaussian elimination over GF(2), 2^k) are binary-specific. So the literal criterion text covers q = 4, 5, 7, 8, 9; the id and the verification method suggest the maintainers had q = 2 in mind. All three merged claims for this target in the pull-request list (#142, #158, #163) are q = 2; the q = 4 filings (#90 to #101) were closed unmerged in the bulk close, so there is no maintainer precedent either way for q other than 2. The live table does hold q = 4, 5, 7, 8, 9 cells (the pages below were fetched and parse), and the same live table page family is the status source.

## Full success criterion, clause by clause

Reproduced criterion (from the target's success criterion): (1) rank exactly k over GF(q), computed independently; (2) exact minimum distance by full enumeration of all q^k - 1 nonzero codewords when feasible, never by sampling; (3) d strictly greater than the lower bound in the live cell and at most the upper bound; (4) not one of the 7 LinCodeEvolve codes or derived from them, and no newer arXiv claim already reaches that d.

My own checker (written from the definition, not shipped in this package; GF(4) symbol v = a + 2b stands for a + b*w with w^2 = w + 1; each codeword kept as two bit-planes; meet-in-the-middle over 4^(k//2) x 4^(k - k//2) message pairs, all-zero message excluded). I did not read or run the author's verifier scripts or receipts for this cell. Output for this cell:

n,k 163 11 claimed 104 7956
rank 11
mindist,count (104, 7956)


- Clause 1 (rank): met. My Gaussian elimination over GF(4) gives rank 11.
- Clause 2 (exact distance, full enumeration): met. All 4^11 messages enumerated (not sampled); minimum nonzero weight 104, number of words of that weight 7956, equal to the claimed A_d.
- Clause 3 (strictly above live lower, at most live upper): met. Live cell fetched once by me: http://www.codetables.de/BKLC/BKLC.php?q=4&n=163&k=11 at 2026-10-19T05:21:24Z, HTTP 200, page sha256 447e2d5ee68ef47d162dc8d39301b3739a324a85331159217b79dc95a0db2187; text reads "Bounds on linear codes [163,11] over GF(4) lower bound: 103 upper bound: 113". Claimed 104 is above 103 and at most 113.
- Clause 4 (not LinCodeEvolve / derived; no newer arXiv claim): the seven LinCodeEvolve codes are binary with k in 20, 21, 22 (as quoted in the body of merged PR #142), so a q = 4 code with k = 11 has no parameter overlap. Whether a newer arXiv claim already reaches this d cannot be decided from the folder; I did not search arXiv (novelty skeptic's job).

Fetch note: I fetched each page below once (curl with the honest user agent, no retry); times are UTC from the machine clock, status 200 for all.
Neighbour cells fetched for the propagation test: (162,11) lower 102 (sha256 b6ad56e7c526627d..., 2026-10-19T05:21:19Z); (164,11) lower 104 (sha256 7ac250602847addb..., 2026-10-19T05:21:28Z); (164,12) lower 103 (sha256 80120c62765286f8..., 2026-10-19T05:21:29Z); (163,12) lower 102 (sha256 3b59150a126aa35e..., 2026-10-19T05:21:25Z). Their fetch times and hashes are as listed here.

## Propagation and derivation (PR #350 rule)

Propagation. One-step implied lower bounds from live neighbours (pad (162,11), puncture (164,11) minus 1, shorten (164,12), subcode (163,12)): 102, 103, 103, 102; best 103, below 104.
Open question 1: a refile of a closed unmerged filing of the same contributor is, by the contributor's review ruling R1 (closed bulk close of 2026-10-14, no comments, no defect), not a prior record; it should be treated as a fresh filing. Open question 2: yes, [162,11,103] (puncture) and the further cells of earlier closed PRs that are punctures or shortenings of it follow by standard rules.

Open questions 3 to 5 (structure of the check, newer arXiv, why #90-#101 closed): Q3: my enumeration is the same full-enumeration idea as the triage's, written separately in a different representation (bit-planes, numpy); the criterion itself names full enumeration for this size, so a structurally different method is optional, not required; I did not run one. Q4: not decided (see clause 4). Q5: nothing known beyond ruling R1 (bulk close of 2026-10-14, no comments).

confirmed_scope: The object is a valid [163,11,104] code over GF(4) (rank 11, exact minimum distance 104 by full enumeration of all 4^11 - 1 messages, 7956 minimum-weight words) whose distance strictly exceeds the live lower bound 103 (upper 113); it is a refile of closed PR #101 (not a prior record by ruling R1), under the literal GF(q) reading of the criterion.

pass: true
