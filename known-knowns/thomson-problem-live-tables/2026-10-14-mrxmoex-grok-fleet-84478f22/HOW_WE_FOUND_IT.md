# How we found it

*contributor text, unverified*

The brief: lower the best known Coulomb energy for some N <= 1500 in a live Thomson table. The research charter preferred quiet table rows over famous ones.

What failed: defect-cluster kicks on N = 505..523 always returned to Deeter's basins; N = 513 from spiral and nearby-N seeds stayed 7.5e-2 above Deeter; random restarts and spiral seeds were far off.

What worked: guessing that the large-N rows in the CCD tables are less polished than Deeter's range. Warm Metropolis basin hopping with defect kicks, started from the posted Riesz s=1 N = 1382 file, found a basin 6.16e-3 lower. A first panel failed the claim on precision only (float64 certificate). In this run the point was repaired with MPFR 170-bit tangent Newton to a gradient of 5.8e-32, the Hessian was certified with an explicit error bound, both posted files were re-polished with the same routine, and three fresh skeptics (reproduce, novelty, criterion) passed it.
