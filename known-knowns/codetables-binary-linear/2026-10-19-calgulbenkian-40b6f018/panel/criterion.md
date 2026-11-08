context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report: bklc-q4-n157-k10-d102

[Edited 2026-11-08 at the maintainer's request on the pull request: references to pull requests other than merged results, to unmerged codes of the same batch, to internal review notes and to the scope question (GF(4) results on this target are now settled) were removed; the checks and numbers are unchanged.]

Cell: [157,10] over GF(4), claimed d = 102. Target id named by README.md: codetables-binary-linear. Win claimed: Full. The contributor's hash list checked from inside the package folder: all files OK.

## Target coverage 

Bank statement (verbatim from the target's success criterion): "For given [n,k] over GF(q), codetables.de (Grassl) records the best known lower and upper bounds on the maximum minimum distance d. A linear code with d larger than the tabulated lower bound is a new record. Binary tables cover n <= 256." The success criterion reads "a k x n generator matrix over GF(q)" and "the live http://www.codetables.de/ cell for (q,n,k)"; this is a GF(4) result, and the live table holds the GF(4) cell (the pages below were fetched and parse). The same live table page family is the status source.

## Full success criterion, clause by clause

Reproduced criterion (from the target's success criterion): (1) rank exactly k over GF(q), computed independently; (2) exact minimum distance by full enumeration of all q^k - 1 nonzero codewords when feasible, never by sampling; (3) d strictly greater than the lower bound in the live cell and at most the upper bound; (4) not one of the 7 LinCodeEvolve codes or derived from them, and no newer arXiv claim already reaches that d.

My own checker (written from the definition, not shipped in this package; GF(4) symbol v = a + 2b stands for a + b*w with w^2 = w + 1; each codeword kept as two bit-planes; meet-in-the-middle over 4^(k//2) x 4^(k - k//2) message pairs, all-zero message excluded). I did not read or run the author's verifier scripts or receipts for this cell. Output for this cell:

n,k 157 10 claimed 102 5304
rank 10
mindist,count (102, 5304)

- Clause 1 (rank): met. My Gaussian elimination over GF(4) gives rank 10.
- Clause 2 (exact distance, full enumeration): met. All 4^10 messages enumerated (not sampled); minimum nonzero weight 102, number of words of that weight 5304, equal to the claimed A_d.
- Clause 3 (strictly above live lower, at most live upper): met. Live cell fetched once by me: http://www.codetables.de/BKLC/BKLC.php?q=4&n=157&k=10 at 2026-10-19T05:20:52Z, HTTP 200, page sha256 16ce6e96ca31a9d96ed62987ebcb5d13214280eac6c5a1a432d65c997266fe21; text reads "Bounds on linear codes [157,10] over GF(4) lower bound: 101 upper bound: 110". Claimed 102 is above 101 and at most 110.
- Clause 4 (not LinCodeEvolve / derived; no newer arXiv claim): the seven LinCodeEvolve codes are binary with k in 20, 21, 22 (binary codes of length 172 to 200), so a q = 4 code with k = 10 has no parameter overlap. Whether a newer arXiv claim already reaches this d cannot be decided from the folder; I did not search arXiv (novelty skeptic's job).

Fetch note: I fetched each page below once (curl with the honest user agent, no retry); times are UTC from the machine clock, status 200 for all.
Neighbour cells fetched for the propagation test: (156,10) lower 100 (sha256 5665589dddd70040..., 2026-10-19T05:20:47Z); (158,10) lower 102 (sha256 5460d9294de9f2a3..., 2026-10-19T05:20:58Z); (158,11) lower 99 (sha256 728b85ab401abdb3..., 2026-10-19T05:21:00Z); (157,11) lower 98 (sha256 e0349fb3c204c509..., 2026-10-19T05:20:54Z). Their fetch times and hashes are as listed here.

## Propagation and derivation

Propagation. One-step implied lower bounds from live neighbours (pad (156,10), puncture (158,10) minus 1, shorten (158,11), subcode (157,11)): 100, 101, 99, 98, so the best implied value is 101, below 102.
Open question 1: criterion item 4 excludes only the seven LinCodeEvolve codes (arXiv:2609.37056) and codes derived from them; those improvements are binary codes at k = 20, 21, 22, so a q = 4, k = 10 code has no parameter overlap with them. The code is a one-column extension of a [156,10,101]_4 code from the same search, which is not in the live table (live lower bound 100 for [156,10]) and is not excluded by any criterion clause. Open question 2: yes, puncturing this code gives [156,10,101]_4 (standard puncture, 102 - 1), so a lower bound of 101 for that cell (live 100) is implied by this record.

Open questions 3 and 4 (structure of the check, newer arXiv): Q3: my enumeration is the same full-enumeration idea as the package checker's, written separately in a different representation (bit-planes, numpy); the criterion itself names full enumeration for this size, so a structurally different method is optional, not required; I did not run one. Q4: not decided (see clause 4).

confirmed_scope: The object is a valid [157,10,102] code over GF(4) (rank 10, exact minimum distance 102 by full enumeration of all 4^10 - 1 messages, 5304 minimum-weight words) whose distance strictly exceeds the live lower bound 101 (upper 110) and is not implied by the live neighbours.

pass: true
