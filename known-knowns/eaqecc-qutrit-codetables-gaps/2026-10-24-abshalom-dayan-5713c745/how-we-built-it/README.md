# How we built it

Commands from this folder (python3 standard library and cc), in the order the object was found:

1. The two algebraic-geometry codes of the Hermitian curve y^3 + y = x^4 over GF(9), with Q the place of degree 3
   numbered 0 in deg3.py's list (arithmetic in GF(729); coordinates: the 27 affine points, then P_inf):

       python3 deg3.py code 0 4 4 C1.code      # C(D_28, 4Q + 4P_inf) = [28,14], Goppa bound d >= 12
       python3 deg3.py code 0 3 4 C2.code      # C(D_28, 3Q + 4P_inf) = [28,11], Goppa bound d >= 15
       python3 prep_x.py C1.code C2.code X16_q0_a4.xin    # byte-identical to the X16_q0_a4.xin here (sha256 c1c111c3...6332)

2. The maximum Hermitian hull of every Construction X code of this pair (all 2^27 head sign patterns, every
   [5,3,3] tail and every 3 x 3 gluing matrix; minimal-rank-completion bound, made exact by the rank classification of
   Hermitian forms; about 4 minutes on one core). Unverified: this "exact maximum", here and in bound_X16_q0_a4.txt,
   is unverified contributor text, as README.md says; the claim does not depend on it:

       cc -O3 -o hullbound hullbound.c && ./hullbound bound < X16_q0_a4.xin    # bound_X16_q0_a4.txt: exact maximum 7 (unverified)

   Hull 7 is reached at exactly one head pattern (the "exact 7" line), +-+---+-+-++---+-+++----+-+- (a column marked
   - is multiplied by w, of norm -1).

3. A tail and gluing matrix that reach hull 7 at that pattern (random tries, seed 1; the fifth try succeeds):

       ./hullbound real +-+---+-+-++---+-+++----+-+- 1 200000 < X16_q0_a4.xin    # real_X16_q0_a4.txt

   Points 3, 9 (infinity), 0, 1, 5; tail signs +++++; M = 5,7,7,8,8,0,1,6,1.

4. The object (the X code, its Hermitian dual and S = phi(dual) over GF(3)):

       python3 build_x_lead.py 0 4 4 3,9,0,1,5 5,7,7,8,8,0,1,6,1 +-+---+-+-++---+-+++----+-+-+++++ out.json 15

   out.json is byte-identical to ../object/eaqecc_33_7_15_12.json (sha256 5713c745...87256). It prints
   `X code [33,14] hull=7 -> [[33,7,?;12]]`. The object's "construction" string says "rows 11..13 of the tail = M A",
   which is right for this pair (C2 has dimension 11, so rows 11..13, 0-based, carry M A).

- `PREREG.md`: the frozen plan of the run that panelled this claim, written before any of its
  checkers ran on the object. No null test: an explicit object checked by deterministic exact checkers against a
  table value.
