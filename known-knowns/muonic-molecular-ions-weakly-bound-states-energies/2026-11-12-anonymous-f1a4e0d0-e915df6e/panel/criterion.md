# Criterion skeptic

context: subagent (fresh context, saw only claim/)

Claimed: partial win p1, one cell, ddmu (2,0). Not claimed: the full criterion (a (1,1) state), p2, or the dtmu/ttmu cells.

## 1. What p1 literally requires, item by item

p1 (verbatim in CLAIM.md): "A (2,0) cell: for dd-mu, dt-mu or tt-mu, with the same masses, L = 2, natural parity
(exchange-symmetric spatial part for dd-mu and tt-mu), the lowest root of that block certified STRICTLY LOWER than
Frolov's Table I value (-0.4887083249914, ...) by at least 1e-13."

| requirement | evidence | verdict |
|---|---|---|
| system dd-mu, charges (+1,+1,-1) | cert/basis.txt header `charges 1 1 -1`, two equal heavy masses, third mass 1 | met |
| "the same masses" = eq. (14) | PDF text eq. (14): Md = 3670.48296788 me, m_mu = 206.7682830 me. Header: `masses 3670.48296788/206.7682830 3670.48296788/206.7682830 1`. The checker parses `n/d` as arb(d)/arb(n) for the inverse mass, i.e. the exact decimal quotient enclosed in a 320-bit ball; no rounded ratio is used | met |
| muon-atomic units, centre of mass removed, eq. (2) Hamiltonian | PDF eq. (2): H = -(1/2X) Lap_1 - (1/2Y) Lap_2 - (1/2) Lap_3 - 1/r32 - 1/r31 + 1/r21. Checker: T = -(1/2)[w1 Lap_x + w2 Lap_y + 2 w3 grad_x.grad_y] with w1 = 1/M1 + 1/M3, w2 = 1/M2 + 1/M3, w3 = 1/M3 in x = r1 - r3, y = r2 - r3, which is the standard exact reduction of eq. (2) with total momentum zero; potentials q_i q_j / r_ij | met |
| L = 2 | every function is a symmetric traceless rank-2 Cartesian tensor in (x, y) times a scalar function of (X, Y, R); such a tensor is a pure L = 2 object. Summing matrix elements over the tensor components is a sum over the multiplet, which leaves the Rayleigh quotient of each M component unchanged because H is rotation invariant | met |
| natural parity (-1)^L = +1 | rank-2 tensors bilinear in x, y are even under inversion | met |
| exchange-symmetric spatial part | header `sym 1`; function = phi + P12 phi; the checker's exch() maps type 0 <-> 2, a <-> b, sign +1 for L = 2, which is exactly x <-> y. M1 = M2 as strings, so P12 commutes with H and the half-symmetrised element used by the checker is legitimate | met |
| comparison value is the right Table I entry | PDF Table I, ddmu (2,0) column, last row N = 3700: -0.4887083249914. Same number in p1 and in --bar | met |
| "lowest root of that block certified strictly lower ... by at least 1e-13" | see section 2 | met, in the upper-bound sense |

## 2. Is a Rayleigh-quotient upper bound a certification of "the lowest root"?

