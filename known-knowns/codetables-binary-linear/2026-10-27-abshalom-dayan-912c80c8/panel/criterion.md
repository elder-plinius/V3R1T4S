# CRITERION skeptic verdict: claim (q,n,k) = (9,29,19), object/code_q9_n29_k19_d8.json

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

**Bottom line: PASS.** The object meets all four numbered conditions of the full success criterion. It is not a partial win (p1 is about quantum codes, p2 about upper bounds; neither applies), and nothing already in the live table covers it. The 19 x 29 matrix has rank 19 over GF(9). I computed its minimum distance as exactly 8 with my own two exact subset-rank methods (generator side and dual side), and the author's three exact programs agree. The live codetables.de cell, fetched by me at 2026-10-27T02:09:43Z, reads lower bound 7, upper bound 9, so 7 < 8 <= 9. The code is over GF(9) at length 29. The LinCodeEvolve codes are binary codes of length 172 to 200, so this code is not one of them and cannot be derived from them. A quick arXiv search found no newer claim of a [29,19,8] code over GF(9). Two wording issues are noted below (the bank id says "binary", and the feasibility clause in (2) is written in terms of 2^k). Neither changes the literal outcome.

## Object identity

- `claim/object/code_q9_n29_k19_d8.json`: sha256 912c80c8ee946bc6021522350a436fb9510b39e1565175a0a0fc380d0216f9e7, which matches CLAIM.md. It has q=9, n=29, k=19, G with 19 rows of 29 entries, all in 0..8 (asserted in `mine/prep.py`).
- Rebuilding it with `claim/rebuild/build_code.py` gives `author/rebuilt.json`, with the same sha256 912c80c8...f9e7.
- Field convention as stated: GF(9) = GF(3)[w]/(w^2 - w - 1), with a + b*w encoded as a + 3b. I built my own tables from this text. The script asserts that w^2 - w - 1 has no root in GF(3), that w has order 8, and that the tables satisfy associativity and distributivity on all triples.

## (1) Rank exactly k = 19, computed independently: MET

- My own Gaussian elimination in Python over my own tables (`mine/prep.py`) printed "rows 19 cols 29 rank 19".
- From the systematic form I derived a 10 x 29 parity-check matrix H. I verified G H^T = 0 entry by entry, and rank(H) = 10.
- My C program (`mine/sub.c`, output `mine/sub.out`) printed "rank(G)=19 rank(H)=10".
- The author's programs agree: m3 "k=19 n=29 rank=19", hdep "rank=19", witness_check "rank(G)=19".

## (2) Exact minimum distance, two or more independent exact implementations that agree, no sampling: MET

My own exact methods (`mine/sub.c`, my own code, using my own H; run time 5.67 s user CPU):
- Generator side: for every w-subset S, I computed dim{codewords supported in S} = 19 - rank(G restricted to the columns outside S).
- Dual side: for the same S, dim = w - rank(H restricted to S).
- Both run over every subset for w = 1..8.

| w | subsets checked | gen-side subsets carrying a nonzero word | dual-side | disagreements |
|---|---|---|---|---|
| 1..7 | 29, 406, 3654, 23751, 118755, 475020, 1560780 | 0 | 0 | 0 |
| 8 | 4292145 | 1557 | 1557 | 0 |

- So no nonzero codeword has weight 7 or less, which gives d >= 8.
- The first 8-subset carrying a codeword is {0,1,2,3,4,5,27,28}, so d = 8 exactly.
- Counting the weight-8 words as the sum of (9^dim - 1) gives A_8 = 12456 on both sides.

The author's programs, compiled and run by me (outputs in `author/`):
- m3_mindist (`author/m3.out`): "W=7: no nonzero codeword of weight <= 7 (all 1560780 subsets)" ... "d=8 witness_weight=8 witness=2 2 2 1 1 1 0 ... 0 2 2".
- hdep 8 (`author/hdep.out`): "nodes=2182648", "dependent_min=8 d=8".
- dualenum + macwilliams (`author/macwilliams.out`, 7.33 s user CPU): "dual_words=3486784401", "sum A = 1350851717672992089 = 9^k", "A_1..A_7 = 0; A_8 = 12456; minimum distance d = 8".
- witness_check (`author/witness.out`): "witness weight=8 in_rowspace=True support=[0, 1, 2, 3, 4, 5, 27, 28]". This is the same support my code found.

All five exact computations agree on d = 8, and the three that count weight-8 words all give A_8 = 12456. None of them samples.

