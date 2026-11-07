# How we found it

contributor text, unverified

An [n, kappa, d]_9 code with Hermitian hull dimension h gives an [[n, kappa - h, d; n - kappa - h]]_3 code (Luo,
Ezerman, Grassl and Ling, arXiv:2207.05647, Prop. 1). codetables.de lists [35,14]_9 at d = 16 (a shortened, punctured
code of Xing and Ling, 2000). Ours is a different [35,14,16]_9 code: a Construction X code built from two
algebraic-geometry codes of the Hermitian curve y^3 + y = x^4 over GF(9), C(D_28, 2Q + 8P_inf) [28,14,12] >
C(D_28, Q + 8P_inf) [28,10,16], where Q is a place of degree 4 and D_28 is the 27 affine points plus P_inf, glued to
a [7,4,4] Reed-Solomon tail. With Hermitian hull 7 it gives [[35,7,16;14]]_3, where the qutrit table lists 15-26; the
table has d = 16 at (35,7) only with 15 entangled pairs.

Earlier runs of this workspace scored every Construction X family of Hermitian-curve AG codes against the live
table under the table's own propagation rules. For the degree-4 places, every pair aQ + (16 - 4a)P_inf >
(a - 1)Q + (16 - 4a)P_inf (a = 1..6, four orbits of the 1512 degree-4 places) is exactly [28,14,12] > [28,10,16]
(Brouwer-Zimmermann), so every X code with a [7,4,4] tail is a [35,14,16]_9 code, and it beats a listed cell beyond
everything known only with hull >= 7. The tail of an X code only touches a 4 x 4 block of the Hermitian Gram matrix,
so the hull of every X code of a pair is bounded by ranks computed from the head alone (a minimal-rank-completion
bound), and the bound becomes exact once Hermitian forms are classified by rank. An exhaustive pass over all 2^27 head
sign patterns (column scalings of norm -1) of the 24 pairs gave: a = 2 and a = 6 reach exactly 7 in every orbit,
the other a at most 6 with Reed-Solomon tails, and no pair reaches 8 with any tail. Random GRS tails at the hull-7 head pattern of place 0,
a = 2 reached true hull 7 on try 11535. The code has d = 16 exactly.

The run that claimed it rebuilt the object byte for byte from frozen parameters, re-tested its checkers on a known
positive and a seeded negative, and found d = 16 by exact methods that agree (a GF(9) information-set test over all
3,247,943,160 sets of 20 columns; a GF(3) position-subset rank test over all 3,247,943,160 sets of 15 positions, with
7762 = 7762 counts one step up), a Brouwer-Zimmermann computation, and weight-16 witnesses outside the isotropic part.

A proof without a computer search (goppa_x4.py checks every hypothesis in a few seconds):
1. span(S)^perp = phi(C) for C = span(G9) (rank and orthogonality checks), and phi turns Hamming weight into
   symplectic weight, so d_EA >= d(C).
2. The head of C (first 28 coordinates, the scalings undone) is exactly C_L(D_28, 2Q + 8P_inf) for one place Q of
   degree 4, and the words with zero tail have heads forming exactly C_L(D_28, Q + 8P_inf); the head map is injective;
   the tail code is an MDS [7,4,4] code.
3. Goppa bound: a nonzero function in L(G) vanishes on at most deg G of the 28 points, so the weights are
   >= 28 - 16 = 12 and >= 28 - 12 = 16.
4. Construction X: a nonzero word with zero tail weighs >= 16; one with a nonzero tail has a nonzero head (>= 12) and
   a nonzero tail (>= 4). So d(C) >= 16, and a weight-16 word outside span(S) gives d_EA = 16.

What failed on the way: hull 8 for these pairs (exact maximum 7, so [[35,6,16;13]] is out of reach for this family),
d = 17 (the X bound min(16, 12 + 4) is attained: 7762 sets of 19 columns are not information sets), and every other
X family scored so far (degree-3, -5, -6, -7 and -8 divisors, tails of length 3 to 8, heads on 27 or 28 points): none
beats a listed cell beyond everything known except the degree-3 n = 33 and degree-4 n = 35 families already used.
