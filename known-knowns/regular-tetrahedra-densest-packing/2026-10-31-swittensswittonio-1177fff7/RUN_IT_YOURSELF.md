# Run it yourself

From a fresh shell in this folder (Python 3.9+, POSIX shell, network for pip):

```sh
sh verify-it-yourself/run_checks.sh
```

It (1) checks the sha256 of every file in `object/` against `verify-it-yourself/object.sha256`, (2) creates a venv in a temp dir and installs `python-flint==0.9.0 numpy` (uses an importable python-flint 0.9.0 instead if present), (3) runs `object/verify_final2.py 40`, which recomputes every stored rho bound with Arb ball arithmetic and prints the bound. Expected output ends with:

```
rho_hat(0,Q) used = 5.342361e-12 ; b >= 4.501141e-15 ; CERTIFIED density <= 1 - 4.501141e-15
previous bound deficit 1.0215562e-15 ; new/prev = 4.4062 ; strictly larger: True
published (GEK): 1 - 2.6e-25 ; ratio of deficits = 1.731e+10
PASS
```

Exit code 0 on PASS; on any error or a changed object file the last line is `FAIL` and the exit code is 1.

## Rebuild the object

In a venv with `python-flint==0.9.0 numpy`, in a scratch copy of `object/` (the scripts write next to themselves). `rho_cert.json` from the previous chain is only needed by the ablation; it is in `how-we-built-it/`:

```sh
python rig_dp.py 150 > rig_dp.out       # previous chain (Lemma V), writes rho_cert.json
python estab.py > estab_test.out        # Lemma V2 against Lemma V
python rig2.py 150 > rig2.out           # certified chain with Lemma V2, writes rho_cert2.json
python scheme2.py 40 150 > scheme2.out  # scans (k,u) for Q=40 and Q=150, writes scheme2_best_40.json, scheme2_best_150.json
python verify_final2.py 40 > verify_final2.out
```

Rebuild outputs should match the stored `*.out` files and the `*.json` objects.
