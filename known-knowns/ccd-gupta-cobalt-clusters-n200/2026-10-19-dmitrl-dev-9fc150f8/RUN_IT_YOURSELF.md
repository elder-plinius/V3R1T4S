# Run it yourself

From this folder, in a fresh shell, with Python 3.8+ and numpy and scipy installed:

    sh verify-it-yourself/run_checks.sh

The checker downloads cobalt.html, points.tgz and Co.zip once each from https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/
(or reads them from the folder named by CCD_DATA_DIR) and refuses any file whose sha256 differs from its pin. It
recomputes all 199 table rows and the ten Co.zip rows of object/ccd_cobalt_audit.csv and prints, as its last line, PASS
if every field agrees. About 20 seconds on a laptop. Expected output: see verify-it-yourself/RECEIPTS.md.

Rebuild the object (same inputs): python3 how-we-built-it/code/build_p1_object.py DATA_DIR object.csv
