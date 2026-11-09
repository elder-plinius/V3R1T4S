# Run it yourself

From this package folder, in a fresh shell (needs python3, standard library only, and cc; no network):

    sh verify-it-yourself/run_checks.sh

Expected output (about 5 seconds with 4 free cores; 4.2 s measured, see verify-it-yourself/RECEIPTS.md):

    n=28 s=28 c=6 k=6 dim_isotropic=16 dim_dual=28
    {"n": 28, "s": 28, "c": 6, "k": 6, "dim_perp": 28, "dim_isotropic": 16, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
    W=11 part=0/4 total_subsets=21474180 examined=5368545 with_vector_outside_isotropic=0
    W=11 part=1/4 total_subsets=21474180 examined=5368545 with_vector_outside_isotropic=0
    W=11 part=2/4 total_subsets=21474180 examined=5368545 with_vector_outside_isotropic=0
    W=11 part=3/4 total_subsets=21474180 examined=5368545 with_vector_outside_isotropic=0
    T=[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
    v_x=0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 2 2 2 2 2 2 0
    v_z=0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0 0 0
    symplectic_weight=12 orthogonal_to_all_rows_of_S=True in_span_S=False support=[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
    ok:   parameters computed from S
    ok:   computed n=28 s=28 c=6 k=6; claimed n=28 k=6 c=6
    ok:   GF(9) description consistent with S
    ok:   all parts of the W=11 subset test present
    ok:   examined 21474180 of C(28,11) = 21474180 subsets
    ok:   no vector of span(S)^perp outside the isotropic part on <= 11 positions (found 0)
    ok:   witness of symplectic weight 12 outside span(S), claimed d=12
    computed d=12; claimed d=12
    PASS

What it does:
- gf3prep.py (standard library) computes s = rank(S), c = rank(S J S^T)/2, k = n - s + c, a basis of
  N = span(S)^perp and of the isotropic part I = span(S) ∩ N, from S alone.
- check_eaqecc.py prepare checks the object's GF(9) description (D9 is Hermitian-orthogonal to G9 and
  rowspace(S) = phi(D9)). Only its `prepare` mode is used here.
- subset_ea.c examines every one of the C(28,11) = 21474180 sets T of 11 positions and compares, by exact GF(3)
  ranks, the dimension of the vectors of N supported inside T with that of the vectors of I supported inside T.
  They are equal for every T, so no vector of N outside I has symplectic weight <= 11: d >= 12.
- witness.py finds, inside the given 12 positions, a vector of N that is not in span(S) (so not in I), of
  symplectic weight 12: d <= 12.
- verdict.py compares every computed value with the claim in the JSON.

Why the subset test is complete: a vector of N outside I with weight <= 11 is supported inside some 11-set T; for
that T the vectors of N supported in T then include one outside I, so dim N_T > dim I_T. Conversely, any T with
dim N_T > dim I_T holds such a vector. The program checks the condition through incremental elimination of the
basis restricted to the positions outside T (both the x and z column of each position).

A second, independent exact check (a GF(9) information-set test, about 1 second; it shares no code with the
first). N is closed under multiplication by w, so N = phi(C) for a GF(9)-linear [28,14] code C, and symplectic
weight on N is Hamming weight on C. If every 17 of C's 28 coordinates hold an information set, no nonzero word of C
vanishes on 17 coordinates, so every nonzero word has weight >= 12:

    python3 verify-it-yourself/gf9info.py prep object/eaqecc_28_6_12_6.json G9.txt
    cc -O3 -o infoset verify-it-yourself/infoset.c
    for p in 0 1 2 3; do ./infoset 17 $p 4 < G9.txt; done
    python3 verify-it-yourself/gf9info.py witness object/eaqecc_28_6_12_6.json 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,27

Expected: `n=28 s=28 c=6 k=6 dim_N=28 dim_I=16 N_closed_under_w=True` and `kappa=14 (2*kappa == dim_N: True)`;
four lines `kappa=14 n=28 m=17 part=P/4 subsets=... deficient=0` whose subsets values (740317, 2063341, 5386501,
13284021 for parts 3, 2, 1, 0) sum to 21474180 = C(28,17); and the witness line
`weight=12 in_N=True orthogonal_to_all_rows_of_S=True in_isotropic_part=False`.

Rebuild the object from scratch:

    python3 how-we-built-it/build_obj.py 16 rebuilt.json 12
    shasum -a 256 rebuilt.json object/eaqecc_28_6_12_6.json   # both 51f713462c7db831723702a4d0b0cc9a73faacd2552999a7007f75d393188573
