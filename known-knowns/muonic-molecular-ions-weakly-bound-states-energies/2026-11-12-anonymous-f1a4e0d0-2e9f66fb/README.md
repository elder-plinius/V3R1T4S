# ttmu (2,0): an explicit 480-function trial wavefunction below Frolov's 2025 Table I value

## What
For the tt-mu Coulomb three-body Hamiltonian of arXiv:2503.17389 eq. (2) with the eq. (14) masses in muon-atomic units, the explicit 480-function L = 2, natural-parity, nuclear-exchange-symmetric trial function in cert/ has a Rayleigh quotient enclosed by the supplied 320-bit ball-arithmetic checker in [-0.51256864796989822024343949062712751210532790167646 +/- 1.86e-51], which upper-bounds the lowest root of that block and lies 2.9689e-9 below the Table I (2,0) value -0.5125686450010, exceeding the 1e-13 margin of partial win p1 for this one cell only.

Target: muonic-molecular-ions-weakly-bound-states-energies (bank), partial win p1, cell ttmu (2,0). Status:
CONFIRMED_PARTIAL (three fresh-context skeptics passed; see panel/).

The object is a list of 480 basis functions and one coefficient vector (object/). Function i is phi_i + P12 phi_i with
phi_i = T(x, y) exp(-a X - b Y - c R): x and y are the positions of the two tritons relative to the muon, X = |x|,
Y = |y|, R = |x - y|, T is a symmetric traceless Cartesian tensor of rank 2 (type 0: x x, 1: x y, 2: y y,
3: (x - y)(x - y)), and P12 swaps the two nuclei. The checker rebuilds the overlap and Hamiltonian matrices in arb
ball arithmetic and encloses the Rayleigh quotient: upper end -0.512568647969898220243439490627127512105327902
    bar -0.5125686450010 margin 1e-13 bar - upper end = [2.9688982202434394906e-9 +/- 2.72e-29]
upper end < bar - margin, bar minus upper end [2.9688982202434394906e-9 +/- 2.72e-29].

## Check it yourself
    V3R1T4S_PYTHON=/path/to/python-with-python-flint-and-sympy sh verify-it-yourself/run_checks.sh
Expected last line: PASS. Time: about 3 minutes of CPU on a laptop. Needs python-flint and sympy
(pip install python-flint sympy); not standard-library only, because the check is done in arb ball arithmetic.

## Compared to
| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| A. M. Frolov, arXiv:2503.17389v1, Table I | ttmu (2,0), N = 3800 | -0.5125686450010 | https://arxiv.org/abs/2503.17389 | 2026-11-11T19:16:03Z; NOVELTY skeptic: Wed Nov 11 22:10:45 UTC 2026 |
Details in the-record-we-beat/record.md.

## Not claimed
- Not the exact energy and not a converged value: the same boxes at 960 functions give a lower Rayleigh quotient
  (contributor text, unverified by the panel), so the true level lies lower still.
- Nothing about the (1,1) states, the bank's main criterion, or the dtmu (2,0) cell (not beaten in this run).
- Not a statement about other mass sets: older calculations at earlier mass values (for example arXiv:1008.3010)
  are not comparable at these digits; the comparison is only with Table I at the eq. (14) masses.
- The table value is beaten because that column of Table I is not converged, not because of a new method.

## Credits
- Alexei M. Frolov, arXiv:2503.17389 (https://arxiv.org/abs/2503.17389): the problem statement, masses and Table I.
- V. I. Korobov's pseudo-random exponent boxes for three-body exponential expansions (Phys. Rev. A 61, 064503, 2000).
- FLINT/Arb (https://flintlib.org), python-flint, SymPy and GMP for the arithmetic.
- The V3R1T4S bank entry for the target definition (https://github.com/elder-plinius/V3R1T4S).
