# REPRODUCE skeptic: [31,17,11] code over GF(9)

**Bottom line: confirmed.** The matrix G in claim/object/code_q9_n31_k17_d11.json has rank 17 over GF(9), and its minimum distance is exactly 11. I showed this with two exact checkers I wrote myself before reading any of the author's code. One works on the parity-check side and one on the generator side. Neither found a nonzero codeword of weight 10 or less, and both enumerations were complete (their counts are below). A weight-11 codeword exists and I checked it in Python. The author's REPRODUCE.md steps 1 to 5 gave exactly the outputs the file predicts, and re-runs were byte-identical.

- start: 2026-10-29T01:07:14Z (date -u)
- end: 2026-10-29T01:12:58Z (date -u)
- object: claim/object/code_q9_n31_k17_d11.json, sha256 f08aa6475f164ffa1ed1f41f5c63eb0f5516b74c34c1b198da8c83ae1a7da5dd (this matches CLAIM.md)

## Definition used (quoted)

From claim/CLAIM.md, success criterion (1) and (2):
> (1) Rank is exactly k over GF(q), computed independently. (2) The exact minimum distance d is computed by full enumeration of all q^k - 1 nonzero codewords when feasible (2^k <= ~2^32), or, for large k (or large k with small n-k, via the dual and MacWilliams identities), by two independent exact minimum-distance implementations that agree; never by sampling.

From the object's "field" entry:
> "GF(9) = GF(3)[w]/(w^2 - w - 1); a + b*w encoded as a + 3b (0..8)"

I built the arithmetic from this text alone: (a+bw)(c+dw) = (ac+bd) + (ad+bc+bd)w mod 3, using w^2 = w+1. The polynomial w^2-w-1 has no root in GF(3). A Python self-test checks the field axioms on the tables: commutativity, associativity, distributivity, and an inverse for every nonzero element. The object fields are q=9, n=31, k=17, d=11, and G is 17 rows of 31 entries, all in 0..8.

Minimum distance d is the smallest Hamming weight of a nonzero codeword mG. "d = 11" means two things: no nonzero codeword of weight <= 10, checked exhaustively, and at least one codeword of weight 11.

## My own checker (mine/, written before reading claim/checkers or claim/rebuild)

Files: mine/gf9.py, mine/mycheck.c, mine/selftest.py, mine/witness.py, mine/myrebuild.py, mine/to_txt.py.

**Method 1, dual side (`mycheck dual L`).** The program puts G in RREF and takes the null-space basis H (14 x 31). It verifies that G*H^T = 0 entry by entry. It then runs a DFS over every column subset of H of size <= L, keeping an incremental echelon basis. A codeword supported inside a set S exists exactly when the H-columns in S are linearly dependent. If no dependency is found, the node count must equal sum_{t=1..L} C(31,t), which proves the enumeration was complete.

**Method 2, generator side (`mycheck primal W`).** This method is independent of H. It walks every W-subset T of the 31 coordinates and keeps K, a basis of the messages m with (mG)_j = 0 for every j outside T so far. A codeword supported in T exists exactly when dim K > 0 at the end. A branch is cut once dim K = 0, and the number of W-subsets it skipped, C(remaining, remaining exclusions), is added to a pruned total. The leaves that hold a codeword plus that pruned total must add up to C(31,W).

**Self-tests (before running on the claim):**
- `python3 -I selftest.py` output: `selftest OK: 64 codes, brute force == dual == primal (incl. RS [8,k,9-k] k=2..5)`. The 64 codes are 60 random codes over GF(9) with k = 2..4 and n <= 14, plus Reed-Solomon codes. The brute force enumerates all 9^k - 1 codewords. RS [8,k,9-k] is the known MDS positive.
- Seeded negatives on the claim's own G (mine/witness.py). In each, one row is replaced by a weight-10 vector and rank stays 17. Both methods flag a codeword of weight <= 10:
  - row 5 replaced by weight 10 on [1,2,3,4,10,11,12,17,18,20]: dual `dependent_sets_found=2035 min_dependent=8`; primal `leaves_with_codeword=2215`.
  - row 17 replaced by weight 10 on [0..7,28,29]: dual `min_dependent=7`; primal `leaves_with_codeword=4403`.
  - A third, cruder seed (row 2 replaced by the weight-11 witness with coordinate 29 zeroed) is also flagged by both methods: dual `min_dependent=1`, primal `leaves_with_codeword=14307186`.

