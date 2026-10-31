# Run it yourself

From a fresh shell in this folder (Python 3.9+, POSIX shell, network for pip):

```sh
sh verify-it-yourself/run_checks.sh
```

It (1) checks the sha256 of every file in `object/` against `verify-it-yourself/object.sha256`, (2) re-runs the exact-integer branch-and-bound `object/code/k4_bb.py 1 1000` (standard library only, about 15 s) and requires `RESULT: PROVED (all boxes certified)`, (3) creates a venv in a temp dir and installs `python-flint==0.9.0 numpy` (uses an importable python-flint 0.9.0 instead if present), (4) runs `object/code/verify_final.py 40 1000`, which re-certifies every stored rho bound and the counting scheme with Arb ball arithmetic. Expected output ends with:

```
RESULT: PROVED (all boxes certified)
...
rho(0,Q) used = 5.342391e-12 ; b >= 4.501166e-15
CERTIFIED (Arb, modulo the Residual trust list) density <= 1 - 4.501166e-15
PASS
```

Exit code 0 on PASS; on any error or a changed object file the last line is `FAIL` and the exit code is 1.

## Rebuild the object

In a venv with `python-flint==0.9.0 numpy`, in a scratch copy of `object/code/` (scripts write next to themselves; paths `code/...` in REDUCTION_FULL.md mean `object/code/...` here, the sanity scripts are in `how-we-built-it/`):

```sh
python k4_bb.py 1 1000    > k4_bb_eps_1_1000.out
python k4_bb.py -1 100    > k4_bb_negative_control_eps_-1_100.out   # must end NOT PROVED
python fullchain.py build  1000 40 > build_eps1000.out              # writes rho_cert.json
python fullchain.py scheme 1000 40 > scheme_eps1000_Q40.out         # writes scheme_best_40.json
python verify_final.py 40 1000     > verify_final.out
```

Outputs should match the stored `*.out` files and `*.json` objects byte for byte (a skeptic reproduced this).