For any nonzero v, v.Hv / v.Sv >= lambda_min(H, S) of the 480-function generalized eigenproblem (S is positive definite
on a linearly independent set; the checker asserts v.Sv > 0 as a ball). So an upper end U of a rigorous enclosure of the
Rayleigh quotient gives lambda_min <= U. With U < bar - 1e-13 the statement "the lowest root of that block is strictly
lower than the table value by at least 1e-13" is literally proved. What is NOT provided is a two-sided error ball for
lambda_min itself (the bank's verification method says "certify the required root ... with an error ball"). For a
direction-min criterion on the lowest root, a one-sided certified upper bound is logically sufficient; I accept it, but
the confirmed scope must say "upper bound", not "the root equals".

No hidden quantifier found: the claim is about one explicit vector in one explicit basis, with one explicit mass set.
The claim does not assert that the value is the true energy, that it is converged, or that it beats other literature
(the "lower than any other published value" clause belongs to the full criterion, not to p1; I did not and could not
check literature from inside claim/, and I confirm nothing about it).

## 3. Is the checker ball arithmetic end to end?

Read check_cert.py in full.

- Inputs: exponents, masses and coefficients are parsed from decimal strings by arb(...), which encloses the decimal.
  (The coefficient vector needs no rigour at all: any vector is admissible.)
- Polynomial coefficients of the integrand are derived symbolically by sympy with exact rationals, then multiplied by a
  common integer so they are integer polynomials in arb arguments. I inspected the generated lambdify source of all 32
  functions: 0 division signs and no float literals, so no Python float enters.
- Radial integrals: closed-form finite sums with integer coefficients (math.comb, factorials) times powers of
  1/(A+B), 1/(A+C), 1/(B+C) in arb; the integrability condition is asserted as a ball inequality. All 480 rows have
  strictly positive a, b, c and zero imaginary parts (awk scan: im 0, bad 0, neg 0; types: 3 x 240, 0 x 120, 1 x 120).
- Worker results are passed between processes as str(mid), str(rad). I tested this transport: the rebuilt ball
  contains the original (the decimal rounding of the midpoint comes back as an extra radius). Rigorous.
- Final comparison `E < thr` is an arb ball comparison (true only if certain); exit status follows it.

One assumption the checker makes without testing it: it computes only j <= i and doubles, i.e. it assumes the
operator-form matrix is symmetric. I tested that (below).

## 4. Rerun (2 processes, new folder panel_work_criterion/)

    python ../claim/check_cert.py ../claim/cert/basis.txt ../claim/cert/vector.txt --bar -0.4887083249914 --margin 1e-13 --procs 2

    basis ../claim/cert/basis.txt L 2 N 480 sym 1 masses 3670.48296788/206.7682830 3670.48296788/206.7682830 1 complex False prec 320
    Rayleigh quotient (upper bound on the lowest root of the block)
    enclosure: [-0.48870832506160774125251078147287715439325858526224 +/- 1.06e-51]
    upper end: -0.488708325061607741252510781472877154393258585
    bar -0.4887083249914 margin 1e-13 bar - upper end = [7.0207741252510781473e-11 +/- 1.24e-31]
    CERTIFIED: upper end < bar - margin
    141.12s user 1.17s system 194% cpu 1:13.12 total
    exit=0

Identical to expected_output.txt apart from the path prefix. The margin achieved is 7.02e-11, about 700 times the
required 1e-13.

## 5. My own tests of the checker's matrix elements (panel_work_criterion/tests.py)

A wrong Hamiltonian formula would make a perfectly rigorous enclosure of the wrong number, so I tested the L = 2
formulas the checker derives, by means that do not depend on the certificate:

    test1 division signs in generated code: 0
    test2 ... roundtrip contains original: True
    test3 3d x 1s energy: [-0.555555555555555555555555555556 +/- 4.45e-31]  exact -5/9
    test3b: [-0.555555555555555555555555555556 +/- 4.45e-31]
    test4 Hermiticity all 16 type pairs: balls overlap; worst rel diff upper [2.0301e-91 +/- 3.38e-96]
    test5 relabel 1<->3 invariance (9 type pairs, unequal masses): True
    test5b type1 relabel: True [2.1153692633038215474 +/- 2.07e-20] [2.1153692633038215474 +/- 2.07e-20]
    test6 He 1D (L=2, sym) lowest two roots, 60 random functions: -2.05559746317 -2.03101701888  exact 3^1D = -2.05562073285, 4^1D = -2.03127984; bound respected: True

- test3: exact eigenfunction (hydrogenic 3d in x times 1s in y, fixed centre, no 1-2 interaction) reproduces -5/9
  exactly, for tensor types 0 and 2.
- test4: operator-form H is symmetric for all 16 type pairs with the real ddmu masses and c != 0 (this is the
  assumption behind the lower-triangle sum).
- test5: the same physical matrix element computed with particle 1 instead of particle 3 as the reference particle
  (masses 7/2, 11/3, 1, unequal on purpose) agrees ball for ball. This exercises the mass-polarisation term w3 and the
  mapping between tensor types 0, 1, 2, 3, which test3 does not.
- test6: with the checker's own symmetrised L = 2 elements, 60 random functions for infinite-mass helium give a
  lowest root 2.3e-5 ABOVE the 3 1D level and a second root above the 4 1D level, as a variational method must. (The
  two reference energies are quoted from my memory, not from a file in claim/; treat that test as supporting only.)

I found no defect. I did not write a fully independent second implementation of the 480 x 480 calculation.

## 6. Plausibility, subsumption, overstatement, null model

- Plausibility that 480 functions beat a 3700-function table entry: the ddmu (2,0) column of Table I is visibly
  unconverged (last steps -9.2e-11 for 200 functions, then -3.1e-11 for 100 functions), so a true level some 1e-10
  below the last row is consistent with the table itself. Nothing here shows the result is too low to be variational.
- Subsumed by something trivial? No. It is not a restatement of the table, not an extrapolation, and not a
  different-mass or different-symmetry number: it is an explicit, re-checkable function in the named block. Whether
  some other publication at identical masses already has a lower value is outside what I can see and outside p1.
- Overstatement: the one-sentence claim says only that the Rayleigh quotient's upper end is the printed number and
  that it is below the table value by more than 1e-13. That is no wider than the evidence. The sentence in "The
  object" that the lowest root "is itself an upper bound on the lowest L = 2 ... level" is the standard variational
  principle and is correct. CLAIM.md does not call the number the energy of the state; it must not be reported as such.
- Deviation from the bank's verification method (noted, not disqualifying): no eigenproblem is solved and no two-sided
  ball for the root is given; the basis is Cartesian-tensor rather than bipolar-harmonic (equivalent L = 2 natural
  parity space; the bank's "e.g." allows it); precision 320 bits is about 96 digits, above the 40 required; the eV
  consistency check with the factor 5626.451612133 is not in the package (it is a sanity step, not part of p1).
- Null model: I agree none is needed. The claim is a deterministic inequality about one explicit object; there is no
  sampling, no selection among random outcomes, and nothing for a null distribution to explain.

## Verdict

p1, cell ddmu (2,0), is met literally in the one-sided (upper bound) sense, with margin 7.02e-11 against a required 1e-13.

confirmed_scope: For dd-mu with charges (+1, +1, -1) and exactly the eq. (14) masses of arXiv:2503.17389 in muon-atomic units with the centre of mass removed, the explicit 480-function trial wavefunction in cert/ (L = 2, natural parity, spatial part symmetric under exchange of the two deuterons) has a Rayleigh quotient rigorously enclosed by 320-bit ball arithmetic with upper end -0.488708325061607741252510781472877154393258585, which is a certified upper bound on the lowest root of that symmetry block and lies below Frolov's Table I (2,0) value -0.4887083249914 by 7.02e-11, more than the 1e-13 that partial win p1 requires; nothing is confirmed about the true energy, about any (1,1) state, or about other published values.

pass: true
