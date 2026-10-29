# REPRODUCE skeptic verdict: claim/object/code_q9_n32_k19_d10.json

Bottom line: I confirmed the claimed properties independently. G has rank 19 over GF(9), no nonzero codeword has weight <= 9 (checked over every column subset, not a sample), and there is a weight-10 codeword, so d = 10 exactly. The author's two exact programs, the witness check and the rebuild all reproduce, and the rebuild matches the object byte for byte. Out of scope for this role, and not checked here (no network): the live codetables.de bound (criterion 3) and novelty (criterion 4).

Started (date -u): Wed Oct 28 01:21:11 UTC 2026. Last check (date -u): Wed Oct 28 01:24:40 UTC 2026.

## Definition used (quoted from the object, field "field")

> "GF(9) = GF(3)[w]/(w^2 - w - 1); a + b*w encoded as a + 3b (0..8)"

Claim (claim/CLAIM.md): "The 19 x 32 matrix G over GF(9) in object/code_q9_n32_k19_d10.json generates a linear [32,19,10] code over GF(9)". Success criterion (2), quoted: "The exact minimum distance d is computed ... by two independent exact minimum-distance implementations that agree; never by sampling."

Object hash (shasum -a 256): `e9e64b4eef94a2fc783bf8e027b849d0d931a3641607aa98121561a77cb77965  claim/object/code_q9_n32_k19_d10.json` (matches the hash in CLAIM.md).

## My own checker (written before I read any author code)

My files are in mine/ inside this skeptic's work folder. They are not part of claim/.

1. mine/gf9prep.py (Python standard library). It builds GF(9) from the definition: (a+bw)(c+dw) = (ac+bd) + (ad+bc+bd)w, using w^2 = w+1. It then checks the field axioms on the tables: w^2 - w - 1 has no root in GF(3), multiplication is associative and distributes over addition for all 729 triples, every nonzero element has an inverse, and w has multiplicative order 8. It row-reduces G and builds the parity-check matrix H (13 x 32) from the RREF. It verifies G*H^T = 0 and rank(H) = 13. Since rank(G) = 19, the row space of H is exactly the dual code.
2. mine/depsearch.c (cc -O2 -Wall). It runs a depth-first search over column subsets of H in increasing index order, keeping an echelon basis. It extends a subset only while the subset stays linearly independent.
   - Why this is exhaustive: a nonzero codeword with support S, |S| <= 9, exists if and only if some set of <= 9 columns of H is linearly dependent. Every subset of an independent set is independent, so the DFS reaches every independent subset. It stops early only after it finds a dependency, and in this run none was found. The per-size visit counts equal C(32,s) for every s = 1..9. That proves every subset of size <= 9 was examined and found independent.
   - Self-test (mine/selftest.py): on 300 random small GF(9) matrices, some with a planted dependency, the C search with limit L found a dependency exactly when a Python brute-force rank check over all subsets gave a minimum dependent size <= L. Result: `selftest trials=300 mismatches=0`. The first harness version used one run with limit L = n and reported mismatches. That was a harness error: depth-first order does not return the smallest set first. After switching to iterative deepening there were 0 mismatches. This does not affect the main run, which found no dependency at all.
3. mine/witness.py solves for the message vector m of the codeword supported on the dependent 10-set and recomputes c = mG directly.
4. mine/myrebuild.py rebuilds G from the construction sentence alone, using my own field tables.

Real outputs:

```
q=9 n=32 k=19 rank(G)=19 pivots=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 21]
rank(H)=13 (n-k=13), G*H^T=0 verified
```

`./depsearch 9 H.txt` (0.66 s user):
```
independent 1-subsets visited: 32
independent 2-subsets visited: 496
independent 3-subsets visited: 4960
independent 4-subsets visited: 35960
independent 5-subsets visited: 201376
independent 6-subsets visited: 906192
independent 7-subsets visited: 3365856
independent 8-subsets visited: 10518300
independent 9-subsets visited: 28048800
no dependent set of size <= 9
```
math.comb(32, s) for s = 1..10: `[32, 496, 4960, 35960, 201376, 906192, 3365856, 10518300, 28048800, 64512240]`. These are equal to the counts for s = 1..9.

`./depsearch 10 H.txt`: `first dependent set size=10 cols= 0 1 2 3 4 5 6 7 8 31`

