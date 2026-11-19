# Run it yourself

From this folder, in a fresh shell:

    python3 -m venv venv && venv/bin/pip install python-flint sympy
    V3R1T4S_PYTHON=venv/bin/python sh verify-it-yourself/run_checks.sh

Expected output: the lines in verify-it-yourself/RECEIPTS.md, ending with
"CERTIFIED: upper end < bar - margin" and then "PASS".

What it does: checks the sha256 of object/basis.txt and object/vector.txt, then verify-it-yourself/check_cert.py
derives the L = 2 matrix elements symbolically (operator form), builds S and H for the 480 functions in 320-bit ball
arithmetic and prints an enclosure of v.Hv / v.Sv, which must lie below -0.5125686450010 - 1e-13.

To rebuild the object, see how-we-built-it/COMMANDS.md.
