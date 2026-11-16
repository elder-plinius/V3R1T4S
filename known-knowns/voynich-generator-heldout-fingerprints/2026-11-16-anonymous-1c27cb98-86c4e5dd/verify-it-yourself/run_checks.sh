#!/bin/sh
# Verify the outcome-(B) Naibbe-H1 falsification claim from this folder (stdlib python3).
# Recomputes the pooled Naibbe H1 from objects/pooled_{A,B}.wrapped.txt and checks it is
# below the 99.9% Voynich envelope bounds, the 16,000-control minima, and the per-plaintext
# secondary. Exits 0 and prints PASS only if every check holds.
set -e
cd "$(dirname "$0")/.."
if command -v python3 >/dev/null 2>&1; then PY=python3; else PY=python; fi
"$PY" verify-it-yourself/checker.py
