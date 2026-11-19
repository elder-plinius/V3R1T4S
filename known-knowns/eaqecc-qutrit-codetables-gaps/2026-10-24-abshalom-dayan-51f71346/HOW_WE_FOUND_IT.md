# How we found it

contributor text, unverified

The family is the one behind this workspace's earlier [[28,5,15;11]]_3 and [[28,7,14;11]]_3: the extended one-point
codes E_m on the Hermitian curve y^3 + y = x^4 over GF(9) (the 27 affine points plus a coordinate for the point at
infinity), which reach the Goppa distance 28 - m. An [n, kappa, d]_9 code with Hermitian hull dimension l gives an
[[n, kappa - l, d; n - kappa - l]]_3 code (Luo, Ezerman, Grassl and Ling, arXiv:2207.05647, Prop. 1).

E_16 is a [28,14,12]_9 code whose Hermitian hull has dimension 8, the maximum over all 2^27 column sign patterns.
That gives [[28,6,12;6]]_3, where the table lists d_lower = 11. An earlier run the same day found it while scanning
the family against the table and kept it as a panel-ready candidate. This run rebuilt it byte for byte and wrote a
new exact checker: a GF(9) information-set test on the code recovered from S, which checks every one of the
21,474,180 sets of 17 columns. That checker was tested against brute force on 450 random cases, on a known positive
and on seeded negatives. It agrees with the earlier position-subset rank test over GF(3) and with an earlier
Brouwer-Zimmermann run.

What failed, looking for d = 13 at the same cell: a local search started from E_16 (column replacements scored
exactly by the number of weight-12 supports) never improved on the start in three seeds. Column scalings cannot
help: the weight-12 words span the whole code, so they never fit inside a hull of dimension 8. Extended
Construction X codes of lengths 29 to 36, scanned exhaustively against the table, reached no listed cell beyond what
was already known.
