# Run It Yourself — Continuous Guts Weenie Rule Certificates (n=4, n=5)

## 1. Verify the Certificates
From this package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

The checker runs in $< 1$ second using only Python 3 standard library (`json`, `fractions.Fraction`, `math`).
The final line of output is:
```text
PASS
```

## 2. Rebuild the Objects from Scratch
To re-run the symbolic polynomial reductions, Bernstein expansions, and interval branch-and-bound from first principles:

```sh
# Re-run Lens 1 (Chamber Bernstein Positivity)
python3 how-we-built-it/chamber_analysis.py

# Re-run Lens 2 (SOS Interval Solver)
python3 how-we-built-it/sos_interval_solver.py
```

Both scripts regenerate the exact JSON certificate files in `object/`.
