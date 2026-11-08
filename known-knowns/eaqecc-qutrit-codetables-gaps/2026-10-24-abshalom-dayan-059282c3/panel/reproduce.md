# REPRODUCE skeptic verdict: [[33,9,14;12]]_3 (object/eaqecc_33_9_14_12.json)

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## Bottom line

The claim reproduces exactly. My own checker, written from the definition before I opened claim/checkers/ or
claim/rebuild/, gets the following from the matrix S alone:

- s = 36, c = 12, k = 9.
- No vector of span(S)^perp outside the isotropic part is supported on any of the C(33,13) = 573166440 position
  subsets of size 13. All 573166440 subsets were accounted for.
- A vector of symplectic weight 14 exists in span(S)^perp and not in span(S).

So d = 14 exactly. The parameters are [[33,9,14;12]]_3, matching the JSON's n = 33, k = 9, c = 12, d = 14. The
author's REPRODUCE.md steps 1-5 printed every value REPRODUCE.md says they would, with no mismatch, and reruns gave
identical output.

Scope: I did not run step 6, the live table check, which the other skeptics cover. The saved table copy
(table/qutrit.php) has the cell `[[33,9,13-21;12]]`, and 13 < 14 <= 21 holds against that copy.

## Definition (quoted from claim/CLAIM.md, success criterion)

> with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic
> commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in
> the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition
> used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper.
> Results for c = 0 are excluded

