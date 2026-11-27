# Run it yourself (from this folder, fresh shell)
    python3 -m venv venv && venv/bin/pip install python-flint==0.9.0 sympy==1.14.0
    sha256sum -c SHA256SUMS          # or: shasum -a 256 -c SHA256SUMS
    PY=venv/bin/python3 sh verify-it-yourself/run_checks.sh            # last line: PASS (seconds)
    FULL=1 PY=venv/bin/python3 sh verify-it-yourself/run_checks.sh     # last line: PASS (about 20 min)
Rebuild the object: `cd how-we-built-it && ../venv/bin/python3 certify.py 2 55 0 448 96 384 72` prints a JSON report
(compare with object/certify_row2.txt) ending "CERT ROW 2: PASS" and writes A_row2_r55_rerun.json, which should be
byte-identical to object/A_row2_r55.json (two independent reruns were). Controls: `certify.py 1 30 0 320 64 256 44`
needs the figure-eight row (row 1 of the source file; not included) and passes; a box shifted by 1e-6 in vx
(`certify.py 2 30 1e-6`) fails C1.
