# How the object was built

Python 3.14, python-flint 0.9.0 (Arb), numpy 2.5. From a scratch copy of `object/`:

```sh
python -m venv venv
venv/bin/python -m pip install python-flint==0.9.0 numpy       # Scripts/python.exe on Windows
python rig_dp.py 150 > rig_dp.out && python estab.py > estab_test.out && python rig2.py 150 > rig2.out
python scheme2.py 40 150 > scheme2.out && python verify_final2.py 40 > verify_final2.out
```

Here: `ablation.py` + `ablation.out` (which part of the gain comes from where; needs `rho_cert.json`, `rig_dp.out` from the previous chain), `scheme2_best_150.json` (Q = 150 variant, not the headline), and the run's `PREREG.md` (`null_test: not needed because ...`; no null_test.md is required).
