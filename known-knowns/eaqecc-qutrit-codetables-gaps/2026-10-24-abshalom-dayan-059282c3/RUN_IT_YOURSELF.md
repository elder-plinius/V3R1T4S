# Run it yourself

From this package folder, in a fresh shell (needs python3, standard library only, and cc; no network):

    sh verify-it-yourself/run_checks.sh

Expected output (about 9 seconds with 3 free cores; 8.69 s measured, see verify-it-yourself/RECEIPTS.md):

    n=33 s=36 c=12 k=9 dim_isotropic=12 dim_dual=30
    {"n": 33, "s": 36, "c": 12, "k": 9, "dim_perp": 30, "dim_isotropic": 12, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
    n=33 s=36 c=12 k=9 dim_N=30 dim_I=12 N_closed_under_w=True
    kappa=15 (2*kappa == dim_N: True)
    wrote verify-it-yourself/tmp_work/G9.txt
    kappa=15 n=33 m=20 part=0/3 subsets=368070285 deficient=0 (expected subsets in all parts C(n,m)=573166440)
    kappa=15 n=33 m=20 part=1/3 subsets=148206066 deficient=0 (expected subsets in all parts C(n,m)=573166440)
    kappa=15 n=33 m=20 part=2/3 subsets=56890089 deficient=0 (expected subsets in all parts C(n,m)=573166440)
    T=[0, 1, 3, 4, 5, 6, 9, 12, 13, 14, 16, 30, 31, 32]
    v_x=0 2 0 0 1 1 1 0 0 0 0 0 2 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2
    v_z=1 1 0 2 1 0 1 0 0 2 0 0 0 1 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 1 2 1
    symplectic_weight=14 orthogonal_to_all_rows_of_S=True in_span_S=False support=[0, 1, 3, 4, 5, 6, 9, 12, 13, 14, 16, 30, 31, 32]
    GF(729) modulus u^3 + 2 u^2 + 0 u + 1 over GF(9); i = 4; 27 affine points; 288 degree-3 places
    L1: rank S = 36, dim phi(C) = 30, 2n - rank S = 30, phi(C) orthogonal to S: True -> span(S)^perp = phi(C): True
    L2: 5 columns unscaled by w^-1 (pattern ++++++++++++++++++++++++++++-----)
    L3: K = 15, rank(head) = 15 (injective: True), dim zero-tail subcode = 12, rank(tail) = 3
    L4: place #182 (point x0 = 69, y0 = 114 in this GF(729) coding): head code = C_L(D_28, 3Q + 8P_inf) (dim 15), zero-tail code = C_L(D_28, 2Q + 8P_inf) (dim 12): True
    L4: 1 of 288 places identify both codes
    L5: Goppa bounds d(head code) >= 28 - 17 = 11, d(zero-tail code) >= 28 - 14 = 14
    L6: tail code dimension 3, all 10 maximal minors nonzero: True -> d(tail) = 3
    L7: d(C) >= min(14, 11 + 3) = 14, so d_EA >= 14
    L8: witness weight 14, in C: True, phi(witness) orthogonal to S: True, outside span(S): True
    RESULT: d_EA = 14 exactly (theorem-based; no distance search): True
    ok:   parameters computed from S
    ok:   computed n=33 s=36 c=12 k=9; claimed n=33 k=9 c=12
    ok:   GF(9) description consistent with S
    ok:   span(S)^perp is closed under w (GF(9)-linear, dimension 2 kappa)
    ok:   the two parameter computations agree
    ok:   all parts of the m=20 information-set test present
    ok:   test run on the code recovered from S (kappa=15)
    ok:   examined 573166440 of C(33,20) = 573166440 coordinate subsets
    ok:   every 20 coordinates hold an information set (deficient subsets: 0), so d >= 14
    ok:   witness of symplectic weight 14 outside span(S), claimed d=14
    computed d=14; claimed d=14
    PASS

What it does:
- gf3prep.py (standard library) computes s = rank(S), c = rank(S J S^T)/2, k = n - s + c, a basis of
  N = span(S)^perp and of the isotropic part I = span(S) ∩ N, from S alone.
- check_eaqecc.py prepare checks the object's GF(9) description (D9 is Hermitian-orthogonal to G9 and
  rowspace(S) = phi(D9)). Only its `prepare` mode is used here.
