# Run it yourself

From this package folder, in a fresh shell (needs python3, standard library only, and cc; no network):

    sh verify-it-yourself/run_checks.sh

Expected output (about 21 seconds on one core; 21.40 s measured, see verify-it-yourself/RECEIPTS.md):

    n=35 s=42 c=14 k=7 dim_isotropic=14 dim_dual=28
    {"n": 35, "s": 42, "c": 14, "k": 7, "dim_perp": 28, "dim_isotropic": 14, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
    n=35 s=42 c=14 k=7 dim_N=28 dim_I=14 N_closed_under_w=True
    kappa=14 (2*kappa == dim_N: True)
    wrote verify-it-yourself/tmp_work/G9.txt
    kappa=14 n=35 m=20 part=0/3 subsets=2004173586 deficient=0 (expected subsets in all parts C(n,m)=3247943160)
    kappa=14 n=35 m=20 part=1/3 subsets=875699289 deficient=0 (expected subsets in all parts C(n,m)=3247943160)
    kappa=14 n=35 m=20 part=2/3 subsets=368070285 deficient=0 (expected subsets in all parts C(n,m)=3247943160)
    T=[1, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26]
    v_x=0 2 0 0 0 0 0 0 0 0 2 2 0 1 0 1 0 2 2 1 0 1 0 2 2 0 2 0 0 0 0 0 0 0 0
    v_z=0 1 0 0 0 0 0 0 0 0 0 2 0 2 2 0 2 1 0 0 1 0 0 2 2 1 1 0 0 0 0 0 0 0 0
    symplectic_weight=16 orthogonal_to_all_rows_of_S=True in_span_S=False support=[1, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26]
    GF(6561) modulus u^4 + 3 u^3 + 0 u^2 + 0 u + 3 over GF(9); i = 4; 27 affine points; 6076 points over GF(6561); 1512 degree-4 places
    L1: rank S = 42, dim phi(C) = 28, 2n - rank S = 28, phi(C) orthogonal to S: True -> span(S)^perp = phi(C): True
    L2: 20 columns unscaled by w^-1 (pattern +---++---+--+++-+----++-+--+-+--++-)
    L3: K = 14, rank(head) = 14 (injective: True), dim zero-tail subcode = 10, rank(tail) = 4, K - dim zero-tail = 4
    L4: place #1319 (point x0 = 2329, y0 = 2788 in this GF(6561) coding): head code = C_L(D_28, 2Q + 8P_inf) (dim 14), zero-tail code = C_L(D_28, 1Q + 8P_inf) (dim 10): True
    L4: 1 of 1512 places identify both codes
    L5: Goppa bounds d(head code) >= 28 - 16 = 12, d(zero-tail code) >= 28 - 12 = 16
    L6: tail code dimension 4 (= K - dim zero-tail: True), all 35 maximal minors nonzero: True -> d(tail) = 4
    L7: d(C) >= min(16, 12 + 4) = 16, so d_EA >= 16
    L8: witness weight 16, in C: True, phi(witness) orthogonal to S: True, outside span(S): True
    RESULT: d_EA = 16 exactly (theorem-based; no distance search): True
    ok:   parameters computed from S
    ok:   computed n=35 s=42 c=14 k=7; claimed n=35 k=7 c=14
    ok:   GF(9) description consistent with S
    ok:   span(S)^perp is closed under w (GF(9)-linear, dimension 2 kappa)
    ok:   the two parameter computations agree
    ok:   all parts of the m=20 information-set test present
    ok:   test run on the code recovered from S (kappa=14)
    ok:   examined 3247943160 of C(35,20) = 3247943160 coordinate subsets
    ok:   every 20 coordinates hold an information set (deficient subsets: 0), so d >= 16
    ok:   witness of symplectic weight 16 outside span(S), claimed d=16
    computed d=16; claimed d=16
    PASS

What it does:
- gf3prep.py (standard library) computes s = rank(S), c = rank(S J S^T)/2, k = n - s + c, a basis of
  N = span(S)^perp and of the isotropic part I = span(S) ∩ N, from S alone.
- check_eaqecc.py prepare checks the object's GF(9) description (D9 is Hermitian-orthogonal to G9 and
  rowspace(S) = phi(D9)). Only its `prepare` mode is used here.
