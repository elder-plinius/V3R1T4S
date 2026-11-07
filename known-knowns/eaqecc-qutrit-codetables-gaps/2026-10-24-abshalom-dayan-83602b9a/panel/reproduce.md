# REPRODUCE skeptic verdict: [[28,5,15;11]]_3 EAQECC

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## Bottom line

From S alone (claim/object/eaqecc_28_5_15_11.json, field "S", 34 x 56 over GF(3)) my own exact checker computes
n = 28, s = 34, c = 11, k = 5 and, by a complete enumeration of all 3^22 = 31,381,059,609 vectors of span(S)^perp,
d = 15 (71,280 vectors of weight 15 outside the isotropic part, none lighter). This matches the claimed [[28,5,15;11]]_3.
The saved table cell (n,k,c) = (28,5,11) reads 13-22, so d = 15 is strictly above d_lower = 13 and at most
d_upper = 22. The author's rebuild reproduces the object byte for byte, and both author checkers agree with my result
(details below). Nothing is sampled.

## Definition used (quoted from claim/CLAIM.md, success criterion)

> with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation
> matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the
> symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by
> Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper.

Conventions I applied: rows of S are (x|z), J = [[0,I],[-I,0]], so <(x|z),(x'|z')> = x.z' - z.x' (mod 3); weight is
the symplectic weight #{i : (x_i, z_i) != (0,0)}; s = rank(S) over GF(3). Only S was used; the JSON's n, k, c, d
fields were read only for the final comparison.

## My checker (written and tested before opening claim/checkers/ or claim/rebuild/)

Files (all in panel/work-reproduce/):

- mycheck.py: exact GF(3) linear algebra with Python integers. Computes s = rank(S), the 34 x 34 Gram matrix
  M = S J S^T (asserts antisymmetry), c = rank(M)/2, k = n - s + c; a basis of span(S)^perp as the null space of the
  rows (-z | x) (asserts every basis vector has symplectic product 0 with every row of S and that the dimension is
  2n - s); a basis of the isotropic part H = {lambda S : lambda M = 0} (asserts each vector lies in span(S) by a rank
  test, lies in span(S)^perp, and dim H = s - rank(M)); then completes H's basis to a basis of span(S)^perp, H first.
  `combine` sums the part outputs, checks the part ranges tile [0, 3^22) exactly and the visited counts add to
  3^22, that the H histogram sums to 3^dim H, and re-verifies the minimum-weight witness in exact arithmetic
  (recomputes it from its coefficients, checks all 34 symplectic products are 0, checks rank([S; w]) = s + 1, i.e.
  w is not in span(S) and so not in the isotropic part, and recounts its weight).
- enum.c: bit-sliced GF(3) enumerator (element e stored as bits p = [e==1], q = [e==2]; x_i in bit i, z_i in bit 32+i).
  Walks the span of the 22 basis vectors with a modular ternary Gray code (each step adds exactly one basis vector),
  over a contiguous slice [start, end) of the counter range, so slices are independent and can run in parallel. A
  vector is in H exactly when its coefficients on the non-H basis vectors are all 0 (the basis is a direct sum
  H + complement). It histograms the weights of all vectors, of the H vectors, and of the vectors outside H, and keeps
  the first lightest vector outside H as a witness.

### Tests of my checker

1. Definition-level brute force (bf_test.py, bf_test2.py; outputs bf_test.out, bf_test2.out). The brute force does
   not use my linear algebra: it enumerates all of GF(3)^(2n) for n = 3..6, keeps the vectors with zero symplectic
   product against every row (span(S)^perp by definition), builds span(S) as the set of all GF(3) combinations of the
   rows, gets ranks by counting (|row space| = 3^rank), and histograms the weights over perp, perp ∩ span(S) and
   perp \ span(S). For each case my pipeline (with the enumeration split into 1 to 5 parts) must give identical s, c, k
   and identical full histograms, and a witness that passes the exact re-check. Result: 39 cases (17 + 22), all OK,
   including dependent rows, c = 0 and c >= 1 cases, an empty d, and 6 cases where the isotropic part contains a
   nonzero vector lighter than d (e.g. hand_iso_wt1: d_EA = 2 with a weight-1 isotropic vector; iso1: d_EA = 3 with a
   weight-2 isotropic vector), so the exclusion is exercised.

       cases=17 exclusion_exercised_in=1 ALL_OK=True
       cases=22 exclusion_exercised_in=5 ALL_OK=True

