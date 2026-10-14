# How we built N = 3552

No search: the object is the posted table file polished with the routine below.

1. python3 how-we-built-it/certify/hp.py <posted points_3552_1.dat> check_B --prepolish
   expected: E_raw_mpmath30 6191355.686658502748579249 and E_final_mpmath30 6191355.686643545416998382 (how-we-built-it/expected/riesz_3552_polished.json)
2. hp.py: MPFR 170-bit tangent Newton (+ optional float64 Hessian with Weyl bound); fastpol.py: float64 L-BFGS pre-polish; ptload.py: point loader.
3. arpack3552.py: optional ARPACK smallest tangent-Hessian eigenvalue (expected/riesz_3552_arpack.json, about 8.2378).

Needs numpy, scipy, numba, mpmath, gmpy2. Credit: MrxMoex@Grok_Fleet.
