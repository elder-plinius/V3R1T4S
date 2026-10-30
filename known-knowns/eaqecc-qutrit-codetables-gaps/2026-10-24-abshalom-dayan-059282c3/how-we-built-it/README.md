# How we built it

Commands from this folder (python3 standard library and cc), in the order the object was found:

1. The two algebraic-geometry codes of the Hermitian curve y^3 + y = x^4 over GF(9), with Q the place of degree 3
   numbered 0 in deg3.py's list (arithmetic in GF(729); coordinates: the 27 affine points, then P_inf):

       python3 deg3.py code 0 3 8 C1.code      # C(D_28, 3Q + 8P_inf) = [28,15], Goppa bound d >= 11
       python3 deg3.py code 0 2 8 C2.code      # C(D_28, 2Q + 8P_inf) = [28,12], Goppa bound d >= 14
       python3 prep_x.py C1.code C2.code X17_q0_a3.xin    # byte-identical to the X17_q0_a3.xin here (sha256 db455dfe...32df)

2. The exact maximum Hermitian hull of every Construction X code of this pair (all 2^27 head sign patterns, every
   [5,3,3] tail and every 3 x 3 gluing matrix; minimal-rank-completion bound, made exact by the rank classification of
   Hermitian forms; about 5 minutes on one core):

       cc -O3 -o hullbound hullbound.c && ./hullbound bound < X17_q0_a3.xin    # bound_X17_q0_a3.txt: exact maximum 6

   Hull 6 is reached at exactly one head pattern (the "exact 6" line): all 28 head columns unscaled.

3. A tail and gluing matrix that reach hull 6 at that pattern (random tries, seed 1; try 2511 succeeds):

       ./hullbound real ++++++++++++++++++++++++++++ 1 200000 < X17_q0_a3.xin    # real_X17_q0_a3.txt

   Points 1, 0, 6, 9 (infinity), 5; tail signs ----- (every tail column multiplied by w); M = 1,3,8,0,7,7,4,1,2.

4. The object (the X code, its Hermitian dual and S = phi(dual) over GF(3)):

       python3 build_x_lead.py 0 3 8 1,0,6,9,5 1,3,8,0,7,7,4,1,2 ++++++++++++++++++++++++++++----- out.json 14

   out.json is byte-identical to ../object/eaqecc_33_9_14_12.json (sha256 059282c3...91). It prints
   `X code [33,15] hull=6 -> [[33,9,?;12]]`. Erratum: the object's "construction" string says "rows 11..13 of the
   tail = M A" (a fixed phrase in build_x_lead.py); for this pair C2 has dimension 12, so the rows carrying M A are
   rows 12..14 (0-based) of G9. The matrices are unaffected.

- `PREREG.md`: the frozen plan of the run folder that produced this claim, written before any of
  its checkers ran on the object. No null test: an explicit object checked by deterministic exact checkers against a
  table value.
