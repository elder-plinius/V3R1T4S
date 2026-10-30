# How we found it

contributor text, unverified

An [n, kappa, d]_9 code with Hermitian hull dimension l gives an [[n, kappa - l, d; n - kappa - l]]_3 code (Luo,
Ezerman, Grassl and Ling, arXiv:2207.05647, Prop. 1). An earlier search of the same workspace ranked the cells of the
qutrit table where codetables.de's best classical GF(9) code would beat the listed d_lower if it had a large enough
hull; [33,13,16]_9 with hull 5 at (33,8,15) was one of them. codetables.de builds its [33,13,16]_9 record (its
codetables.de page was last modified 2003-10-23; Ding, Niederreiter and Xing, "Some new codes from algebraic
curves", IEEE Trans. Inform. Theory 46(7) (2000) 2638-2642, https://doi.org/10.1109/18.887873) by Construction X from two
algebraic-geometry codes of the Hermitian curve with a divisor supported on a place of degree 3, [28,10,16] inside
[28,13,13], and a [5,3,3] tail.

We rebuilt those codes (GF(729) arithmetic for the 288 places of degree 3, which fall into two orbits under the
curve's automorphisms) and searched the free choices of a Construction X code, the tail's points, the 3 x 3 matrix
gluing the tail to C1/C2 and the column scalings of norm -1, with a random-restart greedy walk on the hull
dimension. One detail mattered: the subcode must drop the degree-3 place, not the point at infinity, or its 28th
coordinate dies and d falls to 15. Hull 5 turned up about once in 16,000 restarts; the code has d = 16 exactly. That
gives [[33,8,16;15]]_3, where the table lists d_lower = 15. The run that claimed it rebuilt it byte for byte and
checked it with two exact methods that agree (a GF(9) information-set test over all 1,037,158,320 sets of 18
columns, and a GF(3) position-subset rank test over all 1,037,158,320 sets of 15 positions, each with weight-16
witnesses outside the isotropic part) plus a Brouwer-Zimmermann distance computation, after re-testing the
widened checkers on a known positive and a seeded negative.

What failed: hull 6, which would give [[33,7,16;14]]_3 at the listed (33,7,14) (15-24), and it now fails
provably (unverified). The tail only touches a 3 x 3 block of the Hermitian Gram matrix, so the hull of every such code is bounded
by ranks computed from the head alone, and the bound becomes exact once Hermitian forms are classified by rank. An
exhaustive pass over all 2^27 head sign patterns of all eight pairs of this kind (both orbits of degree-3 places, the
four divisor classes C(aQ + bP_inf) > C((a-1)Q + bP_inf) of degrees 15 > 12), covering every tail of length 5 and
every gluing matrix, gives a maximum hull of exactly 5 for every pair (the random search had reached 5 for only one
of them). Hull 6 is impossible for this construction
(unverified: no proof of this is shipped).
