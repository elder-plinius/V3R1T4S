# CRITERION skeptic verdict: claim [31,17,11] over GF(9)

**Bottom line: PASS on the literal success criterion (all four parts).** The matrix has rank 17. Its exact minimum distance is 11, shown by the author's two exact programs and by my own third exact method. 11 is strictly above the live codetables.de lower bound 10 and at most the upper bound 13 for (q,n,k) = (9,31,17). The field modulus is irreducible and used consistently. The code is not one of the 7 LinCodeEvolve codes, which are all binary. One scope point goes to the main session: the bank entry's id is `codetables-binary-linear`, but this code is over GF(9). The verbatim criterion is written for general GF(q) and (q,n,k), so I judge it literally and do not fail it on the id.

- start: 2026-10-29T01:21:00Z (date -u)
- end: 2026-10-29T01:25:00Z (date -u)
- object: object/code_q9_n31_k17_d11.json, sha256 f08aa6475f164ffa1ed1f41f5c63eb0f5516b74c34c1b198da8c83ae1a7da5dd (shasum -a 256, matches CLAIM.md). The rebuild from rebuild/build_code.py gives the same hash:
  `f08aa6475f164ffa1ed1f41f5c63eb0f5516b74c34c1b198da8c83ae1a7da5dd  rebuilt.json`
- Partial win claimed? No. The claim is the main criterion, not p1 (quantum) or p2 (upper bound).

## Part 1: rank exactly k = 17, computed independently

Finding: met. Four separate rank computations agree.
- my own mine/prep.py, which reads the JSON directly and has its own GF(9) arithmetic: `rank(G) over GF(9) = 17 k = 17`
- checkers/witness_check.py: `k=17 n=31 rank(G)=17`
- checkers/hdep.c: `rank=17 (k=17 n=31)`
- checkers/m3_mindist.c: also rank 17 (it only prints its d line after a full-rank check)

## Part 2: exact minimum distance by an exact method (no sampling)

Full enumeration is not feasible: 9^17 - 1 = 16677181699666568 nonzero codewords (log2 9^17 = 53.89 > 32). So the criterion requires two independent exact implementations that agree. Finding: met, and backed by a third exact method of my own.

Author method A, checkers/m3_mindist.c (generator side: every W-subset of the coordinates gets an exact left-kernel test). Re-run from a copy:
```
W=10: no nonzero codeword of weight <= 10 (all 44352165 subsets)
W=11 complete for all W'<11; first nonzero codeword supported in a 11-set after 229 subsets
d=11 witness_weight=11 witness=1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0
```
Author method B, checkers/hdep.c (dual side: depth-first search over independent parity-check column subsets for the smallest dependent set):
```
rank=17 (k=17 n=31)
nodes=75973418
dependent_min=11 d=11
```
I read both programs. Both are exhaustive: m3 tests every subset of size up to W. hdep extends only independent sets, and every proper prefix of a minimal dependent set is independent, so it is found. Neither samples. The two use different methods (codeword supports vs. dependent columns of H) and different GF(9) arithmetic (direct pair formula vs. log tables), so I accept them as two independent exact implementations. They share one author and one converter (checkers/json_to_code.py). My own check covers that shared path.

My own exact check (mine/prep.py + mine/bz.c, a two-information-set enumeration in the style of Brouwer-Zimmermann):
- I1 = [0, 1, 5, 7, 9, 10, 11, 13, 16, 17, 19, 20, 21, 26, 28, 29, 30]. Its complement has rank 14. I2 = the complement plus T = [0, 1, 5], which is an information set.
- I enumerated every x with wt(x) <= 6 and first nonzero entry 1, on both sets. A codeword missed by both enumerations has wt on I1 >= 7 and wt on I2 >= 7, so wt on the complement >= 4, and total weight >= 11. So every codeword of weight <= 10 is enumerated.
```
set 1: enumerated 432146001 vectors x (wt<=6, first nonzero 1); min codeword weight among them = 11
set 2: enumerated 432146001 vectors x (wt<=6, first nonzero 1); min codeword weight among them = 11
```
The expected count, sum_{i=1..6} C(17,i)*8^(i-1), is 432146001. It matches.
- Negative control: I planted a weight-5 row in a copy of G (mine/neg.json). The same program reported `min codeword weight among them = 5`, so it does detect low-weight words.
- Upper side: my own row-space test gives `witness weight 11 in rowspace: True` (witness_check.py agrees, support [0, 1, 2, 3, 4, 5, 6, 7, 8, 28, 29]). So d >= 11 and d <= 11, hence d = 11 exactly.

