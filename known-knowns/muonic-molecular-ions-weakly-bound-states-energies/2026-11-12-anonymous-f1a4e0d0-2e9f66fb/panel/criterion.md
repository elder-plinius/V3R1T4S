# Criterion skeptic report: muonic-molecular-ions-weakly-bound-states-energies, partial win p1, cell ttmu (2,0)

context: subagent (fresh context, saw only claim/)

## What is claimed, and against which rule

The claim is for the enumerated partial win p1 only (not full success, not p2), one cell: ttmu (2,0).
p1 verbatim: "A (2,0) cell: for dd-mu, dt-mu or tt-mu, with the same masses, L = 2, natural parity (exchange-symmetric
spatial part for dd-mu and tt-mu), the lowest root of that block certified STRICTLY LOWER than Frolov's Table I value
(-0.4887083249914, -0.500118077325475 or -0.5125686450010) by at least 1e-13."

## Literal check, clause by clause

1. Named cell. tt-mu is one of the three cells p1 enumerates. Met.
2. "the same masses" = eq. (14). I extracted the PDF text in claim/source/: eq. (14) reads
   "Mt = 5496.92153573 me, mmu = 206.7682830 me, Md = 3670.48296788 me". cert/basis.txt has
   "masses 5496.92153573/206.7682830 5496.92153573/206.7682830 1"; the checker turns each into an arb ball of the
   exact decimal quotient (inverse mass = arb(den)/arb(num)). Charges "1 1 -1". The Hamiltonian in the checker
   docstring is eq. (2) of the PDF (muon-atomic units, muon mass 1), centre of mass removed through x = r1 - r3,
   y = r2 - r3 with w1 = 1/M1 + 1/M3, w2 = 1/M2 + 1/M3, w3 = 1/M3. Met.
3. L = 2, natural parity. Every basis function is a symmetric traceless rank-2 Cartesian tensor built from the two
   polar vectors x and y (types xx, xy, yy, (x-y)(x-y)) times a scalar exponential. Symmetric traceless rank 2 is pure
   L = 2; an even number of polar vectors gives parity +1 = (-1)^2. Met. (Basis content: 240 of type 3, 120 of type 1,
   120 of type 0, all exponents real, smallest pairwise exponent sum 0.68 > 0, so every function is square integrable.)
4. Exchange-symmetric spatial part. "sym 1": each function is phi + P12 phi; the checker's exchange map (a <-> b,
   type 0 <-> 2, types 1 and 3 fixed, sign +1) is the correct action of swapping the two nuclei for L = 2. The checker
   evaluates <phi_i| O (1 + P12) |phi_j>, which equals half of <(1+P12)phi_i| O |(1+P12)phi_j> for both O = 1 and O = H
   because the two nuclear masses are identical; the common factor cancels in the quotient. Met.
5. Comparison value. Table I of the PDF, column "tt-mu ion; (2,0)-state", last row N = 3800: -0.5125686450010. This is
   the number p1 lists for tt-mu and the number passed as --bar. Met.
6. "the lowest root of that block certified STRICTLY LOWER ... by at least 1e-13". The checker does not enclose the
   lowest root of the 480 x 480 generalized eigenproblem two-sidedly. It encloses the Rayleigh quotient of the explicit
   vector in cert/vector.txt. Because the overlap form is positive on this vector (asserted in ball arithmetic,
   Sm > 0), the lowest root of the block is <= that quotient, so the lowest root is certified to lie below
   bar - 1e-13 whenever the upper end of the quotient does. For a "direction: min, strictly lower" clause an upper
   bound is exactly what has to be certified, so I read the clause as literally met. I record that the bank's
   verification method speaks of certifying the root "with an error ball"; no two-sided ball for the root is supplied,
   and the claim sentence correctly does not assert one.
   Margin: bar - upper end = 2.9689e-9, about 3e4 times the required 1e-13. Met.

## Is the checker ball arithmetic end to end?

Read check_cert.py in full.
- Inputs (masses, exponents, coefficients) enter as arb(decimal string): rigorous enclosures. A ball-valued
  coefficient vector is harmless: every vector inside the balls is a valid trial function.
- Matrix-element coefficient polynomials are derived symbolically (sympy, exact rationals), scaled by one common
  integer so only integer coefficients are lambdified with an empty module namespace; they are then evaluated on arb.
  My scan of the generated source found no "." or "/" (weak check, but the exact tests below would expose a float).
- Radial integrals: finite closed-form sums with integer coefficients over arb powers of 1/(A+B), 1/(A+C), 1/(B+C).
- Worker-to-parent transfer goes through decimal strings of midpoint and radius; I tested that
  arb(str(x.mid()), str(x.rad())) contains x (True): the string of the midpoint carries its own rounding radius and the
  radius string is rounded outward.
- Final test is arb "E < bar - margin", which is true only if certain for the whole ball; exit status 0 only then.
I found no floating-point step between the certificate files and the verdict.

## Rerun (2 processes, about 68 s wall, 133 s CPU)

    basis ../claim/cert/basis.txt L 2 N 480 sym 1 masses 5496.92153573/206.7682830 5496.92153573/206.7682830 1 complex False prec 320
    Rayleigh quotient (upper bound on the lowest root of the block)
    enclosure: [-0.51256864796989822024343949062712751210532790167646 +/- 1.86e-51]
    upper end (rounded to 45 digits): -0.512568647969898220243439490627127512105327902
    bar -0.5125686450010 margin 1e-13 bar - upper end = [2.9688982202434394906e-9 +/- 2.72e-29]
    CERTIFIED: upper end < bar - margin
    exit=0

