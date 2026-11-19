# Honesty gate (main session), written Thu Nov 12 03:01:33 UTC 2026

Read: panel/reproduce.md (pass: true; own matrix elements checked against quadrature of the nine-coordinate
Hamiltonian on 18 pairs, full 480 x 480 Rayleigh quotient equal to the claimed enclosure, same at 320, 384 and 512
bits), panel/novelty.md (pass: true; status page fetched 2026-11-11 22:10:45 UTC, HTTP 200, still v1; no equal or
lower value at the eq. (14) masses; it notes that older work at another mass set implies the exact energy lies
roughly 1.7e-10 below this bound, so this is not a converged value), panel/criterion.md (pass: true, with three
recorded caveats: upper bound only, its own second quadrature unfinished, no second full implementation by that
skeptic), and selfbreak.md (verdict: SURVIVES).

Downgrade checks: the caveats do not touch the p1 wording (an upper bound below the table value is what is asked, and
the REPRODUCE skeptic did write a full independent implementation); no reproduction mismatch; strictly below the table
value by 2.9689e-9 > 1e-13; scope is one explicit 480-function object and one cell; nothing presented as exhaustive
or converged; honest single table requests; panel fetch less than 6 hours old.

Not confirmed and not claimed: the true energy, convergence, the (1,1) states, the main success criterion.

status: CONFIRMED_PARTIAL
confirmed_scope: For the tt-mu Coulomb three-body Hamiltonian of arXiv:2503.17389 eq. (2) with the eq. (14) masses in muon-atomic units, the explicit 480-function L = 2, natural-parity, nuclear-exchange-symmetric trial function in cert/ has a Rayleigh quotient enclosed by the supplied 320-bit ball-arithmetic checker in [-0.51256864796989822024343949062712751210532790167646 +/- 1.86e-51], which upper-bounds the lowest root of that block and lies 2.9689e-9 below the Table I (2,0) value -0.5125686450010, exceeding the 1e-13 margin of partial win p1 for this one cell only.
