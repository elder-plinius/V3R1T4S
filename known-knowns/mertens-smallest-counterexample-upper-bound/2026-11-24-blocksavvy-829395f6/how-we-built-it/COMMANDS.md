# Commands used to build the object (contributor notes)

Fresh shell, Python 3.10+, python-flint 0.9.0. From a copy of this package (or of claim_v3/):

    python3 -m venv v && . v/bin/activate && pip install python-flint==0.9.0
    # zeros n = 1..99,200 (about 20 min on 3 cores at nice 10; about 1 h on 1 core)
    python how-we-built-it/code/zeros.py 1 99200 400 3 zeros
    # completeness + certified values for all 19 y (about 30 s)
    python how-we-built-it/code/verify_p1.py zeros > my_values.json

Every 256-bit and 320-bit ball must overlap the shipped object/p1_certified_values.json, and the
zero counts must be N(14000) = 14950 and N(74000) = 98625. The 19-row printed comparison (both
conventions) is:

    python how-we-built-it/check/compare_printed.py

Expect 8 mismatches under rounding, 6 under truncation, 0 ambiguous, and corrections at printed
precision only for Table 2 rows 1, 4, 12 and 14. The package checker (stdlib, no flint) is
sh verify-it-yourself/run_checks.sh and does not recompute the zeros.