Identical to expected_output.txt apart from the path, and identical to the digits quoted in CLAIM.md.

## Is the checker's Hamiltonian right? (the real risk: a wrong H would give a meaningless "bound")

A 480-function result beating an N = 3800 table entry is the kind of thing a checker bug produces, so I tested the
checker's matrix elements against cases with exactly known answers, using its own Basis.element on single functions
that are exact eigenfunctions of separable variants of the same Hamiltonian (panel_work_criterion/exact2.py,
quick.py):

    A (type 3, tests w1,w2,w3 cross term and R dependence): checker [-0.06211111111111111111111111 +/- 1.12e-27] exact [-0.06211111111111111111111111 +/- 1.12e-27] contains: True
    B (type 1): checker [-0.07600000000000000000000000 +/- 1e-30] exact [-0.07600000000000000000000000 +/- 3e-30] contains: True
    C (type 3 mirrored): checker [-0.06211111111111111111111111 +/- 1.12e-27] exact [-0.06211111111111111111111111 +/- 1.12e-27] contains: True
    5. hydrogenic 3d test type 0 checker [-0.006555555555555555555555556 +/- 4.45e-28] exact -0.006555555555555551
    5. hydrogenic 3d test type 2 checker [-0.006555555555555555555555556 +/- 4.45e-28] exact -0.006555555555555551

(A: particle 1 fixed, particle 2 of mass 2 in a 3d state in R = |r1 - r2| with exponent 2/3, neutral particle 3 of
mass 5 with exp(-0.7 X): E = -2/18 + 0.49/10. This exercises the mixed grad_x.grad_y term, all three w's and the R
dependence. B: 2p x p-wave coupled to L = 2, E = -1/8 + 0.49/10. Test 5: hydrogen 3d plus a free factor,
E = -1/18 + 0.49/10.) All four tensor types are covered and all agree to about 27 digits.

Hermiticity of the operator-form elements on actual certificate pairs (H applied to the ket, so symmetry is not
built in):

    4. pair (0, 1) types 3 3 hermiticity |H_ij - H_ji| / |H_ij| = 4.2e-95  S asym 0.0
    4. pair (5, 40) types 3 3 hermiticity |H_ij - H_ji| / |H_ij| = 3.7e-96  S asym 0.0
    4. pair (17, 300) types 3 1 hermiticity |H_ij - H_ji| / |H_ij| = 1.9e-91  S asym 0.0
    4. pair (100, 479) types 3 0 hermiticity |H_ij - H_ji| / |H_ij| = 1.2e-94  S asym 0.0

Not done: I started a fully independent gradient-form numerical quadrature of H/S for generic certificate pairs but
stopped it for time before it produced output, so there is no result from it. I did not write an independent full
480 x 480 recomputation.

Plausibility of beating the table. Table I's tt-mu (2,0) column is visibly unconverged: -0.5125686421485 (N = 3400),
-0.5125686439316 (3600), -0.5125686446090 (3700), -0.5125686450010 (3800); the last step is still 3.9e-10. A value
3.0e-9 lower is consistent with that trend and does not contradict the variational principle. Physical sanity: with
the t-mu(1s) threshold -0.48187416483 m.a.u. and the paper's factor 5626.451612133 eV per m.a.u. the certificate gives
a binding energy of 172.701024 eV against 172.701007 eV from the table value, the right level and a tiny shift.

## Hidden quantifiers, stretched definitions, overstatement

- The claim sentence says only that the explicit trial function's Rayleigh quotient has a ball-arithmetic upper end
  below the table value by more than 1e-13. It does not claim the exact energy, convergence, a lower bound, a
  two-sided root enclosure, or anything about dd-mu, dt-mu or the (1,1) states. I find no overstatement.
- "by more than 1e-13" is true and understated (the gap is 2.97e-9).
- The clause "lower than any other published variational value for the identical masses" belongs to the full success
  criterion, not to p1, so it is not required here; the scout record reports none found, and I did not verify that
  search (outside my lane and outside what I may read).
- "Certified" rests on the author's checker. Its correctness is supported here by exact-eigenfunction tests and
  hermiticity, not by a second full implementation.

## Null model and subsumption

I agree no null model is needed: the claim is a deterministic inequality about one explicit object, not a statistical
or search-rate statement, so there is no chance baseline to beat. The claim is not subsumed by anything trivial: the
bar is the best row of the source table, the basis is not derivable from the paper (which releases no wavefunctions),
and the exact-test results show the bound is not an artefact of the kinetic or potential normalisation. It is one
cell of p1; it is not full success and says nothing toward p2.

confirmed_scope: For the tt-mu Coulomb three-body Hamiltonian of arXiv:2503.17389 eq. (2) with the eq. (14) masses in muon-atomic units, the explicit 480-function L = 2, natural-parity, nuclear-exchange-symmetric trial function in cert/ has a Rayleigh quotient enclosed by the supplied 320-bit ball-arithmetic checker in [-0.51256864796989822024343949062712751210532790167646 +/- 1.86e-51], which upper-bounds the lowest root of that block and lies 2.9689e-9 below the Table I (2,0) value -0.5125686450010, exceeding the 1e-13 margin of partial win p1 for this one cell only.

pass: true
