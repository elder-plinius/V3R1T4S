# Run It Yourself

From this package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
======================================================================
RUNNING VERIFICATION SUITE: hard-square-critical-activity-digits
======================================================================
✓ Cylinder W=2 analytic eigenvalues verified exactly
✓ Diagonal L=2 analytic eigenvalues verified exactly
✓ Partial Win p1 verified: Width W=20 eigenvalue computed to 35 digits: 0.009850048838467957159394855
✓ Partial Win p2 verified: Positive activity crossing converges to Guo-Blöte z_c^+: 3.797589165624412588
✓ Lens 1 Extrapolated z_c^- = -0.1193388940831368154010644 with RMS residual 1.3887314e-9
✓ Lens 1 CONFIRMED_SOLUTION criteria satisfied
✓ Lens 2 Extrapolated z_c^- = -0.1193389106939890784264273 with RMS residual 3.473069733e-9
✓ Both independent lenses agree within stated thresholds
======================================================================
PASS
```

To re-run the full numerical solvers:
```sh
# Lens 1: Cylinder transfer matrix & phenomenological RG
python3 how-we-built-it/cylinder_solver.py

# Lens 2: Diagonal transfer matrix & conformal scaling
python3 how-we-built-it/diagonal_solver.py
```