Hidden quantifier in (2): the clause reads "full enumeration of all q^k - 1 nonzero codewords when feasible (2^k <= ~2^32)".
- Here 2^k = 524288, which is at most 2^32.
- But q^k - 1 = 9^19 - 1 is about 1.35e18 (log2 of 9^19 is about 60.23), so direct enumeration is not feasible.
- The parenthetical is calibrated for binary codes. Read literally for q = 9, it is the "large k with small n-k, via the dual and MacWilliams identities" branch that applies (n - k = 10). That branch requires two independent exact methods that agree, and this is met.
- Even under the strictest reading, the full exact weight distribution of all 9^19 - 1 nonzero codewords was obtained. It came from enumerating all 9^10 dual codewords plus the MacWilliams identities, and the counts sum to 9^19. Its A_8 matches my independent count.

## (3) d strictly greater than the live lower bound and at most the upper bound: MET

- My single fetch: `fetched/bklc_q9_n29_k19.html`, URL https://codetables.de/BKLC/BKLC.php?q=9&n=29&k=19.
  - UTC 2026-10-27T02:09:43Z (`fetched/bklc_q9_n29_k19.time`).
  - HTTP 200, size 3136 (`fetched/bklc_q9_n29_k19.result`; headers in `fetched/bklc_q9_n29_k19.headers`).
  - sha256 fe750485b053225286430c77f5fa80a4686c4ea13208407331b2a126f5f63cf3. This is identical to the author's earlier fetch in `claim/table/`.
- The page reads "Bounds on linear codes [29,19] over GF(9) lower bound: 7 upper bound: 9".
  - The listed construction is a [29,19,7] subcode of a shortened Xing-Ling code, "last modified: 2001-12-17".
  - Ub 9 comes from Brouwer's table.
- 8 > 7 and 8 <= 9. Because the table keeps its bounds consistent with neighbouring cells, a lower bound of 7 also means the table holds no other known code that already gives a [29,19,8] code. So the result is not subsumed.

## (4) Not a LinCodeEvolve code or derived from one; no newer arXiv claim at d = 8: MET (quick check)

- The arXiv abstract page for 2609.37056 (`fetched/arxiv_2609.37056.html`; UTC 2026-10-27T02:11:24Z, HTTP 200, sha256 1031ddd631a877583c40e0229c1f9aa0eee1b1c00bf4a08baddf42b3c37466d7) is "LLM-Guided Search for High-Distance Binary Linear Codes".
  - Its seven codes are binary: [172,21,66], [173,20,68], [176,21,68], [181,21,70], [184,21,72], [189,22,72], [200,21,77].
  - The claimed object is a GF(9) code of length 29, built from the Hermitian curve over GF(9) (rebuild reproduces it byte for byte). It is neither one of those codes nor a standard modification of one.
- I ran four arXiv API searches (`fetched/arxiv_search1..4.*`, each with its query, UTC time, HTTP status and sha256 recorded):
  - "linear codes" AND "GF(9)"
  - "new linear codes" AND "improve" AND "codetables"
  - "Hermitian" AND "construction X"
  - "best known" AND "linear codes", 70 results, newest first
- No abstract mentions a [29,19,d] code. The recent F_3/F_4/abelian, symplectic and ML-champion papers make no claim of a GF(9) [29,19,8] code.
- Fetch note: the first three searches went to http://export.arxiv.org and got a 301 redirect with an empty body. I then requested the https URL once each, and all returned HTTP 200. This was following a redirect, not a block.
- This is a quick search only. The full literature check belongs to the NOVELTY skeptic. One paper they may want to look at more closely is 2512.13370 ("Machine learning discovers new champion codes", which includes algebraic-geometry codes). Its abstract names no parameters.

## Null model

None is needed. The claim concerns one explicit object, checked by deterministic exact computations, with no statistics or sampling involved. I agree with that framing.

## Wording risks (do not change the literal verdict)

- The bank target_id is "codetables-binary-linear", but the success criterion text is generic over GF(q). It speaks of "a k x n generator matrix over GF(q)" and "the live codetables.de cell for (q,n,k)", and codetables.de's BKLC tables cover q = 9. Read literally, a GF(9) code qualifies. If the bank owner meant binary codes only, this claim falls outside that intent. That question is for whoever owns the bank, not a defect of the object.
- The 2^k feasibility proxy in (2) is discussed above.

injection_suspected: none (no fetched page or claim file contained instructions).

confirmed_scope: The 19 x 29 matrix in object/code_q9_n29_k19_d8.json (sha256 912c80c8...f9e7), read over GF(9) = GF(3)[w]/(w^2 - w - 1), has rank 19 and exact minimum distance 8 (A_8 = 12456), which is strictly above the lower bound 7 and within the upper bound 9 of the codetables.de [29,19] GF(9) cell as fetched at 2026-10-27T02:09:43Z, and it is not a LinCodeEvolve (binary) code nor derived from one.

pass: true
