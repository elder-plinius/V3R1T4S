# Run it yourself

From this package folder, in a fresh shell (needs python3, standard library only, and cc; no network):

    sh verify-it-yourself/run_checks.sh

Expected output (about 4 seconds with 3 free cores; 4.04 s measured, see verify-it-yourself/RECEIPTS.md):

    n=28 s=26 c=7 k=9 dim_isotropic=12 dim_dual=30
    {"n": 28, "s": 26, "c": 7, "k": 9, "dim_perp": 30, "dim_isotropic": 12, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
    W=10 part=0/3 total_subsets=13123110 examined=4374370 with_vector_outside_isotropic=0
    W=10 part=1/3 total_subsets=13123110 examined=4374370 with_vector_outside_isotropic=0
    W=10 part=2/3 total_subsets=13123110 examined=4374370 with_vector_outside_isotropic=0
    T=[0, 1, 2, 3, 4, 5, 6, 11, 18, 26, 27]
    v_x=0 1 1 2 0 2 2 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2
    v_z=1 0 2 1 2 0 2 0 0 0 0 2 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0
    symplectic_weight=11 orthogonal_to_all_rows_of_S=True in_span_S=False support=[0, 1, 2, 3, 4, 5, 6, 11, 18, 26, 27]
    ok:   parameters computed from S
    ok:   computed n=28 s=26 c=7 k=9; claimed n=28 k=9 c=7
    ok:   GF(9) description consistent with S
    ok:   all parts of the W=10 subset test present
    ok:   examined 13123110 of C(28,10) = 13123110 subsets
    ok:   no vector of span(S)^perp outside the isotropic part on <= 10 positions (found 0)
    ok:   witness of symplectic weight 11 outside span(S), claimed d=11
    computed d=11; claimed d=11
    PASS

What it does:
- gf3prep.py (standard library) computes s = rank(S), c = rank(S J S^T)/2, k = n - s + c, a basis of
  N = span(S)^perp and of the isotropic part I = span(S) ∩ N, from S alone.
- check_eaqecc.py prepare checks the object's GF(9) description (D9 is Hermitian-orthogonal to G9 and
  rowspace(S) = phi(D9)). Only its `prepare` mode is used here.
- subset_ea.c examines every one of the C(28,10) = 13123110 sets T of 10 positions and compares, by exact GF(3)
  ranks, the dimension of the vectors of N supported inside T with that of the vectors of I supported inside T.
  They are equal for every T, so no vector of N outside I has symplectic weight <= 10: d >= 11.
- witness.py finds, inside the given 11 positions, a vector of N that is not in span(S) (so not in I), of
  symplectic weight 11: d <= 11.
- verdict.py compares every computed value with the claim in the JSON.

Why the subset test is complete: a vector of N outside I with weight <= 10 is supported inside some 10-set T; for
that T the vectors of N supported in T then include one outside I, so dim N_T > dim I_T. Conversely, any T with
dim N_T > dim I_T holds such a vector.

A second, independent exact check (a GF(9) information-set test, under a second; it shares no code with the first).
N is closed under multiplication by w, so N = phi(C) for a GF(9)-linear [28,15] code C, and symplectic weight on N
is Hamming weight on C. If every 18 of C's 28 coordinates hold an information set, no nonzero word of C vanishes on
18 coordinates, so every nonzero word has weight >= 11:

    python3 verify-it-yourself/gf9info.py prep object/eaqecc_28_9_11_7.json G9.txt
    cc -O3 -o infoset verify-it-yourself/infoset.c
    for p in 0 1 2; do ./infoset 18 $p 3 < G9.txt; done
    python3 verify-it-yourself/gf9info.py witness object/eaqecc_28_9_11_7.json 7,8,9,10,12,13,14,15,16,17,19,20,21,22,23,24,25

Expected: `n=28 s=26 c=7 k=9 dim_N=30 dim_I=12 N_closed_under_w=True` and `kappa=15 (2*kappa == dim_N: True)`;
three lines `kappa=15 n=28 m=18 part=P/3 subsets=... deficient=0` whose subsets values (8788392, 3226638, 1108080
for parts 0, 1, 2) sum to 13123110 = C(28,18); and the witness line
`weight=11 in_N=True orthogonal_to_all_rows_of_S=True in_isotropic_part=False`.

Rebuild the object from scratch:

    python3 how-we-built-it/build_obj.py 17 rebuilt.json 11
    shasum -a 256 rebuilt.json object/eaqecc_28_9_11_7.json   # both 2a0a1ae5e178dcc0264b6a9f40ee1935991f28e65199a0712aecffe879b6c7d0
