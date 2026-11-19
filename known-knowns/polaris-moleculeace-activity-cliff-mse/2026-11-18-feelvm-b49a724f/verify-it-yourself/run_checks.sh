#!/bin/sh
# Standalone check of the p2 claim, from the package folder.
# Needs a python with scikit-learn and rdkit (any recent versions; the objects are
# deterministic SVR fits). Works under POSIX shells, Git-bash, and WSL bash (Windows
# interpreters are probed with their .exe names, which WSL runs via interop).
# The MoleculeACE CSV is fetched from its public source and pinned by sha256; no
# dataset ships inside this package.
cd "$(dirname "$0")/.."
PY=""
for c in python3 python python3.exe python.exe py py.exe; do
  if command -v "$c" >/dev/null 2>&1; then
    if "$c" -c "import sklearn, rdkit" >/dev/null 2>&1; then
      PY="$c"
      break
    fi
  fi
done
if [ -z "$PY" ]; then
  echo "VERIFY_P2: FAIL (no python with scikit-learn+rdkit found on PATH; install them and rerun)"
  exit 1
fi
exec "$PY" verify-it-yourself/verify_p2.py
