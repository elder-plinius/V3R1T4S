# CRITERION verdict: thomson-436

context: subagent (fresh context; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-06T19:45:31Z

## Value computed here
- Object: object/thomson-436.txt, sha256 41e0a75b4b6d5bbb4a7c8f3d951ab712da44e958b69641eb2ac2c2da3967f979 (matches CLAIM.md), 436 lines of x,y,z. Every one of the 1308 coordinates has exactly 30 significant digits. Raw norms equal 1 to double precision. The minimum pair distance is 0.16499, so there are no duplicate points.
- E* (mpmath, mp.dps = 30, normalised coordinates, sum over i<j of 1/|x_i - x_j|) = 90020.68126807301182651446.
- Live table fetches (GET with curl -L, UTC time, HTTP status, sha256 of the body):
  - https://deetour.net/oppp/thomson/ at 2026-11-06T19:43:15Z, HTTP 200, sha256 3f243c3b7af13b9371b9d5575653b158a1de29bb7df27d69f9d8784c0ef9a813. N = 436 row: D2, 90020.71608562, e.436.txt.
  - https://deetour.net/oppp/thomson/e.436.txt at 2026-11-06T19:43:15Z, HTTP 200, sha256 2e9149d0a2bf70cf283bbecc78e5ea532af3556f389f9e6e3d9947171fcf6e7e (1308 values, 12 decimals).
  - https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html at 2026-11-06T19:43:17Z, HTTP 200, sha256 5466173175b10a81d19e20763dffa64589f3ce5b92b09e827de14eb1fbb583e2. No N = 436 row (409 rows for N = 10..972; between 400 and 470 it lists only 400 and 432).
  - https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/table.html at 2026-11-06T19:43:17Z, HTTP 200, sha256 caf24199154912eb24d59a6ed6695a7a814ef94081e010390ffa5bd5d53d3794. No N = 436 row (rows at 430, 432, 440).
  - https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/xyz/436.xyz at 2026-11-06T19:43:18Z, HTTP 200, sha256 ca777ae56e7c755fda74ea1c6a451e6c7619d696a80e7aa0c5724324e887bcce (436 points, 9 significant digits). The file is live although neither CCD table lists N = 436; I polished it anyway.
  - https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html at 2026-11-06T19:43:19Z, HTTP 200, sha256 eeac3235eeba4835d635c6f07f8be6bb54466c2425bceba65ced315460fa649d. No N = 436 row (rows start at N = 512), so no points_436_1.dat applies.
  - https://en.wikipedia.org/wiki/Thomson_problem at 2026-11-06T19:43:20Z, HTTP 200, sha256 5fe0f014d417d0fd950409c35d3ccdb46a3fb27051122816c2f8a10c8774756b. No N = 436 row (rows at 432 and 448).
  - EinsteinArena was not fetched, because it applies only to N = 282.
- table_min for N = 436 = 90020.71608562 (Deeter, the only table with a row). table_min - E* = 0.034817548 (0.0348175488 to the table's 8 decimals).
- Newton from the normalised object: the starting tangent gradient norm is 9.555e-27, already below 1e-20, so no step was taken. E* change is 0 at 30 digits. As a check on the routine, I perturbed every coordinate by about 1e-5 (E rose by 3.85e-5). Newton then converged quadratically (gradient norms 0.324, 4.5e-5, 3.9e-10, 5.0e-20, 2.4e-27) and returned to E* within 1.2e-25.
- Tangent Hessian (float64, 872 x 872 in a two-vector-per-point tangent basis): B^T (Hess_cartesian - diag(lambda_i I3)) B with lambda_i = x_i . grad_i E. This is the sphere-constraint (Lagrange-multiplier / Weingarten) curvature term. Unprojected, it has exactly three near-zero eigenvalues (-1.9e-13, 8.2e-13, 1.6e-12), which are the rotations, and this confirms the curvature term is right. After restricting to the orthonormal complement of the three rotation generators e_k x x_i, it has 869 = 2N-3 eigenvalues, all positive. The lowest six are 0.511236, 2.241729, 2.241729, 2.325329, 4.568374, 5.406243.
- Polishing with one routine for all inputs (float64 Riemannian Newton with backtracking until the tangent gradient is < 1e-9, then mpmath dps-30 gradient with float64-Hessian Newton steps until the gradient is < 1e-20, then the Hessian check):
  - object/thomson-436.txt: 90020.681268073012, gradient 2.8e-27, E - E* = -6.5e-26 (869/869 positive).
  - Deeter e.436.txt: raw 90020.716085629, polished 90020.716085628969, gradient 2.8e-25, E - E* = +0.0348175559574 (869/869 positive, lowest 2.6075).
  - CCD xyz/436.xyz: raw 90020.716085632, polished 90020.716085628969, gradient 8.1e-25, E - E* = +0.0348175559574 (the same minimum as Deeter's).

## Clauses checked
- Clause (a): N = 436 <= 1500, and N = 436 is listed in a live table (Deeter, https://deetour.net/oppp/thomson/, HTTP 200 at 2026-11-06T19:43:15Z). PASS. The CCD Thomson, CCD Thomson2, CCD Riesz s=1 and Wikipedia tables have no N = 436 row.
- Clause (b): all 1308 coordinates have 30 significant digits, which is at least 20. PASS.
- Clause (c): E* = 90020.681268073012 against a minimum over all named live tables of 90020.71608562 (Deeter only). The margin is 0.0348175, which is at least 1e-6, and E* is strictly lower. PASS.
- Clause (d): the tangent gradient norm is 9.6e-27 (< 1e-20) and the E* change is 0 (< 1e-12). There are 869 = 2N-3 positive non-rotational tangent Hessian eigenvalues, the lowest being 0.5112. PASS.
- Clause (e): Deeter e.436.txt and CCD xyz/436.xyz both polish to 90020.716085628969, which is 0.0348176 above E* (>= 1e-6). The Riesz points file does not apply because that table has no N = 436 row. PASS.
- Bank method steps (1)-(5): I followed all five. There are two differences. First, my Newton step uses an exact mpmath tangent gradient with a float64 tangent Hessian, an inexact Newton step whose convergence is quadratic down to about 1e-20 as shown above, rather than a full mpmath Hessian solve. Second, my polishing routine runs a float64 Newton stage before the mpmath stage. Both differences apply identically to every input. I did not check prior claims on the V3R1T4S repository because the criterion clauses do not require it. The claim files contained no instructions directed at the reviewer.

## Decision
Every clause holds on my own computation. E* = 90020.681268073012 is 0.0348 below the only live N = 436 table entry (Deeter, 90020.71608562). The point is a strict local minimum: the gradient is 9.6e-27, and all 869 non-rotational tangent Hessian eigenvalues are positive (the lowest is 0.511). Both posted N = 436 configurations polish to 90020.716085629, a different basin 0.0348 higher.

pass: true