2. Altered copies of the object at full size (each a complete 3^22 enumeration):

   | copy | change | s, c, k from S | d | verdict line |
   |---|---|---|---|---|
   | corrupt_S0_0.json | S[0][0] 1 -> 2 | 34, 12, 6 | 14 | MISMATCH |
   | nonlocal_0.json | row 25 += a weight-27 vector of span(S)^perp | 34, 11, 5 | 14 (3,288 vectors) | MISMATCH |
   | nonlocal_1.json | row 14 += a weight-26 vector of span(S)^perp | 34, 11, 5 | 14 (3,138 vectors) | MISMATCH |
   | random_S.json | random 34 x 56 matrix | 34, 17, 11 | 11 | MISMATCH |
   | object_rowmixed.json | S -> R S with random invertible R, then a random qudit permutation (an equivalent code) | 34, 11, 5 | 15 | MATCH, histograms identical to the object's |

   The two nonlocal copies keep n, s, c, k unchanged, so only the enumeration can catch them; it does (d = 14, with
   exactly verified weight-14 witnesses). Outputs: my_result_corrupt_S0_0.txt, my_result_nonlocal_0.txt,
   my_result_nonlocal_1.txt, my_result_random_S.txt, my_result_rowmixed.txt.

   Something I checked because it looked wrong at first: three single-entry corruptions that kept c = 11
   (corrupt_S33_55, corr_16_47_2, corr_5_13_2) gave weight histograms identical to the original. explain_corrupt.out
   shows why: each touches a qudit that only one pair of rows of S touches, with local parts (1,0) and (0,1) (the
   row pair phi(r), phi(w r) of a D9 row whose free column is that qudit), and the changed row is one of that pair.
   Changing one entry there equals applying an invertible 2 x 2 map to that one qudit in every vector; such a map keeps
   the symplectic weight, and span(S)^perp moves by another invertible map on the same qudit, so these copies have the
   same weight distributions and identical histograms are the correct answer. They are not counted as corruption tests. The non-local copies above
   are the real test.

## Results on the object (real output)

Basis preparation (`python3 -I mycheck.py prep object_copy.json obj.basis`; object_copy.json has the same sha256
83602b9ae21bd9ab3d1872f4bb244f452a689cb88254e0cc398a75df2e9fd434 as claim/object/eaqecc_28_5_15_11.json):

    from S: rows=34 n=28 s=rank(S)=34 rank(SJS^T)=22 c=11 k=5 dim(perp)=22 dim(H)=12

Enumeration: `./enum obj.basis i 10` for i = 0..9 (10 processes, under 30 s wall in total), then
`python3 -I mycheck.py combine object_copy.json obj.basis run_obj/part*.out`:

    from S: rows=34 n=28 s=rank(S)=34 rank(SJS^T)=22 c=11 k=5 dim(perp)=22 dim(H)=12
    parts=10 contiguous_cover_of_[0,3^22)=True visited=31381059609 3^22=31381059609 equal=True
    sum hist_all=31381059609 sum hist_H=531441 (3^h=531441) sum hist_EA=31380528168
    hist_all (weight:count): {0: 1, 15: 72288, 16: 719064, 17: 2752704, 18: 13038504, 19: 62009928, 20: 214710912, 21: 650700000, 22: 1671807600, 23: 3477330000, 24: 5795890272, 25: 7423211520, 26: 6849363240, 27: 4059635528, 28: 1159818048}
    hist_H   (weight:count): {0: 1, 15: 1008, 18: 3336, 21: 27648, 22: 69984, 23: 69984, 24: 147168, 25: 139968, 26: 34992, 27: 37352}
    hist_EA  (weight:count): {15: 71280, 16: 719064, 17: 2752704, 18: 13035168, 19: 62009928, 20: 214710912, 21: 650672352, 22: 1671737616, 23: 3477260016, 24: 5795743104, 25: 7423071552, 26: 6849328248, 27: 4059598176, 28: 1159818048}
    d_all(nonzero in perp)=15 d=d_EA=15 count_at_d=71280
    witness vec (x|z) = 00000000000102201000200200211010000220002200201000020120
    witness check: {'recomputed_from_coeffs': True, 'in_perp': True, 'not_in_spanS': True, 'weight': 15}
    computed {'n': 28, 'k': 5, 'c': 11, 'd': 15} claimed {'n': 28, 'k': 5, 'c': 11, 'd': 15} MATCH | enumeration integrity: True

