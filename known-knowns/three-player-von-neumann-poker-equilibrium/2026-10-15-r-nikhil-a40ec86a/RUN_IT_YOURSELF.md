# Run it yourself

From this package folder, in a fresh shell (Python 3.8 or newer, standard library only; nothing is downloaded):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (about 10 seconds; see verify-it-yourself/RECEIPTS.md for a real run):

```
== exact_certificate (exit 0): PASS: exact b=2 equilibrium certificate; printed decimal criterion is FALSE
== universal_check (exit 0): PASS: universal exact polynomial certificate
== ordered_cone_check (exit 0): PASS: exact nonnegative-gap polynomial certificates for all 12 raw payoff regions
== finite_calibration (exit 0): PASS: exact finite calibrations and deliberately exploitable profile
== independent_check (exit 0): PASS
PASS
```

("printed decimal criterion is FALSE" is expected: it records that the exact b=2 value does not round to the paper's
printed 0.122557074714865, which is why only partial win p1 is claimed.)

What each checker does:
- exact_certificate.py object/equilibrium.json: b=2 thresholds A, B, C and the value as algebraic numbers (defining
  polynomials, rational isolating intervals, Sturm counts) satisfying Eq. A-C, ordered 0<A<C<B<1, with every
  action-advantage sign checked exactly.
- universal_check.py object/universal.json: the polynomial identities used by the all-b proof (object/all_b_proof.md),
  for symbolic b.
- ordered_cone_check.py object/raw_payoffs.txt: the 24 raw action payoffs (three players, four hand regions, two
  actions) minus the matching Eq. A-C identity, with ordered gaps substituted, have only nonnegative coefficients:
  the prescribed action is optimal on every region for every b>0 and every ordered solution.
- finite_calibration.py: exact finite-deck calibrations and a deliberately exploitable profile (negative control).
- independent_check.py: written separately from the definition: exact terminal-utility integration (Fractions) at
  300 seeded random rational points against the closed-form payoffs for all three players, the identities
  D_I = 3(A^2 - x^2) on (0,C] and D_I = b(3x^2 - 2Cx - 1) on [C,1), the caller's four region forms, the existence
  identities, and the b=2 values in 110-digit Decimal arithmetic plus an exact sign change of the degree-8 eliminant.

Rebuilding the objects (optional, needs sympy 1.14.0: `pip install -r how-we-built-it/requirements.txt`):
- `python3 how-we-built-it/code/rectangle_check.py` regenerates the raw payoff table by integrating rectangles of
  opponent hands from terminal pot utilities, with symbolic b.
- `python3 how-we-built-it/code/universal_identities.py` re-checks the proof identities with a second computer-algebra
  implementation.
- `python3 how-we-built-it/code/independent_certify_sympy.py` is an independent sympy derivation (closed forms vs a
  cell integrator at 400 points, sign identities for all b, existence/uniqueness facts, b=2 minimal polynomial of C,
  digits comparison).