- gf9info.py prep checks that N is closed under multiplication by w (a primitive element of GF(9)), so
  N = phi(C) for a GF(9)-linear [35,14] code C recovered from S, and symplectic weight on N is Hamming weight on C.
  It writes a generator matrix of C.
- infoset.c examines every one of the C(35,20) = 3247943160 sets of 20 coordinates and checks, by exact GF(9)
  ranks, that the columns of C's generator matrix on those coordinates have rank 14 (an information set). If every
  20 coordinates hold an information set, no nonzero word of C vanishes on 20 coordinates, so every nonzero word has
  weight >= 16, and every vector of N, inside or outside I, has symplectic weight >= 16: d >= 16.
- witness.py finds, inside the given 16 positions, a vector of N that is not in span(S) (so not in I), of
  symplectic weight 16: d <= 16.
- goppa_x4.py is a second proof of d >= 16 that searches no codewords at all: it checks (with its own GF(9) and
  GF(6561) arithmetic) that span(S)^perp = phi(C), that C is a Construction X code whose head code is exactly the
  algebraic-geometry code C_L(D_28, 2Q + 8P_inf) of the Hermitian curve y^3 + y = x^4 for one of its 1512 places Q
  of degree 4 and whose zero-tail code is exactly C_L(D_28, Q + 8P_inf), and that the tail code is an MDS [7,4,4]
  code. The Goppa bound (d >= 28 - deg) gives 12 and 16 for the two AG codes, and the Construction X lemma gives
  d(C) >= min(16, 12 + 4) = 16. Each step (L1-L8) is printed.
- verdict.py compares every computed value with the claim in the JSON.

A third, independent exact check (a GF(3) position-subset rank test on S itself, which excludes the isotropic part
inside the test and shares no code with the first two; about 18 CPU-minutes per part measured on a shared, loaded
machine, 1082.48 s, 1080.88 s and 1082.28 s, 02:40:09Z to 03:34:14Z for the three parts run one at a time). For every
set T of 15 positions it compares, by exact GF(3) ranks, the dimension of the vectors of N supported inside T with
that of the vectors of I supported inside T. They are equal for every T, so no vector of N outside I has symplectic
weight <= 15: d >= 16.

    python3 verify-it-yourself/gf3prep.py object/eaqecc_35_7_16_14.json basis.txt
    cc -O3 -o subset_ea64 verify-it-yourself/subset_ea64.c
    for p in 0 1 2; do ./subset_ea64 15 $p 3 < basis.txt & done; wait

Expected: three lines
`W=15 part=P/3 total_subsets=3247943160 examined=1082647720 with_vector_outside_isotropic=0` (P = 0, 1, 2).
With 16 in place of 15 the test finds 2593 + 2556 + 2613 = 7762 sets of 16 positions that hold such a vector, as
many as the information-set test finds sets of 19 coordinates that are not information sets.

A fourth check (Brouwer-Zimmermann minimum distance of C, about 12 seconds: 02:40:55Z to 02:41:07Z measured):

    python3 verify-it-yourself/gf9info.py prep object/eaqecc_35_7_16_14.json G9.txt
    cc -O3 -o bz64 verify-it-yourself/bz64.c
    ./bz64 < G9.txt

Expected: a line beginning `K=14 n=35 d=16 sets=14,14,4,3 maxw=7 words=4027269016`.

Rebuild the object from scratch (how-we-built-it/README.md has the whole search; about 5 seconds):

    cd how-we-built-it
    python3 build_x4.py 0 2 8 8,0,4,6,3,7,5 6,8,4,5,7,4,0,1,5,1,7,2,0,1,8,3 '+---++---+--+++-+----++-+--+-+--++-' out.json 16
    shasum -a 256 out.json ../object/eaqecc_35_7_16_14.json   # both e3d6a8cad3db3a6ea28262ced2969b03a429b1ede488ae9cd59b69f5055b73b4

It prints `X code [35,14] hull=7 -> [[35,7,?;14]]  S 42x70  D9 21x35` (5.48 s measured).
