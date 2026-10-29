# Run it yourself

From this package folder, in a fresh shell (needs python3, standard library only, and cc; no network):

    sh verify-it-yourself/run_checks.sh

Expected output (about 2 seconds on one core; 2.2 s measured, see verify-it-yourself/RECEIPTS.md):

    n=24 s=30 c=10 k=4 dim_isotropic=10 dim_dual=18
    {"n": 24, "s": 30, "c": 10, "k": 4, "dim_perp": 18, "dim_isotropic": 10, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
    W=12 part=0/3 total_subsets=2704156 examined=901386 with_vector_outside_isotropic=0
    W=12 part=1/3 total_subsets=2704156 examined=901385 with_vector_outside_isotropic=0
    W=12 part=2/3 total_subsets=2704156 examined=901385 with_vector_outside_isotropic=0
    T=[0, 10, 11, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23]
    v_x=0 0 0 0 0 0 0 0 0 0 2 1 0 2 0 0 0 1 1 1 0 1 1 2
    v_z=2 0 0 0 0 0 0 0 0 0 0 2 0 2 2 0 2 1 2 0 1 2 0 1
    symplectic_weight=13 orthogonal_to_all_rows_of_S=True in_span_S=False support=[0, 10, 11, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23]
    1. n=24 rank S=30 rank(S J S^T)=20 c=10 k=4
    2. E_11: 9 monomials (pole orders [0, 3, 4, 6, 7, 8, 9, 10, 11]), top monomial (1, 2); deleted coordinates [0, 3, 6, 11] (affine points [(0, 0), (1, 2), (2, 2), (3, 6)]); columns [1, 3, 5, 7, 10, 11, 12, 15, 17, 18, 20, 22] of the result times w
    3. phi(E') orthogonal to every row of S: True; dim_GF(3) phi(E') = 18; 2n - rank S = 18; span(S)^perp = phi(E'): True
       GF(9) dimension of E' = 9 (E_11 has 9 monomials)
    4. bound (proved in the docstring): d(E') >= 28 - 11 - 4 = 13, so d_EA >= 13
    5. witness weight 13, in E': True, phi(witness) in span(S): False -> d_EA <= 13
    RESULT: d_EA = 13 exactly (no distance search): True
    ok:   parameters computed from S
    ok:   computed n=24 s=30 c=10 k=4; claimed n=24 k=4 c=10
    ok:   GF(9) description consistent with S
    ok:   all parts of the W=12 subset test present
    ok:   examined 2704156 of C(24,12) = 2704156 subsets
    ok:   no vector of span(S)^perp outside the isotropic part on <= 12 positions (found 0)
    ok:   witness of symplectic weight 13 outside span(S), claimed d=13
    computed d=13; claimed d=13
    PASS

What it does:
- gf3prep.py (standard library) computes s = rank(S), c = rank(S J S^T)/2, k = n - s + c, a basis of
  N = span(S)^perp and of the isotropic part I = span(S) ∩ N, from S alone.
- check_eaqecc.py prepare checks the object's GF(9) description (D9 is Hermitian-orthogonal to G9 and
  rowspace(S) = phi(D9)). Only its `prepare` mode is used here.
- subset_ea64.c examines every one of the C(24,12) = 2704156 sets T of 12 positions and compares, by exact GF(3)
  ranks, the dimension of the vectors of N supported inside T with that of the vectors of I supported inside T.
  They are equal for every T, so no vector of N outside I has symplectic weight <= 12: d >= 13.
- witness.py finds, inside the given 13 positions, a vector of N that is not in span(S) (so not in I), of
  symplectic weight 13: d <= 13.
- punct_check.py is a second proof of d >= 13 that searches no codewords at all: from its own point list and
  monomials it builds E' (the extended one-point code E_11, 9 monomials with the unique top monomial x y^2, with the
  four affine points (0,0), (1,2), (2,2), (3,6) deleted and the given columns multiplied by w), checks that phi(E') is
  orthogonal to S with dimension 2n - rank S (so span(S)^perp = phi(E')), and applies the bound proved in its
  docstring: a nonzero f in L(11 P_inf) has at most 11 affine zeros, and at most 10 when its x y^2 coefficient (the
  28th coordinate) is 0, so d(E_11) >= 17; each deleted coordinate lowers a weight by at most one and scaling a
  column by a nonzero element changes no weight, so d(E') >= 17 - 4 = 13. It then checks the weight-13 witness.
- verdict.py compares every computed value with the claim in the JSON. It does not compute d itself: its last line,
  "computed d=...", repeats the claimed d once the subset test and the witness have passed.

Why the subset test is complete: a vector of N outside I with weight <= 12 is supported inside some 12-set T; for
that T the vectors of N supported in T then include one outside I, so dim N_T > dim I_T. Conversely, any T with
dim N_T > dim I_T holds such a vector. With 13 in place of 12 the test finds 208 + 218 + 199 = 625 sets of 13
positions that hold such a vector.

The extra checks below write files (G9.txt, infoset, bz64, sb_basis.txt, sbenum_bz9, rebuilt.json) into the current
folder, so run them from a scratch copy of the package, for example `T=$(mktemp -d); cp -R . "$T"; cd "$T"`.

A third, independent exact check (a GF(9) information-set test, about half a second; it shares no code with the
first). N is closed under multiplication by w, so N = phi(C) for a GF(9)-linear [24,9] code C, and symplectic
weight on N is Hamming weight on C. If every 12 of C's 24 coordinates hold an information set, no nonzero word of C
vanishes on 12 coordinates, so every nonzero word has weight >= 13:

    python3 verify-it-yourself/gf9info.py prep object/eaqecc_24_4_13_10.json G9.txt
    cc -O3 -o infoset verify-it-yourself/infoset.c
    for p in 0 1 2; do ./infoset 12 $p 3 < G9.txt; done
    python3 verify-it-yourself/gf9info.py witness object/eaqecc_24_4_13_10.json 1,2,3,4,5,6,7,8,9,12,15

Expected: `n=24 s=30 c=10 k=4 dim_N=18 dim_I=10 N_closed_under_w=True` and `kappa=9 (2*kappa == dim_N: True)`;
three lines `kappa=9 n=24 m=12 part=P/3 subsets=... deficient=0` whose subsets values (1532779, 785460, 385917
for parts 0, 1, 2) sum to 2704156 = C(24,12); with 11 in place of 12 the parts print deficient = 346, 184, 95
(625 in all, the number of 11-sets that are zero sets of weight-13 words); and the witness lines
`codewords of C vanishing on the 11 given positions: GF(9)-dimension 1`,
`codeword (a+3b): 1 0 0 0 0 0 0 0 0 0 5 8 0 3 1 0 1 6 8 7 2 8 7 4` and
`weight=13 in_N=True orthogonal_to_all_rows_of_S=True in_isotropic_part=False`.

A fourth check (Brouwer-Zimmermann minimum distance of C, under a second):

    cc -O3 -o bz64 verify-it-yourself/bz64.c
    ./bz64 < G9.txt

Expected: `K=9 n=24 d=13 sets=9,9,6 maxw=5 words=1758843 witness=1 0 0 0 0 0 0 0 0 0 5 8 0 3 1 0 1 6 8 7 2 8 7 4`.

A fifth check, a full enumeration of span(S)^perp over GF(3) with no GF(9) structure used (about 1 second):

    python3 verify-it-yourself/sb_prep.py object/eaqecc_24_4_13_10.json sb_basis.txt
    cc -O2 -o sbenum_bz9 verify-it-yourself/sb_enum.c
    ./sbenum_bz9 13 < sb_basis.txt

Expected: `n=24 s=30 rank(SJS^T)=20 c=10 k=4 dimN=18 dimI=10 (claimed n=24 k=4 c=10 d=13)`,
`nonzero vectors enumerated=387420488` (all 3^18 - 1), the weight histogram starting `13:5000 14:52776`,
`weight 13: in isotropic part 0, outside 5000` and `d_EA = 13`.

Rebuild the object from scratch (well under a second):

    python3 how-we-built-it/build_punct_obj.py 11 rebuilt.json 13 0,3,6,11 1,3,5,7,10,11,12,15,17,18,20,22
    shasum -a 256 rebuilt.json object/eaqecc_24_4_13_10.json   # both feeeff03749ecfd57a5b84b8778a2ffe2111723da17f31a3f197d02d048c1794

It prints `E_11 deleted=[0, 3, 6, 11] scaled_cols=[1, 3, 5, 7, 10, 11, 12, 15, 17, 18, 20, 22] [24,9] hull=5 -> [[24,4,?;10]]  S 30x48  D9 15x24`.