- gf9info.py prep checks that N is closed under multiplication by w (a primitive element of GF(9)), so
  N = phi(C) for a GF(9)-linear [33,15] code C recovered from S, and symplectic weight on N is Hamming weight on C.
  It writes a generator matrix of C.
- infoset.c examines every one of the C(33,20) = 573166440 sets of 20 coordinates and checks, by exact GF(9)
  ranks, that the columns of C's generator matrix on those coordinates have rank 15 (an information set). If every
  20 coordinates hold an information set, no nonzero word of C vanishes on 20 coordinates, so every nonzero word has
  weight >= 14, and every vector of N, inside or outside I, has symplectic weight >= 14: d >= 14.
- witness.py finds, inside the given 14 positions, a vector of N that is not in span(S) (so not in I), of
  symplectic weight 14: d <= 14.
- goppa_x.py is a second proof of d >= 14 that searches no codewords at all: it checks (with its own GF(9) and
  GF(729) arithmetic) that span(S)^perp = phi(C), that C is a Construction X code whose head code is exactly the
  algebraic-geometry code C_L(D_28, 3Q + 8P_inf) of the Hermitian curve for one of its 288 places Q of degree 3 and
  whose zero-tail code is exactly C_L(D_28, 2Q + 8P_inf), and that the tail code is an MDS [5,3,3] code. The Goppa
  bound (d >= 28 - deg) gives 11 and 14 for the two AG codes, and the Construction X lemma gives
  d(C) >= min(14, 11 + 3) = 14. Each step (L1-L8) is printed; the proof is written out in HOW_WE_FOUND_IT.md.
- verdict.py compares every computed value with the claim in the JSON.

A third, independent exact check (a GF(3) position-subset rank test on S itself, which excludes the isotropic
part inside the test and shares no code with the first two; about 12 minutes measured on a shared, loaded machine,
20:26:08Z to 20:37:59Z). For every set T of 13 positions it compares, by exact GF(3) ranks, the dimension of the
vectors of N supported inside T with that of the vectors of I supported inside T. They are equal for every T, so no
vector of N outside I has symplectic weight <= 13: d >= 14.

    python3 verify-it-yourself/gf3prep.py object/eaqecc_33_9_14_12.json basis.txt
    cc -O3 -o subset_ea64 verify-it-yourself/subset_ea64.c
    for p in 0 1 2; do ./subset_ea64 13 $p 3 < basis.txt & done; wait

Expected: three lines
`W=13 part=P/3 total_subsets=573166440 examined=191055480 with_vector_outside_isotropic=0` (P = 0, 1, 2).
With 14 in place of 13 the test finds 3469 + 3448 + 3487 = 10404 sets of 14 positions that hold such a vector, as
many as the information-set test finds sets of 19 coordinates that are not information sets.

A fourth check (Brouwer-Zimmermann minimum distance of C, a few seconds):

    python3 verify-it-yourself/gf9info.py prep object/eaqecc_33_9_14_12.json G9.txt
    cc -O3 -o bz64 verify-it-yourself/bz64.c
    ./bz64 < G9.txt

Expected: a line beginning `K=15 n=33 d=14`.

Rebuild the object from scratch (how-we-built-it/README.md has the whole search):

    python3 how-we-built-it/build_x_lead.py 0 3 8 1,0,6,9,5 1,3,8,0,7,7,4,1,2 ++++++++++++++++++++++++++++----- rebuilt.json 14
    shasum -a 256 rebuilt.json object/eaqecc_33_9_14_12.json   # both 059282c383e7d059867ecd1a1ec51d54197af25b2c6a320dd26b150ac1a99391
