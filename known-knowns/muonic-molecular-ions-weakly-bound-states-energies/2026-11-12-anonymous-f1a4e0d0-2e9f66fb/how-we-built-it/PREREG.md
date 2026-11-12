# PREREG (frozen Wed Nov 11 19:28:12 UTC 2026, before any attack output is scored)

Only validation runs existed when this was written: helium P and D smoke tests and one unoptimised 350-function
ddmu L = 1 run (second root -0.47366303, 2.4e-5 above the bar), all in attempts/evaluator-first/.

## Criterion (verbatim from the bank)
Success means an explicit variational wavefunction for the (1,1) state of dd-mu or of dt-mu. It is a three-body Coulomb system with charges (+1, +1, -1) and exactly the masses of arXiv:2503.17389 eq. (14), in muon-atomic units with the centre of mass removed. The state has total angular momentum L = 1, natural parity (-1)^L, and, for dd-mu, the exchange symmetry (-1)^L under d <-> d. The energy must be the SECOND-lowest root of the generalized eigenproblem in that symmetry block (Hylleraas-Undheim-MacDonald: the second root bounds the (1,1) level from above). The checker's certified root must be STRICTLY LOWER (direction: min) than Frolov's Table I value for that state (-0.47368672970969890623 for dd-mu, -0.4819915265298649455 for dt-mu) by at least 1e-19. It must also be lower than any other published variational value for the identical masses found by a literature search immediately before claiming.

p1: A (2,0) cell: for dd-mu, dt-mu or tt-mu, with the same masses, L = 2, natural parity (exchange-symmetric spatial part for dd-mu and tt-mu), the lowest root of that block certified STRICTLY LOWER than Frolov's Table I value (-0.4887083249914, -0.500118077325475 or -0.5125686450010) by at least 1e-13.

p2: An open, checkable certificate for either (1,1) state whose certified second root lies within 1e-15 of Frolov's Table I value, above or below. It is the first public reproduction, since Frolov releases no wavefunctions.

## Object
A certificate file: the mass ratios as exact decimal quotients of the eq. (14) numbers, the list of basis functions
(tensor type and exponents as exact decimal strings), the exchange symmetry, and one coefficient vector (two for a
(1,1) claim) as decimal strings.

## Statistic and thresholds
All decided by attempts/evaluator-first/code/check_cert.py, which rebuilds the overlap and Hamiltonian matrices in arb
ball arithmetic at 256 bits or more from the certificate alone:
- p1 (one cell per claim): U = upper end of the ball of the Rayleigh quotient v.Hv / v.Sv, with v.Sv certified > 0.
  Pass iff U < bar - 1e-13, bar = -0.4887083249914 (ddmu), -0.5125686450010 (ttmu) or -0.500118077325475 (dtmu).
  The lowest root of the block is <= U, so this certifies the lowest root.
- main: with two vectors, the larger root of the 2 x 2 projected problem, upper end of its ball, must be
  < bar - 1e-19 (it bounds the second root of the block from above), bar as in the criterion.
- p2: the same upper bound must be <= bar + 1e-15, and an inertia count in ball arithmetic must show exactly one root
  of the full block below bar - 1e-15.
- The margin by which a cell is beaten is reported from the same output. A value that does not meet its threshold is
  reported as not met, whatever its size.

## Gates that must hold before any claim
- G1: the GMP engine (gradient form, perimetric integrals) and the arb checker (operator form, relative-coordinate
  integrals) agree on the claimed Rayleigh quotient to 1e-30.
- G2: for the same code path, the dtmu (2,0) lowest root, whose Table I column is the best converged, must come out
  within 1e-9 of -0.500118077325475; and the ddmu (1,1) second root within 1e-6 of -0.47368672970969890623.
- G3: negative controls: the checker must fail the threshold for a deliberately perturbed coefficient vector, and the
  energy must change when the masses are changed to the CODATA 2022 values.
- Novelty: a literature search for the identical masses immediately before claiming (step 6 NOVELTY repeats it).

null_test: not needed because the claim is an explicit object (basis and coefficient vector) checked by a deterministic ball-arithmetic checker against a table value; no search statistic or "beats chance" statement is involved.

Baseline (step 3c): not an empirical benchmark score; the table value is the comparison, and G2 is the reproduction gate.

Budget: heavy; started Wed Nov 11 19:12:39 UTC 2026; no new line of work after 01:36 UTC on 2026-11-12.