Conventions (from the object's S_convention): rows are (x|z) over GF(3), and <(x|z),(x'|z')> = x.z' - z.x'. The
weight is symplectic weight, #{i : (x_i, z_i) != (0,0)}.

## What I computed and how (files in mine/)

The object file has sha256 059282c383e7d059867ecd1a1ec51d54197af25b2c6a320dd26b150ac1a99391. That is the claimed
hash, measured with shasum -a 256.

1. **gf3.py and prep_object.py**: exact GF(3) linear algebra in the Python standard library, reading only n and S.
   - S is 36 x 66 with entries in {0,1,2}, and s = rank(S) = 36, so the 36 generators are independent.
   - The Gram matrix G = S J S^T is antisymmetric with rank 24, so c = 12, and k = 33 - 36 + 12 = 9.
   - D = span(S)^perp is the null space of the functionals (-s_z | s_x) and has dimension 30 = 2n - s.
   - I = span(S) ∩ D = {yS : yG = 0} has dimension 12 = s - 2c.
   - L completes I to a basis of D, with dimension 18. The code asserts that every basis vector is orthogonal to S.
2. **subsets.c**: my exhaustive position-subset test. For a size w it visits every w-subset T of the 33 positions,
   depth first, with incremental elimination over GF(3) using bit-sliced trits.
   - Each D basis row carries its L-coefficients b. A vector of D lies in I exactly when b = 0.
   - D_T (the vectors of D that vanish outside T) is contained in I exactly when every surviving row has b = 0.
   - Some T fails that test exactly when D \ I has a vector of weight <= w.
   - Pruning is sound: once every surviving row has b = 0, every subspace below that node stays inside I. Such a
     subtree is credited with the binomial count of its subsets, not skipped.
   - The program checks that the credited total equals C(n,w).
3. **verify_witness.py**: checks a witness vector straight from S. It tests <s,v> = 0 for all 36 rows, tests v not in
   span(S) by comparing rank(S + v) with rank(S), and computes the weight.
4. **gf9check.py**: my own GF(9) arithmetic (w^2 = w + 1, conj = x^3), used to check the JSON's other matrices
   against S.

Results on the object:

| quantity | mine | JSON / claim |
|---|---|---|
| s = rank(S) | 36 | 36 rows |
| rank(S J S^T), c | 24, 12 | c = 12 |
| k = n - s + c | 9 | 9 |
| dim span(S)^perp, dim isotropic part | 30, 12 | - |
| w = 13: subsets covered / C(33,13) / violations | 573166440 / 573166440 / 0 | d >= 14 |
| w = 14: subsets covered / C(33,14) / violating 14-subsets | 818809200 / 818809200 / 10404 | - |
| witness (mine): support 10,12,14,15,16,17,18,20,21,22,23,24,26,27 | in span(S)^perp: True; in span(S): False; weight 14 | d <= 14 |
| d | **14** | 14 |

- Run time: 3.55 s for w = 13 and 6.96 s for w = 14. Peak resident memory was about 1.6 MB (/usr/bin/time -l).
- gf9check.py found:
  - rank G9 = 15 and rank D9 = 18, and G9 · conj(D9)^T = 0, so D9 is the Hermitian dual of span(G9).
  - S equals the rows phi(r), phi(w r) for each row r of D9, in that order.
  - phi(span_GF9(G9)) has GF(3) rank 30, is orthogonal to S, and equals span(S)^perp.
  - The Hermitian hull of span(G9) has dimension 6, which gives the 12-dimensional isotropic part.
  - So the JSON's GF(9) description is consistent with S.

## Tests of my checker

- **Brute force, tier A** (test_small.py; 60 cases, n = 3..5): computed straight from the definition over all of
  GF(3)^(2n). D is the set of vectors orthogonal to every row of S, I = D ∩ span(S) with span(S) enumerated as a
  set, and d is the minimum weight of D \ I.
  - The counts |D| = 3^(2n-s), |span S| = 3^s and |I| = 3^(s-2c) also confirm s and c.
- **Brute force, tier B** (60 cases, n = 6..9): enumerates all 3^dim(D) vectors of D.
  - Combined result for tiers A and B: 120 cases, 0 mismatches.
  - d values across the 120 cases: 1 (42), 2 (31), 3 (10), 4 (13), 5 (5), 6 (1), and undefined (18, where D ⊆ I).
- **Mid-size brute force** (test_mid.py; 40 cases, n = 10..16, dim D <= 13): numpy enumeration of all of D. Membership
  in span(S) is tested independently, through the ordinary-dot-product dual of S.
  - S was built with planted low-weight isotropic rows. In 28 of the cases, I has a vector lighter than d, so
    excluding I changes the answer.
  - d ranged over 2..10, with 0 mismatches.
- **Seeded negatives at full size** (negatives.py): S' = basis of {s in span(S) : <s,v> = 0}, so span(S')^perp
  contains a planted v that is not in span(S') (checked).
  - Planted weight 13: the checker reported a violation at w = 13, and the witness was verified (weight 13).
  - Planted weight 9: the checker reported a violation at w = 9, and the witness was verified (weight 9).
- **Invariance**: after a random permutation of the 33 positions, s, c, k = 36, 12, 9. The w = 13 run was clean with
  573166440 of 573166440 covered, and the w = 14 run again found 10404 violating subsets (the traversal differs, with
  128186342 nodes against 126250105).
- **Determinism**: two runs each at w = 13 and w = 14 gave byte-identical output, and the basis file was
  byte-identical when regenerated.

## Author's REPRODUCE.md steps 1-5

These ran in a copy of claim/ (run/claim/) so that claim/ stayed untouched. Its file hashes before and after hash to
the same digest, 44fe776c98f4511fe8234dbf0ad968c31251935cd88093e08de66f7e42e4df85.

| step | REPRODUCE.md expects | printed | match |
|---|---|---|---|
| 1 rebuild | `X code [33,15] hull=6 -> [[33,9,?;12]]  S 36x66  D9 18x33`, hash 059282c3...99391 | same line; rebuilt.json sha256 059282c383e7d059867ecd1a1ec51d54197af25b2c6a320dd26b150ac1a99391 (twice) | yes |
| 2 prep | `n=33 s=36 c=12 k=9 dim_N=30 dim_I=12 N_closed_under_w=True`, `kappa=15` | same, plus `(2*kappa == dim_N: True)` | yes |
| 2 m=20 | deficient=0 in every part; subsets 368070285, 148206066, 56890089 (sum 573166440) | 368070285 / 148206066 / 56890089, deficient 0 / 0 / 0; sum 573166440 | yes |
| 2 m=19 | deficient 5931, 3016, 1457 (sum 10404) | 5931 / 3016 / 1457 (subsets 507629004 / 219864219 / 91315977, sum 818809200) | yes |
| 3 GF(9) witness | `weight=14 in_N=True orthogonal_to_all_rows_of_S=True in_isotropic_part=False` | same (codeword unique up to scalar: GF(9)-dimension 1) | yes |
| 3 GF(3) witness | `symplectic_weight=14 orthogonal_to_all_rows_of_S=True in_span_S=False` | same, support 0,1,3,4,5,6,9,12,13,14,16,30,31,32 | yes |
| 4 prep | `n=33 s=36 c=12 k=9 dim_isotropic=12 dim_dual=30` | same | yes |
| 4 W=13 | each part examined=191055480, with_vector_outside_isotropic=0 | 191055480 / 191055480 / 191055480, 0 / 0 / 0 | yes |
| 4 W=14 | with_vector_outside_isotropic 3469, 3448, 3487 (sum 10404) | 3469 / 3448 / 3487, examined 272936400 each; sum 10404 | yes |
| 5 BZ | `K=15 n=33 d=14 sets=15,15,3 maxw=6 words=531098949` and a weight-14 witness | same line, with a witness | yes |

- **My checker agrees with the author's numbers.**
  - All three author witnesses (step 3 GF(3), step 3 GF(9) mapped by phi, step 5 mapped by phi) pass my
    verify_witness.py: each is in span(S)^perp, is not in span(S), and has symplectic weight 14.
  - My count of 10404 violating 14-subsets equals the author's method B total and method A's 10404 deficient
    19-subsets (their complements).
- **Reruns were byte-identical**: step 1 (hash), step 2 (all six infoset parts), step 4 prep (basis.txt) and step 5
  (bz64). I did not rerun step 4's six parts; my own w = 13 and w = 14 runs cover the same ground.
- **Times on this loaded machine**:
  - Step 4 W=13 parts took 250.66, 250.79 and 241.77 s real; W=14 parts took 359.79, 360.27 and 358.80 s.
  - Step 2 parts took 1-11 s, and step 5 took 1.76 s.
  - Peak resident memory per process was under 1.5 MB.
  - At most 2 heavy processes ran at a time, all under nice and an alarm cap.
- **Proof steps re-derived.**
  - **d >= 14.** Three routes give it:
    - My own exhaustive 13-subset test, which works directly on D \ I.
    - The author's method B, the same idea in a different implementation.
    - The author's method A and BZ. These rest on D = phi(C), which my gf9check.py confirms independently. They
      bound the weight of every nonzero word of D, which is stronger than needed, because D \ I is a subset of
      D \ {0}.
  - **d <= 14.** Several witnesses verified from S give it.
  - **c and k.** The rank computations above give them.
- **Harness slip (mine, not the author's).** My first loop over the remaining step 2 parts called infoset without
  its part argument, because of zsh word splitting. It printed only the usage line and produced no result. I deleted
  those empty files and reran with explicit arguments; the values above come from the reruns.
- **Note.** CLAIM.md flags an erratum in the JSON's "construction" text (rows 11..13 should read 12..14). It does not
  affect G9, D9 or S, which are what I checked.

pass: true