Summary of computed values: n = 28, s = 34, rank(S J S^T) = 22 so c = 11, k = 28 - 34 + 11 = 5, dim span(S)^perp = 22,
dim of the isotropic part = 12, d = 15. The isotropic part's own minimum weight is also 15 (1,008 vectors), so here the
exclusion does not change the answer: the pure distance is 15 as well.

Extra consistency check on the histograms (panel/work-reproduce/macwilliams.py, output macwilliams.out): the MacWilliams
transform for symplectic weight (alphabet size 9 per qudit) of the enumerated distributions gives dual distributions
made of non-negative integers with B_0 = 1 and the right total, for span(S)^perp (dual span(S), minimum weight 9) and
for the isotropic part (dual H^perp). A miscounted histogram would almost surely fail this.

    span(S)^perp -> dual span(S): |C|=31381059609 B_0=1 all_integer=True all_nonnegative=True sum_B=16677181699666569 expected=16677181699666569
    isotropic H -> dual H^perp: |C|=531441 B_0=1 all_integer=True all_nonnegative=True sum_B=984770902183611232881 expected=984770902183611232881

Determinism and basis independence: the equivalent copy object_rowmixed.json (different generator matrix, qudits
permuted, therefore a completely different enumeration basis) split into 7 parts instead of 10 gives the identical
histograms (hist_all, hist_H, hist_EA, d, count) with a different witness, which also passes the exact re-check.

## Author's steps (REPRODUCE.md), run in a copy, panel/work-reproduce/author_copy/

Step 1, rebuild (`python3 rebuild/build_claim.py 13 rebuilt.json 15`, then shasum):

    [28,11] hull=6 -> [[28,5,?;11]]  S 34x56  D9 17x28
    83602b9ae21bd9ab3d1872f4bb244f452a689cb88254e0cc398a75df2e9fd434  rebuilt.json
    83602b9ae21bd9ab3d1872f4bb244f452a689cb88254e0cc398a75df2e9fd434  object/eaqecc_28_5_15_11.json

The rebuilt object is byte-identical to the claimed one.

Step 2, checker B over GF(9) (`cc -O3 -o checkers/checkB_gf9 checkers/checkB_gf9.c`,
`python3 checkers/checkB.py object/eaqecc_28_5_15_11.json`; output in author_copy/B.out):

    kappa=11 n=28 rank=11 gram_rank=5 hull=6 EA: k=5 c=11
    enumerated_nonzero_messages=31381059608 in_hull_nonzero=531440 d_all=15 (count 72288) d_ea=15 (count 71280)
    D9 orthogonal to G9: True; rank phi(D9)=34, rank S=34, rank [S;phi(D9)]=34 -> S == phi(C^perp_H): True
    computed {'k': 5, 'c': 11, 'd': 15, 'n': 28} claimed {'n': 28, 'k': 5, 'c': 11, 'd': 15} MATCH

This is exactly the expected output in REPRODUCE.md (about 20 minutes wall here, on the loaded machine).

Step 3, checker A over GF(3) (10 parts, at most 9 at once next to checker B, then `combine_checkA.py`; outputs in
author_copy/A_part*.out and author_copy/A_combined.out):

