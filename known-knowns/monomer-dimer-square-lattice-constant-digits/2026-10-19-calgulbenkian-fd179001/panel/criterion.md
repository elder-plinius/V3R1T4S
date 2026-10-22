# Criterion report, md-p1-enclosure-13

context: Claude Code subagent, fresh context [Claude Sonnet 5.5]

Role: criterion. I read only the package. I fetched nothing for this cell.

## What the partial win p1 says, clause by clause

1. "rigorous enclosure": MET. I re-derived object/PROOF.md step by step. Theorem U (h2 <= ln beta(M)/M, M even >= 4) follows from beta(m)^M <= Tr P_m^M = Tr P_M^m <= 2^M beta(M)^m and ln beta(m)/m -> h. Theorem L (p h2 >= ln beta(p+2q) - ln beta(2q)) follows from Tr B^{p+2q} <= rho^p Tr B^{2q} for symmetric B, the torus identity, and the same limit. The torus identity needs both cycle lengths >= 3: here 22 and 24, fine. U needs M even: M = 22. L needs q >= 2, p >= 1: 2q = 22, p = 2. The use of Collatz-Wielandt for a symmetric nonnegative matrix with an integer positive vector is correct. The dihedral-orbit shortcut is sound because P_m[s,t] depends only on s union t and on s and t being disjoint, so the matrix commutes with rotations and reflection and an invariant x gives an invariant y.
2. "at least 12 decimals": MET. The two bounds share 13 decimals (0.6627989728337) by truncation and by rounding.
3. "improving Friedland-Peled's 8 certified decimals": MET against the quoted comparator (8 decimals). Whether a better certified value exists elsewhere is the novelty skeptic's question.
4. "making Kong's bracket rigorous or not": MET in the "or not" sense. The enclosure lies strictly inside Kong's bracket and supersedes it; the claim does not prove Kong's ends, and says so.
5. "Friedland-Peled transfer-matrix inequalities evaluated in exact or interval arithmetic": MET. Ratios are exact integer fractions; logarithms are 70-digit Decimal with an outward margin of 1e-55, far above the rounding error. The inequalities are the two periodic-cylinder inequalities, derived from the definitions and stated to agree with the Friedland-Peled forms.
6. "with published certificate vectors": MET. Five parts, hashes in object/MANIFEST.txt, all hashes in the contributor's hash list verified.

## My own checks

- Own small test (a small script of mine, not shipped in this package): built P_m from the definition for m = 4 to 12 with numpy; every upper bound ln beta(M)/M (M = 4,6,...,12) is above 0.6627989728337 and every lower bound (ln beta(2q+p) - ln beta(2q))/p tested (2q = 4,6,8,10; p = 1,2) is below it. This is a consistency check of the theorems, not of the width 22 and 24 result.
- I ran the shipped check_p1.py on a copy of object/ and the checker, with python -I. Output: hashes verified; m=22 96909 orbits, m=24 352698 orbits; min and max ratios as in RECEIPTS.md; ENCLOSURE 0.6627989728337138109756 <= h2 <= 0.6627989728337490653104; 13 common decimals; CERTIFIED. This is a rerun of the author's checker, not an independent matrix build at m = 22 and 24; the independent reproduction is the reproduce skeptic's role.

## Hidden quantifiers and stretched definitions

- Widths 22 and 24 were chosen after wider intervals were seen. Every bound is proved separately, so this cannot affect validity. Disclosed.
- The 13 decimals are for the pair of bounds (a rigorous interval), not a point estimate. The claim states this. Nothing is claimed for the main criterion.
- Validity rests on the checker and on Python integer arithmetic. The fast sweep is tested against the definition only for m = 3 to 8; for 22 and 24 no independent matrix is built. This is a disclosed limit, not a violation of any p1 clause.
- Null model: if the vectors were arbitrary, the ratios would not agree to 1e-15 relative width; the tight ratio spread is itself strong evidence they approximate the Perron vector.

confirmed_scope: For the monomer-dimer entropy h2 of the square lattice (natural log, per site), the shipped certificate vectors for the cylinder transfer matrices of circumference 22 and 24 give, through exact integer Collatz-Wielandt ratios and the two proved inequalities, the rigorous enclosure 0.6627989728337138109756 <= h2 <= 0.6627989728337490653104, certifying 13 decimals; nothing wider is confirmed (no claim on the main criterion, none on novelty beyond the two quoted comparators).
pass: true
