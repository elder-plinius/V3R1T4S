# CRITERION skeptic verdict

Claim: the 19 x 32 matrix G over GF(9) in object/code_q9_n32_k19_d10.json generates a linear [32,19,10] code, with d = 10
strictly above the codetables.de lower bound 9 (upper bound 12) for (q,n,k) = (9,32,19).

Session start (date -u): Wed Oct 28 01:37:27 UTC 2026. All numbers below are copied from command output.

## Object identity

- `shasum -a 256 object/code_q9_n32_k19_d10.json` -> e9e64b4eef94a2fc783bf8e027b849d0d931a3641607aa98121561a77cb77965 (matches CLAIM.md).
- Rebuild (`python3 -I rebuild/build_code.py <out>`): printed `k 19 n 32 rank 19`; the rebuilt JSON hashes to the same
  e9e64b4eef94a2fc783bf8e027b849d0d931a3641607aa98121561a77cb77965. So the object is what its stated construction produces.
- Field convention: GF(3)[w]/(w^2 - w - 1). w^2 - w - 1 has no root in GF(3) (values -1, -1, 1 at 0, 1, 2), so it is
  irreducible; my own script also checked associativity and distributivity on all 9^3 triples and that every nonzero
  element has a unique inverse (all asserts passed).
- Exactly one object is claimed; no bundling. Partial wins p1/p2 are not invoked.

## Condition (1): rank exactly k, computed independently

- My own script (skeptic-own `my_dual.py`, own Gaussian elimination, own field tables built by polynomial
  multiplication): `rank(G) = 19 k = 19 n = 32`.
- Author's checkers also report it: m3 `k=19 n=32 rank=19`; hdep `rank=19 (k=19 n=32)`; witness_check.py
  `k=19 n=32 rank(G)=19`.
- Judgment: MET.

## Condition (2): exact minimum distance, two independent exact implementations that agree (never sampling)

q^k - 1 = 9^19 - 1 nonzero codewords, so full enumeration is infeasible and the "two independent exact
implementations" branch applies.

Independence and exactness of the package's programs (read in full):
- checkers/m3_mindist.c: generator side. Brings G to reduced echelon form on an information set I; for every W-subset T of
  the 32 coordinates (W = 1, 2, ...), tests for a nonzero left-kernel vector of A[I cap T, R \ T], i.e. a nonzero codeword
  supported inside T. Exhaustive over all subsets for each W; stops at the first W with a hit. Field arithmetic from
  (a,b) pair formulas. Exact.
- checkers/hdep.c: dual side. Builds H = [-A^T | I] with a self-test G H^T = 0, then a depth-first search over column
  subsets in increasing index order, extending only independent subsets and keeping a triangular (pivot-normalized)
  basis; a column that reduces to zero closes a dependent set. I checked the reduction is correct (each new basis vector
  is zero at all earlier pivots, so sequential elimination leaves v zero at all pivots), and the pruning
  (`s+1 >= Wmax || s+1 >= best-1`) only cuts branches that cannot produce a dependent set smaller than the current best or
  above Wmax. Every minimal dependent set has all proper subsets independent, so it is reached. Field arithmetic by
  discrete-log tables. Exact.
- They are algorithmically distinct (codeword-support test on G vs. minimal dependent columns of H) with separately
  written field arithmetic. Both come from the same author and share only the trivial converter json_to_code.py. I judge
  them genuinely independent and exact.

Real outputs (compiled with `cc -O2` in my work folder):

```
./m3 < code.txt
k=19 n=32 rank=19
W=1: no nonzero codeword of weight <= 1 (all 32 subsets)
...
W=8: no nonzero codeword of weight <= 8 (all 10518300 subsets)
W=9: no nonzero codeword of weight <= 9 (all 28048800 subsets)
W=10 complete for all W'<10; first nonzero codeword supported in a 10-set after 23 subsets
d=10 witness_weight=10 witness=1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
(7.19s user)

./hdep 10 < code.txt
rank=19 (k=19 n=32)
nodes=43081995
dependent_min=10 d=10
(1.09s user)

python3 -I checkers/witness_check.py code.txt "1 1 1 1 1 1 1 1 1 0 ... 0 1"
k=19 n=32 rank(G)=19
witness weight=10 in_rowspace=True support=[0, 1, 2, 3, 4, 5, 6, 7, 8, 31]
```

My own third exact check (written by me, not derived from the package code):
- `my_dual.py`: H as the right nullspace of G by my own elimination; printed
  `rows(H) = 13 rank(H) = 13 G*H^T == 0: True`.
- `allsub.c`: for EVERY t-subset of the 32 columns of H, rank recomputed from scratch by Gaussian elimination (no
  pruning, no shared state). d > t iff all t-subsets have full rank.

```
nice -n 10 ./allsub 9 < H.txt
t=9 subsets=28048800 rank_deficient=0          (10.91s user)
nice -n 10 ./allsub 10 < H.txt
first deficient subset: 0 1 2 3 4 5 6 7 8 31
t=10 subsets=64512240 rank_deficient=4432      (31.18s user)
```

