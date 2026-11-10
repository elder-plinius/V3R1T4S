#!/bin/sh
# Verify submission 2026-11-10-thefullnacho-7a8195e9 from a clean copy.
# Builds a throwaway venv in a temporary directory (nothing is written into
# the package), installs the checker's requirements, and runs check.py.
# Last line printed is PASS on success, FAIL otherwise.
set -e
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT INT TERM
python3 -m venv "$WORK/venv"
"$WORK/venv/bin/pip" install -q --disable-pip-version-check -r verify-it-yourself/requirements.txt
"$WORK/venv/bin/python" verify-it-yourself/check.py