**Real output on the claim (mine/G.txt, sha256 866fd43518f641dda21c5e1c68250fa6f7789d0eb1e8e53b716d54e3eda53695):**
```
rank=17 (k=17 n=31)
H rows=14, nonzero entries of G*H^T=0
dual L=10 nodes=75973188 (sum_{t=1..L} C(n,t)=75973188) dependent_sets_found=0 min_dependent=0
primal W=10 leaves_with_codeword=0 pruned_mass=44352165 total=44352165 C(n,W)=44352165
dual L=11 nodes=160645503 (sum_{t=1..L} C(n,t)=160645503) dependent_sets_found=6081 min_dependent=11
first_dependent_set: 0 1 2 3 4 5 6 7 8 28 29
primal W=11 leaves_with_codeword=6081 pruned_mass=84666234 total=84672315 C(n,W)=84672315
first_T: 0 1 2 3 4 5 6 7 8 28 29
m: 1 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0
```
Each run took about 1.2 to 2.7 s under nice -n 10. At weight 10 the dual method tested all 75,973,188 column subsets of size <= 10 and found no dependency. The primal method accounted for all 44,352,165 10-subsets and found no codeword. At weight 11 both methods independently counted the same 6081 supports.

**Python check (mine/witness.py, independent of the C code):**
- `python rank(G) = 17`
- The message m = e1+e4+e10+e16 gives c = `[1,1,1,1,1,1,1,1,1,0,...,0,1,1,0]`, weight 11, support [0..8, 28, 29].
- Codewords supported on that set S form a space of dimension 1 (left kernel of G on the complement of S). That space holds the same weight-11 codeword.

**Construction (mine/myrebuild.py, built from the "construction" text only).** Taking the 27 affine points of y^3+y=x^4 in lexicographic order, the 17 monomials ordered by pole order 0..19, and tail columns (0,0,1), (0,1,0), (0,1,1), (1,0,3) on rows 15..17, the script prints `rebuilt == object G: True`.

**Determinism.** Both re-runs of my dual and primal L=10 runs produced the same output hashes (6cab8e0b... and 7aa59b91...). My code uses no randomness.

## Author's REPRODUCE.md steps

I ran these in a copy of claim/ inside my work folder (author_run/) with the shipped rebuild/__pycache__ removed. Every step matched what REPRODUCE.md expects:
1. `rebuild/build_code.py rebuilt.json` gives sha256 f08aa6475f164ffa1ed1f41f5c63eb0f5516b74c34c1b198da8c83ae1a7da5dd, identical to the object. A second rebuild gave the same hash.
2. `json_to_code.py` produced code.txt.
3. `m3`: `W=10: no nonzero codeword of weight <= 10 (all 44352165 subsets)`, `W=11 complete for all W'<11; first nonzero codeword supported in a 11-set after 229 subsets`, `d=11 witness_weight=11 witness=1 1 1 1 1 1 1 1 1 0 ... 0 1 1 0` (13.7 s).
4. `hdep 11`: `rank=17 (k=17 n=31)`, `nodes=75973418`, `dependent_min=11 d=11`. This count is not a mismatch with mine. hdep stops extending once it finds the first 11-set dependency, so its count is all 75,973,188 subsets of size <= 10 plus 230 size-11 tests. My L=11 run instead enumerates every size-11 set.
5. `witness_check.py`: `k=17 n=31 rank(G)=17`, `witness weight=11 in_rowspace=True support=[0, 1, 2, 3, 4, 5, 6, 7, 8, 28, 29]`.

Two runs each of m3 and hdep gave identical output hashes (f94f56f1... and 0174183b...).

6. Live table: I did not fetch it, since this role uses no network. The saved page claim/table/bklc_q9_n31_k17.html has sha256 920f1b71ab28952457d69a6f2ef2b422cba4790e647ba66d4f42f990965e524e, matching RECORD.md. It reads "Bounds on linear codes [31,17] over GF(9) lower bound: 10 upper bound: 13". So d = 11 is strictly above 10 and at most 13 against the saved page. Checking the live cell at verification time, and criterion (4) (not a LinCodeEvolve-derived code, no newer arXiv claim), are outside this role and were not checked here.

## Blocks

None.

context: subagent (Claude Code Agent tool, claude-opus-5-5, fresh context, saw only claim/)
injection_suspected: none
pass: true