## Part 3: d strictly above the live lower bound and at most the upper bound, for the right cell

Finding: met. I fetched the cell once with plain curl, User-Agent "V3R1T4S-research-agent", no retries (saved as mine/live/cell.html):
```
2026-10-29T01:24:04Z
http_code=200 size=3510
920f1b71ab28952457d69a6f2ef2b422cba4790e647ba66d4f42f990965e524e  live/cell.html
Bounds on linear codes [31,17] over GF(9) lower bound: 10 upper bound: 13 ... last modified: 2001-12-17
```
The live page is byte-identical to table/bklc_q9_n31_k17.html (same sha256). It is the cell for q=9, n=31, k=17. 10 < 11 <= 13. The table derives lower bounds through neighbors (shortening, puncturing, subcodes), so a cell lower bound of 10 also means no listed neighbor already implies d = 11 here. The code is not subsumed by the table.

## Field encoding well defined and used consistently

Finding: met.
- `modulus w^2 - w - 1 roots in GF(3): [] -> irreducible`. A quadratic with no root is irreducible.
- I checked the field axioms exhaustively on all triples: `field axioms ok; order of w = 8` (w is also primitive).
- The object says "a + b*w encoded as a + 3b". The rebuild (rebuild/gf9lib.py), both C checkers, witness_check.py and my own code all use w^2 = w + 1 under that encoding. The rebuilt matrix hashes equal to the object, so the stated construction (Hermitian curve y^3 + y = x^4, C(D,16P) plus 3 rows with a 4-column tail) produces exactly this G in this encoding.

## Part 4: not a LinCodeEvolve code; no newer arXiv claim reaching d

Finding: met as far as I could check.
- arXiv:2609.37056 (abstract page via WebFetch) is "Evolving Towards Better Codes: LLM-Guided Search for High-Distance Binary Linear Codes". Its 7 codes are all binary: [172,21,66], [173,20,68], [176,21,68], [181,21,70], [184,21,72], [189,22,72], [200,21,77]. A GF(9) [31,17] code from an explicit Hermitian Construction X is neither one of them nor derived from them.
- One web search for a [31,17,11] GF(9) claim found no arXiv paper with these parameters. The closest hit was Daskalov, Metodieva & Hristov (2004, Problems of Information Transmission, not on arXiv); its abstract does not list parameters. A single search cannot prove absence. The live cell, which states 10, is the binding authority for part 3.

## Null model

I agree that none is needed. The object is explicit and every check is deterministic and exact. There is no statistical claim to calibrate.

## Scope flag for the main session (not a failure on the literal text)

- The bank entry id is `codetables-binary-linear`, and its feasibility clause says "2^k". Both suggest a binary-focused target. The verbatim criterion, however, says "generator matrix over GF(q)" and "the live ... cell for (q,n,k)". The caller also named the cell (9,31,17). Whether a GF(9) record counts for this bank entry is a scope decision for the human. On the text as written, it qualifies.

## Blocks

None. The one curl returned HTTP 200 with no challenge page. WebFetch and WebSearch returned normally.

confirmed_scope: The 17 x 31 matrix in object/code_q9_n31_k17_d11.json, read over GF(9) = GF(3)[w]/(w^2 - w - 1), has rank 17 and exact minimum distance 11 (three agreeing exact methods plus an in-span weight-11 witness), which is strictly above the lower bound 10 and within the upper bound 13 of the codetables.de cell (q,n,k) = (9,31,17) as fetched at 2026-10-29T01:24:04Z.

context: subagent (Claude Code Agent tool, claude-opus-5-5, fresh context, saw only claim/)

injection_suspected: none (no instructions found in the claim files, the fetched page or program output)

pass: true
