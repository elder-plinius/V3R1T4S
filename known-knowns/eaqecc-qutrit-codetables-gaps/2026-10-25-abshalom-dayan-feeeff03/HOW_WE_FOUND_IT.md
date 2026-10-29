# How we found it

contributor text, unverified

The family is the one behind this workspace's earlier qutrit codes: the extended one-point codes E_m on the
Hermitian curve y^3 + y = x^4 over GF(9) (the 27 affine points plus a coordinate for the point at infinity), which
reach the Goppa distance 28 - m. An [n, kappa, d]_9 code with Hermitian hull dimension l gives an
[[n, kappa - l, d; n - kappa - l]]_3 code (Luo, Ezerman, Grassl and Ling, arXiv:2207.05647, Prop. 1).

At length 28, E_11 to E_18 already sit at their maximum hull (unverified; an exhaustive search over all 2^27 column sign
patterns had shown that in earlier runs), so the run's constructor lens punctured instead. It
deleted 1 to 3 coordinates of E_11 to E_16 (4 of E_11 to E_13, 5 of E_11 and E_12; one deletion set per orbit of the
216 automorphisms of the curve that fix the point at infinity) and computed the exact maximum Hermitian hull of each
punctured code over all 2^(n-1) column sign patterns (epsbig). It then scored every hull value against the live table
and the closure of every known code. E_11 with the four affine points (0,0), (1,2), (2,2), (3,6) deleted (orbit 38 of
the 4-subsets) is a [24,9,>=13]_9 code whose hull is 1 as built and 5 under 4 of the 2^23 sign patterns (12 columns
times w in the one used here). That gives [[24,4,13;10]]_3, where the table lists [[24,4,12-19;10]]_3.

The claim folder then rebuilt the object byte for byte and checked it with exact methods
that agree: a GF(9) information-set test on the code recovered from S (all 2,704,156 sets of 12 columns; 625 deficient
11-sets), a GF(3) position-subset rank test (all 2,704,156 sets of 12 positions; 625 sets of 13 hold a vector outside
the isotropic part), a Brouwer-Zimmermann computation, a proof that searches no codewords (punct_check.py: the
Goppa-type bound minus the four deleted points), and a full enumeration of all 3^18 - 1 vectors of span(S)^perp. A
fresh-code self-check (an enumeration of all 3^18 vectors with an isotropic-membership test for each low-weight
vector) agreed. The run ended before its panel finished; the supervising session then ran the three skeptics one at a
time (see `panel/gate.md`).

What failed or was ruled out: puncturing at one or two points (n = 27, 26) gave hulls too small for any listed
cell; the other full-criterion hits of the sweep, at (25,5,8) and (23,4,9), are separate claims (the first is draft PR
#739); the sweep's other hits only match a listed d with fewer entangled pairs and were not pursued. The closure of
every known code under the table's propagation rules gives 12 at (24,4,10).
