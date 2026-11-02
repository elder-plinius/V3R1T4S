# Run it yourself

From this package folder, in a fresh shell (needs python3, standard library only, and cc; no network):

    sh verify-it-yourself/run_checks.sh

Expected output (about 2 seconds on one core; 1.5 s measured, see verify-it-yourself/RECEIPTS.md):

    n=23 s=28 c=9 k=4 dim_isotropic=10 dim_dual=18
    {"n": 23, "s": 28, "c": 9, "k": 4, "dim_perp": 18, "dim_isotropic": 10, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
    W=11 part=0/3 total_subsets=1352078 examined=450693 with_vector_outside_isotropic=0
    W=11 part=1/3 total_subsets=1352078 examined=450693 with_vector_outside_isotropic=0
    W=11 part=2/3 total_subsets=1352078 examined=450692 with_vector_outside_isotropic=0
    T=[9, 10, 11, 12, 13, 14, 15, 17, 19, 20, 21, 22]
    v_x=0 0 0 0 0 0 0 0 0 0 0 2 1 0 0 1 0 2 0 1 2 1 0
    v_z=0 0 0 0 0 0 0 0 0 1 1 2 1 2 2 0 0 0 0 0 2 1 2
    symplectic_weight=12 orthogonal_to_all_rows_of_S=True in_span_S=False support=[9, 10, 11, 12, 13, 14, 15, 17, 19, 20, 21, 22]
    1. n=23 rank S=28 rank(S J S^T)=18 c=9 k=4
    2. E_11: 9 monomials (pole orders [0, 3, 4, 6, 7, 8, 9, 10, 11]), top monomial (1, 2); deleted coordinates [0, 3, 11, 12, 16] (affine points [(0, 0), (1, 2), (3, 6), (4, 2), (5, 5)]); columns [1, 3, 6, 8, 10, 11, 14, 15, 16, 17, 19, 21] of the result times w
    3. phi(E') orthogonal to every row of S: True; dim_GF(3) phi(E') = 18; 2n - rank S = 18; span(S)^perp = phi(E'): True
       GF(9) dimension of E' = 9 (E_11 has 9 monomials)
    4. bound (proved in the docstring): d(E') >= 28 - 11 - 5 = 12, so d_EA >= 12
    5. witness weight 12, in E': True, phi(witness) in span(S): False -> d_EA <= 12
    RESULT: d_EA = 12 exactly (no distance search): True
    ok:   parameters computed from S
    ok:   computed n=23 s=28 c=9 k=4; claimed n=23 k=4 c=9
    ok:   GF(9) description consistent with S
    ok:   all parts of the W=11 subset test present
    ok:   examined 1352078 of C(23,11) = 1352078 subsets
    ok:   no vector of span(S)^perp outside the isotropic part on <= 11 positions (found 0)
    ok:   witness of symplectic weight 12 outside span(S), claimed d=12
    computed d=12; claimed d=12
    PASS

What it does:
- gf3prep.py (standard library) computes s = rank(S), c = rank(S J S^T)/2, k = n - s + c, a basis of
  N = span(S)^perp and of the isotropic part I = span(S) ∩ N, from S alone.
- check_eaqecc.py prepare checks the object's GF(9) description (D9 is Hermitian-orthogonal to G9 and
  rowspace(S) = phi(D9)). Only its `prepare` mode is used here.
- subset_ea64.c examines every one of the C(23,11) = 1352078 sets T of 11 positions and compares, by exact GF(3)
  ranks, the dimension of the vectors of N supported inside T with that of the vectors of I supported inside T.
  They are equal for every T, so no vector of N outside I has symplectic weight <= 11: d >= 12.
- witness.py finds, inside the given 12 positions, a vector of N that is not in span(S) (so not in I), of
  symplectic weight 12: d <= 12.
- punct_check.py is a second proof of d >= 12 that searches no codewords at all: from its own point list and
  monomials it builds E' (the extended one-point code E_11, 9 monomials with the unique top monomial x y^2, with the
  five affine points (0,0), (1,2), (3,6), (4,2), (5,5) deleted and the given columns multiplied by w), checks that
  phi(E') is orthogonal to S with dimension 2n - rank S (so span(S)^perp = phi(E')), and applies the bound proved in
  its docstring: a nonzero f in L(11 P_inf) has at most 11 affine zeros, and at most 10 when its x y^2 coefficient
  (the 28th coordinate) is 0, so d(E_11) >= 17; each deleted coordinate lowers a weight by at most one and scaling a
  column by a nonzero element changes no weight, so d(E') >= 17 - 5 = 12. It then checks the weight-12 witness.
- verdict.py compares every computed value with the claim in the JSON. It does not compute d itself: its last line,
  "computed d=...", repeats the claimed d once the subset test and the witness have passed.

Why the subset test is complete: a vector of N outside I with weight <= 11 is supported inside some 11-set T; for
that T the vectors of N supported in T then include one outside I, so dim N_T > dim I_T. Conversely, any T with
dim N_T > dim I_T holds such a vector. With 12 in place of 11 the test finds 114 + 110 + 102 = 326 sets of 12
positions that hold such a vector (run `./subset_ea64 12 P 3 < basis.txt` for P = 0, 1, 2 after
`python3 verify-it-yourself/gf3prep.py object/eaqecc_23_4_12_9.json basis.txt` and
`cc -O3 -o subset_ea64 verify-it-yourself/subset_ea64.c`).

The extra checks below write files (G9.txt, infoset, bz64, sb_basis.txt, sbenum_bz9, rebuilt.json) into the current
folder, so run them from a scratch copy of the package, for example `T=$(mktemp -d); cp -R . "$T"; cd "$T"`.

A third, independent exact check (a GF(9) information-set test, about half a second; it shares no code with the
first). N is closed under multiplication by w, so N = phi(C) for a GF(9)-linear [23,9] code C, and symplectic
weight on N is Hamming weight on C. If every 12 of C's 23 coordinates hold an information set, no nonzero word of C
vanishes on 12 coordinates, so every nonzero word has weight >= 12:

    python3 verify-it-yourself/gf9info.py prep object/eaqecc_23_4_12_9.json G9.txt
    cc -O3 -o infoset verify-it-yourself/infoset.c
    for p in 0 1 2; do ./infoset 12 $p 3 < G9.txt; done
    python3 verify-it-yourself/gf9info.py witness object/eaqecc_23_4_12_9.json 0,1,2,3,4,5,6,7,8,16,18

Expected: `n=23 s=28 c=9 k=4 dim_N=18 dim_I=10 N_closed_under_w=True` and `kappa=9 (2*kappa == dim_N: True)`;
three lines `kappa=9 n=23 m=12 part=P/3 subsets=... deficient=0` whose subsets values (785460, 385917, 180701
for parts 0, 1, 2) sum to 1352078 = C(23,12); with 11 in place of 12 the parts print deficient = 185, 98, 44
(327 in all, the number of 11-sets that are zero sets of weight-12 words); and the witness lines
`codewords of C vanishing on the 11 given positions: GF(9)-dimension 1`,
`codeword (a+3b): 0 0 0 0 0 0 0 0 0 1 1 6 3 2 2 5 0 7 0 5 6 3 2` and
`weight=12 in_N=True orthogonal_to_all_rows_of_S=True in_isotropic_part=False`.

A fourth check (Brouwer-Zimmermann minimum distance of C, under a second):

    cc -O3 -o bz64 verify-it-yourself/bz64.c
    ./bz64 < G9.txt

Expected: `K=9 n=23 d=12 sets=9,9,5 maxw=5 words=1758843 witness=0 0 0 0 0 0 0 0 0 1 1 6 3 2 2 5 0 7 0 5 6 3 2`.

A fifth check, a full enumeration of span(S)^perp over GF(3) with no GF(9) structure used (about 1 second):

    python3 verify-it-yourself/sb_prep.py object/eaqecc_23_4_12_9.json sb_basis.txt
    cc -O2 -o sbenum_bz9 verify-it-yourself/sb_enum.c
    ./sbenum_bz9 12 < sb_basis.txt

Expected: `n=23 s=28 rank(SJS^T)=18 c=9 k=4 dimN=18 dimI=10 (claimed n=23 k=4 c=9 d=12)`,
`nonzero vectors enumerated=387420488` (all 3^18 - 1), the weight histogram starting `12:2616 13:33288`,
`weight 12: in isotropic part 8, outside 2608` and `d_EA = 12`.

Rebuild the object from scratch (well under a second):

    python3 how-we-built-it/build_punct_obj.py 11 rebuilt.json 12 0,3,11,12,16 1,3,6,8,10,11,14,15,16,17,19,21
    shasum -a 256 rebuilt.json object/eaqecc_23_4_12_9.json   # both c64bdf57a5280892b8d4e085ea565c865d5584de5198baa9763cb516318f06f4

It prints `E_11 deleted=[0, 3, 11, 12, 16] scaled_cols=[1, 3, 6, 8, 10, 11, 14, 15, 16, 17, 19, 21] [23,9] hull=5 -> [[23,4,?;9]]  S 28x46  D9 14x23`.
