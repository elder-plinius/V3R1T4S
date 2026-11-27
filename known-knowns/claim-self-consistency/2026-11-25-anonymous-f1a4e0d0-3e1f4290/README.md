# White 2011 warp-field interferometer: the 1 cm, boost 1.0000001 test article needs at least 1.127e37 J of negative energy by the source's own equations

## What
Under White 2011's own Eq. (1), top-hat f(r), Eq. (3) and gamma = cosh(0.5 ln|1 - v^2 f^2|), every field with bubble radius R = 5 mm whose boost reaches 1 + 1e-7 has a flat-slice integrated Eq. (3) energy E <= -(c^4/(48G)) u*^2 R = -1.127e37 J (u* = 0.0299002893) for every wall parameter sigma > 0, a negative energy that the source's proposed positive-energy capacitor ring cannot supply within its own equations.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` (Python 3 standard library only; a few seconds on a laptop). Expected last line: `PASS`.

## Compared to
| source | statement | value | URL | fetched (UTC) |
|---|---|---|---|---|
| White 2011, NTRS 20110015936 (paper and slide 21) | 1 cm test article, boost "on the order of 1.0000001", "very high-voltage capacitor ring", "toroidal-ring of positive energy density" | no energy figure given | https://ntrs.nasa.gov/api/citations/20110015936/downloads/20110015936.pdf | 2026-11-25T19:07:59Z |

## Not claimed
- Not claimed as new: that the Alcubierre metric needs negative energy (the source itself says it violates the energy
  conditions; Lee & Cleaver 2014 say so for this experiment). Only the size of the bound at the source's operating point is claimed.
- Not claimed: anything outside the source's Eq. (1), Eq. (3) and boost formula (other metrics, other couplings such as
  the slide's suggestion of acting on the ions' potential), anything about any built Eagleworks apparatus or its data,
  or a value for a boost other than 1 + 1e-7 or a radius other than 5 mm (the bound scales as u*^2 R).
- The figure with the slide's special-relativity speed (0.0004c, giving -2.017e33 J) rests on a different premise and
  is not part of the claim; the bound is not tight (the least |E| over sigma is 2.67 times larger).

## Credits
- Source: H. White, "Warp Field Mechanics 101", NASA Johnson Space Center, 2011 (NTRS 20110015936).
- Metric and energy density: M. Alcubierre, Class. Quantum Grav. 11 (1994) L73, https://arxiv.org/abs/gr-qc/0009013.
- Total-energy integral E = -(v^2/12) int f'^2 r^2 dr: M. J. Pfenning and L. H. Ford, Class. Quantum Grav. 14 (1997)
  1743, https://arxiv.org/abs/gr-qc/9702026.
- Closest prior critique of this experiment: J. S. Lee and G. B. Cleaver, arXiv 1407.7772 (2014),
  https://arxiv.org/abs/1407.7772.
- V3R1T4S kit and three-skeptic panel (https://github.com/elder-plinius/V3R1T4S).
