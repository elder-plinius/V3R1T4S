saved by the main session from the subagent's returned text (REPRODUCE skeptic, model fable, returned 2026-10-17 about 18:58Z)
context: REPRODUCE skeptic, fresh subagent (Claude Agent tool), model fable, sees only claim/

# panel/reproduce.md — REPRODUCE skeptic, run 2026-10-17-1119

Finished 18:57Z (deadline 19:35Z). No web requests were made by this skeptic; nothing appended to the stop list. Only claim/ was read; all scratch work lives in a separate work directory.

## 1. Definition my checker was written from (quoted, before opening verify/ or REPRODUCE.md)

From claim/CLAIM.md, "Success criterion (verbatim, from the V3R1T4S bank)":

> "with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper."

From claim/CLAIM.md, "Object":

> "Each row is a stabilizer generator on Alice's 33 qutrits: X part x_1..x_33, then Z part z_1..z_33." / "Symplectic form used: <u,v> = u_X . v_Z - u_Z . v_X (mod 3). Symplectic weight = number of positions i with (x_i, z_i) != (0,0)."

Note: S^perp \ (S ∩ S^perp) = S^perp \ S, so for a vector already in the dual, "not in the isotropic part" is exactly "not in span(S)".

## 2. My method (deliberately different from the author's)

my_checker.py (pure-Python GF(3) row reduction for ranks, numpy only for the enumeration grid):
1. parse rows, check alphabet {0,1,2}, 66 columns -> n = 33;
2. s = rank(S) by my own RREF over GF(3);
3. Gram matrix G = S J S^T with <u,v> = u_X.v_Z - u_Z.v_X, assert antisymmetric with zero diagonal; c = rank(G)/2 (assert even);
4. k = n - s + c;
5. dual basis = nullspace of (S J) via free-variable method; assert dim = 2n - s and every basis vector is symplectically orthogonal to every generator;
6. enumerate ALL 3^dim vectors of the dual as the full coefficient grid times the basis (assert 3^dim distinct vectors; no sampling);
7. isotropic membership by solving the linear system x S = v: reduce each dual vector against the pivot rows of RREF(S); in span(S) iff residual is zero;
8. independent cross-check of the isotropic set: { x S : x in nullspace(G) } enumerated fully, asserted equal as a set of tuples to the set flagged in step 7;
9. d = min symplectic weight over dual minus isotropic; full weight distribution kept; sha256 digest of the sorted logical vectors printed for determinism comparison.

The author's verify/eacheck.py (read only afterwards) instead extends the isotropic basis to a basis of the dual and enumerates cosets b.E + Iso for nonzero b — a different enumeration and a different membership route.

A third, numpy-free route (my_checker_pure.py, run under plain python3 that has no numpy at all) builds the dual and the isotropic part as explicit sets by incremental closure and takes the set difference.

## 3. Commands and outputs

Object integrity:
```
shasum -a 256 claim/object/S_33_1_31_24.txt
925e749d364cd1e7c4f71101484aab051bd2dae5522ad57900fd022c11629edc   (matches CLAIM.md)
```
56 non-comment rows, each 66 entries, alphabet tally: 3557 zeros, 89 ones, 50 twos. One comment line (it notes "replaces d=28 file", i.e. the object was revised during the run; informational only).

My checker (venv python with numpy, `python -I my_checker.py claim/object/S_33_1_31_24.txt`), identical output on runs 1, 2, 3:
```
rows (generators listed) = 56, columns = 66, n = 33
s = rank(S) over GF(3) = 56  (independent generators)
rank(S J S^T) = 48, c = 24
k = n - s + c = 33 - 56 + 24 = 1
dim span(S)^perp = 10  (expected 2n - s = 10)
enumerated 59049 = 3^10 vectors of span(S)^perp (exhaustive)
isotropic part |span(S) ∩ span(S)^perp| = 6561 = 3^8  (expected 3^(s-2c) = 3^8 = 6561)
cross-check: isotropic part via nullspace(SJS^T) matches (6561 vectors)
d = min symplectic weight over span(S)^perp \ isotropic = 31
weight distribution (weight: all-dual, isotropic, logical=dual-minus-isotropic):
  w= 0:      1      1      0
  w= 2:     24     24      0
  w= 3:      8      8      0
  w= 4:    216    216      0
  w= 5:    144    144      0
  w= 6:    888    888      0
  w= 7:    864    864      0
  w= 8:   1584   1584      0
  w= 9:   1760   1760      0
  w=10:    864    864      0
  w=11:    192    192      0
  w=12:     16     16      0
  w=31:  17496      0  17496
  w=32:  17496      0  17496
  w=33:  17496      0  17496
min nonzero weight of isotropic part = 2
digest sha256(sorted logical vectors) = 040696b987d9b92dff7f58bf4619c5d27367a8b1aab402ceaf203f8834c3ef0d
RESULT n=33 s=56 c=24 k=1 d=31
```
Weight distribution near d: no logical vector of weight below 31; 17496 logical vectors at each of weights 31, 32, 33 (52488 = 3^10 - 3^8 total). Every dual vector of weight <= 12 lies in the isotropic part. The code is impure/degenerate (isotropic part contains weight-2 elements); the quoted criterion explicitly uses the impure-allowed Grassl definition, so this does not affect d, but the other skeptics may want to note it.

