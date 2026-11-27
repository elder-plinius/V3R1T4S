# Independent verification of the full certificate package

Place `check_alternate.py`, `finite_geometry.cpp` and `verify_scalar.py` beside the certificate manifest. On macOS or Linux with a C++17 compiler and Python 3.9 or later, run

```sh
c++ -O3 -std=c++17 -fPIC -shared finite_geometry.cpp -o finite_geometry.so
python3 -B check_alternate.py
```

From another directory use `python3 -B check_alternate.py PACKAGE LIBRARY`, where `PACKAGE` is the directory containing `MANIFEST.json` and `LIBRARY` is the path to the compiled shared library. The program prints the minimum strict surplus for each group of anchored models, the outcome of the scalar exclusions, and a final `PASS` or `FAIL`. It uses the Python standard library and the C++ standard library. It reads the nine plain certificate files used by the main checker.

## Coverage and inequalities

The verifier binds the eight-prime certificate to unrestricted exponents on the first eight odd primes. It derives the mixed representatives from their orbit signatures. Its traversal accepts the four basic column vertices under each triple, or descends through the mixed representatives, the two budget vertices for the distinguished column, the four fixed residues at seven, the possible ternary rows, and the seven residues at modulus fifteen for the class of modulus 165. A row is consumed only through this traversal. The checker rejects missing and unused rows. Each consumed row must have the exact stated reserve and total loss and strictly positive difference.

The anchored evaluator computes a finite set of multiplier atoms directly and integrates the rest by its mass and first moment. For the last phase it starts with the free stages, subtracts the exact improvement from retaining the class of modulus 165 at stage eleven on the explicit heights and eligible multipliers, and checks the resulting sum at the declared residue. The same residue is held fixed in both channels. The formulas apply to the supplied models with first-stage cap \(C_7=3/2\).

All 5,028 admissible exponent vectors at nine primes must fit verified nine-prime caps. The scalar part factors multipliers of the squarefree kernel and sums the hinge over the complete product distribution. It also evaluates the scalar expression at the actual exponents of every candidate of rank ten to thirteen. The maximal remaining vectors must agree exactly with the finite models whose anchored inequalities were verified. The program checks the fourteen-prime product and the proper-divisor completion sums. The prime replacement and tail comparison arguments are in the proof.

## The geometric integer computation

The seven free residues have moduli \(3,9,27,5,15,45,135\). Enumerate the quinary column of the modulus-5 residue and the ternary first-digit branches of the modulus-3 and modulus-15 residues. Within the selected branch enumerate the column of the modulus-15 residue. What remains is the allocation of four deeper residues to the surviving ternary depth-two bands.

In one such band the fixed offset must be constant on each quinary column of positive weight. There must be one ternary child whose weight is maximal simultaneously in all these columns. The implementation checks both conditions for each actual layout before reducing it. The modulus-9 residue acts on the band and the modulus-45 residue on one column. The modulus-27 and modulus-135 residues can share the common heaviest child whenever they act on this band. To see this, holding the wide residues fixed, changing the fine residue from one child to the heaviest weakly increases every column's nonnegative hinge increment. If both fine residues use the same column, convexity makes their joint increment at least the sum of their separate increments. Thus the heaviest child attains the maximum in both cases.

For each of the sixteen subsets of the four deeper residues the band table gives the best weighted hinge sum. The two column-specific choices of moduli 45 and 135 may be assigned to one column or to separate columns. The former possibility is explicitly enumerated. The sum of the largest separate gains can be used even if both maxima occur in one column, since in that case the enumerated joint gain dominates their sum. To join bands, maximize over all ways of partitioning the subset between them and add the two values. Join the two ternary first-digit branches the same way. The final maximum therefore uses each residue exactly once, with the same choice in every cell it affects.

A simultaneous permutation of the four quinary labels, independent permutations of depth-two bands within each ternary branch, and exchange of the two ternary branches preserve the maximum. The cache canonicalizes layouts only under these operations. The native kernel receives integer coefficients after exact clearing of denominators. The wrapper limits total integer cell weight to \(10^6\), every input coefficient in absolute value to \(10^8\), and all offset counts to four. Within these bounds every intermediate integer fits in signed 64 bits. A further per-query bound limits the maximum weighted positive load to \(2^{50}\). All outer sums use arbitrary-precision rational arithmetic.
