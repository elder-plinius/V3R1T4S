#!/bin/sh
# Integrity first: every object/ file must match the package SHA256SUMS (added by the orchestrator, 2026-10-19).
_PKG=$(cd "$(dirname "$0")/.." && pwd)
if command -v shasum >/dev/null 2>&1; then _S="shasum -a 256"; else _S="sha256sum"; fi
( cd "$_PKG" && grep "  object/" SHA256SUMS > "${TMPDIR:-/tmp}/objsums.$$" && $_S -c "${TMPDIR:-/tmp}/objsums.$$" >/dev/null 2>&1 ) || { echo "object file sha256 MISMATCH against SHA256SUMS"; echo "FAIL"; exit 1; }
echo "all object/ files match SHA256SUMS"
# Z^4 dimer bound at (3,3,2).  Python 3.8+ standard library only.  About 6 minutes; CW_QUICK=1 skips the all-sector
# iteration (about 25 seconds remain).
cd "$(dirname "$0")" || exit 1
python3 -I check_z4.py
