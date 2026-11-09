# How we built it

- `build_obj.py m out.json d_claimed [columns scaled by w]`: builds the claim JSON from the extended one-point
  Hermitian code E_m (`hermitian.py`: points and monomials of y^3 + y = x^4 over GF(9); `gf9lib.py`: GF(9)
  arithmetic, Hermitian dual, phi map to GF(3)). This object: `python3 build_obj.py 15 out.json 13` (E_15, no column
  scaled), byte-identical to `object/eaqecc_28_7_13_9.json` (sha256 64c0cbdd...0c78). It prints
  `E_15 scaled_cols=[] [28,13] hull=6 -> [[28,7,?;9]]`.
- `PREREG.md`: the frozen plan of the run that panelled this claim. `PREREG_found_run.md`: the
  frozen plan of the run that found it and kept it as a candidate. No null test: an explicit
  object checked by deterministic exact checkers against a table value.