Third route, numpy-free, plain python3 (`python3 -I my_checker_pure.py claim/object/S_33_1_31_24.txt`, 3.6 s):
```
|D|=59049 |I|=6561 |D\I|=52488
logical weight distribution: [(31, 17496), (32, 17496), (33, 17496)]
digest sha256(sorted logical vectors) = 040696b987d9b92dff7f58bf4619c5d27367a8b1aab402ceaf203f8834c3ef0d
RESULT n=33 s=56 c=24 k=1 d=31
```
Same digest as the numpy route, so the two independently built logical sets are identical vector-for-vector.

## 4. Author-check comparison (claim/REPRODUCE.md steps, run with -I and explicit paths)

Step 1, `python3 -I verify/eacheck.py object/S_33_1_31_24.txt --expect 33,1,31,24` (venv python; REPRODUCE.md declares numpy as a requirement and the plain python3 on this machine has no numpy, so the venv interpreter was used), two runs, identical:
```
n 33 s 56 c 24 k 1 d 31
PASS        (exit 0)
```
Agrees with my n, s, c, k, d exactly.

Step 2, `python3 -I verify/parse_table.py data/qutrit.php.html <tsv>` then the row for 33/1/24 (both via `grep -P '^33\t1\t24\t'` as written and via awk):
```
entries 3888 gaps 3281 gaps c>=1 2892 gaps c>=1 n<=15 165
33	1	24	25	32	#ff9900	lengthening of [[25,1,25;24]] increasing dimension of [[25,0,25;23]] from arXiv:2207.05647
```
Step 3, `shasum -a 256 data/qutrit.php.html`:
```
37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c   (matches REPRODUCE.md and TABLE_RECORD.md)
```

## 5. Table cell, parsed independently (my_table_parse.py, own regex over `<TD ... class="EAQECC" title="...">[[n,k,dl-du;c]]<sub>3</sub></TD>`)

```
sha256(file) = 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c bytes = 628039
Last change: 10.07.2025
total EAQECC entries parsed: 3888   (equals the count of class="EAQECC" TDs in the file: 3888)
entries with (n,k,c) = (33,1,24): 1
  [[33,1,25-32;24]]_3  d_lower=25 d_upper=32  title='lengthening of [[25,1,25;24]] increasing dimension of [[25,0,25;23]] from arXiv:2207.05647'
(n=33,k=1) box by c: c=0: 11-15; c=1: 24-32; c=24: 25-32; c=25: 26-32; c=26: 27-32; c=27: 28-32; c=28: 29-32; c=29: 30-32; c=30: 31-32; c=31: 32-32; c=32: 33-33
```
Exactly one cell for (33,1,24); d_lower = 25, d_upper = 32; byte count 628039, sha256, "Last change: 10.07.2025" and the title string all match claim/TABLE_RECORD.md. My entry count (3888) equals the author's parser's count.

Criterion arithmetic: c = 24 >= 1; d = 31 > d_lower = 25 (strict); d = 31 <= d_upper = 32; k = 1 = n - s + c. All satisfied.

## 6. Determinism

- My numpy checker: three runs, byte-identical output (run 1 differed only by a Python SyntaxWarning line about a docstring escape, fixed before runs 2 and 3; result lines identical in all three).
- My numpy-free checker under a different interpreter: same RESULT line and same logical-set digest 040696b9...3ef0d.
- Author's eacheck.py: two runs, byte-identical output, PASS both times.
- Four result lines and four digests across all my runs collapse to one unique value each.

## 7. Limits of this check

- The criterion's "re-fetched live immediately before claiming" is attested only by claim/TABLE_RECORD.md (three lens re-fetches at 18:11-18:15Z with identical sha256); this role has no web access and did not re-fetch. Every property verifiable from the saved files was verified.
- The dual is small (3^10 = 59049 vectors), so exhaustive enumeration is complete, not a spot check.

pass: true
