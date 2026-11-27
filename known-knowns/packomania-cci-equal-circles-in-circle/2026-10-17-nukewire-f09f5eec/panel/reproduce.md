# REPRODUCE skeptic verdict — claim package for N = 3307 (packomania-cci-equal-circles-in-circle, partial win p2)

## What I implemented (my own code, scratch under the system temp dir, written before running the author's)

Definition, quoted verbatim from the Success criterion in `CLAIM.md`:

> r\* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ), computed in mpmath at 50 digits directly
> from the submitted coordinates (no tolerance)

Method: parse the coordinate strings; use float64 + scipy cKDTree ONLY to screen a superset of the
argmin pairs (all pairs with float distance <= dmin_float\*(1+1e-6): 9711 pairs) and of the argmax
norms (norms >= nmax_float\*(1-1e-9): 4 points); every reported quantity is then exact mpmath
arithmetic at dps 62 on the coordinate strings (18-decimal inputs, so 50+ digits are unambiguous;
the 1e-6 relative screening slack dwarfs the ~1e-16 float64 error, so the true argmin/argmax are
provably inside the exactly-evaluated sets). Fully deterministic, no RNG. Non-isometry checked by
full 5,466,471-distance sorted multisets in float64 (both configs), which is decisive at the
observed magnitudes.

## Results (all from my own checker unless stated)

1. Object integrity — `candidate_N3307.txt`: exactly 3307 centres; every line exactly two
   18-decimal tokens; no duplicate points; pure LF, trailing newline; sha256 (as-is)
   f09f5eecbb7b14f10607e97c3a74829129931cc0e0285e4372a5b4c4f61b0194 == recorded in `CLAIM.md`.
   `radius.txt` sha256 6c60da0a2feb2ad01f2bed8dd99646021bcfd4cbfecb5ea2a7b332ecfa0beaad and
   `cci3307.txt` sha256 6f20614bebd12e279da00f83456f7dfee556b9199ebc8599d0cae3cd99e32ba7 both
   match `table_record.md`.

2. My independently computed r\* (dps 62, binding term = min-pair-distance/2):
   - min pair distance hp_min = 0.03263860020193628154195355854487379256082016098045068398
   - max norm hp_max        = 0.9836806998990318230328826811933853097599939328115454405
   - r\* = 0.0163193001009681407709767792724368962804100804902253419885095
   The headline value in `CLAIM.md` (0.016319300100968140770976779272437) is the correctly rounded
   32-significant-digit form of exactly this number (verified: rounding my value to 32 significant
   digits reproduces the claimed string character-for-character). Float64 cross-check:
   |float64 r\* − exact r\*| = 1.19e-18, consistent with the claim's "agrees to 1e-16".

3. Table value and margin: `radius.txt` contains exactly one row with first token 3307:
   0.016314899796158766989004378524 (== the string in `CLAIM.md`). My margin =
   r\* − table = 4.400304809373781972400748436896e-6 >= 1e-11 (claim says 4.400e-6; `REPRODUCE.md`
   says 0.0000044003048093737...: both consistent). Live re-check (my own fetch of the table,
   2026-10-17): row 3307 identical, and the whole live file is byte-identical to the packaged
   `radius.txt` (same sha256 as above).

4. Posted-configuration integrity — `cci3307.txt`: 3307 lines, three columns, indices sequential
   1..3307, 30-decimal coordinates. Its own string-exact r\* (same definition, dps 62) =
   0.01631489979615876698900437852318546948165396741875295332231362, which reproduces its own
   table row to −8.14530518e-31 (`table_record.md` says −8.15e-31 — correctly rounded quote).

5. Non-isometry: both configurations yield 5,466,471 = 3307·3306/2 pairwise distances; the sorted
   multisets are NOT equal; max elementwise difference 0.0218081794 (`table_record.md` says
   2.181e-2 — correctly rounded quote); already the smallest-distance slot differs
   (0.0326386002 vs 0.0326297996). The configurations are genuinely non-isometric.

6. Queue rule (live, my fetch of the pending-requests page, 2026-10-17): zero occurrences of "cci"
   and of "3307"; the 26-Sep-2026 category-unspecified "*many*" 4666-candidate bundle is still
   listed. Caveat (per the criterion, restated): that bundle cannot be resolved to a category, so
   N = 3307 must be re-checked against the live table once it disappears from the pending list.

7. Author's code, run only after my checker passed: `verify_standalone.py` (stdlib + Decimal
   prec 60) reproduces my r\* and margin digit-for-digit to all 61 printed significant digits and
   ends `PASS` (exit 0). No disagreement anywhere.

## Errata in the package's auxiliary numbers

None material. Two rounding notes: (a) the r\* headline in `CLAIM.md` is a 32-significant-digit
rounded quote, not the full 60-digit value — the full value continues ...4368962804... (harmless,
correctly rounded); (b) `table_record.md`'s −8.15e-31 and 2.181e-2 are likewise correctly rounded
quotes of −8.14530518e-31 and 0.0218081794. All hashes, counts, table strings, the margin and both
r\* values reproduce exactly.

context: zcode Agent-tool subagent, fresh context
pass: true
