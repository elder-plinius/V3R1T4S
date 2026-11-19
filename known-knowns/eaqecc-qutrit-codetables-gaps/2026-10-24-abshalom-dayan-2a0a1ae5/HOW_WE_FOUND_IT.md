# How we found it

contributor text, unverified

The family is the one behind this workspace's earlier [[28,5,15;11]]_3, [[28,7,14;11]]_3 and [[28,6,12;6]]_3: the
extended one-point codes E_m on the Hermitian curve y^3 + y = x^4 over GF(9) (the 27 affine points plus a coordinate
for the point at infinity), which reach the Goppa distance 28 - m. An [n, kappa, d]_9 code with Hermitian hull
dimension l gives an [[n, kappa - l, d; n - kappa - l]]_3 code (Luo, Ezerman, Grassl and Ling, arXiv:2207.05647,
Prop. 1).

E_17 is a [28,15,11]_9 code whose natural Hermitian hull has dimension 6, the maximum over all 2^27 column sign
patterns. That gives [[28,9,11;7]]_3, where the table lists d_lower = 10. An earlier run the same day found it while
scanning the family against the table and kept it as a panel-ready candidate. This run rebuilt it byte for byte and
checked it with two exact methods that agree: a GF(9) information-set test on the code recovered from S (all
13,123,110 sets of 18 columns) and a GF(3) position-subset rank test (all 13,123,110 sets of 10 positions), each with
a weight-11 witness outside the isotropic part, after re-testing both on a known positive and on seeded negatives.

What failed, looking for d = 12 at the same cell: a local search started from E_17 (column replacements scored
exactly by the number of weight-11 supports) never improved on the start in three seeds. Column scalings cannot
help: the weight-11 words span the whole code, so they never fit inside a hull of dimension 6. A [28,15,12]_9 code
would itself be a new classical record (codetables.de lists 11-12).
