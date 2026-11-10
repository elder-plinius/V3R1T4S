# Run it yourself

Everything runs from this folder in a fresh shell and needs only Python 3 (standard library). `PY` is your Python.

## 1. The standalone check (seconds)
    sh verify-it-yourself/run_checks.sh
Expected output: verify-it-yourself/RECEIPTS.md. The last line is `PASS`.

## 2. Rebuild the certificate record (about a minute)
    cd object && $PY cert.py 4433/10000 3 bound_rebuilt.json && cd ..
Expected:
    depth 0: worst margin -1.207390163e-03 ... -> fail
    depth 1: worst margin -4.498328179e-05 ... -> fail
    depth 2: worst margin 1.362252386e-04 ... -> PASS
    depth 3: worst margin 1.658527535e-04 ... -> PASS
    certified p_c >= 5567/10000: True
object/bound_rebuilt.json must be byte-identical to object/bound.json. Delete it afterwards, or the hash check in
step 1 will still pass but SHA256SUMS will list one file fewer.

## 3. Depth 0 is the 1996 paper
    $PY how-we-built-it/code/vdbe1996.py
Expected: "table rows reproduced: 13 of 13" and the exact optimum 0.5560829132 of the 1996 method.

## 4. Everything else
how-we-built-it/REPRODUCE.md lists the full set of commands the panel ran, with expected outputs.
