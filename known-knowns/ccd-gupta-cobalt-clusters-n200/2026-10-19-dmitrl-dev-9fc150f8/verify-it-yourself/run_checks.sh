#!/bin/sh
# run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs Python 3.8+ with numpy and scipy, and either network access to www-wales.ch.cam.ac.uk or CCD_DATA_DIR set to a
# folder holding cobalt.html, points.tgz and Co.zip (checked against sha256 pins either way).
if [ -n "$CCD_DATA_DIR" ]; then
  python3 verify-it-yourself/check_p1.py object/ccd_cobalt_audit.csv "$CCD_DATA_DIR"
else
  python3 verify-it-yourself/check_p1.py object/ccd_cobalt_audit.csv
fi
