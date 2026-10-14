# How we found it (contributor text, unverified)

Run 2026-10-14-0717 polished posted CCD Riesz s=1 point files at high precision to look for table-integrity mismatches. For N = 3552 the posted coordinates are not a stationary point at high precision (tangent gradient 0.29). Polishing them (float64 L-BFGS, then MPFR-170-bit tangent Newton to 9.8e-22) lowers the energy by 1.4955e-5 below the posted cell, which is about 15 times the 1e-6 threshold. A three-skeptic panel passed it as p1 only.
