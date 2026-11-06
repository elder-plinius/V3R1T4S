# How we built it

- `build_x_obj.py out.json d_claimed [out_G9.code]`: builds the claim JSON from its construction. `deg3.py` builds
  the algebraic-geometry codes C(D_28, aQ + bP_inf) of the Hermitian curve y^3 + y = x^4 over GF(9) with a place Q of
  degree 3 (arithmetic in GF(729), the 27 affine points plus the point at infinity as coordinates); `gf9lib.py`:
  GF(9) arithmetic, Hermitian dual, the map phi to GF(3). The object is the Construction X code of
  C1 = C(D_28, 4Q + 3P_inf) [28,13,13]_9 and C2 = C(D_28, 3Q + 3P_inf) [28,10,16]_9 (Q = place 0 of deg3.py's
  list) with a [5,3,3]_9 Reed-Solomon tail, the tail parameters and the column sign pattern written in the script.
  This object: `python3 build_x_obj.py out.json 16`, byte-identical to `object/eaqecc_33_8_16_15.json`.
- `PREREG.md`: the frozen plan of the run that produced this claim, written before any of its
  checkers ran on the object. No null test: an explicit object checked by deterministic exact checkers against a
  table value.
