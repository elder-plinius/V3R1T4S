# Run it yourself

From a fresh shell in this folder (Python 3.9+, POSIX shell, network for pip):

```sh
sh verify-it-yourself/run_checks.sh
```

It (1) checks the sha256 of every file in `object/` against `verify-it-yourself/object.sha256`, (2) creates a venv in a temp dir and installs `python-flint==0.9.0 numpy` (uses an importable python-flint 0.9.0 instead if present), (3) runs `verify-it-yourself/recert.py`, which recomputes every stored rho bound with Arb ball arithmetic and prints the bound. Expected output ends with:

```
rho_hat(0,Q) used = 3.636896e-12 ; b >= 1.021556e-15 ; CERTIFIED density <= 1 - 1.021556e-15
published (GEK): 1 - 2.6e-25 ; ratio of deficits = 3.929e+09
RECERT OK: b >= 1.0215562e-15
PASS
```

Exit code 0 on PASS; on any error or a changed object file the last line is `FAIL` and the exit code is 1.

## Rebuild the object

In a venv with `python-flint==0.9.0 numpy`, in a scratch copy of `object/` (both scripts write next to themselves):

```sh
python rig_dp.py 150 > rig_dp.out    # certified chain rho_hat(c,w), 155 states, a few seconds; writes rho_cert.json
python scheme.py 40  > scheme.out    # scans (k,u) for Q=40 with certified inequalities, a few seconds; writes scheme_best.json
```

The outputs should match `object/rig_dp.out`, `object/scheme.out`, `object/rho_cert.json`, `object/scheme_best.json`. The numerical sanity scripts (not needed for the certificate) are in `how-we-built-it/`.
