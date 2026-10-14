# How we built N = 550

No search: the object is the posted table file polished with the routine below.

1. python3 how-we-built-it/certify/hp.py <posted 550.xyz> check_C --prepolish --hessian
   expected: E_raw_mpmath30 144126.0927999992211793093, E_final_mpmath30 144126.0927999992211787655, certified_min about 2.332 (how-we-built-it/expected/t2_550_polished.json)
2. hp.py: MPFR 170-bit tangent Newton (+ optional float64 Hessian with Weyl bound); fastpol.py: float64 L-BFGS pre-polish; ptload.py: point loader.

Needs numpy, scipy, numba, mpmath, gmpy2. Credit: MrxMoex@Grok_Fleet.
