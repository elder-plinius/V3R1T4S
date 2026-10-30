# Run it yourself

From this package folder, in a fresh shell (needs python3, standard library only, and cc; no network):

    sh verify-it-yourself/run_checks.sh

Expected output (about 5 seconds with 3 free cores; 4.58 s measured, see verify-it-yourself/RECEIPTS.md):

    n=33 s=40 c=15 k=8 dim_isotropic=10 dim_dual=26
    {"n": 33, "s": 40, "c": 15, "k": 8, "dim_perp": 26, "dim_isotropic": 10, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
    n=33 s=40 c=15 k=8 dim_N=26 dim_I=10 N_closed_under_w=True
    kappa=13 (2*kappa == dim_N: True)
    wrote verify-it-yourself/tmp_work/G9.txt
    kappa=13 n=33 m=18 part=0/3 subsets=620845293 deficient=0 (expected subsets in all parts C(n,m)=1037158320)
    kappa=13 n=33 m=18 part=1/3 subsets=287764785 deficient=0 (expected subsets in all parts C(n,m)=1037158320)
    kappa=13 n=33 m=18 part=2/3 subsets=128548242 deficient=0 (expected subsets in all parts C(n,m)=1037158320)
    T=[9, 10, 11, 15, 16, 17, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31]
    v_x=0 0 0 0 0 0 0 0 0 2 1 2 0 0 0 1 0 0 0 0 0 1 1 2 1 0 0 2 0 1 0 0 0
    v_z=0 0 0 0 0 0 0 0 0 2 1 2 0 0 0 2 1 2 0 0 0 1 1 0 2 2 2 0 0 1 1 1 0
    symplectic_weight=16 orthogonal_to_all_rows_of_S=True in_span_S=False support=[9, 10, 11, 15, 16, 17, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31]
    ok:   parameters computed from S
    ok:   computed n=33 s=40 c=15 k=8; claimed n=33 k=8 c=15
    ok:   GF(9) description consistent with S
    ok:   span(S)^perp is closed under w (GF(9)-linear, dimension 2 kappa)
    ok:   the two parameter computations agree
    ok:   all parts of the m=18 information-set test present
    ok:   test run on the code recovered from S (kappa=13)
    ok:   examined 1037158320 of C(33,18) = 1037158320 coordinate subsets
    ok:   every 18 coordinates hold an information set (deficient subsets: 0), so d >= 16
    ok:   witness of symplectic weight 16 outside span(S), claimed d=16
    computed d=16; claimed d=16
    PASS

What it does:
- gf3prep.py (standard library) computes s = rank(S), c = rank(S J S^T)/2, k = n - s + c, a basis of
  N = span(S)^perp and of the isotropic part I = span(S) ∩ N, from S alone.
- check_eaqecc.py prepare checks the object's GF(9) description (D9 is Hermitian-orthogonal to G9 and
  rowspace(S) = phi(D9)). Only its `prepare` mode is used here.
- gf9info.py prep checks that N is closed under multiplication by w (a primitive element of GF(9)), so
  N = phi(C) for a GF(9)-linear [33,13] code C recovered from S, and symplectic weight on N is Hamming weight on C.
  It writes a generator matrix of C.
- infoset.c examines every one of the C(33,18) = 1037158320 sets of 18 coordinates and checks, by exact GF(9)
  ranks, that the columns of C's generator matrix on those coordinates have rank 13 (an information set). If every
  18 coordinates hold an information set, no nonzero word of C vanishes on 18 coordinates, so every nonzero word has
  weight >= 16, and every vector of N, inside or outside I, has symplectic weight >= 16: d >= 16.
- witness.py finds, inside the given 16 positions, a vector of N that is not in span(S) (so not in I), of
  symplectic weight 16: d <= 16.
- verdict.py compares every computed value with the claim in the JSON.

A second, independent exact check (a GF(3) position-subset rank test on S itself, which excludes the isotropic
part inside the test and shares no code with the first; about 5 to 6 minutes with 3 cores). For every set T of 15
positions it compares, by exact GF(3) ranks, the dimension of the vectors of N supported inside T with that of the
vectors of I supported inside T. They are equal for every T, so no vector of N outside I has symplectic weight
<= 15: d >= 16.

    python3 verify-it-yourself/gf3prep.py object/eaqecc_33_8_16_15.json basis.txt
    cc -O3 -o subset_ea64 verify-it-yourself/subset_ea64.c
    for p in 0 1 2; do ./subset_ea64 15 $p 3 < basis.txt & done; wait

Expected: three lines
`W=15 part=P/3 total_subsets=1037158320 examined=345719440 with_vector_outside_isotropic=0` (P = 0, 1, 2).
With 16 in place of 15 the test finds 2775 + 2832 + 2815 = 8422 sets of 16 positions that hold such a vector, as
many as the information-set test finds sets of 17 coordinates that are not information sets.

A third check (Brouwer-Zimmermann minimum distance of C, a few seconds):

    python3 verify-it-yourself/gf9info.py prep object/eaqecc_33_8_16_15.json G9.txt
    cc -O3 -o bz64 verify-it-yourself/bz64.c
    ./bz64 < G9.txt

Expected: a line beginning `K=13 n=33 d=16`.

Rebuild the object from scratch:

    python3 how-we-built-it/build_x_obj.py rebuilt.json 16
    shasum -a 256 rebuilt.json object/eaqecc_33_8_16_15.json   # both 763a503e8ca0560a07e6c650f172b8de932bfd91474eafc5302c6a00013ab459
