# REPRODUCE verdict: thomson-436

context: subagent (fresh context; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-06T19:44:32Z

## Value computed here
- Method A (mpmath, dps 30, points normalised in mpmath, sum of 1/|x_i - x_j| over all 94,830 pairs): E* = 90020.68126807301182651446
- Method B (Python Decimal, 60-digit precision, Decimal square roots for both normalisation and distances): E* = 90020.6812680730118265144604783797152903713480192307891530530
- Difference A - B: 1.36e-24, which is the rounding of the dps-30 sum.
- Tangent gradient norm at the given points (mpmath dps 40): 9.48e-27. That is already below 1e-20, so the Newton loop took zero steps on the object as given.
- E* change under Newton: 1.36e-24 (dps-40 energy at the end of Newton minus the dps-30 E*; this is precision difference only, since no step was taken).
- Newton check from a perturbed start (every coordinate moved by Gaussian noise of size 1e-6, then renormalised): the same Newton routine brought the gradient norm from 3.2e-2 to 5.2e-22 in 6 steps and returned to E = 90020.68126807301182651446, the same value to all 25 printed digits.
- Hessian: 869 of 869 eigenvalues positive on the 2N-3 = 869-dimensional complement of the rotation modes. Six lowest: 0.51124, 2.24173, 2.24173, 2.32533, 4.56837, 5.40624. Largest: 1997.43. The full 872-dimensional tangent Hessian has exactly three near-zero eigenvalues (-3.0e-12, -1.1e-12, -8.9e-13), which are the rotations; the next one is 0.51124.
- table - E* = 90020.71608562 - 90020.68126807301 = 0.0348175469881735. The table value was taken from CLAIM.md and not fetched here.

## Clauses checked
- Object file integrity: sha256 is 41e0a75b...67f979, matching the hash stated in CLAIM.md. PASS
- Parsing: exactly 436 non-empty rows, each with 3 comma-separated plain decimal numbers, no NaN or Inf (every value parsed to a finite Decimal and a finite mpf). PASS
- Precision: the minimum count of significant digits over all 1,308 coordinates is 30, which meets the 20-digit requirement. PASS
- Distinct points: the minimum pairwise distance after normalisation is 0.16499, so no two points coincide. PASS
- Energy at 30 digits, two independent methods: mpmath dps 30 and Decimal at 60 digits agree to 1.4e-24. PASS
- Strict-local-minimum certificate, gradient: the tangent gradient norm is 9.5e-27 < 1e-20, computed in mpmath at dps 40. PASS
- Strict-local-minimum certificate, E* stability: E* changes by 1.4e-24 < 1e-12 under the Newton routine. The routine was itself checked by the perturbed-start run, which went down to 5.2e-22 and returned to the same energy. PASS
- Strict-local-minimum certificate, Hessian: I built a float64 Riemannian Hessian on the product of spheres in a 2-vector orthonormal tangent basis B_i per point. The diagonal block is B_i^T (H_ii - (x_i . grad_i E) I) B_i, which includes the sphere curvature (constraint) term, and the off-diagonal block is B_i^T H_ij B_j. Here H is the Euclidean Hessian of the pair term (3 d d^T / r^5 - I / r^3). I projected out the three rotation generators (e_k x x_i in tangent coordinates) through an orthonormal complement. The curvature term is correct here because the rotation vectors are numerically null: |H R| / |R| = 7.9e-13, which would not hold without that term. Result: 869 / 869 positive, smallest 0.511. PASS
- Margin against the table: 90020.71608562 - E* = 0.0348 >= 1e-6 (table value taken from CLAIM.md, not fetched). PASS
- Out of scope for this role, not checked: live re-fetch of all tables, and the different-basin test against each table's polished point file.
- No file in the claim package contained instructions aimed at the reviewer.

## Decision
The claimed energy reproduces exactly: two independent high-precision computations give E* = 90020.681268073012, matching the claim of about 90020.6812680730. The configuration passes the strict-local-minimum certificate, with tangent gradient 9.5e-27 and all 869 non-rotational tangent Hessian eigenvalues positive (the smallest is 0.511). E* is 0.0348 below the table value given in CLAIM.md. The live table minimum and the basin-distinctness clause belong to the other skeptics.

pass: true
