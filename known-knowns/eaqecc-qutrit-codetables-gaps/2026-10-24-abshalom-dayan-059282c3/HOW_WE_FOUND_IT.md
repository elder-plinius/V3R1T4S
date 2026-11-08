# How we found it

contributor text, unverified

An [n, kappa, d]_9 code with Hermitian hull dimension h gives an [[n, kappa - h, d; n - kappa - h]]_3 code (Luo,
Ezerman, Grassl and Ling, arXiv:2207.05647, Prop. 1). codetables.de's [33,15,14]_9 is a Construction X code built
from two algebraic-geometry codes [28,15,11] > [28,12,14] of the Hermitian curve over GF(9), "based on 2 divisors of
degree [3, 5]" (Ding, Niederreiter and Xing 2000). Ours uses a place Q of degree 3 and the point at infinity. The qutrit table has its distance 14 only at the cells of Hermitian hulls 0, 1, 2.
With hull 6 it gives [[33,9,14;12]]_3, where the table lists 13-21.

An earlier run of this workspace asked which hulls such X codes can reach at all. The tail of an X code only touches
a 3 x 3 block of the Hermitian Gram matrix, so the hull of every X code of a pair C1 > C2 is bounded by ranks computed
from the head alone (a minimal-rank-completion bound), and the bound becomes exact once Hermitian forms are classified
by rank. An exhaustive pass over all 2^27 head sign patterns (column scalings of norm -1) of the pair
C(D_28, 3Q + 8P_inf) [28,15,11] > C(D_28, 2Q + 8P_inf) [28,12,14] gives an exact maximum hull of 6, reached only with
the head unscaled. Random tails at that pattern reached 6 on try 2511. The code has d = 14 exactly.

The run that claimed it rebuilt the object byte for byte from frozen parameters, re-tested its checkers on a known
positive and a seeded negative, and found d = 14 by two exact methods that agree (a GF(9) information-set test over
all 573,166,440 sets of 20 columns; a GF(3) position-subset rank test over all 573,166,440 sets of 13 positions, with
10404 = 10404 counts one step up), a Brouwer-Zimmermann computation, and weight-14 witnesses outside the isotropic part.

A proof without a computer search (goppa_x.py checks every hypothesis in a second):
1. span(S)^perp = phi(C) for C = span(G9) (rank and orthogonality checks), and phi turns Hamming weight into
   symplectic weight, so d_EA >= d(C).
2. The head of C (first 28 coordinates, the tail scalings undone) is exactly C_L(D_28, 3Q + 8P_inf) for one place Q of
   degree 3, and the words with zero tail have heads forming exactly C_L(D_28, 2Q + 8P_inf); the head map is
   injective; the tail code is an MDS [5,3,3] code.
3. Goppa bound with the generalized evaluation at P_inf: a nonzero f in L(aQ + bP_inf) with z affine zeros and
   leading coefficient 0 at P_inf (e = 1) lies in L(aQ + bP_inf - zeros - e P_inf), whose degree 3a + b - z - e must be
   >= 0. So weights are >= 28 - 17 = 11 and >= 28 - 14 = 14.
4. Construction X: a nonzero word with zero tail weighs >= 14; one with a nonzero tail has a nonzero head (>= 11) and
   a nonzero tail (>= 3). So d(C) >= 14, and a weight-14 word outside span(S) gives d_EA = 14.

What failed on the way: hull 7 for this pair (exact maximum 6, so [[33,8,14;11]] is out of reach for it), and, in the
same run, the punctured degree-3-place codes at n = 27 and the longer-tail X families at n = 34..36.
