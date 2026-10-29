# How we found it

contributor text, unverified

The family is the one behind this workspace's earlier qutrit codes: the extended one-point codes E_m on the
Hermitian curve y^3 + y = x^4 over GF(9) (the 27 affine points plus a coordinate for the point at infinity), which
reach the Goppa distance 28 - m. An [n, kappa, d]_9 code with Hermitian hull dimension l gives an
[[n, kappa - l, d; n - kappa - l]]_3 code (Luo, Ezerman, Grassl and Ling, arXiv:2207.05647, Prop. 1).

At length 28, E_11 to E_18 already sit at their maximum hull (unverified; an exhaustive search over all 2^27 column sign
patterns had shown that in earlier runs), so this run's constructor lens punctured instead. It deleted 1 to 3 coordinates of E_11 to E_16
(4 of E_11 to E_13, 5 of E_11 and E_12; one deletion set per orbit of the 216 automorphisms of the curve that fix the point at infinity) and computed the
exact maximum Hermitian hull of each punctured code over all 2^(n-1) column sign patterns (epsbig). It then scored
every hull value against the live table and the closure of every known code. E_13 with the three points of the line
x = 0 deleted is a [25,11,>=12]_9 code whose hull is 4 as built and 6 under one sign pattern (13 columns times w).
That gives [[25,5,12;8]]_3, where the table lists [[25,5,11-18;8]]_3.

The claim folder then rebuilt the object byte for byte and checked it with exact methods that agree: a GF(9)
information-set test on the code recovered from S (all 4,457,400 sets of 14 columns; 1204 deficient 13-sets), a
GF(3) position-subset rank test (all 4,457,400 sets of 11 positions; 1192 sets of 12 hold a vector outside the
isotropic part, and the other 12 weight-12 supports carry only hull words), a Brouwer-Zimmermann computation, and a
proof that searches no codewords (punct_check.py: the Goppa-type bound minus the three deleted points). A fresh-code
self-check (column dependences of the parity-check matrix over GF(9)) agreed. The claim then went to a
three-skeptic panel, one skeptic at a time.

What failed or was ruled out: puncturing at one or two points (n = 27, 26) gave hulls too small for any listed
cell; the other full-criterion hits of the sweep, at (24,4,10) and (23,4,9), are separate claims; the sweep's other
hits only match a listed d with fewer entangled pairs and were not pursued. The closure of every known code under
the table's propagation rules gives 11 at (25,5,8).
