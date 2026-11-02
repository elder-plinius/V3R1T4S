# How we built it

- `build_punct_obj.py m out.json d_claimed deleted scaled`: builds the claim JSON from the extended one-point
  Hermitian code E_m (`hermitian.py`: points and monomials of y^3 + y = x^4 over GF(9); `gf9lib.py`: GF(9)
  arithmetic, Hermitian dual, phi map to GF(3)), deletes the given coordinates (0-based, of the length-28 code) and
  multiplies the given columns of the punctured code by w. This object:
  `python3 build_punct_obj.py 11 out.json 13 0,3,6,11 1,3,5,7,10,11,12,15,17,18,20,22`, byte-identical to
  `object/eaqecc_24_4_13_10.json` (sha256 feeeff03...1794). It prints `E_11 deleted=[0, 3, 6, 11]
  scaled_cols=[1, 3, 5, 7, 10, 11, 12, 15, 17, 18, 20, 22] [24,9] hull=5 -> [[24,4,?;10]]  S 30x48  D9 15x24`.
- The search that found it: `punct.py` writes E_m punctured at one deletion set per orbit of the automorphisms of the
  curve fixing the point at infinity (one `.code` file per code: dimension, length, generator rows over GF(9) coded
  a + 3b); `epsbig.c` (with `gf9.h`) computes the exact maximum Hermitian hull over all 2^(n-1) column sign patterns
  (column 0 fixed; usage `epsbig 0 0 < file.code`); `run_eps.sh list P cap out` runs it over a list of code files,
  P at a time, each capped. `epsbig_result.txt` is its output line for this code (E_11, deleted set of orbit 38 of
  4-subsets: coordinates 0, 3, 6, 11): maximum hull 5, reached by 4 sign patterns (`-` marks a column times w in the
  first maximizing pattern it found, which is the pattern the object uses: columns 1, 3, 5, 7, 10, 11, 12, 15, 17, 18,
  20, 22 of the length-24 code, 0-based), with the histogram of hull dimensions
  over all 2^23 patterns.
- `PREREG.md`: the frozen plan of the run folder that claimed this code. No null test: an
  explicit object checked by deterministic exact checkers against a table cell.
