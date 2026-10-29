# Run it yourself

From this package folder, in a fresh shell (needs python3, standard library only, and cc; no network):

    sh verify-it-yourself/run_checks.sh

Expected output (about 6 seconds on one core; 6.30 s measured, see verify-it-yourself/RECEIPTS.md):

    n=25 s=28 c=8 k=5 dim_isotropic=12 dim_dual=22
    {"n": 25, "s": 28, "c": 8, "k": 5, "dim_perp": 22, "dim_isotropic": 12, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
    W=11 part=0/3 total_subsets=4457400 examined=1485800 with_vector_outside_isotropic=0
    W=11 part=1/3 total_subsets=4457400 examined=1485800 with_vector_outside_isotropic=0
    W=11 part=2/3 total_subsets=4457400 examined=1485800 with_vector_outside_isotropic=0
    T=[1, 8, 11, 14, 15, 16, 17, 18, 19, 21, 23, 24]
    v_x=0 2 0 0 0 0 0 0 2 0 0 1 0 0 0 2 0 0 2 2 0 2 0 2 1
    v_z=0 1 0 0 0 0 0 0 2 0 0 1 0 0 2 1 1 2 0 1 0 2 0 1 0
    symplectic_weight=12 orthogonal_to_all_rows_of_S=True in_span_S=False support=[1, 8, 11, 14, 15, 16, 17, 18, 19, 21, 23, 24]
    1. n=25 rank S=28 rank(S J S^T)=16 c=8 k=5
    2. E_13: 11 monomials (pole orders [0, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13]), top monomial (3, 1); deleted coordinates [0, 1, 2] (affine points [(0, 0), (0, 4), (0, 8)]); columns [6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24] of the result times w
    3. phi(E') orthogonal to every row of S: True; dim_GF(3) phi(E') = 22; 2n - rank S = 22; span(S)^perp = phi(E'): True
       GF(9) dimension of E' = 11 (E_13 has 11 monomials)
    4. bound (proved in the docstring): d(E') >= 28 - 13 - 3 = 12, so d_EA >= 12
    5. witness weight 12, in E': True, phi(witness) in span(S): False -> d_EA <= 12
    RESULT: d_EA = 12 exactly (no distance search): True
    ok:   parameters computed from S
    ok:   computed n=25 s=28 c=8 k=5; claimed n=25 k=5 c=8
    ok:   GF(9) description consistent with S
    ok:   all parts of the W=11 subset test present
    ok:   examined 4457400 of C(25,11) = 4457400 subsets
    ok:   no vector of span(S)^perp outside the isotropic part on <= 11 positions (found 0)
    ok:   witness of symplectic weight 12 outside span(S), claimed d=12
    computed d=12; claimed d=12
    PASS

What it does:
- gf3prep.py (standard library) computes s = rank(S), c = rank(S J S^T)/2, k = n - s + c, a basis of
  N = span(S)^perp and of the isotropic part I = span(S) ∩ N, from S alone.
- check_eaqecc.py prepare checks the object's GF(9) description (D9 is Hermitian-orthogonal to G9 and
  rowspace(S) = phi(D9)). Only its `prepare` mode is used here.
- subset_ea64.c examines every one of the C(25,11) = 4457400 sets T of 11 positions and compares, by exact GF(3)
  ranks, the dimension of the vectors of N supported inside T with that of the vectors of I supported inside T.
  They are equal for every T, so no vector of N outside I has symplectic weight <= 11: d >= 12.
- witness.py finds, inside the given 12 positions, a vector of N that is not in span(S) (so not in I), of
  symplectic weight 12: d <= 12.
- punct_check.py is a second proof of d >= 12 that searches no codewords at all: from its own point list and
  monomials it builds E' (the extended one-point code E_13, 11 monomials with the unique top monomial x^3 y, with the
  three affine points of the line x = 0 deleted and the given columns multiplied by w), checks that phi(E') is
  orthogonal to S with dimension 2n - rank S (so span(S)^perp = phi(E')), and applies the bound proved in its
  docstring: a nonzero f in L(13 P_inf) has at most 13 affine zeros, and at most 12 when its x^3 y coefficient (the
  28th coordinate) is 0, so d(E_13) >= 15; each deleted coordinate lowers a weight by at most one and scaling a
  column by a nonzero element changes no weight, so d(E') >= 15 - 3 = 12. It then checks the weight-12 witness.
- verdict.py compares every computed value with the claim in the JSON. It does not compute d itself: its last line,
  "computed d=...", repeats the claimed d once the subset test and the witness have passed.

Why the subset test is complete: a vector of N outside I with weight <= 11 is supported inside some 11-set T; for
that T the vectors of N supported in T then include one outside I, so dim N_T > dim I_T. Conversely, any T with
dim N_T > dim I_T holds such a vector. With 12 in place of 11 the test finds 401 + 402 + 389 = 1192 sets of 12
positions that hold such a vector (the other 12 of the 1204 weight-12 supports carry only vectors of I).

A third, independent exact check (a GF(9) information-set test, about half a second; it shares no code with the
first). N is closed under multiplication by w, so N = phi(C) for a GF(9)-linear [25,11] code C, and symplectic
weight on N is Hamming weight on C. If every 14 of C's 25 coordinates hold an information set, no nonzero word of C
vanishes on 14 coordinates, so every nonzero word has weight >= 12:

    python3 verify-it-yourself/gf9info.py prep object/eaqecc_25_5_12_8.json G9.txt
    cc -O3 -o infoset verify-it-yourself/infoset.c
    for p in 0 1 2; do ./infoset 14 $p 3 < G9.txt; done
    python3 verify-it-yourself/gf9info.py witness object/eaqecc_25_5_12_8.json 0,2,3,4,5,6,7,9,10,12,13,20,22

Expected: `n=25 s=28 c=8 k=5 dim_N=22 dim_I=12 N_closed_under_w=True` and `kappa=11 (2*kappa == dim_N: True)`;
three lines `kappa=11 n=25 m=14 part=P/3 subsets=... deficient=0` whose subsets values (2708307, 1223980, 525113
for parts 0, 1, 2) sum to 4457400 = C(25,14); with 13 in place of 14 the parts print deficient = 728, 323, 153
(1204 in all, the number of weight-12 supports); and the witness lines
`codewords of C vanishing on the 13 given positions: GF(9)-dimension 1`,
`codeword (a+3b): 0 1 0 0 0 0 0 0 5 0 0 7 0 0 8 1 4 8 6 1 0 5 0 1 3` and
`weight=12 in_N=True orthogonal_to_all_rows_of_S=True in_isotropic_part=False`.

A fourth check (Brouwer-Zimmermann minimum distance of C, under a second):

    cc -O3 -o bz64 verify-it-yourself/bz64.c
    ./bz64 < G9.txt

Expected: `K=11 n=25 d=12 sets=11,11,3 maxw=5 words=6216969 witness=0 1 0 0 0 0 0 0 5 0 0 7 0 0 8 1 4 8 6 1 0 5 0 1 3`.

Rebuild the object from scratch (well under a second):

    python3 how-we-built-it/build_punct_obj.py 13 rebuilt.json 12 0,1,2 6,7,8,12,13,14,15,16,17,18,19,20,24
    shasum -a 256 rebuilt.json object/eaqecc_25_5_12_8.json   # both e33e8fb04dc70d4d703e033310b6efafb1825109a93d649ecef183451ee09ec3

It prints `E_13 deleted=[0, 1, 2] scaled_cols=[6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24] [25,11] hull=6 -> [[25,5,?;8]]  S 28x50  D9 14x25`.
