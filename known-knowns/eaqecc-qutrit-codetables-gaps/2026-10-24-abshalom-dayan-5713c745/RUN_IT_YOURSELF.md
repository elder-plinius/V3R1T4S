# Run it yourself

From this package folder, in a fresh shell (needs python3, standard library only, and cc; no network):

    sh verify-it-yourself/run_checks.sh

Expected output (about 7 seconds with 3 free cores; 6.89 s measured, see verify-it-yourself/RECEIPTS.md):

    n=33 s=38 c=12 k=7 dim_isotropic=14 dim_dual=28
    {"n": 33, "s": 38, "c": 12, "k": 7, "dim_perp": 28, "dim_isotropic": 14, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
    n=33 s=38 c=12 k=7 dim_N=28 dim_I=14 N_closed_under_w=True
    kappa=14 (2*kappa == dim_N: True)
    wrote verify-it-yourself/tmp_work/G9.txt
    kappa=14 n=33 m=19 part=0/3 subsets=507629004 deficient=0 (expected subsets in all parts C(n,m)=818809200)
    kappa=14 n=33 m=19 part=1/3 subsets=219864219 deficient=0 (expected subsets in all parts C(n,m)=818809200)
    kappa=14 n=33 m=19 part=2/3 subsets=91315977 deficient=0 (expected subsets in all parts C(n,m)=818809200)
    T=[0, 11, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    v_x=2 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 1 2 0 0 2 2 1 2 1 0 0 0 0 0 0
    v_z=1 0 0 0 0 0 0 0 0 0 0 1 0 0 2 2 0 1 0 0 2 1 0 1 1 2 2 2 0 0 0 0 0
    symplectic_weight=15 orthogonal_to_all_rows_of_S=True in_span_S=False support=[0, 11, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    GF(729) modulus u^3 + 2 u^2 + 0 u + 1 over GF(9); i = 4; 27 affine points; 288 degree-3 places
    L1: rank S = 38, dim phi(C) = 28, 2n - rank S = 28, phi(C) orthogonal to S: True -> span(S)^perp = phi(C): True
    L2: 16 columns unscaled by w^-1 (pattern +-+---+-+-++---+-+++----+-+-+++++)
    L3: K = 14, rank(head) = 14 (injective: True), dim zero-tail subcode = 11, rank(tail) = 3
    L4: place #182 (point x0 = 69, y0 = 114 in this GF(729) coding): head code = C_L(D_28, 4Q + 4P_inf) (dim 14), zero-tail code = C_L(D_28, 3Q + 4P_inf) (dim 11): True
    L4: 1 of 288 places identify both codes
    L5: Goppa bounds d(head code) >= 28 - 16 = 12, d(zero-tail code) >= 28 - 13 = 15
    L6: tail code dimension 3, all 10 maximal minors nonzero: True -> d(tail) = 3
    L7: d(C) >= min(15, 12 + 3) = 15, so d_EA >= 15
    L8: witness weight 15, in C: True, phi(witness) orthogonal to S: True, outside span(S): True
    RESULT: d_EA = 15 exactly (theorem-based; no distance search): True
    ok:   parameters computed from S
    ok:   computed n=33 s=38 c=12 k=7; claimed n=33 k=7 c=12
    ok:   GF(9) description consistent with S
    ok:   span(S)^perp is closed under w (GF(9)-linear, dimension 2 kappa)
    ok:   the two parameter computations agree
    ok:   all parts of the m=19 information-set test present
    ok:   test run on the code recovered from S (kappa=14)
    ok:   examined 818809200 of C(33,19) = 818809200 coordinate subsets
    ok:   every 19 coordinates hold an information set (deficient subsets: 0), so d >= 15
    ok:   witness of symplectic weight 15 outside span(S), claimed d=15
    computed d=15; claimed d=15
    PASS

What it does:
- gf3prep.py (standard library) computes s = rank(S), c = rank(S J S^T)/2, k = n - s + c, a basis of
  N = span(S)^perp and of the isotropic part I = span(S) ∩ N, from S alone.
- check_eaqecc.py prepare checks the object's GF(9) description (D9 is Hermitian-orthogonal to G9 and
  rowspace(S) = phi(D9)). Only its `prepare` mode is used here.
- gf9info.py prep checks that N is closed under multiplication by w (a primitive element of GF(9)), so
  N = phi(C) for a GF(9)-linear [33,14] code C recovered from S, and symplectic weight on N is Hamming weight on C.
  It writes a generator matrix of C.
- infoset.c examines every one of the C(33,19) = 818809200 sets of 19 coordinates and checks, by exact GF(9)
  ranks, that the columns of C's generator matrix on those coordinates have rank 14 (an information set). If every
  19 coordinates hold an information set, no nonzero word of C vanishes on 19 coordinates, so every nonzero word has
  weight >= 15, and every vector of N, inside or outside I, has symplectic weight >= 15: d >= 15.
- witness.py finds, inside the given 15 positions, a vector of N that is not in span(S) (so not in I), of
  symplectic weight 15: d <= 15.
- goppa_x.py is a second proof of d >= 15 that searches no codewords at all: it checks (with its own GF(9) and
  GF(729) arithmetic) that span(S)^perp = phi(C), that C is a Construction X code whose head code is exactly the
  algebraic-geometry code C_L(D_28, 4Q + 4P_inf) of the Hermitian curve for one of its 288 places Q of degree 3 and
  whose zero-tail code is exactly C_L(D_28, 3Q + 4P_inf), and that the tail code is an MDS [5,3,3] code. The Goppa
  bound (d >= 28 - deg) gives 12 and 15 for the two AG codes, and the Construction X lemma gives
  d(C) >= min(15, 12 + 3) = 15. Each step (L1-L8) is printed; the proof is written out in HOW_WE_FOUND_IT.md.
- verdict.py compares every computed value with the claim in the JSON.

A third, independent exact check (a GF(3) position-subset rank test on S itself, which excludes the isotropic
part inside the test and shares no code with the first two; about 12 minutes measured on a shared, loaded machine, 19:59:31Z to 20:11:29Z). For every set T of 14
positions it compares, by exact GF(3) ranks, the dimension of the vectors of N supported inside T with that of the
vectors of I supported inside T. They are equal for every T, so no vector of N outside I has symplectic weight
<= 14: d >= 15.

    python3 verify-it-yourself/gf3prep.py object/eaqecc_33_7_15_12.json basis.txt
    cc -O3 -o subset_ea64 verify-it-yourself/subset_ea64.c
    for p in 0 1 2; do ./subset_ea64 14 $p 3 < basis.txt & done; wait

Expected: three lines
`W=14 part=P/3 total_subsets=818809200 examined=272936400 with_vector_outside_isotropic=0` (P = 0, 1, 2).
With 15 in place of 14 the test finds 3362 + 3252 + 3332 = 9946 sets of 15 positions that hold such a vector, as
many as the information-set test finds sets of 18 coordinates that are not information sets.

A fourth check (Brouwer-Zimmermann minimum distance of C, about 15 seconds):

    python3 verify-it-yourself/gf9info.py prep object/eaqecc_33_7_15_12.json G9.txt
    cc -O3 -o bz64 verify-it-yourself/bz64.c
    ./bz64 < G9.txt

Expected: a line beginning `K=14 n=33 d=15`.

Rebuild the object from scratch (how-we-built-it/README.md has the whole search):

    python3 how-we-built-it/build_x_lead.py 0 4 4 3,9,0,1,5 5,7,7,8,8,0,1,6,1 +-+---+-+-++---+-+++----+-+-+++++ rebuilt.json 15
    shasum -a 256 rebuilt.json object/eaqecc_33_7_15_12.json   # both 5713c745e8e837dc41e1883a120488fb38dce3b4254292335ca98f99a1787256
