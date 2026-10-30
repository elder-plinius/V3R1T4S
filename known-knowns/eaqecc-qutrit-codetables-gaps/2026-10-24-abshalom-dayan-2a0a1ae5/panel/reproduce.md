# REPRODUCE skeptic verdict: [[28,9,11;7]]_3 from claim/object/eaqecc_28_9_11_7.json

**Bottom line: pass.** I wrote my own exact checker before reading the author's checkers/ or rebuild/. From the
matrix S alone it gives s = 26, c = 7, k = 9 and d = 11. The search is exhaustive: all 13,123,110 position
10-subsets hold no vector of span(S)^perp outside the isotropic part, and my own explicit vector of symplectic
weight 11 lies in span(S)^perp and outside span(S). Every value printed by the author's REPRODUCE.md steps 1-4
matches the document exactly, and the steps are deterministic: two runs gave identical output. Out of scope here:
the live table cell (d_lower = 10, d_upper = 14) and novelty, which other skeptics cover. The bound check
10 < 11 <= 14 holds for the values CLAIM.md cites.

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

Time window (date -u): 2026-10-24 17:04:12 UTC to 17:14:09 UTC.
Object hash (shasum -a 256 claim/object/eaqecc_28_9_11_7.json): 2a0a1ae5e178dcc0264b6a9f40ee1935991f28e65199a0712aecffe879b6c7d0,
the same as stated in CLAIM.md.

## The definition (quoted from claim/CLAIM.md, success criterion)

> with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic
> commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in
> the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition
> used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper.
> Results for c = 0 are excluded

