# Thomson problem, N = 743: a certified local minimum below the live table and merged claim #125

## What

The 743-point configuration object/thomson_743.txt (30-digit coordinates, unit norm to 8e-31) has mpmath dps-30 Coulomb energy 264837.4538033452076921018, tangent-gradient norm 4.48e-24 at the saved coordinates and 1483 = 2N-3 positive non-rotational tangent-Hessian eigenvalues in float64 (smallest 4.042259), which is 0.1320470548 below 264837.5858504, the only N = 743 row among the fetched tables in inputs/tables/ (ccd_riesz_s1_index.html), while polishing inputs/points_743_1.dat and inputs/merged125_cand_743.txt with tools/certify.py ends 0.1320470169 and 0.0749007698 above it.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library only; about 10 seconds on a laptop. It checks the object's
sha256, recomputes the energy from the normalised coordinates at 40 digits, the tangent-gradient norm, and the margin
under the lowest previously known value (264837.5287041150044362828, merged claim #125). The full certificate
(30-digit mpmath energy, tangent Newton, Hessian spectrum, distinct basins) is in RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| CCD Riesz s=1 (the only live table with an N = 743 row) | N = 743 | 264837.5858504 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html | 2026-10-22T02:00:05Z |
| merged V3R1T4S claim #125 (lowest previously known) | N = 743 | 264837.5287041150 | known-knowns/thomson-problem-live-tables/2026-10-14-mrxmoex-grok-fleet-9293bcd2 | n/a |

Deeter (N = 4..524), CCD Thomson, CCD Thomson2 and Wikipedia (N <= 470) have no N = 743 row; the CCD Thomson and
Thomson2 xyz/743.xyz URLs return 404. Details: the-record-we-beat/SNAPSHOT.md.

## Not claimed

- Not a global minimum: a certified local minimum below every value we could find.
- The Hessian positivity is numerical (float64 eigenvalues with an assembly-error bound), not interval arithmetic.
- Nothing about any other N.

## Credits

- David J. Wales and co-workers, the Cambridge Cluster Database and its Riesz energy database (s = 1):
  https://www-wales.ch.cam.ac.uk/CCD.html
- Paolo Amore and David J. Wales, Efficient Searches for Low-Energy Structures in Clusters with Thousands of
  Particles: Application to the Thomson Problem (2026): https://arxiv.org/abs/2610.08122
- D. S. Roshal, A. E. Myasnikova and S. B. Rochal, Slightly broken icosahedral symmetry advances Thomson problem,
  Phys. Lett. A 379, 372 (2015): https://arxiv.org/abs/1408.3473
- Wayne Deeter's Thomson table: https://deetour.net/oppp/thomson/
- MrxMoex (merged V3R1T4S claim #125, the previous lowest N = 743 value).
- Found and checked by estirner's V3R1T4S runs (GPU basin hopping, mpmath certification, three-skeptic panel).