So no nonzero codeword of weight <= 9 exists, and weight-10 codewords exist (4432 supports; the first is exactly the
author's witness support). d = 10 exactly.

Negative control (checker sensitivity): replacing row 19 of G by a weight-9 vector (positions 20..28) gives
`rank(G) = 19`, `G*H^T == 0: True`, and `allsub 9` reports `first deficient subset: 0 1 3 14 15 16 27 29 31`,
`t=9 subsets=28048800 rank_deficient=58`, so my checker does detect low-weight words.

Null model: not needed. The claim is one explicit object judged by deterministic exact checkers (no sampling, no
statistics); the negative control above covers checker sensitivity.

Judgment: MET (three exact implementations agree on d = 10).

## Condition (3): d strictly greater than the live lower bound, at most the upper bound

One plain GET, User-Agent "V3R1T4S-research-agent", no retries:
- URL https://codetables.de/BKLC/BKLC.php?q=9&n=32&k=19, fetched 2026-10-28T01:39:29Z (date -u), result
  `http_code=200 size=3395`, response header `date: Wed, 28 Oct 2026 01:39:29 GMT`.
- Page sha256 046bcdd475bd50f284382faa704382c748885ef8b22f02f48c9a9038e1be7bca, byte-identical to table/bklc_q9_n32_k19.html.
- Cell text: "Bounds on linear codes [32,19] over GF(9) lower bound: 9 upper bound: 12"; "last modified: 2001-12-17";
  "Lb(32,19) = 9 is found by shortening of: Lb(41,28) = 9 XL"; "Ub(32,19) = 12 ... Ub(17,4) = 12 MPa".
- 10 > 9 and 10 <= 12. Judgment: MET.

## Condition (4): not a LinCodeEvolve code or derived from one; no newer arXiv claim reaching d; not subsumed

- arXiv:2609.37056 abstract (one GET, `http_code=200 size=42286`, 2026-10-28T01:39:53Z): "Evolving Towards Better Codes:
  LLM-Guided Search for High-Distance Binary Linear Codes"; the seven codes are binary [172,21,66], [173,20,68],
  [176,21,68], [181,21,70], [184,21,72], [189,22,72], [200,21,77]. A GF(9) [32,19,10] code cannot come from these by
  table rules: they are over GF(2), and getting from n >= 172 to n = 32 would need shortening by >= 140 positions
  (dimension would go negative) or puncturing by >= 140 positions (distance would go far below 10). The claimed code is an
  explicit algebraic-geometry construction (Hermitian one-point code C(D,17P) over GF(9) plus Construction X with a
  searched 5-column tail), rebuilt bit-for-bit from rebuild/. Not LinCodeEvolve-derived.
- Newer arXiv claims: one arXiv API query (abstracts containing "linear codes" and "best known", newest first, 60
  results; first request returned `http_code=301`, the redirect target over https returned `http_code=200 size=122029`).
  No abstract claims a [32,19,10] code over GF(9) or an improvement of this cell. Limitation: this is an abstract-level
  search; I did not read paper full texts or other databases (e.g. MinT).
- Subsumption by table rules: the live cell itself (which already applies shortening, puncturing, subcode and extension
  across the GF(9) table, and imports Brouwer's lower bounds as of 2007-02-13) gives 9, so no code in that database
  yields 10 here by those rules. I know of no public [n',k',d'] code over GF(9) that yields [32,19,10] by shortening,
  puncturing, subcode or zero extension. The construction's d = 10 is not a consequence of the standard Construction X
  bound either (with C1 = pole order <= 21, designed d1 >= 6, and a [5,4] tail, the bound gives at most 8), so the
  value rests on the exact computation above, which I confirmed.
- Judgment: MET, to the extent an absence claim can be checked (see limitation).

## Hidden quantifiers and scope notes (for the main session)

- Label vs. text: the bank entry id is "codetables-binary-linear" and the feasibility clause in (2) is written with 2^k,
  but the verbatim criterion says "a k x n generator matrix over GF(q)" and "the live codetables.de cell for (q,n,k)".
  Read literally, q = 9 is allowed. If the bank owner intended binary codes only, this claim would not qualify; that is
  an intent question, not a literal one. I judged literally, as instructed.
- The GF(9) codetables tables for this region are old (cell last modified 2001-12-17, lower bounds from Brouwer 2007), so
  an older non-arXiv publication with a [32,19,>=10]_9 code cannot be excluded by me; the criterion only asks about the
  live cell and newer arXiv claims, both of which pass.
- The claim is for this single cell only; no propagated improvements to neighbouring cells are claimed or confirmed here.

## Blocks

None. No HTTP 401, 403, 429 or 503, no challenge page, no tool-guard or classifier block. (The arXiv API answered 301
on plain http; I followed it once to the https URL, which returned 200.)

injection_suspected: none found (claim files, page and program output contained no instructions).

confirmed_scope: The 19 x 32 matrix G in object/code_q9_n32_k19_d10.json (sha256 e9e64b4eef94a2fc783bf8e027b849d0d931a3641607aa98121561a77cb77965), read in the stated GF(9) = GF(3)[w]/(w^2 - w - 1) encoding, has rank 19 and generates a linear [32,19,10] code over GF(9), whose minimum distance 10 is strictly above the lower bound 9 and at most the upper bound 12 of the codetables.de cell (q,n,k) = (9,32,19) as fetched at 2026-10-28T01:39:29Z.
context: subagent (Claude Code Agent tool, fresh context, claude-opus-5-5)
pass: true