Conventions used (from the object JSON's `S_convention`): rows (x|z) over GF(3), 2n = 56 columns, symplectic form
<(x|z),(x'|z')> = x.z' - z.x'. The weight is the symplectic weight, meaning the number of positions i with
(x_i, z_i) != (0, 0).

## What I computed and how (files in mine/, relative to the work folder)

- `mine/gf3lin.py` handles exact GF(3) linear algebra, from S only. It computes s = rank(S) and the Gram matrix
  <s_i, s_j> with c = rank/2, then k = n - s + c. It finds N = span(S)^perp as the null space of the rows (s_z | -s_x).
  It finds I = span(S) ∩ N as the null space of those rows plus the rows (b_z | -b_x) for each basis vector b of N.
  This works because span(S) = N^perp. I is cross-checked by a second route, I = {uS : u in the left kernel of
  the Gram matrix}, and both routes give the same space.
- `mine/dsearch.c` runs the exhaustive search. For a position set T, the vectors of N supported on T form N_T, with
  dim N_T = 2|T| - rank(H_N restricted to T's 2|T| columns), and likewise for I_T. Some vector of N \ I is supported
  on T exactly when rank(H_I|T) > rank(H_N|T). Every vector of weight <= W has its support inside some W-subset, so
  checking all C(n,W) W-subsets covers every vector of weight <= W. The search is a depth-first enumeration with
  incremental GF(3) echelon forms (bit-sliced), checking every subset with no sampling or pruning. d is the first
  W with a positive count. For that W it also sums 3^dim N_T - 3^dim I_T, which is the exact number of
  minimum-weight vectors of N \ I.
- `mine/witness_mine.py` turns a reported T into an explicit vector and re-checks it from the definition: weight,
  <v, s_i> = 0 for every row, and rank(S + v) > rank(S).

### Results on the claimed object

`python3 mine/gf3lin.py claim/object/eaqecc_28_9_11_7.json`:
`n=28 rows=26 s=26 c=7 k=9 dimN=30 dimI=12` (the 26 rows are independent; c = 7 >= 1).

`mine/dsearch 1 14` (output in `mine/obj_run1.txt`, sha256 6ef0d09f...c325; run twice, identical):

| W | subsets checked | subsets with a vector of N \ I |
|---|---|---|
| 1 to 9 | C(28,W) each | 0 |
| 10 | 13,123,110 = C(28,10) | 0 |
| 11 | 21,474,180 = C(28,11) | 5,211 (41,688 = 5,211 x 8 vectors of weight 11 in N \ I) |

The first 11-subset is T = {0,1,2,3,4,5,6,11,18,26,27}. `mine/witness_mine.py` on it gives
`dim_N_T=2 support=[0, 1, 2, 3, 4, 5, 6, 11, 18, 26, 27] symplectic_weight=11 in_N=True in_span_S=False -> in_N_minus_I=True`. So **d = 11 exactly**.

### Further checks of the saved files (`mine/check_json.py`, own GF(9) arithmetic with w^2 = w + 1)

- S equals phi(D9) exactly, with rows r and w*r for each row r of D9, as the JSON states.
- G9 . conj(D9)^T = 0, so D9 is Hermitian-orthogonal to G9. The ranks are 30 for phi(G9) and 26 for S.
- span(S)^perp = phi(C), where C is the GF(9)-span of G9.
- I rebuilt G9 from the construction text with my own code: 27 affine points of y^3 + y = x^4, 15 monomials, and one
  monomial (3,2) of pole order 17. Its rows equal the rows of G9 as a set.
- The author's GF(9) witness codeword from step 3, converted to (x|z) by my code, has weight 11, lies in N, and is
  not in span(S).

## Tests of my checker

| test | cases | result |
|---|---|---|
| `mine/test_small.py` seed 1: random S, n = 1..6, generic / sparse / near-Lagrangian / GF(9)-linear, against brute force over all 3^(2n) vectors and all 3^r combinations of rows (no shared code) | 400 | 0 mismatches in s, c, k, dim N, dim I, d, or the count of minimum-weight vectors; brute d ranged over 1..6 plus the empty case (N = I) |
| same, seed 2 | 600 | 0 mismatches (d over 1..5 and empty) |
| `mine/test_n7.py`, n = 7, brute force over 3^14 vectors | 16 | 0 mismatches (d up to 5) |
| `mine/test_degenerate.py`: cases where the lightest nonzero vector of N lies in I, so excluding I matters | 40 (from 6,555 drawn) | 0 mismatches |
| seeded negative (a): position 0 zeroed in the object's S, known d = 1 | 1 | checker: c=8, d=1 (detected at W=1) |
| seeded negative (b): weight-10 vector v planted by S_b = basis of span(S) ∩ v^perp, with v checked to be in N_b and outside span(S_b), so d <= 10 is known | 1 | checker: s=25, d=7 <= 10; witness re-checked (weight 7, in N, outside span) |
| seeded negative (c): one entry of S changed (row 0, column 0, +1) | 1 | checker: c=8, k=10, d=10, so the claim's parameters are not met; witness re-checked |

## Author's REPRODUCE.md steps 1-4, reproduced

I ran them verbatim in a copy of claim/ (`author_run/`) so the package stays unchanged. The script is
`mine/run_author_steps.sh`, with output in `mine/author_run1.txt` and `mine/author_run2.txt`. With timing lines
removed, both runs hash to 9fd7dad178a629f2255b033fb9dc263fd570b5124ee240c31974a6b28e0c1d43, so they are identical.
Total time was 30.98 s.

| step | REPRODUCE.md expects | printed | match |
|---|---|---|---|
| 1 rebuild | rebuilt.json sha256 = 2a0a1ae5...c7d0 | `2a0a1ae5e178dcc0264b6a9f40ee1935991f28e65199a0712aecffe879b6c7d0  rebuilt.json` (and the same for the object) | yes |
| 2 prep | `n=28 s=26 c=7 k=9 dim_N=30 dim_I=12 N_closed_under_w=True`, `kappa=15` | identical | yes |
| 2 m=18 | every part `deficient=0`, subsets sum to 13,123,110 | 8,788,392 + 3,226,638 + 1,108,080 = 13,123,110; deficient 0, 0, 0 | yes |
| 2 m=17 | deficient = 3396, 1335, 480 (sum 5211 of 21,474,180) | 3396, 1335, 480; subsets 13,793,868 + 5,561,754 + 2,118,558 = 21,474,180 | yes |
| 3 GF(9) witness | `weight=11 in_N=True orthogonal_to_all_rows_of_S=True in_isotropic_part=False` | identical | yes |
| 3 GF(3) witness | `symplectic_weight=11 orthogonal_to_all_rows_of_S=True in_span_S=False` | identical; the vector equals the one from my own witness_mine.py | yes |
| 4 prep | `n=28 s=26 c=7 k=9 dim_isotropic=12 dim_dual=30` | identical | yes |
| 4 W=10 | every part `with_vector_outside_isotropic=0`, all 13,123,110 subsets | 0, 0, 0; examined 3 x 4,374,370 = 13,123,110 | yes |
| 4 W=11 | 1735, 1745, 1731 (sum 5211) | 1735, 1745, 1731; examined 3 x 7,158,060 = 21,474,180 | yes |

The proof steps hold up when re-derived:
1. s, c and k come straight from ranks of S and of its Gram matrix, and my code agrees.
2. **d >= 11 (method A).** N is closed under w, so N = phi(C) for a GF(9)-linear [28,15] code. Symplectic weight on
   phi(C) equals Hamming weight on C. A nonzero codeword of weight <= 10 would vanish on some 18-subset U, which
   would make rank(G_U) < 15. infoset finds 0 such U, so d(C) >= 11, and d >= 11 since N \ I is inside N \ {0}.
   The infoset pruning only bulk-counts completions that are certainly full rank or certainly rank-deficient,
   which is exact.
3. **d >= 11 (method B and mine).** This is the subset rank test. My own implementation uses a different
   formulation (parity checks restricted to T, not bases restricted to the complement) and gives the same 0 at
   W = 10 and the same 5,211 at W = 11.
4. **d <= 11.** Two explicit weight-11 vectors, the author's two and mine, each re-checked by my code.

Not checked here: step 5 (the live fetch of the qutrit table) and novelty, which belong to the other skeptics.

pass: true
