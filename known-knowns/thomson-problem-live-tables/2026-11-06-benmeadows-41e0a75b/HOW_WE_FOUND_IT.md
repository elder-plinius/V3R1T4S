# How we found it (contributor text, unverified)

The brief: an unattended search lane (a series of AI coding sessions in a sandbox, 4 CPU cores each) over the live
Thomson tables for N up to 1500, with the minimum over Deeter's table and the two CCD Thomson tables as the target
values, read 2026-11-04.

What worked: a neighbour scan. For each target N, take the posted record configuration for N + 1 or N - 1 (here
Deeter's posted e.437.txt), remove or add one point (here: remove one point, three tries), relax with L-BFGS on the
sphere, and compare with the table. For N = 436 the configuration from 437 with one point removed relaxed to
E = 90020.6812681, below Deeter's 90020.7160856 by 0.0348 (log: how-we-built-it/runs/pairC.log, line 1). The
configuration was then refined (L-BFGS to gradient 1e-5, float64 tangent Hessian: three zero modes, lowest other
eigenvalue 0.511) and certified with how-we-built-it/src/certify.py (mpmath Newton to gradient 9e-27).

What failed: the same scan found no other N in 300-534 below the table; neighbour moves from this new 436
configuration to 420-452 all ended above the tables (+0.056 or more). The lane's notes call 436 a rare hit, not a
better family.
