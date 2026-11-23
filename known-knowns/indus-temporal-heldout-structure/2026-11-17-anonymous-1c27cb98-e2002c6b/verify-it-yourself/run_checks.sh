#!/bin/sh
# Verify the Indus temporal held-out object-type claim from this folder (stdlib python3).
# Re-derives the per-site 4-class and 2-class accuracies from object/output_sweep_main.json
# pool_detail, re-derives the frozen model's class priors from how-we-built-it/data (M77 +
# im77), checks the frozen model record, the 3x10,000 paired-bootstrap null test and the
# p < 0.001 threshold at pooled / Mohenjo-daro / Harappa. Exits 0 and prints PASS only if
# every check holds; prints FAIL and exits 1 otherwise.
set -e
cd "$(dirname "$0")/.."
if command -v python3 >/dev/null 2>&1; then PY=python3; else PY=python; fi
"$PY" verify-it-yourself/checker.py
