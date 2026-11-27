# ddmu (2,0): an explicit 480-function trial wavefunction below Frolov's 2025 Table I value

## What
For dd-mu with charges (+1, +1, -1) and exactly the eq. (14) masses of arXiv:2503.17389 in muon-atomic units with the centre of mass removed, the explicit 480-function trial wavefunction in cert/ (L = 2, natural parity, spatial part symmetric under exchange of the two deuterons) has a Rayleigh quotient rigorously enclosed by 320-bit ball arithmetic with upper end -0.488708325061607741252510781472877154393258585, which is a certified upper bound on the lowest root of that symmetry block and lies below Frolov's Table I (2,0) value -0.4887083249914 by 7.02e-11, more than the 1e-13 that partial win p1 requires; nothing is confirmed about the true energy, about any (1,1) state, or about other published values.

Target: muonic-molecular-ions-weakly-bound-states-energies (bank), partial win p1, cell ddmu (2,0). Status:
CONFIRMED_PARTIAL (three fresh-context skeptics passed; see panel/).

The object is a list of 480 basis functions and one coefficient vector (object/). Function i is phi_i + P12 phi_i with
phi_i = T(x, y) exp(-a X - b Y - c R): x and y are the positions of the two deuterons relative to the muon, X = |x|,
Y = |y|, R = |x - y|, T is a symmetric traceless Cartesian tensor of rank 2 (type 0: x x, 1: x y, 2: y y,
3: (x - y)(x - y)), and P12 swaps the two nuclei. The checker rebuilds the overlap and Hamiltonian matrices in arb
ball arithmetic and encloses the Rayleigh quotient: upper end -0.488708325061607741252510781472877154393258585
    bar -0.4887083249914 margin 1e-13 bar - upper end = [7.0207741252510781473e-11 +/- 1.24e-31]
upper end < bar - margin, bar minus upper end [7.0207741252510781473e-11 +/- 1.24e-31].

## Check it yourself
    V3R1T4S_PYTHON=/path/to/python-with-python-flint-and-sympy sh verify-it-yourself/run_checks.sh
Expected last line: PASS. Time: about 3 minutes of CPU on a laptop. Needs python-flint and sympy
(pip install python-flint sympy); not standard-library only, because the check is done in arb ball arithmetic.

## Compared to
| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| A. M. Frolov, arXiv:2503.17389v1, Table I | ddmu (2,0), N = 3700 | -0.4887083249914 | https://arxiv.org/abs/2503.17389 | 2026-11-11T19:16:03Z; NOVELTY skeptic: Wed Nov 11 22:06:51 UTC 2026 |
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
