# Honesty gate: thomson-436

gate_by: packaging run, after reading reproduce.md, novelty.md and criterion.md for this claim
gate_time_utc: 2026-11-06T19:55Z

status: CONFIRMED_SOLUTION
panel: reproduce pass: true; novelty pass: true; criterion pass: true
confirmed_scope: 436 points on the unit sphere (object/thomson-436.txt) with Coulomb energy E* = 90020.681268073012 (mpmath, 30 digits), lower than the only live table value for N = 436 (Wayne Deeter's table, 90020.71608562, fetched 2026-11-06) by 0.0348; a certified strict local minimum (tangent gradient norm below 1e-26, all 869 non-rotational tangent Hessian eigenvalues positive, lowest 0.511); and a different basin from both posted N = 436 configurations (Deeter e.436.txt and CCD xyz/436.xyz polish to 90020.716085629).
conditions: the CCD Thomson, CCD Thomson2, CCD Riesz s = 1 and Wikipedia tables have no N = 436 row; the search started from Deeter's posted N = 437 configuration with one point removed (HOW_WE_FOUND_IT.md); the arXiv check covered the 15 newest "Thomson problem" results; no message was sent to any table keeper.

The three skeptics agree on E* to at least 20 digits and on the Hessian spectrum (lowest eigenvalue 0.511236).
