# How we built it

- `build_punct_obj.py m out.json d_claimed deleted scaled`: builds the claim JSON from the extended one-point
  Hermitian code E_m (`hermitian.py`: points and monomials of y^3 + y = x^4 over GF(9); `gf9lib.py`: GF(9)
  arithmetic, Hermitian dual, phi map to GF(3)), deletes the given coordinates (0-based, of the length-28 code) and
  multiplies the given columns of the punctured code by w. This object:
  `python3 build_punct_obj.py 13 out.json 12 0,1,2 6,7,8,12,13,14,15,16,17,18,19,20,24`, byte-identical to
  `object/eaqecc_25_5_12_8.json` (sha256 e33e8fb0...9ec3). It prints `E_13 deleted=[0, 1, 2]
  scaled_cols=[6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24] [25,11] hull=6 -> [[25,5,?;8]]  S 28x50  D9 14x25`.
- The search that found it: `punct.py` writes E_m punctured at one deletion set per orbit of the automorphisms of the
  curve fixing the point at infinity (one `.code` file per code: dimension, length, generator rows over GF(9) coded
  a + 3b); `epsbig.c` (with `gf9.h`) computes the exact maximum Hermitian hull over all 2^(n-1) column sign patterns
  (column 0 fixed; usage `epsbig 0 0 < file.code`); `run_eps.sh list P cap out` runs it over a list of code files,
  P at a time, each capped. `epsbig_result.txt` is its output line for this code (E_13, deleted set of orbit 0 of
  3-subsets: coordinates 0, 1, 2): maximum hull 6, reached by one sign pattern (`-` marks a column times w), with the
  histogram of hull dimensions over all 2^24 patterns.
- `PREREG.md`: the frozen plan of the run folder that claimed this code. No null test:
  an explicit object checked by deterministic exact checkers against a table cell.
