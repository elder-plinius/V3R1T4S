# REPRODUCE skeptic verdict: Pb glue N = 121 (claim/result/Pb_121.xyz)

context: subagent (Claude Code Agent tool, fresh context)

## Definition used (written before reading claim/code/lead.py)
From claim/data/lead.f, which is the archived Fortran with header "Ong-Ercolessi glue potential for Pb. Ref.: H. S. Lim, C. K. Ong and F. Ercolessi, Surf. Sci. 269/270, 1109 (1992)":

    E = sum_{i<j} phi(r_ij) + sum_i U(rho_i),   rho_i = sum_{j != i} rho(r_ij)

I hand-transcribed phi = SUBROUTINE v2 (regions I/II/III, cutoff RC = 4.23), rho = SUBROUTINE rh (cutoff RRC = 5.503) and U = SUBROUTINE uu (breaks at DSW = 9.0814..., DB = 12), with the BLOCK DATA PB constants copied digit for digit. All three use the same `.GE.`/`.GT.` branch conventions as the Fortran. Units are eV and Angstrom.

I wrote my own analytic gradient and analytic 3N x 3N Hessian. The pair term is c2*e e^T + (c1/r)(I - e e^T), with c1 = phi' + (U'_i+U'_j) rho', and the glue term is sum_i U''(rho_i) grad(rho_i) grad(rho_i)^T. The evaluator works generically, so the same code runs in float64 and in mpmath at mp.dps = 30. Scripts: panel_reproduce/mine/pbglue.py, calib.py, certify.py. They are outside claim/, in the skeptic's own scratch area.

Hessian check against central finite differences of the gradient (h = 1e-6, 4 columns): max abs err 1.99e-09.

## Data hashes
`shasum -a 256 -c data/SHA256SUMS` (from claim/): 162 lines OK, 0 failed. This covers result/Pb_121.xyz, data/lead.f, data/aluminum.f, data/lead_table.html and all 158 files in data/lead_points/.

## Calibration (my evaluator vs data/lead_table.html)
158 table rows parsed (N = 3..160). There are 12 random files (Python random.Random(20261123).sample):

| N | mine | table | diff |
|---|---|---|---|
| 150 | -250.9008062 | -250.900806 | -1.73e-07 |
| 129 | -212.6206194 | -212.620619 | -4.29e-07 |
| 43 | -62.5180561 | -62.518056 | -9.57e-08 |
| 47 | -69.2274539 | -69.227454 | 8.95e-08 |
| 146 | -243.6658454 | -243.665845 | -4.00e-07 |
| 25 | -33.3946286 | -33.394629 | 4.30e-07 |
| 141 | -234.3471933 | -234.347193 | -2.89e-07 |
| 99 | -159.5826276 | -159.582628 | 4.29e-07 |
| 102 | -164.7134747 | -164.713475 | 3.18e-07 |
| 50 | -74.3036007 | -74.303601 | 3.30e-07 |
| 10 | -10.3281106 | -10.328111 | 3.57e-07 |
| 21 | -27.1605573 | -27.160557 | -3.22e-07 |

All 12 are within 1e-6 eV. Across all 158 files the maximum |diff| is 6.040e-07, excluding one file. That file is N = 116, which differs by 1.0049e-04 because the posted file and the table row disagree. The authors disclose this in claim/REPRODUCE.md and it does not affect N = 121.

N = 121 posted file under my evaluator: -198.211396576. Table: -198.211397.

## Object: claim/result/Pb_121.xyz (121 x 3, Angstrom)
- E (float64, as saved): -198.479029166272. The float64 gradient norm as saved is 4.729e-14.
- mpmath polish at dps 30: I used Newton steps, with the step taken from the double Hessian pseudo-inverse and the gradient taken in mpmath.
  - it 0: E_mp = -198.4790291662722537928, |g|_mp = 4.7521e-14
  - it 1: |g|_mp = 2.1424e-27
  - Final E_mp = -198.4790291662722537928329, |g|_mp = 2.1424e-27. This is below the 1e-10 threshold.
  - Max atom displacement during the polish: 1.471e-14 A.
- Claimed E -198.47902916627225379. Mine minus claimed = -2.8e-18.
- Double-precision Hessian at the polished point:
  - Eigenvalues with |lambda| < 1e-6: exactly 6.
  - Eigenvalues below -1e-6: 0.
  - The lowest 8 eigenvalues are -5.005e-15, -2.044e-15, -1.569e-15, 1.137e-15, 2.528e-15, 7.731e-15, 1.490e-01, 1.846e-01.
  - The three tiny negative values are roundoff in the six translation and rotation modes. The 7th smallest |lambda| is 1.489796e-01.
- Margin vs table row N = 121 (-198.211397): E - table = -0.267632166272. That is 0.2676 eV below the row, which meets the "at least 1e-4" requirement.
- Distance of pair distances to spline breakpoints: min 1.94e-03 A. Distance of the densities to the U breakpoints: min 0.0271. Minimum pair distance: 3.0044 A. So no pair sits on a piecewise boundary.

## Posted structure: claim/data/lead_points/121, polished the same way
- Start: E64 = -198.2113965759, |g| = 3.338e-06.
- Newton it 1: |g| = 1.752e-12. Newton it 2: |g| = 6.5649e-25.
- Final E_mp = -198.2113965758774409353367.
- Hessian: 6 near-zero eigenvalues, 0 negative. The 7th eigenvalue is 1.422606e-01.
- Max displacement during the polish: 2.366e-07 A, so it stays in its own basin.
- E_posted_polished - E_object = 0.267632590395, which meets the "at least 1e-4" requirement. The basins are distinct.

## Determinism
I ran certify.py twice and the output was byte-identical (diff empty). The calibration rerun gave identical numbers.

## Second check: the authors' claim/REPRODUCE.md
I ran it on a copy of claim/ (built libglue.dylib, then ran calibrate_pb.py and certify_pb.py):
- calibrate: `max |posted - table| 0.00010049102806419796`. The only flagged row is N = 116.
- certify last line: `"E_mp": "-198.47902916627225379", "grad_norm_mp": "4.7398e-14", "grad_ok": true, "zero_modes": 6, "negative_modes": 0, "lowest_nonzero": 0.14897957941348092, "E_table": -198.211397, "margin_vs_table": -0.26763216627225006, "E_posted_polished": -198.21139657587744, "margin_vs_posted": -0.26763259039481113, "certified": true`
- This matches the expected output in REPRODUCE.md and agrees with my independent numbers to better than 1e-12 eV.

## Scope notes (not verified by this skeptic)
- I did not do the live re-fetch of the table or the arXiv / Scholar literature search. I used the saved data/lead_table.html. Its hash matches, and its N = 121 row is -198.211397.
- Exhaustive search is not part of this claim. The bars in claim/bars/ are labelled reference-only and were not used for the verdict.

## Verdict
Every item in my remit checks out with my own independently written evaluator and agrees with the authors' code:
- the calibration
- the hashes
- the energy and the margin
- the certified local minimum: polished gradient 2e-27, 6 zero modes, no negative modes
- the distinct basin
- determinism

pass: true
