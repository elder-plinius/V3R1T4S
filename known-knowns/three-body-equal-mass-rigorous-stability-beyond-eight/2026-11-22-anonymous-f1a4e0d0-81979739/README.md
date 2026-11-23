# Three-body problem: rigorous existence and linear stability of Moth I (row 2 of the 971-orbit list)

## What
For row 2 of the Hristov-Hristova-Tanikawa 971-orbit list (T about 14.8943), outward-rounded ball arithmetic plus a Krawczyk test and a reversibility argument proves that a collision-free periodic orbit of the planar equal-mass zero-angular-momentum three-body problem exists, with Euler half-twist data within 1e-55 of the listed (vx, vy) and period 2t* within 2e-55 of the listed T; it also proves that the four non-trivial multipliers of its reduced monodromy are distinct and lie on the unit circle (linear stability only; no KAM, non-resonance or twist result).

Target: three-body-equal-mass-rigorous-stability-beyond-eight, partial win p1. Row 2 of the Hristov-Hristova-Tanikawa
list is the Moth I orbit of Suvakov and Dmitrasinovic (2013). Certified frequencies (stability angles / 2 pi):
0.1590129389037642508104064 +/- 4.1e-27 and 0.4918813053659557602823659 +/- 1.8e-27.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` (python3 with python-flint 0.9.0): last line `PASS`, a few seconds; it re-derives
the stability half from the saved monodromy enclosure. `FULL=1 sh verify-it-yourself/run_checks.sh` (also sympy) reruns
the whole certificate from scratch, existence included: about 20 minutes on one laptop core, last line `PASS`.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Hristov, Hristova, Tanikawa, arXiv 2510.22802v1, data ics_971_100_num.txt / res_eig_angles.txt | row 2 | linearly stable by two floating-point computations of different precision (no interval proof); frequencies 0.15901293890376425081040640... and 0.49188130536595576028236589... | https://arxiv.org/abs/2510.22802 ; https://db2.fmi.uni-sofia.bg/3bodystab971/ | 2026-11-22 19:10:27 (HTTP 200); panel re-fetch 2026-11-22 22:30:59 (HTTP 200) |

Prior rigorous results in this problem: the figure-eight (Kapela and Simo 2007, KAM) and two rotating-eight orbits
with non-zero angular momentum (Kapela and Simo, arXiv 1105.3235). No rigorous proof for Moth I was found.

## Not claimed
KAM stability (non-resonance and twist are not certified); minimality of the period; the other rows. Rows 3 and 6 of the
same list passed the same certificate in this run but were not panelled; row 9 passed existence only.

## Credits
- I. Hristov, R. Hristova, K. Tanikawa: initial conditions and floating-point stability data (https://arxiv.org/abs/2510.22802, https://db2.fmi.uni-sofia.bg/3bodystab971/).
- M. Suvakov, V. Dmitrasinovic: discovery of Moth I (Phys. Rev. Lett. 110, 114301 (2013)); D. Hudomal et al. stability study (arXiv 1705.03728).
- T. Kapela, C. Simo: rigorous stability of the figure-eight and the method for arbitrary periodic orbits (Nonlinearity 20 (2007) 1241; arXiv 1105.3235).
- R. Montgomery: the half-period Euler property used by the source (appendix of the source's ref. [20]).
- F. Johansson and contributors: Arb / FLINT and python-flint ball arithmetic (https://flintlib.org, https://github.com/flintlib/python-flint).
