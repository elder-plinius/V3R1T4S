# How the object was built

Python 3.14, python-flint 0.9.0 (Arb), numpy 2.5. From a scratch folder holding the scripts:

```sh
python -m venv venv
venv/bin/python -m pip install python-flint==0.9.0 numpy       # Scripts/python.exe on Windows
python rig_dp.py 150 > rig_dp.out      # writes rho_cert.json
python scheme.py 40  > scheme.out      # writes scheme_best.json
python verify_final.py                 # re-verification (packaged as verify-it-yourself/recert.py)
```

`rig_dp.py` and `scheme.py` are in `object/` (with their outputs). Here: `verify_final.py` (+ `.out`), sanity and exploration scripts (`a_check`, `aexact`, `capsph`, `e_sup_check`, `numopt`, `profile_dp`, `sanity_ceg_counts`, `scan_Q`, `scan_scheme`) with their `.out` files, and the run's `PREREG.md` (`null_test: not needed because ...`; no null_test.md is required).
