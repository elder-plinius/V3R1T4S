# How we found it

contributor text, unverified

An [n, kappa, d]_9 code with Hermitian hull dimension h gives an [[n, kappa - h, d; n - kappa - h]]_3 code (Luo,
Ezerman, Grassl and Ling, arXiv:2207.05647, Prop. 1). codetables.de's [33,14,15]_9 is a Construction X code built
from two algebraic-geometry codes [28,14,12] > [28,11,15] of the Hermitian curve over GF(9), "based on 2 divisors of
degree [3, 4]" (Ding, Niederreiter and Xing 2000). Ours uses a place Q of degree 3 and the point at infinity. The qutrit table has no entry beyond the parameters a [33,14,15]_9 with Hermitian hull 0, 1 or 2 would give (it does not name the codes). With
hull 7 it would give [[33,7,15;12]]_3, where the table lists 14-23.

An earlier run of this workspace, after the [[33,8,16;15]]_3 package from the same family, asked which hulls such X
codes can reach at all. The tail of an X code only touches a 3 x 3 block of the Hermitian Gram matrix, so the hull
of every X code of a pair C1 > C2 is bounded by ranks computed from the head alone (a minimal-rank-completion bound),
and the bound becomes exact once Hermitian forms are classified by rank. An exhaustive pass over all 2^27 head sign
patterns (column scalings of norm -1) of the pair C(D_28, 4Q + 4P_inf) [28,14,12] > C(D_28, 3Q + 4P_inf) [28,11,15]
gives an exact maximum hull of 7 (unverified), reached at one head pattern. Random tails at that pattern reached 7 on the fifth try.
The code has d = 15 exactly.

The run that panelled it rebuilt the object byte for byte from frozen parameters, re-tested its checkers on a known
positive and a seeded negative, and found d = 15 by two exact methods that agree (a GF(9) information-set test over
all 818,809,200 sets of 19 columns; a GF(3) position-subset rank test over all 818,809,200 sets of 14 positions, with
9946 = 9946 counts one step up), a Brouwer-Zimmermann computation, and weight-15 witnesses outside the isotropic part.

A proof without a computer search (goppa_x.py checks every hypothesis in a second):
1. span(S)^perp = phi(C) for C = span(G9) (rank and orthogonality checks), and phi turns Hamming weight into
   symplectic weight, so d_EA >= d(C).
2. The head of C (first 28 coordinates, column scalings undone) is exactly C_L(D_28, 4Q + 4P_inf) for one place Q of
   degree 3, and the words with zero tail have heads forming exactly C_L(D_28, 3Q + 4P_inf); the head map is
   injective; the tail code is an MDS [5,3,3] code.
3. Goppa bound with the generalized evaluation at P_inf: a nonzero f in L(aQ + bP_inf) with z affine zeros and
   leading coefficient 0 at P_inf (e = 1) lies in L(aQ + bP_inf - zeros - e P_inf), whose degree 3a + b - z - e must be
   >= 0. So weights are >= 28 - 16 = 12 and >= 28 - 13 = 15.
4. Construction X: a nonzero word with zero tail weighs >= 15; one with a nonzero tail has a nonzero head (>= 12) and
   a nonzero tail (>= 3). So d(C) >= 15, and a weight-15 word outside span(S) gives d_EA = 15.

What failed on the way (this run and the two before it): hull 6 for the [33,13,16]_9 pairs (exact maximum 5, unverified), hull 8
for this pair (exact maximum 7, unverified), the punctured degree-3-place codes at n = 27 (maximum hulls 4 and 5 where 7 and 8 were
needed), and longer-tail X families at n = 34..36 (no cell beaten).
