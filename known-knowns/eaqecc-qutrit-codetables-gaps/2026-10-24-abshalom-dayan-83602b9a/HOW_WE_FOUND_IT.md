# How we found it

contributor text, unverified

The run targeted Grassl's qutrit EAQECC table. A first pass ranked the listed cells where the best known linear
code over GF(9) (codetables.de) has a larger distance than the cell's lower bound: there, what is missing is a code
of that distance with a large enough Hermitian hull, since an [n, kappa, d]_9 code with hull dimension l gives an
[[n, kappa - l, d; n - kappa - l]]_3 code (Luo, Ezerman, Grassl and Ling, arXiv:2207.05647, Prop. 1).

What failed: short lengths (n = 16 to 20). Exhaustive 1-generator 2-quasi-cyclic codes of length 16, one-point codes
on maximal elliptic curves, constacyclic codes of length 17 and the extended quadratic-residue code [20,10,10]_9 with
its shortenings and puncturings all stopped at hull 3 or 4 where hull 4 or 5 was needed, even after an exhaustive
search over column-norm sign patterns (which reaches every monomially equivalent code's hull).

What worked: codetables.de builds its best [23..28, 9..14]_9 codes from algebraic-geometry codes on the Hermitian
curve. The extended one-point codes E_m on y^3 + y = x^4 (the 27 affine points plus a coordinate for the point at
infinity) have the best known distance 28 - m for m = 6..16 and surprisingly large natural Hermitian hulls. E_13 is a
[28,11,15]_9 code with hull 6, giving [[28,5,15;11]]_3 where the table lists 13. Two exact checkers (a full
enumeration over GF(3) from the stabilizer matrix, a full enumeration over GF(9) from the classical code) agreed,
and the standalone checker in verify-it-yourself/ is a third, bit-sliced implementation.

The run that found the object was cut off before its panel. A follow-up run the same day rebuilt the object from its
construction (byte-identical sha256) and re-fetched the table once (unchanged page hash); its skeptic reports, written
in fresh contexts from a claim folder that held only the object, its checkers and the table record, are in panel/.