`witness.py ... 0,1,2,3,4,5,6,7,8,31`:
```
kernel dim of outside-S constraints: 1
message m = 1 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0
codeword c = mG = 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
weight = 10 support = [0, 1, 2, 3, 4, 5, 6, 7, 8, 31]
```
So m = rows 1 + 4 + 10 + 16 of G (1-based), and that sum has weight exactly 10. Together with the exhaustive search, d = 10.

`myrebuild.py`: `my rebuild equals object G: True`. Checked from the text: the 27 affine points of y^3 + y = x^4 in lexicographic order; 19 monomials x^i y^j with j <= 2, ordered by pole order 3i+4j <= 21; rows 16..19 = x^6, x^5 y, x^4 y^2, x^7; the 5 tail columns are the PG(3,9) points listed in the text; the first 15 rows have a zero tail.

Determinism: building H twice gave the same hash (1a8db63e197083a01a265b0c2ee427934161369156187ae11b93fe8795ad994f). Two runs of `depsearch 9` gave the same output hash, 1acf34e033da6566828ee4f4932e14fa91a02fc1f463540d50da60db786648c1 (both).

## Author's commands (claim/REPRODUCE.md), run after my checker

Step 1, rebuild:
```
k 19 n 32 rank 19
e9e64b4eef94a2fc783bf8e027b849d0d931a3641607aa98121561a77cb77965  rebuilt.json
e9e64b4eef94a2fc783bf8e027b849d0d931a3641607aa98121561a77cb77965  object/code_q9_n32_k19_d10.json
BYTE_IDENTICAL   (cmp)
```
The package ships rebuild/__pycache__/*.pyc files, which Python could load in place of the source. So I also rebuilt from a copy of only the .py sources with `python3 -B -I`. The result had the same hash, e9e64b4e...7965.

Step 2: code.txt sha256 298c3f6b897a7a39189e3620f796d06fc382cee50cf9fffc07a56b448459b225.

Step 3, `./m3 < code.txt` (7.29 s user):
```
k=19 n=32 rank=19
W=1: no nonzero codeword of weight <= 1 (all 32 subsets)
...
W=8: no nonzero codeword of weight <= 8 (all 10518300 subsets)
W=9: no nonzero codeword of weight <= 9 (all 28048800 subsets)
W=10 complete for all W'<10; first nonzero codeword supported in a 10-set after 23 subsets
d=10 witness_weight=10 witness=1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
```
(W = 2..7 lines are identical in form; their subset counts are the same as my counts above.)

Step 4, `./hdep 10 < code.txt` (1.10 s user):
```
rank=19 (k=19 n=32)
nodes=43081995
dependent_min=10 d=10
```
Consistency check: the sum of C(32,s) for s = 1..9 is 43081972, and 43081972 + 23 tested 10-sets = 43081995. This agrees with m3's "after 23 subsets".

Step 5:
```
k=19 n=32 rank(G)=19
witness weight=10 in_rowspace=True support=[0, 1, 2, 3, 4, 5, 6, 7, 8, 31]
```
Repeated runs of m3 and hdep gave the same output hashes (ef82253c... twice, cdd1951f... twice).

Step 6 (live table) was not run: this role has no network. The scout's saved record, claim/table/RECORD.md, reads "lower bound: 9 upper bound: 12". On that record, d = 10 is above the lower bound and at most the upper bound.

## Code review notes

- m3_mindist.c checks the generator side over every W-subset T of coordinates, using a left kernel of A[I∩T, R\T]. hdep.c searches dependent columns on the dual side, and its pruning `s+1 >= best-1` only cuts branches after a dependency of size best is found. Both are exact. Their results agree with each other and with my code.
- My checker uses the same dual-side idea as hdep.c, but it is separate code written before I saw hdep.c. It also agrees with m3, which uses a different method.
- The rebuild's to_json.py writes d = 10 as a label passed on the command line. It does not compute d. The exact searches establish d.

## Mismatches

None. Rank, d, the witness, the subset counts, the rebuild hash and determinism all agree.

## Blocks

None. No tool-guard or classifier block occurred, and no HTTP request was made.

injection_suspected: none. A grep of claim/ for instruction-like text found nothing, and none of the files I read contained instructions.

context: subagent (Claude Code Agent tool, fresh context, claude-opus-5-5)
pass: true
