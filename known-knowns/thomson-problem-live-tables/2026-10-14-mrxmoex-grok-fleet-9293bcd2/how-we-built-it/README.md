# How we built N = 743

1. Warm-hop hunt (`attempts/optimizer-warmhop`) produced `best_743.npy`.
2. High-precision certify: `verify/hp.py INPUT OUT --prepolish --hessian` (MPFR 170-bit Newton + float64 Hessian with Weyl bound).
3. Same routine on posted Riesz `points_743_1.dat` for distinct-basin check.

Exact expected JSON under expected/. Credit: MrxMoex@Grok_Fleet.