Each of the 10 parts printed `claimed {'n': 28, 'k': 5, 'c': 11, 'd': 15} MATCH` with s=34, c=11, k=5,
dim_perp=22, dim_isotropic=12, d=15, d_pure=15 (for example part 9:
`{"n": 28, "s": 34, "c": 11, "k": 5, "part": 9, "nparts": 10, "dim_perp": 22, "dim_isotropic": 12, "enumerated": 3138100056, "noniso_vectors": 3138041007, "d": 15, "d_pure": 15}`).
Combined:

    {"n": 28, "k": 5, "c": 11, "s": 34, "d": 15, "d_pure": 15, "enumerated": 31381059609, "parts": 10}
    claimed {'n': 28, 'k': 5, 'c': 11, 'd': 15} MATCH

I also summed the parts' counts myself: enumerated 31381059609 = 3^22 and noniso_vectors 31380528168 = 3^22 - 3^12,
all parts 0..9 present. This is the expected output in REPRODUCE.md (about 11 minutes for parts 0 to 8 and 9 more
minutes for part 9, which waited for a free slot).

Comparison: full agreement. All three computations give n = 28, k = 5, c = 11, d = 15. Checker B's count of weight-15
codewords (72,288 in all, 71,280 outside the hull) and its hull size (531,440 nonzero = 3^12 - 1) equal my GF(3)
histogram exactly (hist_all[15] = 72,288, hist_EA[15] = 71,280, dim H = 12). Checker A's totals (3^22 enumerated,
3^22 - 3^12 outside the isotropic part, d = d_pure = 15) equal mine. The rebuild is byte-identical.

Reading the author's code (after my result was in): checker A uses the same overall plan as mine (null-space basis of
span(S)^perp, isotropic basis first, full enumeration) but different code (numpy table of 3^10 combinations plus an
outer loop over 3^12, split by outer index mod 10) and reports only minima. Checker B works over GF(9) from G9 (an
[28,11] code C, Hermitian Gram rank 5, hull dimension 6), enumerates all 9^11 codewords, and separately checks that
D9 is Hermitian-orthogonal to G9 and that rowspace(S) = phi(D9), which ties S to C^perp_H. Its counts are in
codewords of C, which correspond one to one with vectors of span(S)^perp, so they can be compared with my GF(3)
histogram directly.

## Table cell (claim/table/qutrit.php)

Parsed with panel/work-reproduce/table_check.py (every innermost `<TD>`, displayed text only, attributes such as title
ignored; output table_check.out):

    sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c bytes 628039
    parsed table cells: 3888 distinct (n,k,c): 3888
    keys with more than one cell: 0
    cell (28,5,11): [(13, 22, 'NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[27,5,13;11]] subcode of [[27,8,13;11]] from arXiv:2207.05647"')]
    row n=28,k=5 (c: dl-du): c=0: 9-11, c=3: 10-14, c=5: 12-19, c=11: 13-22, c=12: 14-22, c=13: 16-22, c=15: 17-22, c=17: 18-23, c=19: 19-23, c=21: 20-23, c=23: 21-24
    d=15 d_lower=13 d_upper=22 strictly_above_lower=True at_most_upper=True

The file's sha256 matches the one recorded in claim/table/RECORD.md, the cell text matches RECORD.md verbatim
(`[[28,5,13-22;11]]`), and the row matches RECORD.md's list. A first version of my parser missed the first cell of each
nested column table (the c = 0 cells); fixed before the output above, and it never affected the (28,5,11) cell.

## Worries and limits

- The table is the author's saved copy from 2026-10-24T10:36:29Z. I had no network by instruction, so I did not
  re-fetch the live page; whether d_lower is still 13 now rests on that saved copy and RECORD.md.
- c is computed in the non-catalytic sense of the table header; c = 11 >= 1, so the c = 0 exclusion does not apply.
- The machine was heavily loaded by other jobs (load average up to about 240 on 14 cores). That only slowed the runs;
  every enumeration ran to completion with visited counts summing exactly to 3^22.
- I checked that the code is new relative to the saved table only, not against the literature; that is outside the
  success criterion.
- No mismatch, missing object or non-determinism found.

PIDs I started are listed in panel/work-reproduce/pids.txt; all had exited before this file was finalized
(checked by exact PID).

pass: true
