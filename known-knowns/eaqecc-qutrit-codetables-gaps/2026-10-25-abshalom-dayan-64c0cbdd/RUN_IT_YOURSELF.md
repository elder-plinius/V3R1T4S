# Run it yourself

From this package folder, in a fresh shell (needs python3, standard library only, and cc; no network):

    sh verify-it-yourself/run_checks.sh

Expected output (about 9 seconds with 3 free cores; 8.77 s measured, see verify-it-yourself/RECEIPTS.md):

    n=28 s=30 c=9 k=7 dim_isotropic=12 dim_dual=26
    {"n": 28, "s": 30, "c": 9, "k": 7, "dim_perp": 26, "dim_isotropic": 12, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
    W=12 part=0/3 total_subsets=30421755 examined=10140585 with_vector_outside_isotropic=0
    W=12 part=1/3 total_subsets=30421755 examined=10140585 with_vector_outside_isotropic=0
    W=12 part=2/3 total_subsets=30421755 examined=10140585 with_vector_outside_isotropic=0
    T=[12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    v_x=0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0 0 2 2 2 2 2 2 1
    v_z=0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 1 1 1 1 1 1 2 2 2 0
    symplectic_weight=13 orthogonal_to_all_rows_of_S=True in_span_S=False support=[12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    1. n=28 rank S=30 rank(S J S^T)=18 c=9 k=7
    2. E: 13 monomials (pole orders [0, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]), 27 affine points, top monomial (5, 0)
    3. phi(E) orthogonal to every row of S: True; dim_GF(3) phi(E) = 26; 2n - rank S = 26; span(S)^perp = phi(E): True
       GF(9) dimension of E = 13
    4. Goppa-type bound (proved in the docstring): d(E) >= 28 - 15 = 13, so d_EA >= 13
    5. witness weight 13, in E: True, phi(witness) in span(S): False -> d_EA <= 13
    RESULT: d_EA = 13 exactly (no distance search): True
    ok:   parameters computed from S
    ok:   computed n=28 s=30 c=9 k=7; claimed n=28 k=7 c=9
    ok:   GF(9) description consistent with S
    ok:   all parts of the W=12 subset test present
    ok:   examined 30421755 of C(28,12) = 30421755 subsets
    ok:   no vector of span(S)^perp outside the isotropic part on <= 12 positions (found 0)
    ok:   witness of symplectic weight 13 outside span(S), claimed d=13
    computed d=13; claimed d=13
    PASS

What it does:
- gf3prep.py (standard library) computes s = rank(S), c = rank(S J S^T)/2, k = n - s + c, a basis of
  N = span(S)^perp and of the isotropic part I = span(S) ∩ N, from S alone.
- check_eaqecc.py prepare checks the object's GF(9) description (D9 is Hermitian-orthogonal to G9 and
  rowspace(S) = phi(D9)). Only its `prepare` mode is used here.
- subset_ea64.c examines every one of the C(28,12) = 30421755 sets T of 12 positions and compares, by exact GF(3)
  ranks, the dimension of the vectors of N supported inside T with that of the vectors of I supported inside T.
  They are equal for every T, so no vector of N outside I has symplectic weight <= 12: d >= 13.
- witness.py finds, inside the given 13 positions, a vector of N that is not in span(S) (so not in I), of
  symplectic weight 13: d <= 13.
- onepoint_check.py is a second proof of d >= 13 that searches no codewords at all: from its own point list and
  monomials it builds the extended one-point code E of pole order 15, checks that phi(E) is orthogonal to S with
  dimension 2n - rank S (so span(S)^perp = phi(E)), and applies the bound proved in its docstring: a nonzero f in
  L(15 P_inf) has at most 15 affine zeros if its top coefficient is nonzero (weight >= 27 - 15 + 1) and at most 14 if
  it is zero (weight >= 27 - 14), so d(E) >= 13. It then checks the weight-13 witness.
- verdict.py compares every computed value with the claim in the JSON.

Why the subset test is complete: a vector of N outside I with weight <= 12 is supported inside some 12-set T; for
that T the vectors of N supported in T then include one outside I, so dim N_T > dim I_T. Conversely, any T with
dim N_T > dim I_T holds such a vector.

A third, independent exact check (a GF(9) information-set test, a few seconds; it shares no code with the first).
N is closed under multiplication by w, so N = phi(C) for a GF(9)-linear [28,13] code C, and symplectic weight on N
is Hamming weight on C. If every 16 of C's 28 coordinates hold an information set, no nonzero word of C vanishes on
16 coordinates, so every nonzero word has weight >= 13:

    python3 verify-it-yourself/gf9info.py prep object/eaqecc_28_7_13_9.json G9.txt
    cc -O3 -o infoset verify-it-yourself/infoset.c
    for p in 0 1 2; do ./infoset 16 $p 3 < G9.txt; done
    python3 verify-it-yourself/gf9info.py witness object/eaqecc_28_7_13_9.json 0,1,2,3,4,5,6,7,8,9,10,11,15,16,17

Expected: `n=28 s=30 c=9 k=7 dim_N=26 dim_I=12 N_closed_under_w=True` and `kappa=13 (2*kappa == dim_N: True)`;
three lines `kappa=13 n=28 m=16 part=P/3 subsets=... deficient=0` whose subsets values (18746445, 8232114, 3443196
for parts 0, 1, 2) sum to 30421755 = C(28,16); and the witness line
`weight=13 in_N=True orthogonal_to_all_rows_of_S=True in_isotropic_part=False`.

Rebuild the object from scratch:

    python3 how-we-built-it/build_obj.py 15 rebuilt.json 13
    shasum -a 256 rebuilt.json object/eaqecc_28_7_13_9.json   # both 64c0cbddea11688f7cc06644d8751c2f62328aae74f7f149b89164a73dea0c78
