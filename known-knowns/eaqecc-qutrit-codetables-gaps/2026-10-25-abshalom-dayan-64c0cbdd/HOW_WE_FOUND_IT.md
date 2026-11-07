# How we found it

contributor text, unverified

The family is the one behind the earlier claims [[28,5,15;11]]_3
(https://github.com/elder-plinius/V3R1T4S/pull/643), [[28,7,14;11]]_3
(https://github.com/elder-plinius/V3R1T4S/pull/645), [[28,6,12;6]]_3
(https://github.com/elder-plinius/V3R1T4S/pull/646) and [[28,9,11;7]]_3
(https://github.com/elder-plinius/V3R1T4S/pull/651): the extended one-point codes E_m on the Hermitian curve y^3 + y = x^4 over GF(9) (the 27 affine
points plus a coordinate for the point at infinity), which reach the Goppa distance 28 - m. An [n, kappa, d]_9 code
with Hermitian hull dimension l gives an [[n, kappa - l, d; n - kappa - l]]_3 code (Luo, Ezerman, Grassl and Ling,
arXiv:2207.05647, Prop. 1).

E_15 is a [28,13,13]_9 code whose natural Hermitian hull (no column scaled) has dimension 6. That gives
[[28,7,13;9]]_3, where the table lists d_lower = 12 ("subcode of [[28,9,12;9]]"); in the same row the table reaches
13 only with 11 entangled pairs. An earlier run the same day found it while scanning the family against the table and
checked it by enumerating all 3^26 vectors of span(S)^perp (72288 words of weight 13). This run rebuilt it byte for
byte from frozen parameters and checked it with two exact methods that agree: a GF(9) information-set test on the
code recovered from S (all 30,421,755 sets of 16 columns) and a GF(3) position-subset rank test (all 30,421,755 sets
of 12 positions), with 9036 = 9036 counts one step up (and 72288 = 8 x 9036), each with a weight-13 witness outside
the isotropic part, after re-testing both on a known positive and on a seeded negative. A third route needs no
search at all (onepoint_check.py): span(S)^perp is exactly phi(E_15), and a function with at most 15 poles at
infinity has at most 15 zeros, so every nonzero word of E_15 has weight >= 13. The claim folder then went to a
three-skeptic panel, one skeptic at a time.

What failed: the closure of every known code under the table's propagation rules gives only 12 at this cell, and the
"using teleportation" cells cannot be used as sources (seeding them would push 2700 listed cells above their own
upper bounds).
